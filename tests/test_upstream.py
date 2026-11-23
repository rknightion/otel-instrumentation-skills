import argparse
import importlib.util
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "upstream", ROOT / "plugins/otel-instrumentation-skills/scripts/upstream.py"
)
u = importlib.util.module_from_spec(spec)
spec.loader.exec_module(u)


LAUNCHER = ROOT / "plugins/otel-instrumentation-skills/scripts/upstream.sh"
HOMEBREW_PYTHONS = [
    "/opt/homebrew/bin/python3.15",
    "/home/linuxbrew/.linuxbrew/bin/python3.15",
]


class LauncherTests(unittest.TestCase):
    def run_launcher(self, path):
        return subprocess.run(
            ["/bin/sh", str(LAUNCHER), "--help"],
            env={"PATH": path},
            capture_output=True,
            text=True,
        )

    def test_old_python_is_refused(self):
        with self.assertRaises(SystemExit) as raised:
            u.require_python((3, 14, 3))
        self.assertIn("3.15", str(raised.exception))
        u.require_python((3, 15, 0))

    def test_python_3_15_on_path_runs_the_helper(self):
        with tempfile.TemporaryDirectory() as bin_dir:
            stub = Path(bin_dir) / "python3.15"
            stub.write_text('#!/bin/sh\necho "stub $*"\n')
            stub.chmod(0o755)
            result = self.run_launcher(bin_dir)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("upstream.py --help", result.stdout)

    def test_no_python_3_15_exits_with_instructions(self):
        if any(os.path.exists(p) for p in HOMEBREW_PYTHONS):
            self.skipTest("a Homebrew Python 3.15 is installed")
        with tempfile.TemporaryDirectory() as empty:
            result = self.run_launcher(empty)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Python 3.15", result.stderr)


class LookupTests(unittest.TestCase):
    def test_containment_and_official_sources(self):
        for path in ["../secret", "/etc/passwd", "a/../../b", "a\\b"]:
            with self.assertRaises(ValueError):
                u.source_path(path)
        with self.assertRaises(ValueError):
            u.repository("attacker/opentelemetry")
        self.assertEqual(
            u.repository("open-telemetry/opentelemetry-go"),
            "open-telemetry/opentelemetry-go",
        )

    def test_ref_is_encoded_as_single_identifier(self):
        self.assertEqual(u.segment("sdk/v1.2.3"), "sdk%2Fv1.2.3")
        with self.assertRaises(ValueError):
            u.segment("-bad")

    def test_missing_ref_does_not_fallback(self):
        with patch.object(u, "get_json", side_effect=ValueError("not found")) as get:
            with self.assertRaises(ValueError):
                u.resolve("open-telemetry/opentelemetry-go", "v0.invalid")
            self.assertEqual(get.call_count, 1)

    def test_tag_resolves_to_commit_before_file(self):
        a = argparse.Namespace(
            command="file",
            repo="open-telemetry/opentelemetry-go",
            ref="v1.test",
            path="README.md",
            match=None,
        )
        with (
            patch.object(u, "get_json", return_value={"sha": "a" * 40}),
            patch.object(u, "fetch", return_value="evidence") as fetch,
        ):
            result = u.lookup(a)
            self.assertEqual(result["commit"], "a" * 40)
            self.assertIn("/" + "a" * 40 + "/", fetch.call_args.args[0])
            self.assertEqual(result["requested_ref"], "v1.test")

    def test_truncated_tree_is_not_complete_evidence(self):
        with patch.object(u, "get_json", return_value={"truncated": True, "tree": []}):
            with self.assertRaises(ValueError):
                u.tree("open-telemetry/x", "a" * 40)

    def test_snippets_are_bounded_and_numbered(self):
        result = u.snippets(
            "\n".join("needle" for _ in range(100)), "needle", context=0, limit=3
        )
        self.assertEqual(len(result["matches"]), 3)
        self.assertEqual(result["matches"][0]["start_line"], 1)
        self.assertTrue(result["limited"])

    def test_package_version_does_not_silently_use_latest(self):
        a = argparse.Namespace(
            command="package",
            ecosystem="npm",
            name="@opentelemetry/api",
            version="missing",
        )
        with patch.object(
            u,
            "get_json",
            return_value={"dist-tags": {"latest": "1"}, "versions": {"1": {}}},
        ):
            with self.assertRaises(KeyError):
                u.lookup(a)

    def test_semconv_requires_narrow_domain(self):
        a = argparse.Namespace(
            command="semconv",
            repo="open-telemetry/semantic-conventions",
            ref="vtest",
            domain="http",
            term="route",
            max_files=2,
        )
        with (
            patch.object(u, "resolve", return_value="a" * 40),
            patch.object(
                u, "tree", return_value=["http/a.yaml", "http/b.yaml", "http/c.yaml"]
            ),
        ):
            with self.assertRaises(ValueError):
                u.lookup(a)


if __name__ == "__main__":
    unittest.main()
