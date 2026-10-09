"""Offline file integrity baseline and comparison (read-only file access)."""
import argparse
import hashlib
import json
from pathlib import Path


def hash_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(64 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def snapshot(root):
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("root must be an existing directory")
    files = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            continue
        if path.is_file():
            key = path.relative_to(root).as_posix()
            files[key] = hash_file(path)
    return files


def compare(previous, current):
    before = previous["files"] if "files" in previous else previous
    return {
        "added": sorted(current.keys() - before.keys()),
        "removed": sorted(before.keys() - current.keys()),
        "modified": sorted(k for k in before.keys() & current.keys()
                           if before[k] != current[k]),
        "unchanged": sum(before[k] == current[k]
                         for k in before.keys() & current.keys()),
    }


def main():
    parser = argparse.ArgumentParser(description="Offline SHA-256 file monitoring")
    parser.add_argument("action", choices=["init", "check"])
    parser.add_argument("directory", type=Path)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    root = args.directory.resolve(strict=True)
    manifest_path = args.manifest.resolve()
    if manifest_path.is_relative_to(root):
        parser.error("store the baseline outside the monitored directory")
    if args.report and args.report.resolve().is_relative_to(root):
        parser.error("store the report outside the monitored directory")
    if args.action == "init":
        manifest = {"schema_version": 1, "algorithm": "sha256",
                    "files": snapshot(root)}
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(json.dumps(manifest, indent=2) + "\n")
        print(json.dumps({"baseline_files": len(manifest["files"])}))
    else:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        if manifest.get("algorithm") != "sha256" or manifest.get("schema_version") != 1:
            raise ValueError("unsupported manifest version")
        changes = compare(manifest, snapshot(root))
        payload = json.dumps(changes, indent=2) + "\n"
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(payload, encoding="utf-8")
        print(payload, end="")


if __name__ == "__main__":
    main()
