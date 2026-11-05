import json, sys, html, pathlib

TPL = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{title}</title>
<meta name="description" content="{desc}">
<script type="application/ld+json">{ld}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;800&display=swap" rel="stylesheet">
<style>
:root{{--bg:{bg};--ink:#1d1f22;--muted:#5f6670;--accent:{accent};--card:#fff;--line:#e5e2dc}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 Manrope,system-ui,sans-serif}}
.wrap{{max-width:1080px;margin:0 auto;padding:0 20px}}
.demo{{background:#1d1f22;color:#fff;text-align:center;font-size:13px;padding:6px 12px}}
header{{border-bottom:1px solid var(--line);background:var(--bg);position:sticky;top:0;z-index:5}}
header .wrap{{display:flex;justify-content:space-between;align-items:center;height:64px}}
.logo{{font-weight:800;font-size:20px;text-decoration:none;color:inherit}}
nav a{{margin-left:20px;color:var(--muted);text-decoration:none;font-size:15px}}
.btn{{display:inline-block;background:var(--accent);color:#fff;padding:13px 24px;border-radius:12px;text-decoration:none;font-weight:600}}
.hero{{display:grid;grid-template-columns:1.2fr .8fr;gap:40px;align-items:center;padding:64px 0}}
h1{{font-size:44px;line-height:1.15;margin:0 0 16px}}
h2{{font-size:30px;margin:0 0 20px}}
.lead{{color:var(--muted);font-size:19px}}
.pic{{aspect-ratio:4/3;border-radius:24px;background:{pic};display:grid;place-items:end start;padding:16px;color:#ffffffcc;font-size:14px}}
section{{padding:56px 0;border-top:1px solid var(--line)}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:22px}}
.card h3{{margin:0 0 6px;font-size:19px}}
.card p{{margin:0;color:var(--muted)}}
.info{{display:grid;grid-template-columns:1fr 1fr;gap:28px}}
.map{{border-radius:18px;min-height:220px;background:repeating-linear-gradient(45deg,#e8e4dd,#e8e4dd 12px,#efebe5 12px,#efebe5 24px);display:grid;place-items:center;color:var(--muted)}}
footer{{padding:30px 0;color:var(--muted);font-size:14px;border-top:1px solid var(--line)}}
@media(max-width:800px){{nav{{display:none}}.hero,.info{{grid-template-columns:1fr}}.grid{{grid-template-columns:1fr}}h1{{font-size:32px}}}}
</style>
</head>
<body>
<div class="demo">{t_demo}</div>
<header><div class="wrap"><a class="logo" href="#">{name}</a>
<nav><a href="#paslaugos">{svc_title}</a><a href="#kontaktai">{t_contacts}</a></nav></div></header>
<main class="wrap">
<div class="hero"><div><h1>{h1}</h1><p class="lead">{lead}</p><a class="btn" href="#kontaktai">{cta}</a></div>
<div class="pic">{t_photo}</div></div>
<section id="paslaugos"><h2>{svc_title}</h2><div class="grid">{cards}</div></section>
<section><h2>{t_why}</h2><div class="grid">{why}</div></section>
<section id="kontaktai"><h2>{t_contacts}</h2><div class="info"><div><p>{contacts}</p></div><div class="map">{t_map}</div></div></section>
</main>
<footer><div class="wrap">© 2026 {name} · {city}</div></footer>
</body></html>
"""

UI = {
    "lt": {"country": "LT", "demo": "Juodraštis „{name}“ — tekstai ir nuotraukos bus pakeisti jūsų", "contacts": "Kontaktai",
           "photo": "Čia bus jūsų nuotrauka", "why": "Kodėl mes", "map": "Čia bus Google žemėlapis"},
    "lv": {"country": "LV", "demo": "Melnraksts „{name}“ — teksti un foto tiks aizstāti ar jūsu", "contacts": "Kontakti",
           "photo": "Šeit būs jūsu foto", "why": "Kāpēc mēs", "map": "Šeit būs Google karte"},
    "et": {"country": "EE", "demo": "Mustand „{name}“ — tekstid ja fotod asendatakse teie omadega", "contacts": "Kontakt",
           "photo": "Siia tuleb teie foto", "why": "Miks meie", "map": "Siia tuleb Google'i kaart"},
}

def card(t, p):
    return f'<div class="card"><h3>{html.escape(t)}</h3><p>{html.escape(p)}</p></div>'

def build(c, out):
    ui = UI[c.get("lang", "lt")]
    ld = {"@context": "https://schema.org", "@type": c["schema"], "name": c["name"],
          "address": {"@type": "PostalAddress", "streetAddress": c["street"], "addressLocality": c["city"], "addressCountry": ui["country"]}}
    page = TPL.format(
        title=html.escape(c["title"]), desc=html.escape(c["desc"]), ld=json.dumps(ld, ensure_ascii=False),
        bg=c["bg"], accent=c["accent"], pic=c["pic"], name=html.escape(c["name"]), city=html.escape(c["city"]),
        h1=html.escape(c["h1"]), lead=html.escape(c["lead"]), cta=html.escape(c["cta"]), svc_title=html.escape(c["svc_title"]),
        cards="".join(card(*x) for x in c["services"]), why="".join(card(*x) for x in c["why"]),
        contacts="<br>".join(html.escape(x) for x in c["contacts"]),
        lang=c.get("lang", "lt"), t_demo=html.escape(ui["demo"].format(name=c["name"])), t_contacts=ui["contacts"],
        t_photo=ui["photo"], t_why=ui["why"], t_map=ui["map"])
    p = pathlib.Path(out); p.mkdir(parents=True, exist_ok=True)
    (p / "index.html").write_text(page, encoding="utf-8")

if __name__ == "__main__":
    for c in json.load(open(sys.argv[1], encoding="utf-8")):
        build(c, c["slug"])
        print(c["slug"])
