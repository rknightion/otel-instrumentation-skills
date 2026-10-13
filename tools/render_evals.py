#!/usr/bin/env python3
"""Render identical native-eval scaffolds and graders from canonical corpus/fixtures."""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "plugins/otel/evals"


def outputs():
    result = {}
    for c in json.loads((EVALS / "corpus.json").read_text()):
        case = EVALS / c["id"]
        files = {
            f.name: f.read_text()
            for f in sorted((EVALS / "fixtures" / c["fixture"]).iterdir())
            if f.is_file()
        }
        code = (
            "from pathlib import Path\nimport json\nfiles = json.loads("
            + repr(json.dumps(files))
            + ")\nfor name, text in files.items():\n    Path(name).write_text(text)\n"
        )
        result[case / "fixture.sh"] = (
            "#!/bin/bash\nset -euo pipefail\npython3 - <<'OTEL_FIXTURE'\n"
            + code
            + "OTEL_FIXTURE\n"
        )
        result[case / "case.yaml"] = (
            'schema_version: "1.1"\nname: '
            + c["id"]
            + "\ncontext:\n  scaffold_script: fixture.sh\n"
        )
        result[case / "graders/criteria.md"] = (
            f"---\ntype: llm\nfocus: trace\nweight: 1\n---\n\nPass only if: {c['pass_criteria']}\n\n{c['fail_criteria']} Judge transcript/tool evidence, not only claims in the final answer. Unavailable tools explicitly reported are limitations, not successful runtime validation.\n"
        )
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    stale = []
    for path, content in outputs().items():
        if args.check:
            if not path.exists() or path.read_text() != content:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
    if stale:
        p.exit(1, "Stale eval resources; run just render: " + ", ".join(stale) + "\n")
    print("Eval resources current" if args.check else "Eval resources rendered")


if __name__ == "__main__":
    main()
