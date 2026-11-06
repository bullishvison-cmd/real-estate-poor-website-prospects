#!/usr/bin/env python3
"""Build White Farmhouse Realty REAL 3D demo (business_022-3d).
Single self-contained index.html: Three.js r149 + GSAP inlined, images as WebP data URIs.
Method follows the reels Gautam sent (2026-11-06):
- Reel 3 (textura.us / GetLayers): single self-contained HTML, Three.js, dark cinematic,
  grab-and-spin 3D object, scroll-driven motion, sections arriving out of focus and settling.
- Reel 2 (harshpanwar.ai): dark/black luxury palette, one big floating/rotating 3D hero,
  minimal type, generous black space. Framer Motion = Motion (already saved locally).
- Reel 4 (10xoperator): UI UX Pro Max design system + 21st.dev components (knowledge, not a prompt).
Palette stays §15 #4 Premium Cafe (#38271F / #F3E8D5 / #B77B48) — its dark brown IS the
Brewns-style black-and-brown dark theme. All 12 listings verified 2026-11-05.
WebGL fallback: embedded hero photo shows if WebGL is unavailable.
"""
import json, html

IMG = json.load(open('images.json'))
GSAP = open('/home/hatch/workspace/animation-code/gsap-dist/gsap.min.js').read()
AURORA = open('aurora.js').read()

LISTINGS = [
 ("1307 Meadow Ln, Wayne, NE", 230000, 5, 2, 2200, "House", "New Listing", "l01"),
 ("212 Lincoln St, Wayne, NE", 10000, None, None, None, "Land / Lot", "New Listing", "l02"),
 ("1410 N Main St, Emerson, NE", 170000, 4, 1.5, 3600, "House", "New Listing", "l03"),
 ("Ponca, NE", 247000, 3, 2.5, 3036, "House", "New Listing", "l04"),
 ("608 Logan St, Wayne, NE", 235000, 3, 2, 2475, "House", "For Sale", "l05"),
 ("805 Lincoln St, Wayne, NE", 275000, 3, 2.5, 3040, "House", "For Sale", "l06"),
 ("1116 Crescent Dr, Wayne, NE", 395000, 4, 3, 3151, "House", "For Sale", "l07"),
 ("120 W 10th St, Wayne, NE", 120000, 2, 1, 1248, "House", "Reduced Price", "l08"),
 ("503 Nebraska St, Wayne, NE", 200000, 3, 2, 1784, "House", "Reduced Price", "l09"),
 ("505 E 10th St, Wayne, NE", 290000, 4, 2, 2050, "House", "Reduced Price", "l10"),
 ("57480 850th Rd, Wayne, NE", 360000, 3, 2, 2496, "House", "Sold", "l11"),
 ("1015 Sycamore St, Wayne, NE", 335000, 4, 3, 2374, "House", "Sale Pending", "l12"),
]

def money(n): return "$" + f"{n:,}"

def card(l):
    addr, price, beds, baths, sqft, typ, status, key = l
    bd = "—" if beds is None else str(beds)
    ba = "—" if baths is None else str(baths)
    sf = "—" if sqft is None else f"{sqft:,} sq ft"
    badge_cls = "badge sold" if status == "Sold" else "badge"
    incomplete = beds is None
    tag = ("Details to confirm with the brokerage — listed with no type, beds, baths or size"
           if incomplete else "Listed by White Farmhouse Realty")
    flag = ('<span class="flag">Details to confirm</span>' if incomplete else '')
    return f'''<article class="card" data-price="{price}" data-beds="{beds if beds is not None else 0}" data-baths="{baths if baths is not None else 0}" data-type="{typ}" data-addr="{html.escape(addr.lower())}">
<div class="card-media"><img loading="lazy" src="{IMG[key]}" alt="Concept photo of a home like {html.escape(addr)}"><span class="glare"></span></div>
<div class="card-body"><span class="{badge_cls}">{status}</span>{flag}
<div class="price">{money(price)}</div><div class="addr">{html.escape(addr)}</div>
<div class="meta">{bd} bd · {ba} ba · {sf} · {typ}</div><div class="meta tag">{tag}</div>
<a class="btn" href="#contact">Ask about this home</a></div></article>'''

CARDS = "\n".join(card(l) for l in LISTINGS)

