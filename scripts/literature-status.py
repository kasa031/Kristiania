#!/usr/bin/env python3
"""Synk innsamlingsstatus for literature/ mot TOC og data/*.json."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "sources" / "innsamling" / "manifest.json"
OUT_STATUS = ROOT / "sources" / "innsamling" / "status.json"
OUT_GAPS = ROOT / "sources" / "innsamling" / "gaps.json"
OUT_MD = ROOT / "sources" / "innsamling" / "INNSAMLING.md"
LIT = ROOT / "literature"
EXCERPTS = ROOT / "sources" / "excerpts"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def is_draft_ref(item: dict) -> bool:
    if item.get("verified") is True:
        return False
    ref = item.get("source_ref") or {}
    pages = str(ref.get("pages", ""))
    note = str(ref.get("note", ""))
    if "~" in pages:
        return True
    if re.search(r"verifiser|ukjent|todo", note, re.I):
        return True
    if re.search(r"verifiser|ukjent", pages, re.I):
        return True
    return False


def excerpt_count_for_bind(roman: str) -> int:
    if not EXCERPTS.is_dir():
        return 0
    prefix = f"bind-{roman}".lower()
    n = 0
    for path in EXCERPTS.iterdir():
        if path.name.startswith(".") or path.name == "README.md":
            continue
        if path.name.lower().startswith(prefix):
            n += 1
    return n


def gate_ok(flags: dict, gate_names: list[str]) -> bool:
    return all(flags.get(g, False) for g in gate_names)


def main() -> None:
    manifest = load_json(MANIFEST)
    places = load_json(ROOT / "data" / "places.json")["places"]
    events = load_json(ROOT / "data" / "events.json")["events"]
    all_items = places + events

    bind_rows: list[dict] = []
    blocking: list[dict] = []
    global_gaps: dict = {"draft_refs": [], "missing_pdf": [], "missing_toc": []}

    for spec in manifest["binds"]:
        bind = spec["bind"]
        roman = spec["roman"]
        pdf_path = LIT / spec["pdf_filename"]
        toc_path = ROOT / spec["toc_primary"]

        bind_items = [x for x in all_items if x.get("bind") == bind]
        draft_items = [x for x in bind_items if is_draft_ref(x)]
        verified = [x for x in bind_items if x.get("verified") is True]

        pdf_on_disk = pdf_path.is_file()
        pdf_bytes = pdf_path.stat().st_size if pdf_on_disk else 0
        toc_file = toc_path.is_file() and toc_path.stat().st_size > 200
        toc_lines = 0
        if toc_path.is_file():
            toc_lines = len(toc_path.read_text(encoding="utf-8", errors="replace").splitlines())

        flags = {
            "pdf_on_disk": pdf_on_disk,
            "toc_file": toc_file,
            "toc_reviewed": bool(spec.get("toc_reviewed")),
            "json_has_items": len(bind_items) > 0,
            "json_pages_firm": len(draft_items) == 0 and len(bind_items) > 0,
            "json_verified_all": len(verified) == len(bind_items) and len(bind_items) > 0,
        }
        flags["karina_spot_check"] = flags["json_verified_all"]

        gates = manifest["gates"]
        can_add = gate_ok(flags, gates["before_new_place_or_event"])
        can_tighten = gate_ok(flags, gates["before_replace_tilde_pages"])
        can_verify = gate_ok(flags, gates["before_verified_true"])

        next_steps: list[str] = []
        if not pdf_on_disk:
            next_steps.append(f"Legg PDF i literature/{spec['pdf_filename']}")
            global_gaps["missing_pdf"].append(bind)
        if not toc_file:
            next_steps.append("Kjør `python scripts/extract-toc.py` eller skriv TOC manuelt")
            global_gaps["missing_toc"].append(bind)
        elif not flags["toc_reviewed"]:
            next_steps.append("Sammenlign TOC med fysisk bind; sett toc_reviewed i manifest.json")
        if draft_items:
            next_steps.append(
                f"Fastsett sidetall for {len(draft_items)} JSON-poster (jf. gaps.json bind {bind})",
            )
        if bind_items and not flags["json_verified_all"]:
            next_steps.append("Sluttkontroll: verified mot bind (etter feltgatur)")

        row = {
            "bind": bind,
            "roman": roman,
            "title": spec["title"],
            "pdf_filename": spec["pdf_filename"],
            "episodes": spec.get("episodes", []),
            "flags": flags,
            "counts": {
                "json_items": len(bind_items),
                "json_places": len([x for x in places if x.get("bind") == bind]),
                "json_events": len([x for x in events if x.get("bind") == bind]),
                "draft_refs": len(draft_items),
                "verified": len(verified),
                "excerpts": excerpt_count_for_bind(roman),
                "toc_lines": toc_lines,
                "pdf_bytes": pdf_bytes,
            },
            "permissions": {
                "may_add_json_content": can_add,
                "may_replace_tilde_pages": can_tighten,
                "may_set_verified_true": can_verify,
            },
            "next_steps": next_steps,
        }
        bind_rows.append(row)

        if not can_add:
            blocking.append(
                {
                    "bind": bind,
                    "reason": "before_new_place_or_event",
                    "missing": [g for g in gates["before_new_place_or_event"] if not flags.get(g)],
                },
            )

        for item in draft_items:
            ref = item.get("source_ref") or {}
            global_gaps["draft_refs"].append(
                {
                    "bind": bind,
                    "kind": "place" if item in places else "event",
                    "id": item["id"],
                    "pages": ref.get("pages"),
                    "note": ref.get("note"),
                },
            )

    draft_rows = [r for r in bind_rows if r["counts"]["draft_refs"] > 0]
    priority_bind = (
        max(draft_rows, key=lambda r: r["counts"]["draft_refs"])["bind"] if draft_rows else None
    )

    status = {
        "_generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "summary": {
            "pdfs_on_disk": sum(1 for r in bind_rows if r["flags"]["pdf_on_disk"]),
            "pdfs_expected": len(bind_rows),
            "toc_ready": sum(1 for r in bind_rows if r["flags"]["toc_file"]),
            "toc_reviewed": sum(1 for r in bind_rows if r["flags"]["toc_reviewed"]),
            "json_items_total": len(all_items),
            "draft_refs_total": len(global_gaps["draft_refs"]),
            "verified_total": sum(1 for x in all_items if x.get("verified") is True),
            "priority_bind_for_page_work": priority_bind,
        },
        "blocking_new_json": blocking,
        "binds": bind_rows,
        "ai_checklist_before_more_content": [
            "Les denne filen (status.json) eller INNSAMLING.md",
            "Ikke legg til nye steder/hendelser for bind uten pdf_on_disk + toc_file",
            "Erstatt ~-sidetall kun nar toc_reviewed er true for bindet",
            "Bruk sources/excerpts/ ved tvil - ikke store OCR-filer",
        ],
    }

    OUT_STATUS.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_GAPS.write_text(json.dumps(global_gaps, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Innsamling - bind I-V",
        "",
        f"*Autogenerert {status['_generated']}. Kjør på nytt: `python scripts/literature-status.py`.*",
        "",
        "Dette er **kilde-/boksporing** (supplement til [FREMGANG.md](../../content/FREMGANG.md)), ikke en parallel oppgaveliste.",
        "",
        "## Kan AI utvide JSON nå?",
        "",
        "| Bind | PDF | TOC | TOC sjekket | Draft sidetall | Nytt innhold OK? |",
        "|------|:---:|:---:|:-----------:|:--------------:|:----------------:|",
    ]
    for row in bind_rows:
        f = row["flags"]
        c = row["counts"]
        ok = "ja" if row["permissions"]["may_add_json_content"] else "**nei**"
        pdf = "ja" if f["pdf_on_disk"] else "nei"
        toc = "ja" if f["toc_file"] else "nei"
        rev = "ja" if f["toc_reviewed"] else "nei"
        lines.append(
            f"| {row['roman']} | {pdf} | {toc} | {rev} | {c['draft_refs']} | {ok} |",
        )

    lines.extend(
        [
            "",
            f"**Prioritet for sidetall-arbeid:** bind {priority_bind or '-'}",
            "",
            "## Neste steg per bind",
            "",
        ],
    )
    for row in bind_rows:
        lines.append(f"### Bind {row['roman']} - {row['title']}")
        lines.append(f"Løyper: {', '.join(row['episodes']) or '-'}")
        if row["next_steps"]:
            for step in row["next_steps"]:
                lines.append(f"- {step}")
        else:
            lines.append("- Ingen blokkerende hull i innsamling (fortsett felt/verifisering).")
        lines.append("")

    lines.extend(
        [
            "## Filer",
            "",
            "| Fil | Rolle |",
            "|-----|--------|",
            "| [manifest.json](manifest.json) | Forventninger, pdf-navn, `toc_reviewed` (du/AI) |",
            "| [status.json](status.json) | Maskinlesbar status (AI leser denne) |",
            "| [gaps.json](gaps.json) | Lister over draft `source_ref` |",
            "| `literature/*.pdf` | Lokale boker (gitignorert) |",
            "| [sources/toc/](../toc/) | Innholdsfortegnelser |",
            "| [sources/excerpts/](../excerpts/) | Korte utdrag ved behov |",
            "",
        ],
    )

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_STATUS.relative_to(ROOT)}")
    print(f"Wrote {OUT_GAPS.relative_to(ROOT)} ({len(global_gaps['draft_refs'])} draft refs)")
    print(f"Wrote {OUT_MD.relative_to(ROOT)}")
    print(
        f"PDFs {status['summary']['pdfs_on_disk']}/{status['summary']['pdfs_expected']}; "
        f"draft refs {status['summary']['draft_refs_total']}",
    )


if __name__ == "__main__":
    main()