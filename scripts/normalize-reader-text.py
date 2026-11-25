#!/usr/bin/env python3
"""Fjern forfatter-stemme (Bull/Hammer) fra brukertekst i JSON. Kilde ligger i source_ref."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def clean_sentence(s: str) -> str:
    t = s.strip()
    if not t:
        return t

    # Hele-setning erstattinger først
    whole = [
        (
            "Christian IV påla at en ny by skulle oppføres ved Akershus. Navnet Christiania og det planlagte gateroset markerer starten på bind II i Bulls verk.",
            "Christian IV påla at en ny by skulle oppføres ved Akershus. Navnet Christiania og det planlagte gateroset markerer starten på en ny byperiode.",
        ),
        (
            "Christian IV påla at befolkningen ikke skulle gjenreise den gamle byen, men flytte til en planlagt festningsby ved Akershus. Bull plasserer dette som starten på bind II.",
            "Christian IV påla at befolkningen ikke skulle gjenreise den gamle byen, men flytte til en planlagt festningsby ved Akershus.",
        ),
        (
            "Brannen ødela store deler av middelalder-Oslo. Bull daterer katastrofen til 17. august; kongen ønsket ikke gjenreise på gamle tomter.",
            "Brannen ødela store deler av middelalder-Oslo 17. august 1624. Kongen ønsket ikke gjenreise på gamle tomter.",
        ),
        (
            "1814 gjorde Christiania til hovedstad i den nye unionsstaten. Bull i bind III og Hammer i bind IV beskriver hvordan slottsanlegget ble symbol på embetskultur og nasjonalt sentrum.",
            "1814 gjorde Christiania til hovedstad i den nye unionsstaten. Slottsanlegget ble symbol på embetskultur og nasjonalt sentrum.",
        ),
        (
            "Selv om Bull skriver før den romantiske fortellingen, beskriver han i bind II-III hvordan Sagene og fossen ble knyttet til vannkraft, sag og tidlig fabrikkdrift.",
            "Sagene og fossen ble knyttet til vannkraft, sag og tidlig fabrikkdrift da byen vokste langs elva.",
        ),
        (
            "300-årsjubileet for Christiania i 1924 var kulminasjonen på bind V. Hammer skildrer fest, minner og byens moderne selvbilde.",
            "300-årsjubileet for Christiania i 1924 feiret byens historie med parade, utstillinger og en moderne storbyidentitet.",
        ),
    ]
    for old, new in whole:
        if t == old:
            return new

    # Mønstre (rekkefølge matters)
    patterns: list[tuple[str, str]] = [
        (r"\s*Bull bruker[^.]+til å\s+", " "),
        (r"\s*Bull i bind III og Hammer i bind IV beskriver hvordan\s+", " "),
        (r"\s*Hammer i bind IV\s+", " "),
        (r"\s*Hammer åpner bind V med\s+", " "),
        (r"\s*Hammer lar\s+", " "),
        (r"\s*Bull (?:starter|beskriver|skildrer|framhever|understreker|plasserer|følger|leser|knytter|peker på|ser|tar|diskuterer|viser)\s+(?:at\s+)?", " "),
        (r"\s*Hammer (?:beskriver|følger|framhever|knytter|plasserer|skildrer)\s+(?:at\s+)?", " "),
        (r"\s*i Bulls (?:framstilling|topografikapittel)\s+", " "),
        (r"\s*Bulls bind II beskriver\s+", " "),
        (r"\s*Bull og Hammer[^.]+beskriver\s+", " "),
        (r"\s*som Bull beskriver", ""),
        (r"\s*Bull leser dem som", " De fungerer som"),
        (r"\s*Bull leser\s+", " "),
        (r"\s*I Bulls framstilling hører\s+", " "),
        (r"\s*i Bulls verk", ""),
        (r"\s*på bind II", ""),
        (r"\s*Bind II-III:\s*", ""),
        (r"\s*bind II-III\s*", ""),
        (r"\s*i Bulls\s+", " "),
    ]
    for pat, repl in patterns:
        t = re.sub(pat, repl, t, flags=re.IGNORECASE)

    # Rydd dobbeltrom og kapital
    t = re.sub(r"\s{2,}", " ", t)
    t = re.sub(r"\s+([,.;:])", r"\1", t)
    t = re.sub(r"\.\s*\.", ".", t)
    if t and t[0].islower():
        t = t[0].upper() + t[1:]
    return t.strip()


def main() -> None:
    for fname, key in [
        ("places.json", "places"),
        ("events.json", "events"),
        ("context.json", "entries"),
        ("blue-signs.json", "signs"),
    ]:
        path = ROOT / "data" / fname
        doc = json.loads(path.read_text(encoding="utf-8"))
        n = 0
        for item in doc[key]:
            for field in ("summary",):
                old = item.get(field, "")
                new = clean_sentence(old)
                if new != old:
                    item[field] = new
                    n += 1
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{fname}: oppdatert {n} {key}")

    ep_path = ROOT / "data" / "episodes.json"
    eps = json.loads(ep_path.read_text(encoding="utf-8"))
    ep_map = {
        "middelalder-oslo": "Gamlebyen og parken der middelalderbyens kjerne tok form: kirker, bispegaard og handelsliv mot fjorden.",
        "akerselva-tidlig": "Fra Sagene ned Akerselva til fjorden: vannkraft, verk og arbeidskvarterer i byens vekst.",
        "1814-hovedstaden": "1814 som vendepunkt: slottskvartalet, embetskultur og universitetsbyen.",
        "mot-1924": "Fra unionshovedstad via jernbane og arbeiderkvarter til jubileumsåret 1924.",
    }
    for ep in eps["episodes"]:
        if ep["id"] in ep_map:
            ep["description"] = ep_map[ep["id"]]
    ep_path.write_text(json.dumps(eps, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("episodes.json: descriptions oppdatert")


if __name__ == "__main__":
    main()