CSS = """
:root{--primary:#38271F;--light:#F3E8D5;--accent:#B77B48;--gold:#E8B84B;--bg:#171009;--bg2:#1E150E;--panel:#241A14;--ink:#F3E8D5;--muted:#C9BBA6;--line:rgba(243,232,213,.14);--disc-h:37px}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:Inter,system-ui,-apple-system,sans-serif;color:var(--ink);background:var(--bg);line-height:1.6;overflow-x:hidden}
h1,h2,h3{font-family:'Cormorant Garamond',Georgia,serif;line-height:1.12;color:var(--ink)}
.container{max-width:1200px;margin-inline:auto;padding-inline:40px}
.disclaimer{position:fixed;top:0;left:0;right:0;z-index:55;background:#0E0805;color:var(--muted);text-align:center;font-size:13px;padding:10px 16px;letter-spacing:.02em;border-bottom:1px solid var(--line)}
#progress{position:fixed;top:0;left:0;height:3px;width:100%;background:linear-gradient(90deg,var(--accent),var(--gold));transform-origin:0 50%;transform:scaleX(0);z-index:70;box-shadow:0 0 12px rgba(232,184,75,.7)}
#loader{position:fixed;inset:0;background:#0E0805;z-index:100;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:14px;animation:loaderOut .45s ease 1.6s forwards;pointer-events:none}
#loader .circ{width:230px;height:230px;position:relative}
#loader .circ svg.ring{width:100%;height:100%;animation:spin 8s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
#loader .circ text{fill:var(--ink);font-family:Inter,system-ui,sans-serif;font-size:16px;font-weight:600;letter-spacing:4px}
#loader .circ .mark{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
#loader .circ .mark svg{width:64px;height:64px}
#loader .bar{width:120px;height:2px;background:rgba(243,232,213,.25);overflow:hidden;border-radius:2px}
#loader .bar i{display:block;height:100%;width:40%;background:var(--gold);animation:loadslide 1s ease-in-out infinite}
@keyframes loadslide{0%{transform:translateX(-100%)}100%{transform:translateX(300%)}}
@keyframes loaderOut{to{opacity:0;visibility:hidden}}
header{position:fixed;top:var(--disc-h);left:0;right:0;background:rgba(23,16,9,.82);backdrop-filter:blur(10px);border-bottom:1px solid var(--line);z-index:50}
.nav{display:flex;align-items:center;justify-content:space-between;gap:24px;padding:14px 0}
.brand{font-family:Fraunces,serif;font-weight:700;font-size:22px;color:var(--ink);text-decoration:none}
.brand span{color:var(--accent)}
.nav nav{display:flex;gap:32px;flex-wrap:wrap}
.nav nav a{color:var(--ink);text-decoration:none;font-weight:500;font-size:15px;position:relative;padding-bottom:2px}
.nav nav a::after{content:"";position:absolute;left:0;bottom:0;height:2px;width:100%;background:var(--accent);transform:scaleX(0);transform-origin:0 50%;transition:transform .25s ease}
.nav nav a:hover::after{transform:scaleX(1)}
.btn{display:inline-block;background:var(--accent);color:#fff;text-decoration:none;font-weight:600;padding:12px 22px;border-radius:999px;border:0;cursor:pointer;font-size:15px;position:relative;overflow:hidden;transition:transform .2s ease,box-shadow .2s ease;will-change:transform}
.btn::after{content:"";position:absolute;top:0;left:-80%;width:50%;height:100%;background:linear-gradient(100deg,transparent,rgba(255,255,255,.35),transparent);transform:skewX(-20deg);transition:left .5s ease}
.btn:hover::after{left:130%}
.btn:hover{transform:translateY(-1px);box-shadow:0 8px 24px rgba(183,123,72,.45)}
.btn.ghost{background:transparent;color:var(--ink);border:2px solid var(--ink)}
.btn.ghost::after{background:linear-gradient(100deg,transparent,rgba(243,232,213,.12),transparent)}
.hero{background:radial-gradient(900px 520px at 78% 30%,rgba(183,123,72,.22),transparent 60%),radial-gradient(700px 500px at 10% 90%,rgba(232,184,75,.08),transparent 60%),var(--bg);padding:calc(148px + var(--disc-h)) 0 72px;overflow:hidden;position:relative}
.hero-grid{display:grid;grid-template-columns:1.05fr .95fr;gap:48px;align-items:center}
.hero h1{font-size:clamp(46px,5.8vw,72px);line-height:1.04;margin:16px 0 20px}
.hero h1 em{font-style:italic;color:var(--gold)}
.hero h1 .w{display:inline-block;will-change:transform,opacity}
.eyebrow{font-size:12px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--gold)}
.hero p.lede{font-size:18px;color:var(--muted);max-width:560px}
.pills{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px}
.cap{font-size:12px;color:var(--muted);margin-top:8px}
/* 3D stage */
.stage{position:relative}
#hero-3d{position:relative;height:480px;border-radius:20px;overflow:hidden;background:radial-gradient(420px 300px at 50% 62%,rgba(183,123,72,.28),rgba(23,16,9,0) 70%);cursor:grab;touch-action:none;border:1px solid var(--line);box-shadow:0 30px 80px rgba(0,0,0,.55),inset 0 0 0 1px rgba(232,184,75,.06)}
#hero-3d:active{cursor:grabbing}
#hero-3d canvas{display:block;width:100%;height:100%}
#hero-3d .fallback{position:absolute;inset:0;display:none}
#hero-3d .fallback img{width:100%;height:100%;object-fit:cover;display:block}
#hero-3d.no-webgl .fallback{display:block}
#hero-3d.no-webgl canvas{display:none}
#hero-3d.no-webgl .spin-hint{display:none}
.spin-hint{position:absolute;left:50%;bottom:14px;transform:translateX(-50%);background:rgba(14,8,5,.72);border:1px solid var(--line);color:var(--light);font-size:12px;font-weight:600;letter-spacing:.08em;padding:7px 14px;border-radius:999px;pointer-events:none;white-space:nowrap}
.stats{background:var(--bg2);border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:44px 0}
.stats-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;text-align:center}
.stats .num{font-family:Fraunces,serif;font-size:clamp(28px,3.4vw,40px);font-weight:700;color:var(--light)}
.stats .num em{font-style:normal;color:var(--gold)}
.stats .lbl{font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin-top:4px}
section{padding:96px 0}
section.alt{background:var(--bg2)}
.sec-head{max-width:720px;margin-bottom:40px}
.sec-head h2{font-size:clamp(32px,3.6vw,44px);line-height:1.1;margin:12px 0 14px}
.sec-head p{color:var(--muted);font-size:17px}
.filters{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:24px;display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:32px;box-shadow:0 6px 24px rgba(0,0,0,.35)}
.filters label{font-size:13px;font-weight:600;display:block;margin-bottom:6px;color:var(--light)}
.filters input,.filters select{width:100%;padding:11px 12px;border:1px solid var(--line);border-radius:10px;font:inherit;font-size:15px;background:#171009;color:var(--ink)}
.filters .full{grid-column:1/-1;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.count{font-weight:600;color:var(--light)}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.card{background:linear-gradient(160deg,rgba(243,232,213,.07),rgba(243,232,213,.02));border:1px solid var(--line);border-radius:16px;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 2px 16px rgba(0,0,0,.4);transition:box-shadow .25s ease,border-color .25s ease;transform-style:preserve-3d;will-change:transform;backdrop-filter:blur(6px)}
.card:hover{box-shadow:0 18px 40px rgba(0,0,0,.55),0 0 0 1px rgba(232,184,75,.25);border-color:rgba(232,184,75,.35)}
.card-media{position:relative;overflow:hidden}
.card-media img{width:100%;height:220px;object-fit:cover;display:block;transition:transform .4s ease}
.card:hover .card-media img{transform:scale(1.05)}
.card-media .glare{position:absolute;inset:0;background:radial-gradient(600px circle at var(--gx,50%) var(--gy,50%),rgba(255,255,255,.18),transparent 45%);opacity:0;transition:opacity .25s ease;pointer-events:none}
.card:hover .glare{opacity:1}
.card-body{padding:20px 20px 22px;display:flex;flex-direction:column;gap:8px;flex:1}
.price{font-family:Fraunces,serif;font-size:26px;font-weight:700;color:var(--light)}
.addr{font-weight:600;font-size:16px}
.meta{color:var(--muted);font-size:14px}
.meta.tag{font-size:13px}
.badge{align-self:flex-start;font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;padding:5px 10px;border-radius:999px;background:rgba(243,232,213,.1);color:var(--light);border:1px solid var(--line)}
.badge.sold{background:rgba(255,255,255,.06);color:#999}
.flag{align-self:flex-start;font-size:12px;font-weight:700;padding:5px 10px;border-radius:999px;background:rgba(232,184,75,.14);color:var(--gold);border:1px solid rgba(232,184,75,.4)}
.card .btn{margin-top:auto;text-align:center}
.empty{border:1px dashed var(--line);border-radius:16px;padding:48px;text-align:center;color:var(--muted);grid-column:1/-1}
.note{font-size:13px;color:var(--muted);margin-top:20px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center}
.two img{width:100%;height:380px;object-fit:cover;border-radius:16px;box-shadow:0 16px 40px rgba(0,0,0,.45)}
.why{display:grid;grid-template-columns:repeat(2,1fr);gap:24px}
.why div{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:28px;box-shadow:0 2px 10px rgba(0,0,0,.3);transition:transform .25s ease,box-shadow .25s ease}
.why div:hover{transform:translateY(-2px);box-shadow:0 8px 20px rgba(0,0,0,.4)}
.why h3{font-size:20px;margin-bottom:8px}
.why p{color:var(--muted);font-size:15px}
.chips{display:flex;gap:10px;flex-wrap:wrap}
.chip{background:var(--panel);border:1px solid var(--line);border-radius:999px;padding:9px 16px;font-weight:500;font-size:14px;transition:transform .2s ease,border-color .2s ease;color:var(--ink)}
.chip:hover{transform:translateY(-2px);border-color:var(--accent)}
.fix ol{list-style:none;counter-reset:f;display:grid;gap:24px}
.fix li{counter-increment:f;background:var(--panel);border:1px solid var(--line);border-left:6px solid var(--accent);border-radius:12px;padding:28px}
.fix li h3{font-size:20px;margin-bottom:8px}
.fix li h3::before{content:counter(f) ". ";color:var(--gold)}
.fix p{color:var(--muted)}
.fix p b{color:var(--ink)}
form.lead{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:32px;display:grid;grid-template-columns:1fr 1fr;gap:16px;max-width:820px}
form.lead label{font-size:13px;font-weight:600;display:block;margin-bottom:6px}
form.lead input,form.lead select,form.lead textarea{width:100%;padding:11px 12px;border:1px solid var(--line);border-radius:10px;font:inherit;font-size:15px;background:#171009;color:var(--ink)}
form.lead .full{grid-column:1/-1}
.form-ok{display:none;background:rgba(120,180,120,.12);border:1px solid rgba(140,200,140,.4);border-radius:12px;padding:16px;margin-top:16px;max-width:820px}
.contact-strip{background:var(--primary);color:var(--light);padding:56px 0}
.contact-strip h2{color:var(--light);font-size:32px;margin-bottom:12px}
.contact-strip a{color:var(--light);font-weight:600}
.contact-strip p{opacity:.92}
.cta-final{text-align:center}
.cta-final h2{font-size:clamp(30px,3.6vw,44px);line-height:1.1;margin-bottom:16px}
.cta-final h2 .ch{display:inline-block;will-change:transform,opacity}
.cta-final p{color:var(--muted);max-width:640px;margin:0 auto 28px}
footer{background:#0E0805;color:var(--muted);padding:40px 0 24px;font-size:14px;border-top:1px solid var(--line)}
footer a{color:var(--light)}
footer .cols{display:flex;justify-content:space-between;gap:32px;flex-wrap:wrap;margin-bottom:24px}
#aurora{position:absolute;inset:0;width:100%;height:100%;display:block;z-index:0;pointer-events:none}
.hero .container{position:relative;z-index:1}
.hero h1 .shiny{background:linear-gradient(110deg,#B77B48 30%,#F3E8D5 50%,#E8B84B 70%);background-size:220% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;animation:shine 4.5s linear infinite}
@keyframes shine{to{background-position:-220% 0}}
#hero-photo{position:relative;border-radius:20px;overflow:hidden;border:1px solid var(--line);box-shadow:0 30px 80px rgba(0,0,0,.55)}
#hero-photo img{width:100%;height:480px;object-fit:cover;display:block}
/* settle: sections arrive out of focus and settle (GetLayers pattern).
   Hidden ONLY when JS adds html.js — visible by default otherwise. */
.settle{transition:opacity .7s ease,filter .7s ease,transform .7s ease}
html.js .settle{opacity:0;filter:blur(10px);transform:translateY(20px)}
html.js .settle.in{opacity:1;filter:blur(0);transform:none}
@media(max-width:1024px){.container{padding-inline:28px}section{padding:72px 0}.stats-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:900px){.hero-grid,.two{grid-template-columns:1fr}.grid{grid-template-columns:repeat(2,1fr)}.filters{grid-template-columns:repeat(2,1fr)}.why{grid-template-columns:1fr}#hero-3d{height:380px}#hero-photo img{height:380px}}
@media(max-width:640px){.container{padding-inline:20px}section{padding:56px 0}.grid{grid-template-columns:1fr}.filters{grid-template-columns:1fr}form.lead{grid-template-columns:1fr}.nav nav{display:none}.hero{padding-top:calc(120px + var(--disc-h))}.nav .btn{padding:10px 14px;font-size:13px;white-space:nowrap}:root{--disc-h:52px}.disclaimer{font-size:11px;padding:8px 12px}#hero-3d{height:320px}#hero-photo img{height:320px}}
@media(max-width:400px){.container{padding-inline:16px}section{padding:44px 0}}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*,*::before,*::after{animation:none!important;transition:none!important}html.js .settle{opacity:1!important;filter:none!important;transform:none!important}}
"""

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>White Farmhouse Realty — Wayne, NE — Concept Redesign</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>__CSS__</style>
<noscript><style>.settle{opacity:1!important;filter:none!important;transform:none!important}#loader{display:none!important}#progress{display:none}#hero-3d .fallback{display:block!important}#hero-3d .spin-hint{display:none!important}</style></noscript>
</head>
<body>
<div class="disclaimer">Independent concept redesign &mdash; not affiliated with White Farmhouse Realty, LLC</div>
<div id="loader"><div class="circ"><svg class="ring" viewBox="0 0 230 230" aria-hidden="true"><defs><path id="circPath" d="M115,115 m-88,0 a88,88 0 1,1 176,0 a88,88 0 1,1 -176,0"/></defs><text><textPath href="#circPath">WHITE FARMHOUSE REALTY &#8226; WAYNE, NEBRASKA &#8226; </textPath></text></svg><div class="mark"><svg viewBox="0 0 64 64" fill="none" stroke="#B77B48" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 34 L32 12 L56 34"/><path d="M14 32 V56 H50 V32"/><path d="M28 56 V42 H36 V56"/></svg></div></div><div class="bar"><i></i></div></div>
<div id="progress"></div>
<header><div class="container nav">
<a class="brand" href="#top">White Farmhouse <span>Realty</span></a>
<nav><a href="#listings">Homes for sale</a><a href="#about">About</a><a href="#why">Why us</a><a href="#areas">Areas</a></nav>
<a class="btn" href="tel:4023754663">402-375-4663</a>
</div></header>
<div id="smooth">
<section class="hero" id="top"><canvas id="aurora"></canvas><div class="container hero-grid">
<div>
<p class="eyebrow">Wayne, Nebraska &middot; The Home Place in Northeast Nebraska</p>
<h1 id="hero-h1">Rooted in tradition. <em>Ready to show you home.</em></h1>
<p class="lede">White Farmhouse Realty helps families find homes, acreages and farms across Wayne County and northeast Nebraska &mdash; with real photos, real prices and a people-first team led by owner/broker Trisha Peters.</p>
<div class="pills">
<a class="btn" href="#listings">Search homes for sale</a>
<a class="btn ghost" href="#contact">Talk to Trisha</a>
</div>
<p class="cap" style="margin-top:20px">Residential &amp; acreage, commercial, farm sales and property management in Wayne, NE.</p>
</div>
<div class="stage">
<div id="hero-photo"><img src="__HERO_IMG__" alt="A white farmhouse-style home with a wide front yard"></div>
<p class="cap">Concept imagery &mdash; illustrative photo of a home like the ones listed.</p>
</div>
</div></section>

