#!/usr/bin/env python3
"""Patch 2 (corrected anchors): opening intro = circular rotating logo.
React Bits Circular Text idea (letters around a circle, ring rotating); the real
component's drag/fling physics + framer-motion springs are dropped — a loader has
no dragging. Loader auto-fades, then the hero with the whole building photo shows.
Intro lengthened slightly (1.05s -> 1.6s) so the spinning ring is actually seen.
"""
p = 'build.py'
s = open(p).read()

def rep(old, new, n=1):
    global s
    assert s.count(old) >= n, 'NOT FOUND: ' + old[:90]
    s = s.replace(old, new, n)

# 1. loader timing: fade at 1.6s, removed at 2.2s
rep("animation:loaderOut .45s ease 1.05s forwards", "animation:loaderOut .45s ease 1.6s forwards")
rep("setTimeout(function(){ var l=document.getElementById('loader'); if(l) l.remove(); }, 1600);",
    "setTimeout(function(){ var l=document.getElementById('loader'); if(l) l.remove(); }, 2200);")

# 2. CSS: circular logo styles (replace the old text-mark rules)
rep("#loader .mark{font-family:Fraunces,serif;color:var(--light);font-size:26px;font-weight:700}\n#loader .mark span{color:var(--accent)}",
    "#loader .circ{width:230px;height:230px;position:relative}\n"
    "#loader .circ svg.ring{width:100%;height:100%;animation:spin 8s linear infinite}\n"
    "@keyframes spin{to{transform:rotate(360deg)}}\n"
    "#loader .circ text{fill:var(--cream);font-family:Inter,system-ui,sans-serif;font-size:15.5px;font-weight:600;letter-spacing:3px}\n"
    "#loader .circ .mark{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}\n"
    "#loader .circ .mark svg{width:64px;height:64px}")

# 3. HTML: loader content -> circular rotating logo + house mark + progress bar
rep("""<div id="loader"><div class="mark">White Farmhouse <span>Realty</span></div><div class="bar"><i></i></div></div>""",
    """<div id="loader"><div class="circ"><svg class="ring" viewBox="0 0 230 230" aria-hidden="true"><defs><path id="circPath" d="M115,115 m-88,0 a88,88 0 1,1 176,0 a88,88 0 1,1 -176,0"/></defs><text><textPath href="#circPath">WHITE FARMHOUSE REALTY &#8226; WAYNE, NEBRASKA &#8226; </textPath></text></svg><div class="mark"><svg viewBox="0 0 64 64" fill="none" stroke="#B77B48" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 34 L32 12 L56 34"/><path d="M14 32 V56 H50 V32"/><path d="M28 56 V42 H36 V56"/></svg></div></div><div class="bar"><i></i></div></div>""")

open(p, 'w').write(s)
print('patch2 OK')
print('circ refs:', s.count('circ'), '| loader .mark text refs:', s.count('class="mark">White'))
