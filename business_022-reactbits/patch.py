#!/usr/bin/env python3
"""One-off patch: turn the business_022-3d build into the React Bits build.
- Drop the Three.js cartoon house; hero gets React Bits Aurora (WebGL2 shader, ported
  verbatim in aurora.js) + the real hero photo in a framed stage.
- Blur Text headline (blur->resolve word by word, GSAP) + Shiny Text on the gold word.
- Display font Fraunces -> Cormorant Garamond (italic accent word).
Everything else (listings, filters, stats, sections, disclaimers) untouched.
"""
import re

p = 'build.py'
s = open(p).read()
orig = s

def rep(old, new, n=1):
    global s
    assert s.count(old) >= n, 'NOT FOUND: ' + old[:90]
    s = s.replace(old, new, n)

# 1. inline aurora.js instead of three.min.js
rep("THREE = open('three.min.js').read()", "AURORA = open('aurora.js').read()")

# 2. fonts: Cormorant Garamond display + Inter body
rep("family=Fraunces:opsz,wght@9..144,600;9..144,700;9..144,800&family=Inter:wght@400;500;600;700",
    "family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Inter:wght@400;500;600;700")
rep("h1,h2,h3{font-family:Fraunces,Georgia,serif;",
    "h1,h2,h3{font-family:'Cormorant Garamond',Georgia,serif;")
rep(".hero h1 em{font-style:normal;color:var(--gold)}",
    ".hero h1 em{font-style:italic;color:var(--gold)}")

# 3. hero positioning + aurora canvas + shiny text + photo stage CSS
rep(".hero{background:radial-gradient(900px 520px at 78% 30%,rgba(183,123,72,.22),transparent 60%),radial-gradient(700px 500px at 10% 90%,rgba(232,184,75,.08),transparent 60%),var(--bg);padding:calc(148px + var(--disc-h)) 0 72px;overflow:hidden}",
    ".hero{background:radial-gradient(900px 520px at 78% 30%,rgba(183,123,72,.22),transparent 60%),radial-gradient(700px 500px at 10% 90%,rgba(232,184,75,.08),transparent 60%),var(--bg);padding:calc(148px + var(--disc-h)) 0 72px;overflow:hidden;position:relative}")
rep("/* settle:",
    """#aurora{position:absolute;inset:0;width:100%;height:100%;display:block;z-index:0;pointer-events:none}
.hero .container{position:relative;z-index:1}
.hero h1 .shiny{background:linear-gradient(110deg,#B77B48 30%,#F3E8D5 50%,#E8B84B 70%);background-size:220% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;animation:shine 4.5s linear infinite}
@keyframes shine{to{background-position:-220% 0}}
#hero-photo{position:relative;border-radius:20px;overflow:hidden;border:1px solid var(--line);box-shadow:0 30px 80px rgba(0,0,0,.55)}
#hero-photo img{width:100%;height:480px;object-fit:cover;display:block}
/* settle:""")
rep("@media(max-width:900px){.hero-grid,.two{grid-template-columns:1fr}.grid{grid-template-columns:repeat(2,1fr)}.filters{grid-template-columns:repeat(2,1fr)}.why{grid-template-columns:1fr}#hero-3d{height:380px}}",
    "@media(max-width:900px){.hero-grid,.two{grid-template-columns:1fr}.grid{grid-template-columns:repeat(2,1fr)}.filters{grid-template-columns:repeat(2,1fr)}.why{grid-template-columns:1fr}#hero-3d{height:380px}#hero-photo img{height:380px}}")
rep(".nav .btn{padding:10px 14px;font-size:13px;white-space:nowrap}:root{--disc-h:52px}.disclaimer{font-size:11px;padding:8px 12px}#hero-3d{height:320px}}",
    ".nav .btn{padding:10px 14px;font-size:13px;white-space:nowrap}:root{--disc-h:52px}.disclaimer{font-size:11px;padding:8px 12px}#hero-3d{height:320px}#hero-photo img{height:320px}}")

# 4. hero HTML: aurora canvas + photo stage instead of the 3D stage
rep('<section class="hero" id="top"><div class="container hero-grid">',
    '<section class="hero" id="top"><canvas id="aurora"></canvas><div class="container hero-grid">')
rep("""<div class="stage">
<div id="hero-3d"><canvas id="gl"></canvas><div class="fallback"><img src="__HERO_IMG__" alt="A white farmhouse-style home with a wide front yard"></div><span class="spin-hint">&#10227; DRAG TO SPIN THE HOUSE</span></div>
<p class="cap">A 3D farmhouse, built for this concept &mdash; grab it and spin it. The photo fallback shows if your browser has no 3D.</p>
</div>""",
    """<div class="stage">
<div id="hero-photo"><img src="__HERO_IMG__" alt="A white farmhouse-style home with a wide front yard"></div>
<p class="cap">Concept imagery &mdash; illustrative photo of a home like the ones listed.</p>
</div>""")

# 5. JS: cut the whole Three.js block, start Aurora instead
s2, n = re.subn(r"/\* =+ THREE\.JS FARMHOUSE =+ \*/.*?/\* ---- rAF loop",
                "/* ---- Aurora: React Bits port (aurora.js) ---- */\ninitAurora(document.getElementById('aurora'));\n/* ---- rAF loop",
                s, count=1, flags=re.S)
assert n == 1, 'Three.js block not found'
s = s2
rep("  threeState.scrollP = p;\n", "")

# 6. Blur Text headline (React Bits Blur Text, GSAP port): blur -> resolve, word by word
rep("gsap.from('#hero-h1 .w', {y:26, opacity:0, duration:.7, stagger:.055, ease:'power3.out', delay:.95});",
    "gsap.from('#hero-h1 .w', {y:26, opacity:0, filter:'blur(10px)', duration:.7, stagger:.055, ease:'power3.out', delay:.95});")
# 7. Shiny Text on the gold (em) words: drop the inline gold color, let .shiny rule paint it
rep("var s = document.createElement('span'); s.className='w'; s.style.color='var(--gold)'; s.textContent = w;",
    "var s = document.createElement('span'); s.className='w shiny'; s.textContent = w;")

# 8. assembly: inline aurora.js instead of three.min.js
rep("<script>__THREE__</script>", "<script>__AURORA__</script>")
rep(".replace('__THREE__', THREE)", ".replace('__AURORA__', AURORA)")

open(p, 'w').write(s)
print('patched OK, changed bytes:', len(s) - len(orig))
print('THREE refs left:', s.count('THREE'), '| threeState refs left:', s.count('threeState'), '| hero-3d refs left:', s.count('hero-3d'))
