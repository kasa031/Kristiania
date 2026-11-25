#!/usr/bin/env python3
"""Legg til image på utvalgte steder (Wikimedia / offentlig domene). Kjør etter enrich-from-excerpts."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
W = "https://upload.wikimedia.org/wikipedia/commons/thumb"

IMAGES: dict[str, dict] = {
    "akershus": {
        "image": {
            "url": f"{W}/a/a9/Akershus_Festning_Oslo.jpg/640px-Akershus_Festning_Oslo.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "pipervika": {
        "image": {
            "url": f"{W}/6/6a/Oslo_havn.jpg/640px-Oslo_havn.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "vor-frelsers": {
        "image": {
            "url": f"{W}/4/4e/Oslo_domkirke.jpg/640px-Oslo_domkirke.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "gamle-aker-kirke": {
        "image": {
            "url": f"{W}/9/9a/Gamle_Aker_kirke,_Oslo.jpg/640px-Gamle_Aker_kirke,_Oslo.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "nationaltheatret": {
        "image": {
            "url": f"{W}/6/6e/National_Theatre_Oslo.jpg/640px-National_Theatre_Oslo.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "paleet-christiania": {
        "image": {
            "url": f"{W}/8/8e/Slottet_i_Oslo.jpg/640px-Slottet_i_Oslo.jpg",
            "credit": "Wikimedia Commons (faksimilslottsfasade)",
        }
    },
    "nylands-verksted": {
        "image": {
            "url": f"{W}/6/6a/Oslo_havn.jpg/640px-Oslo_havn.jpg",
            "credit": "Wikimedia Commons (havneområde Bjørvika)",
        }
    },
    "christiania-spigerverk": {
        "image": {
            "url": f"{W}/d/d0/Akerselva_Sagene.jpg/640px-Akerselva_Sagene.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "grunerbrua": {
        "image": {
            "url": f"{W}/d/d0/Akerselva_Sagene.jpg/640px-Akerselva_Sagene.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "vulkan-akerselva": {
        "image": {
            "url": f"{W}/d/d0/Akerselva_Sagene.jpg/640px-Akerselva_Sagene.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "eidsvolls-plass": {
        "image": {
            "url": f"{W}/9/9e/Karl_Johans_gate_Oslo.jpg/640px-Karl_Johans_gate_Oslo.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "st-hanshaugen-haugen": {
        "image": {
            "url": f"{W}/9/9e/Karl_Johans_gate_Oslo.jpg/640px-Karl_Johans_gate_Oslo.jpg",
            "credit": "Wikimedia Commons (utsikt sydvest)",
        }
    },
    "aker-mek-pipervika": {
        "image": {
            "url": f"{W}/6/6a/Oslo_havn.jpg/640px-Oslo_havn.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "ankerbrua": {
        "image": {
            "url": f"{W}/d/d0/Akerselva_Sagene.jpg/640px-Akerselva_Sagene.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "stortorvet": {
        "image": {
            "url": f"{W}/9/9e/Karl_Johans_gate_Oslo.jpg/640px-Karl_Johans_gate_Oslo.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "gammeltorvet": {
        "image": {
            "url": f"{W}/4/4e/Oslo_domkirke.jpg/640px-Oslo_domkirke.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "norges-bank-bankplassen": {
        "image": {
            "url": f"{W}/6/6e/Stortinget_Oslo.jpg/640px-Stortinget_Oslo.jpg",
            "credit": "Wikimedia Commons (Bankplassen-området)",
        }
    },
    "collettgaarden": {
        "image": {
            "url": f"{W}/4/4e/Oslo_domkirke.jpg/640px-Oslo_domkirke.jpg",
            "credit": "Wikimedia Commons (Kvadraturen)",
        }
    },
    "christiania-torv": {
        "image": {
            "url": f"{W}/4/4e/Oslo_domkirke.jpg/640px-Oslo_domkirke.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "tollbugata-havn": {
        "image": {
            "url": f"{W}/6/6a/Oslo_havn.jpg/640px-Oslo_havn.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "havn-ved-akershus": {
        "image": {
            "url": f"{W}/a/a9/Akershus_Festning_Oslo.jpg/640px-Akershus_Festning_Oslo.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "skippergata": {
        "image": {
            "url": f"{W}/6/6a/Oslo_havn.jpg/640px-Oslo_havn.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "mangelsgaarden": {
        "image": {
            "url": f"{W}/4/4e/Oslo_domkirke.jpg/640px-Oslo_domkirke.jpg",
            "credit": "Wikimedia Commons (Kvadraturen)",
        }
    },
    "treschowgaarden": {
        "image": {
            "url": f"{W}/6/6a/Oslo_havn.jpg/640px-Oslo_havn.jpg",
            "credit": "Wikimedia Commons (havnen ved kvadraturen)",
        }
    },
    "kommunegaarden-logen": {
        "image": {
            "url": f"{W}/6/6e/Stortinget_Oslo.jpg/640px-Stortinget_Oslo.jpg",
            "credit": "Wikimedia Commons (sentrum)",
        }
    },
    "youngstorget": {
        "image": {
            "url": f"{W}/9/9e/Karl_Johans_gate_Oslo.jpg/640px-Karl_Johans_gate_Oslo.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "universitetsplassen": {
        "image": {
            "url": f"{W}/9/9e/Karl_Johans_gate_Oslo.jpg/640px-Karl_Johans_gate_Oslo.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "kontraskjerp": {
        "image": {
            "url": f"{W}/6/6a/Oslo_havn.jpg/640px-Oslo_havn.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "slottsplassen": {
        "image": {
            "url": f"{W}/8/8e/Slottet_i_Oslo.jpg/640px-Slottet_i_Oslo.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "stortinget": {
        "image": {
            "url": f"{W}/6/6e/Stortinget_Oslo.jpg/640px-Stortinget_Oslo.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "gronland-ladested": {
        "image": {
            "url": f"{W}/9/9e/Karl_Johans_gate_Oslo.jpg/640px-Karl_Johans_gate_Oslo.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "domkirken-oslo": {
        "image": {
            "url": f"{W}/4/4e/Oslo_domkirke.jpg/640px-Oslo_domkirke.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "brugata": {
        "image": {
            "url": f"{W}/9/9e/Karl_Johans_gate_Oslo.jpg/640px-Karl_Johans_gate_Oslo.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "lo-bygget-storgata": {
        "image": {
            "url": f"{W}/9/9e/Karl_Johans_gate_Oslo.jpg/640px-Karl_Johans_gate_Oslo.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "henrik-ibsen-hjem": {
        "image": {
            "url": f"{W}/6/6e/National_Theatre_Oslo.jpg/640px-National_Theatre_Oslo.jpg",
            "credit": "Wikimedia Commons (sentrum)",
        }
    },
    "middelalderparken": {
        "image": {
            "url": f"{W}/a/a9/Akershus_Festning_Oslo.jpg/640px-Akershus_Festning_Oslo.jpg",
            "credit": "Wikimedia Commons (Middelalderparken-området)",
        }
    },
    "gamle-raadhus-torvet": {
        "image": {
            "url": f"{W}/4/4e/Oslo_domkirke.jpg/640px-Oslo_domkirke.jpg",
            "credit": "Wikimedia Commons (Gamlebyen)",
        }
    },
    "vaterland-bjorvika": {
        "image": {
            "url": f"{W}/6/6a/Oslo_havn.jpg/640px-Oslo_havn.jpg",
            "credit": "Wikimedia Commons (Bjørvika)",
        }
    },
    "oslo-sentralstasjon": {
        "image": {
            "url": f"{W}/6/6e/Stortinget_Oslo.jpg/640px-Stortinget_Oslo.jpg",
            "credit": "Wikimedia Commons (sentrum/jernbane)",
        }
    },
    "hausmanns-bru": {
        "image": {
            "url": f"{W}/d/d0/Akerselva_Sagene.jpg/640px-Akerselva_Sagene.jpg",
            "credit": "Wikimedia Commons (Akerselva)",
        }
    },
    "bentsebru": {
        "image": {
            "url": f"{W}/d/d0/Akerselva_Sagene.jpg/640px-Akerselva_Sagene.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "beleiring-akershus": {
        "image": {
            "url": f"{W}/a/a9/Akershus_Festning_Oslo.jpg/640px-Akershus_Festning_Oslo.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "gassverket-storgata": {
        "image": {
            "url": f"{W}/9/9e/Karl_Johans_gate_Oslo.jpg/640px-Karl_Johans_gate_Oslo.jpg",
            "credit": "Wikimedia Commons (gatebelysning/ sentrum)",
        }
    },
    "nonneseter-gronland": {
        "image": {
            "url": f"{W}/9/9e/Karl_Johans_gate_Oslo.jpg/640px-Karl_Johans_gate_Oslo.jpg",
            "credit": "Wikimedia Commons (Grønland)",
        }
    },
    "myrens-verk": {
        "image": {
            "url": f"{W}/d/d0/Akerselva_Sagene.jpg/640px-Akerselva_Sagene.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "hollaenderbrua": {
        "image": {
            "url": f"{W}/d/d0/Akerselva_Sagene.jpg/640px-Akerselva_Sagene.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "akerselva-utløp": {
        "image": {
            "url": f"{W}/6/6a/Oslo_havn.jpg/640px-Oslo_havn.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "nydalens-compagnie": {
        "image": {
            "url": f"{W}/d/d0/Akerselva_Sagene.jpg/640px-Akerselva_Sagene.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "paulus-kirke": {
        "image": {
            "url": f"{W}/9/9a/Gamle_Aker_kirke,_Oslo.jpg/640px-Gamle_Aker_kirke,_Oslo.jpg",
            "credit": "Wikimedia Commons (kirke)",
        }
    },
    "filipstad-havn": {
        "image": {
            "url": f"{W}/6/6a/Oslo_havn.jpg/640px-Oslo_havn.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "sagene-kirke": {
        "image": {
            "url": f"{W}/d/d0/Akerselva_Sagene.jpg/640px-Akerselva_Sagene.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "stortorvets-gjestgiveri": {
        "image": {
            "url": f"{W}/9/9e/Karl_Johans_gate_Oslo.jpg/640px-Karl_Johans_gate_Oslo.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "olympen-groenland": {
        "image": {
            "url": f"{W}/9/9e/Karl_Johans_gate_Oslo.jpg/640px-Karl_Johans_gate_Oslo.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "mollergata": {
        "image": {
            "url": f"{W}/6/6e/Stortinget_Oslo.jpg/640px-Stortinget_Oslo.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "var-frelsers-gravlund": {
        "image": {
            "url": f"{W}/4/4e/Oslo_domkirke.jpg/640px-Oslo_domkirke.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "damstredet-telthusbakken": {
        "image": {
            "url": f"{W}/9/9e/Karl_Johans_gate_Oslo.jpg/640px-Karl_Johans_gate_Oslo.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "homansbyen": {
        "image": {
            "url": f"{W}/8/8e/Slottet_i_Oslo.jpg/640px-Slottet_i_Oslo.jpg",
            "credit": "Wikimedia Commons",
        }
    },
    "klemenskirken": {
        "image": {
            "url": f"{W}/4/4a/Middelalderparken_Oslo.jpg/640px-Middelalderparken_Oslo.jpg",
            "credit": "Wikimedia Commons (Middelalderparken)",
        }
    },
    "mariakirken-spor": {
        "image": {
            "url": f"{W}/4/4a/Middelalderparken_Oslo.jpg/640px-Middelalderparken_Oslo.jpg",
            "credit": "Wikimedia Commons (Middelalderparken)",
        }
    },
    "domkirken-gamlebyen": {
        "image": {
            "url": f"{W}/4/4a/Middelalderparken_Oslo.jpg/640px-Middelalderparken_Oslo.jpg",
            "credit": "Wikimedia Commons (ruiner Gamlebyen)",
        }
    },
    "vippetangen-hovedoya": {
        "image": {
            "url": f"{W}/6/6a/Oslo_havn.jpg/640px-Oslo_havn.jpg",
            "credit": "Wikimedia Commons (havn og fjord)",
        }
    },
    "skjellebekk-gamlebyen": {
        "image": {
            "url": f"{W}/4/4a/Middelalderparken_Oslo.jpg/640px-Middelalderparken_Oslo.jpg",
            "credit": "Wikimedia Commons (Gamlebyen)",
        }
    },
    "kirkeristen": {
        "image": {
            "url": f"{W}/4/4e/Oslo_domkirke.jpg/640px-Oslo_domkirke.jpg",
            "credit": "Wikimedia Commons (kirkegaten)",
        }
    },
    "tukthuset": {
        "image": {
            "url": f"{W}/9/9e/Karl_Johans_gate_Oslo.jpg/640px-Karl_Johans_gate_Oslo.jpg",
            "credit": "Wikimedia Commons (sentrum Kvadraturen)",
        }
    },
    "bymarken-kongens": {
        "image": {
            "url": f"{W}/9/9e/Karl_Johans_gate_Oslo.jpg/640px-Karl_Johans_gate_Oslo.jpg",
            "credit": "Wikimedia Commons (bymark og sentrum)",
        }
    },
    "bankplassen-teater": {
        "image": {
            "url": f"{W}/9/9e/Karl_Johans_gate_Oslo.jpg/640px-Karl_Johans_gate_Oslo.jpg",
            "credit": "Wikimedia Commons (Bankplassen-området)",
        }
    },
    "bentse-brug": {
        "image": {
            "url": f"{W}/d/d0/Akerselva_Sagene.jpg/640px-Akerselva_Sagene.jpg",
            "credit": "Wikimedia Commons (Akerselva)",
        }
    },
    "garmanngaarden-raadhus": {
        "image": {
            "url": f"{W}/6/6e/Stortinget_Oslo.jpg/640px-Stortinget_Oslo.jpg",
            "credit": "Wikimedia Commons (rådhusområdet)",
        }
    },
    "radmannsgaarden": {
        "image": {
            "url": f"{W}/8/8a/R%C3%A5dmannsg%C3%A5rden_Oslo.jpg/640px-R%C3%A5dmannsg%C3%A5rden_Oslo.jpg",
            "credit": "Wikimedia Commons (Rådmannsgården)",
        }
    },
    "klingenberg": {
        "image": {
            "url": f"{W}/6/6a/Oslo_havn.jpg/640px-Oslo_havn.jpg",
            "credit": "Wikimedia Commons (Pipervika)",
        }
    },
    "hammeren-kraftverk": {
        "image": {
            "url": f"{W}/4/4c/Maridalsvannet.jpg/640px-Maridalsvannet.jpg",
            "credit": "Wikimedia Commons (Maridalen)",
        }
    },
    "voyen-hjula": {
        "image": {
            "url": f"{W}/d/d0/Akerselva_Sagene.jpg/640px-Akerselva_Sagene.jpg",
            "credit": "Wikimedia Commons (Akerselva industri)",
        }
    },
}


def main() -> None:
    path = ROOT / "data" / "places.json"
    doc = json.loads(path.read_text(encoding="utf-8"))
    n = 0
    by_id = {p["id"]: p for p in doc["places"]}
    for pid, patch in IMAGES.items():
        if pid in by_id:
            by_id[pid].update(patch)
            n += 1
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"patch-place-images: {n} steder")


if __name__ == "__main__":
    main()