<section class="stats"><div class="container stats-grid">
<div><div class="num"><span class="countup" data-to="12">12</span></div><div class="lbl">Homes listed</div></div>
<div><div class="num">$<span class="countup" data-to="2.867" data-dec="2">2.87</span>M</div><div class="lbl">Total listed value</div></div>
<div><div class="num"><span class="countup" data-to="3">3</span></div><div class="lbl">Towns &mdash; Wayne, Emerson, Ponca</div></div>
<div><div class="num"><span class="countup" data-to="11">11</span> of 12</div><div class="lbl">Homes with full details</div></div>
</div></section>

<section id="listings"><div class="container">
<div class="sec-head settle"><p class="eyebrow">Homes for sale</p><h2>Find your place in Wayne County, Nebraska</h2><p>Search real, current listings by price, size and type. Every card shows what you need to decide &mdash; no dead ends, no missing photos.</p></div>
<div class="filters settle">
<div><label for="q">Search by town or street</label><input id="q" type="text" placeholder="e.g. Wayne"></div>
<div><label for="maxPrice">Max price</label><select id="maxPrice"><option value="">Any price</option><option value="100000">Up to $100,000</option><option value="150000">Up to $150,000</option><option value="200000">Up to $200,000</option><option value="300000">Up to $300,000</option><option value="400000">Up to $400,000</option><option value="600000">Up to $600,000</option></select></div>
<div><label for="minBeds">Min bedrooms</label><select id="minBeds"><option value="">Any</option><option value="2">2+</option><option value="3">3+</option><option value="4">4+</option><option value="5">5+</option></select></div>
<div><label for="minBaths">Min bathrooms</label><select id="minBaths"><option value="">Any</option><option value="1">1+</option><option value="2">2+</option><option value="3">3+</option></select></div>
<div><label for="type">Property type</label><select id="type"><option value="">All types</option><option>House</option><option>Land / Lot</option></select></div>
<div><label for="sort">Sort by</label><select id="sort"><option value="featured">Featured first</option><option value="plo">Price: low to high</option><option value="phi">Price: high to low</option><option value="beds">Most bedrooms</option></select></div>
<div><label>&nbsp;</label><button class="btn" type="button" id="clearFilters">Clear filters</button></div>
<div class="full"><span class="count" id="count">Showing 12 of 12 homes</span><span style="color:var(--muted);font-size:14px">Prices and availability change &mdash; confirm every listing with the brokerage before a showing.</span></div>
</div>
<div class="grid" id="grid">
__CARDS__
</div>
<p class="note">All 12 listings are real and taken from the brokerage&rsquo;s own homepage (Nov 2026): addresses, prices, beds, baths and square footage as published there. One listing, 212 Lincoln St ($10,000), is published with no type, beds, baths or size &mdash; shown here exactly that way, with details to confirm. Listing photos on the current site are placeholders; the photos here are concept imagery (Unsplash), illustrative only.</p>
</div></section>

