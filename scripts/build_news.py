#!/usr/bin/env python3
"""Genera y valida news.json para Portada 7AM.

Uso:
  python3 scripts/build_news.py draft.json            # escribe news.json (+ valida)
  python3 scripts/build_news.py draft.json --log      # además añade la portada a Briefing/log.md
  python3 scripts/build_news.py --check [fichero]     # solo valida (por defecto news.json)

draft.json:
{
  "updatedAt": "2026-09-29T07:00:00+02:00",
  "sections": {
    "politica": [   # exactamente 10 items, en orden; los 5 con "published": true van a portada
      {"title": "...", "summary": "...", "longSummary": "...", "bullets": ["..","..","..",".."],
       "source": "...", "url": "https://...", "publishedAt": "2026-09-28T14:42:27+02:00",
       "lang": "es", "region": "es", "partial": false, "published": true},
      ...
    ],
    "exterior": [...], "tecnologia": [...], "economia": [...], "cultura": [...]
  }
}
Los ids se asignan solos: <seccion>-01 ... <seccion>-10 (orden del pool).
lang   = idioma de la fuente ORIGINAL ("es" | "en"); si falta se deduce de LANG_BY_SOURCE.
region = ámbito de la noticia ("es" = España | "int" = internacional).
Todo el texto (title, summary, longSummary, bullets) va SIEMPRE en castellano, con palabras propias.
"""
import json, re, sys
from datetime import datetime

SECTIONS = ["politica", "exterior", "tecnologia", "economia", "cultura"]   # orden del menú y de la portada
NAMES = {"politica": "Política", "exterior": "Exterior", "tecnologia": "Tecnología", "economia": "Economía", "cultura": "Cultura"}
FIELDS = ["id", "title", "summary", "longSummary", "bullets", "source", "url", "section", "publishedAt",
          "lang", "region", "partial"]
LANG_BY_SOURCE = {
    "El País": "es", "Cinco Días": "es", "elDiario.es": "es", "Europa Press": "es", "Expansión": "es", "Xataka": "es",
    "BBC Mundo": "es", "El Confidencial": "es",
    "BBC": "en", "BBC News": "en", "The Guardian": "en", "Reuters": "en", "AP": "en", "Financial Times": "en",
    "Politico Europe": "en", "TechCrunch": "en", "The Verge": "en", "Ars Technica": "en",
}
MIN_W, MAX_W = 180, 280          # longSummary normal
PARTIAL_MAX_W = 180              # longSummary parcial (de pago / poco contexto): más corto


def words(s):
    return len(s.split())


def validate(data):
    errs = []
    if set(data.get("sections", {})) != set(SECTIONS):
        errs.append("secciones incorrectas")
    seen = set()
    for sec in SECTIONS:
        block = data["sections"].get(sec, {})
        pool, pub = block.get("pool", []), block.get("published", [])
        if len(pool) != 10: errs.append(f"{sec}: pool tiene {len(pool)} (deben ser 10)")
        if len(pub) != 5: errs.append(f"{sec}: published tiene {len(pub)} (deben ser 5)")
        by_id = {x.get("id"): x for x in pool}
        for it in pub:
            if by_id.get(it.get("id")) != it: errs.append(f"{sec}: {it.get('id')} publicado no es copia exacta de un item del pool")
        for it in pool:
            iid = it.get("id", "?")
            if iid in seen: errs.append(f"id duplicado {iid}")
            seen.add(iid)
            for f in FIELDS:
                if f not in it: errs.append(f"{iid}: falta {f}")
            if not re.fullmatch(r"[a-z]+-\d{2}", str(iid)): errs.append(f"{iid}: id no válido")
            if it.get("section") != sec: errs.append(f"{iid}: section != {sec}")
            b = it.get("bullets", [])
            if not (isinstance(b, list) and len(b) == 4 and all(isinstance(x, str) and x.strip() for x in b)):
                errs.append(f"{iid}: bullets debe tener exactamente 4 textos")
            if not isinstance(it.get("partial"), bool): errs.append(f"{iid}: partial debe ser booleano")
            if it.get("lang") not in ("es", "en"): errs.append(f"{iid}: lang debe ser 'es' o 'en'")
            if it.get("region") not in ("es", "int"): errs.append(f"{iid}: region debe ser 'es' o 'int'")
            for f in ("title", "summary", "source"):
                if not str(it.get(f, "")).strip(): errs.append(f"{iid}: {f} vacío")
            w = words(it.get("longSummary", ""))
            if it.get("partial"):
                if not (20 <= w < PARTIAL_MAX_W): errs.append(f"{iid}: longSummary parcial con {w} palabras")
            elif not (MIN_W <= w <= MAX_W):
                errs.append(f"{iid}: longSummary con {w} palabras (debe estar entre {MIN_W} y {MAX_W})")
            try:
                datetime.fromisoformat(it.get("publishedAt", ""))
            except Exception:
                errs.append(f"{iid}: publishedAt no es ISO 8601")
            if not str(it.get("url", "")).startswith("http"): errs.append(f"{iid}: url no válida")
    return errs


