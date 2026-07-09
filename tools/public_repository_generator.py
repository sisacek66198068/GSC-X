from pathlib import Path
from datetime import datetime
import re
import subprocess

ROOT = Path(".")
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP = ROOT / f"backups_generated_indexes_{STAMP}"
IGNORE_DIRS = {".git", ".venv", ".venv_solar", "__pycache__", "node_modules"}

PROTECTED_NOTE = """
This public index is documentation-only. It does not expose Executive Kernel source code,
CM/ELI/PTM/MR/MRI internals, adaptive rules, coefficients, decision logic, or private telemetry.
"""

def skip(p: Path) -> bool:
    parts = set(p.parts)
    return bool(parts & IGNORE_DIRS) or any(x.startswith("backups_") for x in p.parts)

def files(pattern):
    return sorted(p for p in ROOT.rglob(pattern) if not skip(p))

def git_commit():
    try:
        return subprocess.check_output(["git","rev-parse","--short","HEAD"], text=True).strip()
    except Exception:
        return "unknown"

def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists():
        bp = BACKUP / path
        bp.parent.mkdir(parents=True, exist_ok=True)
        bp.write_bytes(p.read_bytes())
    p.write_text(text.strip() + "\n", encoding="utf-8")
    print("OK", path)

mds = files("*.md")
csvs = files("*.csv")
figs = files("*.png") + files("*.svg") + files("*.pdf")
pys = files("*.py")
validation_dirs = sorted([p for p in (ROOT / "validation").glob("*") if p.is_dir()]) if (ROOT/"validation").exists() else []

doi_re = re.compile(r"https://doi\.org/[^\s\)\]]+")
dois = []
for p in mds[:500]:
    try:
        for d in doi_re.findall(p.read_text(encoding="utf-8", errors="ignore")):
            dois.append((d, str(p)))
    except Exception:
        pass

sandbox_py = [p for p in pys if "sandbox" in p.name.lower() or "gscx_" in p.name.lower()]
commit = git_commit()

write("PUBLIC_REPOSITORY_POLICY.md", f"""
# Public Repository Policy

GSC-X public repository policy.

Allowed public content:
- Markdown documentation
- Aggregated CSV results
- Figures and publication graphics
- DOI references
- Sandbox links
- High-level architecture summaries

Protected content:
- source implementation
- Executive Kernel internals
- CM / ELI / PTM / MR / MRI logic
- adaptive rules
- decision logic
- private coefficients
- private telemetry

Existing Python sandbox files are part of the live project and must not be moved, renamed, deleted or refactored by documentation updates.

Commit reference: {commit}
""")

write("RESULTS_INDEX.md", "# GSC-X Results Index\n\n" + PROTECTED_NOTE + "\n\n## Validation folders\n\n" +
      "\n".join(f"- `{p}`" for p in validation_dirs) + "\n")

write("CSV_INDEX.md", "# CSV Index\n\nAggregate CSV files detected in the repository.\n\n" +
      "\n".join(f"- `{p}`" for p in csvs[:300]) +
      (f"\n\nShowing first 300 of {len(csvs)} CSV files." if len(csvs) > 300 else ""))

write("FIGURES_INDEX.md", "# Figures Index\n\nPublic figure and publication graphic files detected.\n\n" +
      "\n".join(f"- `{p}`" for p in figs[:300]) +
      (f"\n\nShowing first 300 of {len(figs)} figure files." if len(figs) > 300 else ""))

write("DOI_INDEX.md", "# DOI Index\n\nDetected DOI references in Markdown files.\n\n" +
      ("\n".join(f"- {d} — `{src}`" for d, src in sorted(set(dois))) if dois else "No DOI links detected in scanned Markdown files."))

write("SANDBOX_INDEX.md", "# Sandbox Index\n\nDetected sandbox-related Python entry files. Listed for navigation only; contents are not indexed.\n\n" +
      "\n".join(f"- `{p}`" for p in sandbox_py[:200]) +
      (f"\n\nShowing first 200 of {len(sandbox_py)} sandbox-related Python files." if len(sandbox_py) > 200 else ""))

write("VALIDATION_MATRIX.md", "# Validation Matrix\n\n" + PROTECTED_NOTE + "\n\n| Validation folder | CSV count | Figure count |\n|---|---:|---:|\n" +
      "\n".join(
          f"| `{d}` | {len(list(d.rglob('*.csv')))} | {len(list(d.rglob('*.png'))) + len(list(d.rglob('*.svg'))) + len(list(d.rglob('*.pdf')))} |"
          for d in validation_dirs
      ))

write("REPOSITORY_AUDIT_PUBLIC.md", f"""
# Public Repository Audit

Commit: `{commit}`

| Item | Count |
|---|---:|
| Markdown files | {len(mds)} |
| CSV files | {len(csvs)} |
| Figure/PDF files | {len(figs)} |
| Python files | {len(pys)} |
| Validation folders | {len(validation_dirs)} |
| DOI references detected | {len(set(d for d, _ in dois))} |
| Sandbox-related Python files listed | {len(sandbox_py)} |

This audit is documentation-only and does not read Python source contents.
""")

print()
print("DONE")
print("Backup folder:", BACKUP)