<section class="alt settle" id="about"><div class="container two">
<div><img src="__ABOUT_IMG__" alt="A warm, lived-in living room"><p class="cap">Concept imagery &mdash; illustrative photo.</p></div>
<div><p class="eyebrow">Our story</p><h2 style="font-size:clamp(28px,3.4vw,40px);margin:12px 0 16px">The Home Place &mdash; rooted in tradition</h2><p style="color:var(--muted)">The story began generations ago with a two-story white farmhouse on a family farm near Wayne County&rsquo;s southern edge &mdash; a sanctuary after a long day, a safe haven in summer storms. That farmhouse is where the team learned hard work, stewardship and caring for neighbours.</p><p style="color:var(--muted);margin-top:14px">Today White Farmhouse Realty carries that on: residential and acreage sales, commercial real estate, farm sales and property management &mdash; people first, from first showing to long after closing.</p></div>
</div></section>

<section id="why"><div class="container">
<div class="sec-head settle"><p class="eyebrow">Why choose us</p><h2>A local team that knows the ground</h2></div>
<div class="why"><div class="settle"><h3>People first, always</h3><p>The team starts by getting to know you and your goals &mdash; then handles showings, documents, inspections and closing so you can focus on moving forward.</p></div><div class="settle"><h3>Residential, acreage and farm</h3><p>From a first home in Wayne to farmland that has been in a family for generations &mdash; the team lives and works on this land.</p></div><div class="settle"><h3>Commercial and property management</h3><p>Local businesses and rental housing, from two- to four-bedroom homes to apartments and duplexes, kept up like home.</p></div><div class="settle"><h3>Real photos, real detail</h3><p>Every listing with a proper photo and complete facts &mdash; because a buyer should see the home before they fall for it.</p></div></div>
</div></section>

