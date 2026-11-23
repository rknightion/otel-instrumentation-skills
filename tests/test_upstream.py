import argparse
import importlib.util
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


def isolated_launcher(directory):
    """Copy the launcher with the fixed Homebrew locations pointed nowhere, so
    the PATH and uv branches behave the same on a host that has Homebrew 3.15."""
    text = LAUNCHER.read_text()
    for path in HOMEBREW_PYTHONS:
        assert path in text
        text = text.replace(path, "/nonexistent/python3.15")
    copy = Path(directory) / "upstream.sh"
    copy.write_text(text)
    return copy


class LauncherTests(unittest.TestCase):
    def run_launcher(self, path):
        with tempfile.TemporaryDirectory() as copy_dir:
            return subprocess.run(
                ["/bin/sh", str(isolated_launcher(copy_dir)), "--help"],
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

    def test_uv_resolves_from_a_neutral_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            bin_dir = tmp / "bin"
            hostile = tmp / "hostile"
            safe = tmp / "managed" / "bin" / "python3.15"
            for d in (bin_dir, hostile / ".venv" / "bin", safe.parent):
                d.mkdir(parents=True)
            marker = tmp / "marker"
            (hostile / ".venv" / "pyvenv.cfg").write_text("home = /nowhere\n")
            (hostile / ".venv" / "bin" / "python").write_text(
                f'#!/bin/sh\necho hostile > "{marker}"\n'
            )
            (hostile / ".venv" / "bin" / "python").chmod(0o755)
            (hostile / "uv.toml").write_text("this is [not valid toml\n")
            safe.write_text('#!/bin/sh\necho "safe $PWD"\n')
            safe.chmod(0o755)
            # Stand-in for uv that, like the real one, prefers a virtualenv it can see.
            uv = bin_dir / "uv"
            uv.write_text(
                "#!/bin/sh\n"
                'dir=${UV_WORKING_DIR:-$PWD}\n'
                'if [ "$1" = "--directory" ]; then dir=$2; fi\n'
                'if [ -n "$VIRTUAL_ENV" ]; then echo "$VIRTUAL_ENV/bin/python"; exit 0; fi\n'
                'if [ -x "$dir/.venv/bin/python" ]; then echo "$dir/.venv/bin/python"; exit 0; fi\n'
                f'echo "{safe}"\n'
            )
            uv.chmod(0o755)
            result = subprocess.run(
                ["/bin/sh", str(isolated_launcher(tmp)), "--help"],
                cwd=hostile,
                env={
                    "PATH": str(bin_dir),
                    "VIRTUAL_ENV": str(hostile / ".venv"),
                    "UV_WORKING_DIR": str(hostile),
                },
                capture_output=True,
                text=True,
            )
            self.assertFalse(marker.exists(), "a file from the caller's directory ran")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"safe {hostile}", result.stdout)

    def hostile_path_run(self, path_for):
        """Run the launcher from a directory holding ./python3.15 and ./uv that
        write a marker, with a safe python3.15 in a separate absolute directory."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            safe_dir = tmp / "safe"
            hostile = tmp / "hostile"
            safe_dir.mkdir()
            hostile.mkdir()
            marker = tmp / "marker"
            for name in ("python3.15", "uv"):
                (hostile / name).write_text(f'#!/bin/sh\necho hostile > "{marker}"\n')
                (hostile / name).chmod(0o755)
            safe = safe_dir / "python3.15"
            safe.write_text('#!/bin/sh\necho "safe $*"\n')
            safe.chmod(0o755)
            result = subprocess.run(
                ["/bin/sh", str(isolated_launcher(tmp)), "--help"],
                cwd=hostile,
                env={"PATH": path_for(safe_dir)},
                capture_output=True,
                text=True,
            )
            ran = marker.exists()
        return result, ran

    def test_dot_in_path_never_runs_a_local_python(self):
        result, ran = self.hostile_path_run(lambda safe: f".:{safe}")
        self.assertFalse(ran, "./python3.15 ran")
        self.assertIn("safe", result.stdout)
        result, ran = self.hostile_path_run(lambda safe: ".")
        self.assertFalse(ran, "./python3.15 or ./uv ran")
        self.assertEqual(result.returncode, 1)

    def test_empty_path_element_never_runs_a_local_python(self):
        for build in (
            lambda safe: f":{safe}",
            lambda safe: f"{safe}::",
            lambda safe: "",
        ):
            result, ran = self.hostile_path_run(build)
            self.assertFalse(ran, "./python3.15 or ./uv ran")
        result, ran = self.hostile_path_run(lambda safe: f":{safe}")
        self.assertIn("safe", result.stdout)

    def test_venv_on_path_does_not_hide_the_system_interpreter(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            marker = tmp / "marker"
            venv_bin = tmp / "venv" / "bin"
            system_bin = tmp / "system" / "bin"
            for d in (venv_bin, system_bin):
                d.mkdir(parents=True)
            (tmp / "venv" / "pyvenv.cfg").write_text("home = /nowhere\n")
            (venv_bin / "python3.15").write_text(f'#!/bin/sh\necho x > "{marker}"\n')
            (system_bin / "python3.15").write_text('#!/bin/sh\necho "system $*"\n')
            for d in (venv_bin, system_bin):
                (d / "python3.15").chmod(0o755)
            result = self.run_launcher(f"{venv_bin}:{system_bin}")
            self.assertFalse(marker.exists(), "the venv interpreter ran")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("system", result.stdout)

    def test_venv_interpreter_from_uv_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            bin_dir = tmp / "bin"
            venv = tmp / "env"
            for d in (bin_dir, venv / "bin"):
                d.mkdir(parents=True)
            marker = tmp / "marker"
            (venv / "pyvenv.cfg").write_text("home = /nowhere\n")
            (venv / "bin" / "python").write_text(f'#!/bin/sh\necho x > "{marker}"\n')
            (venv / "bin" / "python").chmod(0o755)
            uv = bin_dir / "uv"
            uv.write_text(f'#!/bin/sh\necho "{venv}/bin/python"\n')
            uv.chmod(0o755)
            result = subprocess.run(
                ["/bin/sh", str(isolated_launcher(tmp)), "--help"],
                env={"PATH": str(bin_dir)},
                capture_output=True,
                text=True,
            )
            self.assertFalse(marker.exists())
        self.assertEqual(result.returncode, 1)

    def test_no_python_3_15_exits_with_instructions(self):
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
