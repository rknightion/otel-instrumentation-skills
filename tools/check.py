#!/usr/bin/env python3
"""Dependency-free structural, packaging and freshness gate; no live OTel claims."""

import ast
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "plugins/otel-instrumentation-skills"


def check():
    subprocess.run(
        ["python3", str(ROOT / "tools/render_manifests.py"), "--check"], check=True
    )
    subprocess.run(
        ["python3", str(ROOT / "tools/render_evals.py"), "--check"], check=True
    )
    for p in ROOT.rglob("*.json"):
        if not any(
            x.startswith(".") for x in p.relative_to(ROOT).parts[:-1]
        ) or p.name in ["plugin.json", "marketplace.json"]:
            json.loads(p.read_text())
    extra = sorted(d.name for d in (ROOT / "plugins").iterdir() if d != P)
    assert not extra, f"Unexpected plugin directories: {extra}"
    meta = json.loads((ROOT / "plugin.meta.json").read_text())
    assert re.fullmatch(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", meta["version"]), (
        "Invalid release version"
    )
    portable = json.loads((P / "plugin.json").read_text())
    assert (
        portable["$schema"]
        == "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
    )
    assert set(portable) <= set(
        [
            "$schema",
            "name",
            "version",
            "description",
            "author",
            "homepage",
            "repository",
            "license",
            "keywords",
            "extensions",
        ]
    )
    inventory = json.loads((ROOT / "skill-inventory.json").read_text())
    files = sorted((P / "skills").glob("*/SKILL.md"))
    assert {p.parent.name for p in files} == set(inventory), "Skill inventory drift"
    assert len(files) == len(inventory) == 15
    for p in files:
        text = p.read_text()
        sections = text.split("---", 2)
        assert len(sections) == 3 and sections[0] == "", f"{p}: frontmatter"
        fields = dict(line.split(": ", 1) for line in sections[1].strip().splitlines())
        assert set(fields) == {"name", "description", "license"}, (
            f"{p}: frontmatter fields"
        )
        name = fields["name"]
        desc = json.loads(fields["description"])
        assert (
            name == p.parent.name
            and len(name) <= 64
            and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)
        )
        assert isinstance(desc, str) and 0 < len(desc) <= 1024
        assert len(text.splitlines()) < 150, f"{p}: progressive disclosure budget"
        assert (
            "../../shared/source-policy.md" in text
            and "../../shared/observability-policy.md" in text
        )
    for p in list((P / "skills").rglob("*.md")) + list((P / "shared").glob("*.md")):
        text = p.read_text()
        assert not re.search(r"(?<![\w])v?\d+\.\d+\.\d+(?:b\d+)?", text), (
            f"{p}: embedded release number; use source lookup"
        )
        assert len(re.findall(r"^\|", text, re.M)) < 16, f"{p}: suspicious frozen table"
        assert len(text.splitlines()) < 150, f"{p}: oversized instruction"
        assert not re.search(
            r"https?://[^\s)]*dash0|DASH0_TOKEN|ingress\..*dash0", text, re.I
        ), f"{p}: vendor-specific configuration"
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if "://" in target or target.startswith("#"):
                continue
            resolved = (p.parent / target.split("#")[0]).resolve()
            assert resolved.is_relative_to(P.resolve()), f"{p}: link escapes plugin"
            assert resolved.exists(), f"{p}: missing {target}"
    corpus = json.loads((P / "evals/corpus.json").read_text())
    assert len(corpus) >= 18 and len({c["id"] for c in corpus}) == len(corpus)
    for c in corpus:
        assert set(c) == {
            "id",
            "skill",
            "fixture",
            "prompt",
            "pass_criteria",
            "fail_criteria",
        }
        assert c["skill"] in inventory
        assert (P / "evals/fixtures" / c["fixture"]).is_dir()
        assert (P / "evals" / c["id"] / "prompt.md").exists()
        assert (P / "evals" / c["id"] / "graders/criteria.md").exists()
    for p in list((ROOT / "tools").glob("*.py")) + list((P / "scripts").glob("*.py")):
        ast.parse(p.read_text(), filename=str(p))
    subprocess.run(
        ["python3", "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=ROOT,
        check=True,
    )
    if shutil.which("claude"):
        for path in [ROOT, P]:
            subprocess.run(["claude", "plugin", "validate", str(path)], check=True)
    else:
        print(
            "Claude native validation: SKIP (CLI unavailable); structural checks passed"
        )
    print(
        "PASS: structure, JSON, versions, generated manifests, links, freshness lint, scripts and 18 eval fixtures"
    )


if __name__ == "__main__":
    check()
