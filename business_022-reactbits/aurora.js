/* Aurora — vanilla port of React Bits' Aurora (reactbits.dev/backgrounds/aurora).
   Original source: DavidHDev/react-bits, src/content/Backgrounds/Aurora/Aurora.jsx.
   React lifecycle stripped; shader + render logic kept verbatim.
   Colors tuned for this site: bronze -> brass -> gold on near-black.
   WebGL2 required; if unavailable the canvas hides itself. */
(function () {
  'use strict';
  var MAX_STOPS = 5, MAX_LAYERS = 3, INTRO_SECONDS = 2.4;

  var VERTEX = '#version 300 es\nin vec2 aPosition;\nvoid main() {\n  gl_Position = vec4(aPosition, 0.0, 1.0);\n}';

  var FRAGMENT = '#version 300 es\nprecision highp float;\nprecision highp int;\nuniform vec2 uResolution;\nuniform float uTime;\nuniform vec3 uStops[' + MAX_STOPS + '];\nuniform int uStopCount;\nuniform float uAmplitude;\nuniform float uBlend;\nuniform float uHeight;\nuniform float uScale;\nuniform float uGlow;\nuniform float uBrightness;\nuniform int uLayers;\nuniform float uFlip;\nuniform vec3 uPointer;\nuniform float uReveal;\nuniform float uOpacity;\nuniform float uLightMode;\nout vec4 outColor;\n\nvec3 permute(vec3 x) {\n  return mod(((x * 34.0) + 1.0) * x, 289.0);\n}\n\nfloat snoise(vec2 v) {\n  const vec4 C = vec4(0.211324865405187, 0.366025403784439, -0.577350269189626, 0.024390243902439);\n  vec2 i = floor(v + dot(v, C.yy));\n  vec2 x0 = v - i + dot(i, C.xx);\n  vec2 i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);\n  vec4 x12 = x0.xyxy + C.xxzz;\n  x12.xy -= i1;\n  i = mod(i, 289.0);\n  vec3 p = permute(permute(i.y + vec3(0.0, i1.y, 1.0)) + i.x + vec3(0.0, i1.x, 1.0));\n  vec3 m = max(0.5 - vec3(dot(x0, x0), dot(x12.xy, x12.xy), dot(x12.zw, x12.zw)), 0.0);\n  m = m * m;\n  m = m * m;\n  vec3 x = 2.0 * fract(p * C.www) - 1.0;\n  vec3 h = abs(x) - 0.5;\n  vec3 ox = floor(x + 0.5);\n  vec3 a0 = x - ox;\n  m *= 1.79284291400159 - 0.85373472095314 * (a0 * a0 + h * h);\n  vec3 g;\n  g.x = a0.x * x0.x + h.x * x0.y;\n  g.yz = a0.yz * x12.xz + h.yz * x12.yw;\n  return 130.0 * dot(m, g);\n}\n\nfloat smootherstep(float edge0, float edge1, float x) {\n  float t = clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0);\n  return t * t * t * (t * (t * 6.0 - 15.0) + 10.0);\n}\n\nvec3 oklabToLinear(vec3 c) {\n  float l = c.x + 0.3963377774 * c.y + 0.2158037573 * c.z;\n  float m = c.x - 0.1055613458 * c.y - 0.0638541728 * c.z;\n  float s = c.x - 0.0894841775 * c.y - 1.2914855480 * c.z;\n  l = l * l * l;\n  m = m * m * m;\n  s = s * s * s;\n  return vec3(\n    4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,\n    -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,\n    -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s\n  );\n}\n\nvec3 toSrgb(vec3 c) {\n  c = clamp(c, 0.0, 1.0);\n  return mix(c * 12.92, 1.055 * pow(c, vec3(1.0 / 2.4)) - 0.055, step(0.0031308, c));\n}\n\nvec3 ramp(float t) {\n  float x = clamp(t, 0.0, 1.0) * float(uStopCount - 1);\n  int i = int(min(floor(x), float(uStopCount - 2)));\n  float f = x - float(i);\n  f = f * f * (3.0 - 2.0 * f);\n  vec3 lch = mix(uStops[i], uStops[i + 1], f);\n  lch.x = mix(lch.x, min(lch.x, 0.7), uLightMode);\n  return toSrgb(oklabToLinear(vec3(lch.x, lch.y * cos(lch.z), lch.y * sin(lch.z))));\n}\n\nfloat hash(vec2 p) {\n  p = fract(p * vec2(123.34, 456.21));\n  p += dot(p, p + 45.32);\n  return fract(p.x * p.y);\n}\n\nvoid main() {\n  vec2 frag = gl_FragCoord.xy;\n  float y = 1.0 - frag.y / uResolution.y;\n  y = mix(y, 1.0 - y, uFlip);\n  float u = frag.x / uResolution.x;\n  float X = (frag.x - uResolution.x * 0.5) / uResolution.y;\n  float t = uTime;\n  float reach = uPointer.z * exp(-pow((X - uPointer.x) / 0.38, 2.0));\n\n  vec3 glow = vec3(0.0);\n  float cover = 0.0;\n  for (int k = 0; k < ' + MAX_LAYERS + '; k++) {\n    if (k >= uLayers) break;\n    float layer = float(k);\n    float seed = layer * 13.7;\n    float pace = t * (1.0 - layer * 0.18);\n    float warp = snoise(vec2(X * 0.45 * uScale + pace * 0.02 + seed, pace * 0.05 + seed));\n    float wave = snoise(vec2(X * 0.75 * uScale + warp * 0.35 - pace * 0.03 + seed, pace * 0.07 - seed)) * 0.72\n      + snoise(vec2(X * 1.6 * uScale + warp * 0.5 + pace * 0.04 - seed, pace * 0.1 + seed * 0.5)) * 0.28;\n    float hem = uHeight + layer * 0.07 + wave * 0.15 * uAmplitude;\n    hem += reach * 0.08 * (layer < 0.5 ? 1.0 : 0.4);\n    hem = mix(-0.25, hem, uReveal);\n\n    float soft = (0.04 + uBlend * 0.16) * (1.0 + layer * 0.9);\n    float rise = hem - y;\n    float low = -soft - uGlow * 0.14;\n    float high = 0.26 + soft * 0.6;\n    float body = pow(smootherstep(low, high, rise), 1.5 + uGlow * 0.6);\n    float lobes = 0.86 + 0.14 * snoise(vec2(X * 0.9 * uScale - pace * 0.025 + seed, y * 0.3 + pace * 0.04));\n    float alpha = body * lobes * (layer < 0.5 ? 1.0 : 0.32 / layer);\n    alpha = clamp(alpha * (1.0 + reach * 0.25 * smootherstep(0.9, 0.0, abs(y - hem))), 0.0, 1.0);\n\n    vec3 tint = ramp(u + 0.05 * sin(pace * 0.08 + layer * 2.3) + layer * 0.1 + max(rise, 0.0) * 0.05);\n    glow = 1.0 - (1.0 - glow) * (1.0 - tint * alpha);\n    cover = 1.0 - (1.0 - cover) * (1.0 - alpha);\n  }\n\n  float fade = smootherstep(0.0, 0.7, uReveal) * uOpacity;\n  float strength = clamp(uBrightness, 0.0, 2.0);\n  glow *= fade * min(strength, 1.0);\n  cover *= fade * min(strength, 1.0);\n  glow = 1.0 - pow(1.0 - glow, vec3(max(strength, 1.0)));\n  float dither = (hash(frag) - 0.5) / 255.0;\n\n  if (uLightMode > 0.5) {\n    vec3 tint = cover > 0.0001 ? glow / cover : vec3(0.0);\n    cover *= smootherstep(0.0, 0.25, cover);\n    float alpha = cover * 0.7;\n    outColor = vec4(tint * alpha + dither, clamp(alpha + dither, 0.0, 1.0));\n    return;\n  }\n  outColor = vec4(glow + dither, clamp(cover + dither, 0.0, 1.0));\n}';

  function clamp(v, mn, mx) { return Math.min(mx, Math.max(mn, v)); }

  function toOklch(rgb) {
    var r = rgb[0], g = rgb[1], b = rgb[2];
    r = r <= 0.04045 ? r / 12.92 : Math.pow((r + 0.055) / 1.055, 2.4);
    g = g <= 0.04045 ? g / 12.92 : Math.pow((g + 0.055) / 1.055, 2.4);
    b = b <= 0.04045 ? b / 12.92 : Math.pow((b + 0.055) / 1.055, 2.4);
    var l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b);
    var m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b);
    var s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
    var lab = [
      0.2104542553 * l + 0.793617785 * m - 0.0040720468 * s,
      1.9779984951 * l - 2.428592205 * m + 0.4505937099 * s,
      0.0259040371 * l + 0.7827717662 * m - 0.808675766 * s
    ];
    return [lab[0], Math.hypot(lab[1], lab[2]), Math.atan2(lab[2], lab[1])];
  }

  function unwrapHues(stops) {
    var known = -1;
    for (var i = 0; i < stops.length; i++) { if (stops[i][1] > 0.02) { known = i; break; } }
    var anchor = known === -1 ? 0 : stops[known][2];
    var previous = anchor;
    return stops.map(function (stop) {
      var hue = stop[1] > 0.02 ? stop[2] : previous;
      while (hue - previous > Math.PI) hue -= Math.PI * 2;
      while (hue - previous < -Math.PI) hue += Math.PI * 2;
      previous = hue;
      return [stop[0], stop[1], hue];
    });
  }

  function compile(gl, type, source) {
    var shader = gl.createShader(type);
    if (!shader) return null;
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    if (gl.getShaderParameter(shader, gl.COMPILE_STATUS)) return shader;
    gl.deleteShader(shader);
    return null;
  }

  function link(gl) {
    var vertex = compile(gl, gl.VERTEX_SHADER, VERTEX);
    var fragment = compile(gl, gl.FRAGMENT_SHADER, FRAGMENT);
    var program = gl.createProgram();
    if (!vertex || !fragment || !program) return null;
    gl.attachShader(program, vertex);
    gl.attachShader(program, fragment);
    gl.bindAttribLocation(program, 0, 'aPosition');
    gl.linkProgram(program);
    gl.deleteShader(vertex);
    gl.deleteShader(fragment);
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) { gl.deleteProgram(program); return null; }
    var uniforms = {};
    var count = gl.getProgramParameter(program, gl.ACTIVE_UNIFORMS);
    for (var i = 0; i < count; i++) {
      var info = gl.getActiveUniform(program, i);
      if (info) uniforms[info.name.replace('[0]', '')] = gl.getUniformLocation(program, info.name);
    }
    return { program: program, uniforms: uniforms };
  }

  /* settings: React Bits Aurora defaults, only colorStops changed to brass/gold */
  var S = {
    stops: ['#6B4A2F', '#B77B48', '#E8B84B'],
    amplitude: 1, blend: 0.5, speed: 1, height: 0.45, scale: 1,
    glow: 0.6, brightness: 1, layers: 1, flip: 0,
    mouseInteraction: true, intro: true, opacity: 1, lightMode: false, paused: false
  };

  window.initAurora = function (canvas) {
    if (!canvas) return false;
    var container = canvas.parentElement;
    var gl = canvas.getContext('webgl2', { alpha: true, premultipliedAlpha: true, antialias: false, depth: false, stencil: false });
    if (!container || !gl) { canvas.style.display = 'none'; return false; }
    var prog = link(gl);
    if (!prog) { canvas.style.display = 'none'; return false; }
    var u = prog.uniforms;

    var buffer = gl.createBuffer();
    var vao = gl.createVertexArray();
    gl.bindVertexArray(vao);
    gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    gl.enableVertexAttribArray(0);
    gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);

    var probe = document.createElement('canvas').getContext('2d', { willReadFrequently: true });
    var reduce = (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) || false;
    var cache = new Map();
    function parse(value) {
      if (cache.has(value)) return cache.get(value);
      var rgb = [1, 1, 1];
      if (probe) {
        probe.clearRect(0, 0, 1, 1);
        probe.fillStyle = '#ffffff';
        probe.fillStyle = value;
        probe.fillRect(0, 0, 1, 1);
        var d = probe.getImageData(0, 0, 1, 1).data;
        rgb = [d[0] / 255, d[1] / 255, d[2] / 255];
      }
      cache.set(value, rgb);
      return rgb;
    }
    var palette = new Float32Array(MAX_STOPS * 3);
    var view = { width: 1, height: 1 };
    var pointer = { x: 0, y: 0, inside: false };
    var state = { clock: 0, px: 0, py: 0.5, reach: 0, reveal: (S.intro && !reduce) ? 0 : 1 };
    var raf = 0, last = 0, visible = true;

    function render() {
      unwrapHues(S.stops.map(function (v) { return toOklch(parse(v)); })).forEach(function (stop, i) { palette.set(stop, i * 3); });
      var reveal = state.reveal;
      gl.viewport(0, 0, canvas.width, canvas.height);
      gl.useProgram(prog.program);
      gl.bindVertexArray(vao);
      gl.uniform2f(u.uResolution, canvas.width, canvas.height);
      gl.uniform1f(u.uTime, state.clock);
      gl.uniform3fv(u.uStops, palette);
      gl.uniform1i(u.uStopCount, S.stops.length);
      gl.uniform1f(u.uAmplitude, S.amplitude);
      gl.uniform1f(u.uBlend, S.blend);
      gl.uniform1f(u.uHeight, S.height);
      gl.uniform1f(u.uScale, S.scale);
      gl.uniform1f(u.uGlow, S.glow);
      gl.uniform1f(u.uBrightness, S.brightness);
      gl.uniform1i(u.uLayers, S.layers);
      gl.uniform1f(u.uFlip, S.flip);
      gl.uniform3f(u.uPointer, state.px, state.py, state.reach);
      gl.uniform1f(u.uReveal, 1 - Math.pow(1 - reveal, 3));
      gl.uniform1f(u.uOpacity, S.opacity);
      gl.uniform1f(u.uLightMode, S.lightMode ? 1 : 0);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
    }

    function frame(now) {
      raf = 0;
      if (!visible || document.hidden) return;
      var dt = last ? clamp((now - last) / 1000, 0.0005, 0.05) : 1 / 60;
      last = now;
      if (S.paused) { state.reveal = 1; render(); last = 0; return; }
      var motion = reduce ? 0 : 1;
      state.clock += dt * S.speed * motion;
      var engaged = S.mouseInteraction && pointer.inside && !reduce;
      var follow = 1 - Math.exp(-dt / 0.6);
      if (engaged) {
        var tx = (pointer.x - view.width / 2) / view.height;
        var ty = S.flip ? 1 - pointer.y / view.height : pointer.y / view.height;
        state.px += (tx - state.px) * follow;
        state.py += (ty - state.py) * follow;
      }
      state.reach += ((engaged ? 1 : 0) - state.reach) * (1 - Math.exp(-dt / (engaged ? 0.9 : 1.4)));
      if (!S.intro || reduce) state.reveal = 1;
      else if (state.reveal < 1) state.reveal = Math.min(1, state.reveal + dt / INTRO_SECONDS);
      render();
      raf = requestAnimationFrame(frame);
    }

    function wake() { if (!raf && visible && !document.hidden) raf = requestAnimationFrame(frame); }

    function resize() {
      var width = Math.max(1, window.innerWidth || container.clientWidth);
      var height = Math.max(1, window.innerHeight || container.clientHeight);
      var ratio = Math.min(window.devicePixelRatio || 1, 2);
      view.width = width; view.height = height;
      canvas.width = Math.max(1, Math.round(width * ratio));
      canvas.height = Math.max(1, Math.round(height * ratio));
      render(); wake();
    }

    function onPointerMove(e) {
      var rect = container.getBoundingClientRect();
      pointer.x = e.clientX - rect.left;
      pointer.y = e.clientY - rect.top;
      var wasInside = pointer.inside;
      pointer.inside = pointer.x >= 0 && pointer.y >= 0 && pointer.x <= rect.width && pointer.y <= rect.height;
      if (pointer.inside && !wasInside) {
        state.px = (pointer.x - rect.width / 2) / Math.max(1, rect.height);
        state.py = S.flip ? 1 - pointer.y / Math.max(1, rect.height) : pointer.y / Math.max(1, rect.height);
      }
      if (!S.paused) wake();
    }
    function onPointerUp(e) { if (e.pointerType !== 'mouse') pointer.inside = false; }
    function onPointerLeave() { pointer.inside = false; }
    function onVisibility() { last = 0; wake(); }

    var ro = new ResizeObserver(resize); ro.observe(container);
    var io = new IntersectionObserver(function (es) {
      visible = es.some(function (e) { return e.isIntersecting; });
      if (visible) { last = 0; wake(); }
    });
    io.observe(container);
    window.addEventListener('pointermove', onPointerMove, { passive: true });
    window.addEventListener('pointerdown', onPointerMove, { passive: true });
    window.addEventListener('pointerup', onPointerUp, { passive: true });
    window.addEventListener('pointercancel', onPointerUp, { passive: true });
    document.documentElement.addEventListener('pointerleave', onPointerLeave);
    document.addEventListener('visibilitychange', onVisibility);
    resize();
    return true;
  };
})();
