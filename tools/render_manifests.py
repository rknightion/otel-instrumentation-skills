#!/usr/bin/env python3
"""Generate all client metadata from plugin.meta.json; --check never writes."""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"


def manifests(meta):
    entry = {**meta, "source": "./plugins/otel"}
    return {
        "plugins/otel/plugin.json": {"$schema": SCHEMA, **meta},
        "plugins/otel/.claude-plugin/plugin.json": meta,
        ".claude-plugin/marketplace.json": {
            "name": meta["name"],
            "owner": meta["author"],
            "metadata": {
                "version": meta["version"],
                "description": meta["description"],
            },
            "plugins": [entry],
        },
        ".agents/plugins/marketplace.json": {
            "name": meta["name"],
            "interface": {"displayName": meta["name"]},
            "plugins": [
                {
                    "name": meta["name"],
                    "source": {"source": "local", "path": "./plugins/otel"},
                    "policy": {
                        "installation": "AVAILABLE",
                        "authentication": "ON_INSTALL",
                    },
                    "category": "Developer Tools",
                }
            ],
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale = []
    for name, data in manifests(
        json.loads((ROOT / "plugin.meta.json").read_text())
    ).items():
        path = ROOT / name
        expected = json.dumps(data, indent=2) + "\n"
        if args.check:
            if not path.exists() or path.read_text() != expected:
                stale.append(name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected)
    if stale:
        parser.exit(1, "Stale manifests; run just render: " + ", ".join(stale) + "\n")
    print("Manifests current" if args.check else "Manifests rendered")


if __name__ == "__main__":
    main()