<section class="alt" id="areas"><div class="container">
<div class="sec-head settle"><p class="eyebrow">Areas served</p><h2>Serving northeast Nebraska</h2><p>Wayne and the surrounding communities &mdash; the towns where the team lives, works and already lists homes.</p></div>
<div class="chips settle"><span class="chip">Wayne</span><span class="chip">Emerson</span><span class="chip">Ponca</span><span class="chip">Wakefield</span><span class="chip">Laurel</span><span class="chip">Allen</span><span class="chip">Wayne County</span></div>
</div></section>


<section class="alt" id="contact"><div class="container">
<div class="sec-head settle"><p class="eyebrow">Get in touch</p><h2>Ask about a home &mdash; or about selling yours</h2><p>Concept lead form for demonstration only. It does not send anything anywhere.</p></div>
<form class="lead settle" id="leadForm">
<div><label for="fname">First name</label><input id="fname" required></div>
<div><label for="lname">Last name</label><input id="lname" required></div>
<div><label for="femail">Email</label><input id="femail" type="email" required></div>
<div><label for="fphone">Phone</label><input id="fphone" type="tel"></div>
<div class="full"><label for="finterest">I am interested in</label><select id="finterest"><option>Buying a home</option><option>Selling my home</option><option>Buying land / acreage</option><option>Just browsing &mdash; send me new listings</option></select></div>
<div class="full"><label for="fmsg">Tell us what you are looking for</label><textarea id="fmsg" rows="4" placeholder="Town, budget, bedrooms, land &mdash; anything that helps."></textarea></div>
<div class="full"><button class="btn" type="submit">Send my enquiry (demo)</button></div>
</form>
<div class="form-ok" id="form-ok"><strong>Demo form &mdash; nothing was sent.</strong> In the live version this message would go straight to the brokerage, and an agent would reply. To reach the brokerage today, call <a href="tel:4023754663">402-375-4663</a> or email <a href="mailto:trisha@whitefarmhouserealty.com">trisha@whitefarmhouserealty.com</a>.</div>
</div></section>