def report(data):
    ws, part = [], 0
    for sec in SECTIONS:
        for it in data["sections"][sec]["pool"]:
            if it["partial"]: part += 1
            else: ws.append(words(it["longSummary"]))
    n = sum(len(data["sections"][s]["pool"]) for s in SECTIONS)
    en = sum(it["lang"] == "en" for s in SECTIONS for it in data["sections"][s]["pool"])
    print(f"items: {n} · fuente en inglés: {en} · parciales: {part} · palabras (no parciales): {min(ws)}–{max(ws)}")


def build(draft):
    out = {"updatedAt": draft["updatedAt"], "timezone": "Europe/Madrid", "sections": {}}
    for sec in SECTIONS:
        pool, pub = [], []
        for n, src in enumerate(draft["sections"][sec], 1):
            it = {"id": f"{sec}-{n:02d}", "title": src["title"], "summary": src["summary"],
                  "longSummary": src["longSummary"], "bullets": src["bullets"], "source": src["source"],
                  "url": src["url"], "section": sec, "publishedAt": src["publishedAt"],
                  "lang": src.get("lang") or LANG_BY_SOURCE.get(src["source"], ""),
                  "region": src.get("region", ""), "partial": bool(src.get("partial", False))}
            pool.append(it)
            if src.get("published"): pub.append(dict(it))
        out["sections"][sec] = {"published": pub, "pool": pool}
    return out


def write(out, path="news.json"):
    # Un item por línea: diffs legibles en git.
    lines = ['{', f'"updatedAt":{json.dumps(out["updatedAt"])},', '"timezone":"Europe/Madrid",', '"sections":{']
    for si, sec in enumerate(SECTIONS):
        lines.append(f'"{sec}":{{')
        for ki, key in enumerate(["published", "pool"]):
            items = out["sections"][sec][key]
            lines.append(f'"{key}":[')
            lines += [json.dumps(x, ensure_ascii=False) + ("," if i < len(items) - 1 else "") for i, x in enumerate(items)]
            lines.append("]" + ("," if ki == 0 else ""))
        lines.append("}" + ("," if si < len(SECTIONS) - 1 else ""))
    lines += ["}", "}"]
    open(path, "w").write("\n".join(lines) + "\n")


def append_log(out):
    with open("Briefing/log.md", "a") as f:
        f.write(f"\n## {out['updatedAt']}\n")
        for sec in SECTIONS:
            f.write(f"\n**{NAMES[sec]}**\n" + "".join(
                f"{n}. {x['title']} — {x['source']}{' (fuente en inglés)' if x['lang'] == 'en' else ''}{' (parcial)' if x['partial'] else ''}\n"
                for n, x in enumerate(out["sections"][sec]["published"], 1)))


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["--check"]:
        data = json.load(open(args[1] if len(args) > 1 else "news.json"))
    else:
        data = build(json.load(open(args[0])))
    errs = validate(data)
    if errs:
        print("ERRORES:\n- " + "\n- ".join(errs)); sys.exit(1)
    if args[:1] != ["--check"]:
        write(data)
        json.load(open("news.json"))
        if "--log" in args: append_log(data)
    report(data)
