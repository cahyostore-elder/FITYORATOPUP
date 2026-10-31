#!/usr/bin/env python3
"""Safely consolidate FityoraStore project documentation.

Run this file from the FITYORATOPUP repository root:
  python consolidate_fityora_docs.py          # dry run only
  python consolidate_fityora_docs.py --apply  # apply after reviewing dry run

Result:
- Keep root README.md.
- Merge every other project .md file (including nested README files) verbatim
  into root PEMBARUAN.md, with a table of contents and source headings.
- Redirect Markdown links and quoted file references to PEMBARUAN.md.
- Update audit scripts which read individual phase reports.
- Keep audit:phaseXX npm commands unchanged.
- Archive root-level phase test logs, old ZIP artifacts, catalog manifests,
  and standalone SQL patches instead of deleting them.
- Add a docs-layout regression test and npm run audit:docs.
- Back up every changed/deleted/moved file under the system temporary folder.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath

SKIP_DIRS = {".git", "node_modules", "dist", "build", "coverage", ".vercel"}
CODE_EXTS = {".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".json", ".yml", ".yaml", ".toml"}
ROOT = Path.cwd().resolve()


def git_branch(root: Path) -> str:
    try:
        return subprocess.check_output(["git", "branch", "--show-current"], cwd=root, text=True, stderr=subprocess.DEVNULL).strip() or "(detached / unknown)"
    except Exception:
        return "(not a Git checkout)"


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def collect_markdown(root: Path) -> list[Path]:
    keep = root / "README.md"
    output = root / "PEMBARUAN.md"
    result = []
    for path in root.rglob("*.md"):
        if path in (keep, output):
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        result.append(path)
    return sorted(result, key=lambda p: rel(p, root).casefold())


def slug(value: str) -> str:
    value = value.casefold().replace("\\", "/")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-") or "document"


def root_artifact_moves(root: Path) -> list[tuple[Path, Path]]:
    moves: list[tuple[Path, Path]] = []
    for p in root.iterdir():
        if not p.is_file():
            continue
        low = p.name.lower()
        if re.match(r"^(phase\d+.*|fityora-topup-phase.*|price_input_fix_audit|cyber_ice_icon_static_checks).*\.txt$", low):
            dest = root / "docs" / "archive" / "test-results" / p.name
        elif low.endswith(".zip"):
            dest = root / "artifacts" / "legacy" / p.name
        elif re.match(r"^phase(39|40)_catalog_manifest\.(csv|json)$", low):
            dest = root / "docs" / "archive" / "catalog-manifests" / p.name
        elif p.name == "SUPABASE_SECURITY_READONLY_CHECKS.sql":
            dest = root / "supabase" / "audits" / "legacy" / p.name
        elif p.name == "SUPABASE_VIP_REMOVAL_PATCH.sql":
            dest = root / "supabase" / "archive" / "standalone-patches" / p.name
        else:
            continue
        moves.append((p, dest))
    return moves


def build_maps(root: Path, docs: list[Path], moves: list[tuple[Path, Path]]):
    paths = [rel(p, root) for p in docs]
    anchors = {p: "doc-" + slug(p) for p in paths}
    grouped: dict[str, list[str]] = {}
    for p in paths:
        grouped.setdefault(PurePosixPath(p).name, []).append(p)
    basename_map = {name: (anchors[items[0]] if len(items) == 1 else None) for name, items in grouped.items()}
    asset_map = {rel(src, root): rel(dst, root) for src, dst in moves}
    asset_base_map = {PurePosixPath(old).name: new for old, new in asset_map.items()}
    return anchors, basename_map, asset_map, asset_base_map


def resolve_doc_reference(reference: str, source_path: str, anchors: dict[str, str], basename_map: dict[str, str | None]) -> str | None:
    if reference.startswith(("http://", "https://", "mailto:", "#", "data:")):
        return None
    path_part = reference.split("#", 1)[0].split("?", 1)[0].replace("\\", "/")
    source_dir = str(PurePosixPath(source_path).parent)
    candidate = posixpath.normpath(posixpath.join("" if source_dir == "." else source_dir, path_part))
    candidate = candidate.removeprefix("./")
    if candidate in anchors:
        return anchors[candidate]
    return basename_map.get(PurePosixPath(path_part).name)


def rewrite_markdown(text: str, source_path: str, anchors: dict[str, str], basename_map: dict[str, str | None], asset_map: dict[str, str], asset_base_map: dict[str, str]) -> str:
    link_re = re.compile(r"(?P<open>\]\()(?P<dest>[^)\s]+)(?P<close>\))")

    def link_replace(match: re.Match[str]) -> str:
        destination = match.group("dest")
        doc_anchor = resolve_doc_reference(destination, source_path, anchors, basename_map)
        if doc_anchor:
            return f"](PEMBARUAN.md#{doc_anchor})"
        if destination in asset_map:
            return f"]({asset_map[destination]})"
        base = PurePosixPath(destination.split("#", 1)[0]).name
        if base in asset_base_map:
            return f"]({asset_base_map[base]})"
        return match.group(0)

    text = link_re.sub(link_replace, text)

    # Redirect inline-code references to removed Markdown reports to the central file.
    doc_names = sorted({PurePosixPath(p).name for p in anchors if PurePosixPath(p).name != "README.md"}, key=len, reverse=True)
    for name in doc_names:
        text = text.replace(f"`{name}`", "`PEMBARUAN.md`")
    # Update inline references to archived CSV/JSON/SQL/ZIP artifacts.
    for old, new in sorted(asset_map.items(), key=lambda kv: len(kv[0]), reverse=True):
        text = text.replace(f"`{old}`", f"`{new}`")
        base = PurePosixPath(old).name
        text = text.replace(f"`{base}`", f"`{new}`")
    return text


def build_document(root: Path, docs: list[Path], anchors: dict[str, str], basename_map: dict[str, str | None], asset_map: dict[str, str], asset_base_map: dict[str, str]) -> str:
    paths = [rel(p, root) for p in docs]
    lines = [
        "# PEMBARUAN — Dokumentasi Terpadu FityoraStore",
        "",
        f"> Digabung otomatis: {dt.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M %Z')}.",
        "> README.md utama tetap terpisah. Dokumen sumber lainnya disertakan utuh di bagian masing-masing.",
        "> Gunakan daftar isi untuk membuka laporan, audit, panduan, dan catatan fase tertentu.",
        "",
        "## Daftar isi",
        "",
    ]
    for p in paths:
        lines.append(f"- [{p}](#{anchors[p]})")
    lines.extend(["", "---", ""])
    for path in docs:
        source = rel(path, root)
        original = path.read_text(encoding="utf-8", errors="replace")
        content = rewrite_markdown(original, source, anchors, basename_map, asset_map, asset_base_map)
        lines.extend([
            f'<a id="{anchors[source]}"></a>',
            f"## {source}",
            "",
            f"> **Sumber asli:** `{source}`",
            "",
            content.rstrip(),
            "",
            "---",
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def rewrite_code_references(root: Path, docs: list[Path], anchors: dict[str, str], basename_map: dict[str, str | None], asset_map: dict[str, str], asset_base_map: dict[str, str], dry_run: bool) -> list[Path]:
    doc_names = {PurePosixPath(rel(p, root)).name for p in docs}
    literal_re = re.compile(r"(?P<q>['\"`])(?P<value>[^'\"`\r\n]*\.(?:md|sql|csv|json|txt|zip))(?P=q)", re.IGNORECASE)
    changed: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in CODE_EXTS:
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        try:
            original = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        def replace(match: re.Match[str]) -> str:
            value = match.group("value").replace("\\", "/")
            clean = value.split("#", 1)[0].split("?", 1)[0]
            base = PurePosixPath(clean).name
            if clean in anchors or (base in doc_names and base != "README.md"):
                replacement = "PEMBARUAN.md"
            elif clean in asset_map:
                replacement = asset_map[clean]
            elif base in asset_base_map:
                replacement = asset_base_map[base]
            else:
                return match.group(0)
            return match.group("q") + replacement + match.group("q")

        updated = literal_re.sub(replace, original)
        if updated != original:
            changed.append(path)
            if not dry_run:
                path.write_text(updated, encoding="utf-8")
    return changed


def create_docs_layout_test(root: Path) -> str:
    return '''import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ignored = new Set(['.git', 'node_modules', 'dist', 'build', 'coverage', '.vercel']);
function findMarkdown(dir, result = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory() && ignored.has(entry.name)) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) findMarkdown(full, result);
    else if (entry.isFile() && entry.name.toLowerCase().endsWith('.md')) result.push(path.relative(root, full).split(path.sep).join('/'));
  }
  return result;
}

test('project keeps only README.md and PEMBARUAN.md as Markdown documents', () => {
  assert.ok(fs.existsSync(path.join(root, 'README.md')));
  assert.ok(fs.existsSync(path.join(root, 'PEMBARUAN.md')));
  assert.deepEqual(findMarkdown(root).sort(), ['PEMBARUAN.md', 'README.md']);
});

test('release checks and phase 61/64 regression tests use the consolidated document', () => {
  const required = [
    'scripts/release-preflight.mjs',
    'scripts/phase10-release-audit.mjs',
    'scripts/phase61-migration-baseline.test.mjs',
    'scripts/phase64-production-reconciliation.test.mjs',
  ];
  for (const relative of required) {
    const full = path.join(root, relative);
    if (!fs.existsSync(full)) continue;
    const source = fs.readFileSync(full, 'utf8');
    assert.ok(source.includes('PEMBARUAN.md'), `${relative} must read the consolidated document`);
  }
});
'''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="apply changes; default is a non-destructive dry run")
    args = parser.parse_args()
    root = Path.cwd().resolve()
    if not (root / "package.json").exists() or not (root / "src").is_dir():
        print("ERROR: Jalankan script dari root FITYORATOPUP (folder berisi package.json dan src/).", file=sys.stderr)
        return 2

    docs = collect_markdown(root)
    if not docs:
        print("Tidak ada dokumen tambahan yang perlu digabung; README.md root dikecualikan.")
        return 0
    moves = root_artifact_moves(root)
    conflicts = [(src, dst) for src, dst in moves if dst.exists()]
    if conflicts:
        print("ERROR: tujuan arsip sudah ada; hentikan agar tidak menimpa file:")
        for src, dst in conflicts:
            print(f"  {src.name} -> {rel(dst, root)}")
        return 3

    anchors, basename_map, asset_map, asset_base_map = build_maps(root, docs, moves)
    merged = build_document(root, docs, anchors, basename_map, asset_map, asset_base_map)
    code_changes = rewrite_code_references(root, docs, anchors, basename_map, asset_map, asset_base_map, dry_run=True)
    print(f"Branch: {git_branch(root)}")
    print(f"Dokumen .md digabung: {len(docs)} (README.md root tetap di luar)")
    print(f"PEMBARUAN.md hasil gabungan: {len(merged.encode('utf-8')):,} byte")
    print(f"Skrip/config yang referensinya akan dialihkan: {len(code_changes)}")
    print(f"Artefak root yang dipindahkan ke folder arsip: {len(moves)}")
    print("Dokumen yang digabung:")
    for doc in docs:
        print("  - " + rel(doc, root))
    if not args.apply:
        print("\nDRY RUN: belum ada perubahan. Setelah memeriksa daftar di atas, jalankan ulang dengan --apply.")
        return 0

    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = Path(tempfile.gettempdir()) / f"FITYORATOPUP-doc-consolidation-{timestamp}"
    backup.mkdir(parents=True, exist_ok=False)
    affected = set(docs) | set(code_changes) | {root / "PEMBARUAN.md", root / "scripts" / "docs-layout.test.mjs", root / "package.json"}
    readme = root / "README.md"
    if readme.exists():
        affected.add(readme)
    for src, _ in moves:
        affected.add(src)
    for file in sorted(affected):
        if file.exists() and file.is_file():
            target = backup / file.relative_to(root)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, target)

    (root / "PEMBARUAN.md").write_text(merged, encoding="utf-8")
    rewrite_code_references(root, docs, anchors, basename_map, asset_map, asset_base_map, dry_run=False)

    # Redirect links and inline references in the retained root README.
    if readme.exists():
        old = readme.read_text(encoding="utf-8")
        new = rewrite_markdown(old, "README.md", anchors, basename_map, asset_map, asset_base_map)
        if new != old:
            readme.write_text(new, encoding="utf-8")

    # Archive root-level non-source clutter without deleting any artifacts.
    for src, dst in moves:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))

    # Remove source Markdown only after the complete merge and backups are written.
    for doc in docs:
        doc.unlink()

    # Preserve the intentionally empty Supabase directories after their README guides
    # have been copied verbatim into PEMBARUAN.md.
    for directory in (root / "supabase" / "migrations", root / "supabase" / "schemas"):
        if directory.exists() and not any(directory.iterdir()):
            (directory / ".gitkeep").write_text("", encoding="utf-8")

    # Register a small layout regression check in package.json.
    package_path = root / "package.json"
    package = json.loads(package_path.read_text(encoding="utf-8"))
    package.setdefault("scripts", {})["audit:docs"] = "node --test scripts/docs-layout.test.mjs"
    release = package["scripts"].get("audit:release", "")
    if "npm run audit:docs" not in release:
        package["scripts"]["audit:release"] = release + " && npm run audit:docs"
    package_path.write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (root / "scripts" / "docs-layout.test.mjs").write_text(create_docs_layout_test(root), encoding="utf-8")

    print("\nBERHASIL: seluruh dokumen .md selain README.md root digabung ke PEMBARUAN.md.")
    print(f"Backup seluruh file terdampak: {backup}")
    print("Perintah npm run audit:phaseXX tetap dipertahankan; referensi laporan dialihkan ke PEMBARUAN.md.")
    print("Artefak lama dipindahkan ke docs/archive/, artifacts/legacy/, atau supabase/archive/.")
    print("Selanjutnya jalankan: node --test scripts/*.test.mjs && npm run audit:release")
    print("Periksa hasil dengan: git status --short")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