<section class="contact-strip"><div class="container settle">
<h2>Prefer to talk it through?</h2>
<p>Call <a href="tel:4023754663">402-375-4663</a> &nbsp;&middot;&nbsp; Email <a href="mailto:trisha@whitefarmhouserealty.com">trisha@whitefarmhouserealty.com</a> &nbsp;&middot;&nbsp; 219 Main Street, Wayne, NE 68787</p>
<p style="margin-top:10px">Owner/broker Trisha Peters &mdash; office 402-375-4663, direct 402-518-0675.</p>
</div></section>

<section class="cta-final"><div class="container">
<h2 id="cta-h2">Your next home is out there. <span class="cta-accent">Let&rsquo;s find it.</span></h2>
<p>Search the listings above, save the ones you like, and send one message &mdash; Trisha and the team will take it from there.</p>
<a class="btn" href="#listings">Browse homes for sale</a>
</div></section>

<footer><div class="container">
<div class="cols">
<div><strong style="font-family:Fraunces,serif;font-size:18px">White Farmhouse Realty, LLC</strong><br>219 Main Street, Wayne, NE 68787<br><a href="tel:4023754663">402-375-4663</a><br><a href="mailto:trisha@whitefarmhouserealty.com">trisha@whitefarmhouserealty.com</a></div>
<div>Real website: <a href="https://www.whitefarmhouserealty.com/">https://www.whitefarmhouserealty.com/</a><br>Equal Housing Opportunity</div>
</div>
<p>Independent concept redesign &mdash; not affiliated with White Farmhouse Realty, LLC. Listing photos are concept imagery (Unsplash) &mdash; illustrative only, not photos of these homes. Listing details are from public sources noted above; verify price and availability with the brokerage. The 3D farmhouse is a concept model, not a photo of a real home.</p>
</div></footer>
</div>
<script>__AURORA__</script>
<script>__GSAP__</script>
<script>__JS__</script>
</body>
</html>
"""

JS = r"""
(function(){
"use strict";
document.documentElement.classList.add('js');
var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var finePointer = window.matchMedia('(pointer: fine)').matches;
var hasGsap = typeof window.gsap !== 'undefined';
var hasThree = typeof window.THREE !== 'undefined';
setTimeout(function(){ var l=document.getElementById('loader'); if(l) l.remove(); }, 2200);
/* ---- smooth scroll (lerp) ---- */
var wrap = document.getElementById('smooth');
var smoothOn = false, target = 0, current = 0, maxScroll = 0;
function measure(){ maxScroll = Math.max(0, wrap.scrollHeight - window.innerHeight); document.body.style.height = wrap.scrollHeight + 'px'; }
if(!reduced){
  try{
    wrap.style.position='fixed'; wrap.style.top='0'; wrap.style.left='0'; wrap.style.width='100%';
    measure(); window.addEventListener('resize', measure);
    target = window.scrollY || 0; current = target; smoothOn = true;
  }catch(e){ smoothOn = false; }
}
function scrollToY(y){
  y = Math.max(0, Math.min(y, maxScroll || (document.body.scrollHeight - window.innerHeight)));
  if(smoothOn){ window.scrollTo(0, y); target = y; }
  else { window.scrollTo({top:y, behavior:'smooth'}); }
}
document.querySelectorAll('a[href^="#"]').forEach(function(a){
  a.addEventListener('click', function(ev){
    var id = a.getAttribute('href'); if(id.length < 2) return;
    var el = document.querySelector(id); if(!el) return;
    ev.preventDefault();
    var discH = (document.querySelector('.disclaimer')||{offsetHeight:37}).offsetHeight;
    var y = smoothOn ? el.getBoundingClientRect().top + current - 70 - discH
                     : el.getBoundingClientRect().top + window.scrollY - 70 - discH;
    scrollToY(y);
  });
});
/* ---- Aurora: React Bits port (aurora.js) ---- */
initAurora(document.getElementById('aurora'));
/* ---- rAF loop: lerp scroll, progress light-stream, 3D scroll turn ---- */
var progress = document.getElementById('progress');
function tick(){
  if(smoothOn){
    target = window.scrollY || 0;
    current += (target - current) * 0.11;
    if(Math.abs(target - current) < 0.1) current = target;
    wrap.style.transform = 'translate3d(0,' + (-current) + 'px,0)';
  } else { current = window.scrollY || 0; }
  var doc = (document.body.scrollHeight - window.innerHeight) || 1;
  var p = Math.min(1, current / doc);
  progress.style.transform = 'scaleX(' + p + ')';
  requestAnimationFrame(tick);
}
requestAnimationFrame(tick);
/* ---- hero headline split + GSAP stagger ---- */
var h1 = document.getElementById('hero-h1');
if(h1 && hasGsap && !reduced){
  var nodes = Array.prototype.slice.call(h1.childNodes);
  h1.innerHTML = '';
  nodes.forEach(function(n){
    if(n.nodeType === 3){
      n.textContent.split(/\s+/).filter(Boolean).forEach(function(w){
        var s = document.createElement('span'); s.className='w'; s.textContent = w; h1.appendChild(s); h1.appendChild(document.createTextNode(' '));
      });
    } else if(n.nodeName === 'EM'){
      n.textContent.split(/\s+/).filter(Boolean).forEach(function(w){
        var s = document.createElement('span'); s.className='w shiny'; s.textContent = w; h1.appendChild(s); h1.appendChild(document.createTextNode(' '));
      });
    }
  });
  gsap.from('#hero-h1 .w', {y:26, opacity:0, filter:'blur(10px)', duration:.7, stagger:.055, ease:'power3.out', delay:.95});
  gsap.from('.hero .lede, .hero .pills, .hero .cap, .hero .eyebrow', {y:16, opacity:0, duration:.55, stagger:.08, ease:'power2.out', delay:1.25});
  setTimeout(function(){ gsap.set('#hero-h1 .w, .hero .lede, .hero .pills, .hero .cap, .hero .eyebrow', {clearProps:'all'}); }, 3000);
}
/* ---- settle reveals: out of focus -> sharp (IO) ---- */
if('IntersectionObserver' in window && !reduced){
  var io = new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } }); }, {threshold:.1, rootMargin:'0px 0px -4% 0px'});
  document.querySelectorAll('.settle').forEach(function(el){ io.observe(el); });
} else {
  document.querySelectorAll('.settle').forEach(function(el){ el.classList.add('in'); });
}
/* ---- count-up stats ---- */
function countUp(el){
  var to = parseFloat(el.getAttribute('data-to')), dec = parseInt(el.getAttribute('data-dec')||'0',10);
  setTimeout(function(){ el.textContent = to.toFixed(dec); }, 1600);
  var t0 = null, dur = 1300;
  function step(ts){ if(!t0) t0 = ts; var p = Math.min(1,(ts-t0)/dur); var e = 1-Math.pow(1-p,3);
    el.textContent = (to*e).toFixed(dec); if(p<1) requestAnimationFrame(step); }
  requestAnimationFrame(step);
}
if('IntersectionObserver' in window && !reduced){
  var io3 = new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ countUp(e.target); io3.unobserve(e.target); } }); }, {threshold:.5});
  document.querySelectorAll('.countup').forEach(function(el){ io3.observe(el); });
}
/* ---- tilting glass cards + glare (fine pointers only) ---- */
if(finePointer && !reduced){
  document.querySelectorAll('.card').forEach(function(cardEl){
    var media = cardEl.querySelector('.card-media');
    cardEl.addEventListener('pointermove', function(ev){
      var r = cardEl.getBoundingClientRect();
      var px = (ev.clientX - r.left)/r.width, py = (ev.clientY - r.top)/r.height;
      cardEl.style.transform = 'perspective(900px) rotateY(' + ((px-.5)*7) + 'deg) rotateX(' + ((.5-py)*7) + 'deg) translateY(-3px)';
      if(media){ media.style.setProperty('--gx', (px*100)+'%'); media.style.setProperty('--gy', (py*100)+'%'); }
    });
    cardEl.addEventListener('pointerleave', function(){ cardEl.style.transform=''; });
  });
  document.querySelectorAll('.btn').forEach(function(b){
    b.addEventListener('pointermove', function(ev){
      var r = b.getBoundingClientRect();
      var dx = ev.clientX-(r.left+r.width/2), dy = ev.clientY-(r.top+r.height/2);
      b.style.transform = 'translate(' + (dx*0.18) + 'px,' + (dy*0.28) + 'px)';
    });
    b.addEventListener('pointerleave', function(){ b.style.transform=''; });
  });
}
/* ---- filters with FLIP ---- */
var grid = document.getElementById('grid');
var cards = Array.prototype.slice.call(grid.querySelectorAll('.card'));
function applyFilters(animate){
  var before = {};
  if(animate && hasGsap && !reduced){ cards.forEach(function(c){ if(c.style.display!=='none') before[c.dataset.addr]=c.getBoundingClientRect(); }); }
  var q = document.getElementById('q').value.trim().toLowerCase();
  var maxP = document.getElementById('maxPrice').value;
  var minB = document.getElementById('minBeds').value;
  var minBa = document.getElementById('minBaths').value;
  var ty = document.getElementById('type').value;
  var sort = document.getElementById('sort').value;
  var shown = cards.filter(function(c){
    var price=+c.dataset.price, beds=+c.dataset.beds, baths=+c.dataset.baths;
    if(q && c.dataset.addr.indexOf(q)===-1 && c.dataset.type.toLowerCase().indexOf(q)===-1) return false;
    if(maxP && price > +maxP) return false;
    if(minB && beds < +minB) return false;
    if(minBa && baths < +minBa) return false;
    if(ty && c.dataset.type !== ty) return false;
    return true;
  });
  if(sort==='plo') shown.sort(function(a,b){return +a.dataset.price-+b.dataset.price;});
  if(sort==='phi') shown.sort(function(a,b){return +b.dataset.price-+a.dataset.price;});
  if(sort==='beds') shown.sort(function(a,b){return +b.dataset.beds-+a.dataset.beds;});
  cards.forEach(function(c){ c.style.display='none'; });
  shown.forEach(function(c){ grid.appendChild(c); c.style.display=''; });
  var empty = document.getElementById('no-results');
  if(!shown.length && !empty){ var d=document.createElement('div'); d.id='no-results'; d.className='empty'; d.innerHTML='<strong>No homes match those filters.</strong><br>Try widening the price range or clearing the filters &mdash; or call us and we will search for you.'; grid.appendChild(d); }
  if(shown.length && empty) empty.remove();
  document.getElementById('count').textContent = 'Showing ' + shown.length + ' of ' + cards.length + ' homes';
  if(animate && hasGsap && !reduced){
    shown.forEach(function(c){
      var b = before[c.dataset.addr]; if(!b) { gsap.from(c, {opacity:0, y:14, duration:.4, ease:'power2.out'}); return; }
      var a = c.getBoundingClientRect(); var dx=b.left-a.left, dy=b.top-a.top;
      if(dx||dy) gsap.fromTo(c, {x:dx, y:dy}, {x:0, y:0, duration:.45, ease:'power3.out'});
    });
  }
}
['q','maxPrice','minBeds','minBaths','type','sort'].forEach(function(id){
  document.getElementById(id).addEventListener('input', function(){ applyFilters(true); });
});
document.getElementById('clearFilters').addEventListener('click', function(){
  ['q','maxPrice','minBeds','minBaths','type','sort'].forEach(function(id){ document.getElementById(id).value = id==='sort' ? 'featured' : ''; });
  applyFilters(true);
});
/* ---- final CTA: char-by-char ---- */
var cta = document.getElementById('cta-h2');
if(cta && hasGsap && !reduced){
  var accent = cta.querySelector('.cta-accent');
  var p1 = cta.childNodes[0].textContent, p2 = accent.textContent;
  cta.innerHTML='';
  function chars(str, cls){ str.split('').forEach(function(ch){ var s=document.createElement('span'); s.className='ch '+cls; s.textContent=ch===' '?'\u00a0':ch; cta.appendChild(s); }); }
  chars(p1, ''); chars(' ', ''); chars(p2, 'cta-accent');
  cta.querySelectorAll('.cta-accent').forEach(function(s){ s.style.color='var(--gold)'; });
  if('IntersectionObserver' in window){
    var io4 = new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ gsap.from('#cta-h2 .ch', {opacity:0, y:12, duration:.35, stagger:.018, ease:'power2.out'}); io4.disconnect(); } }); }, {threshold:.5});
    io4.observe(cta);
  }
}
/* ---- demo lead form ---- */
var form = document.getElementById('leadForm');
if(form){ form.addEventListener('submit', function(ev){ ev.preventDefault(); document.getElementById('form-ok').style.display='block'; form.reset(); }); }
})();
"""

out = (HTML.replace('__CSS__', CSS)
           .replace('__HERO_IMG__', IMG['hero'])
           .replace('__ABOUT_IMG__', IMG['about'])
           .replace('__CARDS__', CARDS)
           .replace('__AURORA__', AURORA)
           .replace('__GSAP__', GSAP)
           .replace('__JS__', JS))
open('index.html', 'w').write(out)
print('built index.html:', len(out)//1024, 'KB')
