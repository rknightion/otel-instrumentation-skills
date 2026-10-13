#!/usr/bin/env python3
"""Bounded public upstream lookup. JSON output always includes source provenance."""

import argparse
import datetime
import json
import re
import urllib.error
import urllib.parse
import urllib.request

MAX_BYTES = 8 * 1024 * 1024


def fetch(url):
    request = urllib.request.Request(
        url, headers={"User-Agent": "otel-instrumentation-skills", "Accept": "application/json"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        raw = response.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError("Source exceeds 8 MiB bound; select a narrower source")
    return raw.decode("utf-8")


def get_json(url):
    return json.loads(fetch(url))


def repository(value):
    if not re.fullmatch(r"(open-telemetry|ollygarden|dash0hq)/[A-Za-z0-9_.-]+", value):
        raise ValueError(
            "Use an identified official open-telemetry repository or the recorded synthesis upstream"
        )
    return value


def segment(value):
    if not value or value.startswith("-") or "\n" in value or "\r" in value:
        raise ValueError("Empty or unsafe identifier")
    return urllib.parse.quote(value, safe="")


def source_path(value):
    if value.startswith("/") or ".." in value.split("/") or "\\" in value:
        raise ValueError("Source path must stay inside the repository")
    return urllib.parse.quote(value, safe="/")


def resolve(repo, ref):
    url = f"https://api.github.com/repos/{repository(repo)}/commits/{segment(ref)}"
    data = get_json(url)
    return data["sha"]


def tree(repo, commit):
    data = get_json(
        f"https://api.github.com/repos/{repo}/git/trees/{commit}?recursive=1"
    )
    if data.get("truncated"):
        raise ValueError("GitHub tree is truncated; use a narrower tagged checkout")
    return [x["path"] for x in data["tree"] if x["type"] == "blob"]


def snippets(content, term, context=5, limit=12):
    lines = content.splitlines()
    hits = [i for i, line in enumerate(lines) if term.casefold() in line.casefold()]
    result = []
    end = -1
    for i in hits:
        if i <= end:
            continue
        start, end = max(0, i - context), min(len(lines) - 1, i + context)
        result.append(
            {
                "start_line": start + 1,
                "end_line": end + 1,
                "text": "\n".join(lines[start : end + 1]),
            }
        )
        if len(result) == limit:
            break
    return {
        "matches": result,
        "total_matching_lines": len(hits),
        "limited": len(hits) > limit,
        "limitation": "Text search, not a resolved semantic registry or exhaustive emission analysis",
    }


def lookup(args):
    result = {
        "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "cache": "none; live fetch",
    }
    if args.command == "package":
        name = args.name
        if args.ecosystem == "npm":
            url = "https://registry.npmjs.org/" + segment(name)
            data = get_json(url)
            version = args.version or data["dist-tags"]["latest"]
            selected = data["versions"][version]
            payload = {
                k: selected.get(k)
                for k in [
                    "name",
                    "version",
                    "engines",
                    "dependencies",
                    "peerDependencies",
                    "deprecated",
                    "repository",
                ]
            }
            payload["dist-tags"] = data["dist-tags"]
        elif args.ecosystem == "pypi":
            url = (
                "https://pypi.org/pypi/"
                + segment(name)
                + ("/" + segment(args.version) if args.version else "")
                + "/json"
            )
            info = get_json(url)["info"]
            payload = {
                k: info.get(k)
                for k in [
                    "name",
                    "version",
                    "requires_python",
                    "requires_dist",
                    "project_urls",
                ]
            }
        else:
            escaped = "".join("!" + c.lower() if c.isupper() else c for c in name)
            if not re.fullmatch(r"[a-z0-9!./_-]+", escaped) or ".." in escaped.split(
                "/"
            ):
                raise ValueError("Invalid Go module")
            suffix = (
                "/@v/" + segment(args.version) + ".info" if args.version else "/@latest"
            )
            url = "https://proxy.golang.org/" + escaped + suffix
            payload = get_json(url)
        return {
            **result,
            "source": url,
            "data": payload,
            "compatibility": "not validated",
        }
    repo = repository(args.repo)
    if args.command == "release":
        suffix = "tags/" + segment(args.tag) if args.tag else "latest"
        url = f"https://api.github.com/repos/{repo}/releases/{suffix}"
        data = get_json(url)
        return {
            **result,
            "source": url,
            "repository": repo,
            "data": {
                k: data.get(k)
                for k in ["tag_name", "published_at", "prerelease", "html_url", "body"]
            },
            "limitation": "Repository release is not every independent package/module release",
        }
    commit = resolve(repo, args.ref)
    result.update(repository=repo, requested_ref=args.ref, commit=commit)
    if args.command == "file":
        url = f"https://raw.githubusercontent.com/{repo}/{commit}/{source_path(args.path)}"
        content = fetch(url)
        return {
            **result,
            "source": url,
            "data": snippets(content, args.match) if args.match else content,
        }
    paths = tree(repo, commit)
    if args.command == "tree":
        selected = [p for p in paths if args.match.casefold() in p.casefold()]
        return {
            **result,
            "source": f"https://github.com/{repo}/tree/{commit}",
            "paths": selected[: args.limit],
            "total": len(selected),
            "limited": len(selected) > args.limit,
        }
    # Caller selects a narrow domain before content search. Ref is required, never silently latest.
    paths = [
        p
        for p in paths
        if args.domain.casefold() in p.casefold()
        and p.endswith((".yaml", ".yml", ".md"))
    ]
    if len(paths) > args.max_files:
        raise ValueError(
            f"{len(paths)} files match; narrow --domain (bound {args.max_files})"
        )
    matches = []
    for path in paths:
        url = f"https://raw.githubusercontent.com/{repo}/{commit}/{source_path(path)}"
        hits = snippets(fetch(url), args.term)
        if hits["matches"]:
            matches.append({"source": url, "path": path, **hits})
    return {
        **result,
        "files_searched": len(paths),
        "data": matches,
        "limitation": "Bounded text lookup. Follow referenced definitions and read group context before applying.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ["release", "file", "tree", "semconv"]:
        p = sub.add_parser(name)
        p.add_argument(
            "--repo",
            default="open-telemetry/semantic-conventions"
            if name == "semconv"
            else None,
            required=name != "semconv",
        )
        if name == "release":
            p.add_argument("--tag")
        else:
            p.add_argument("--ref", required=True)
        if name == "file":
            p.add_argument("--path", required=True)
            p.add_argument("--match")
        if name == "tree":
            p.add_argument("--match", required=True)
            p.add_argument("--limit", type=int, default=60)
        if name == "semconv":
            p.add_argument("--domain", required=True)
            p.add_argument("--term", required=True)
            p.add_argument("--max-files", type=int, default=30)
    p = sub.add_parser("package")
    p.add_argument("ecosystem", choices=["go", "pypi", "npm"])
    p.add_argument("name")
    p.add_argument("--version")
    args = parser.parse_args()
    try:
        if hasattr(args, "limit") and not 1 <= args.limit <= 200:
            raise ValueError("--limit must be 1..200")
        if hasattr(args, "max_files") and not 1 <= args.max_files <= 100:
            raise ValueError("--max-files must be 1..100")
        print(json.dumps(lookup(args), indent=2))
    except (ValueError, KeyError, OSError, urllib.error.URLError) as error:
        parser.exit(1, f"Lookup failed; no fallback version selected: {error}\n")


if __name__ == "__main__":
    main()
