#!/usr/bin/env python3
"""Script layer of the v2 build. Imported by tools/apply_v2.py.

Removes the pinned-scroll and counter code that no longer has markup to drive
(markup 18 took the stats band, and the amenity gallery is now a flat grid),
then adds the bedroom filter (markup 20) and the palette switcher.
"""

OLD_GALLERY = '''  // ---- Horizontal pinned amenity gallery with graceful flat fallback ----
  var hscene = document.getElementById('hscene');
  var htrack = document.getElementById('htrack');
  var flatGallery = reduced || !fine || innerWidth < 900 || document.hidden || !('IntersectionObserver' in window);
  if(flatGallery){
    hscene.classList.add('flat');
  } else {
    var hTicking = false;
    function hFrame(){
      hTicking = false;
      var vh = innerHeight;
      if(!vh || hscene.classList.contains('flat')) return;
      var r = hscene.getBoundingClientRect();
      var total = r.height - vh;
      if(total <= 0) return;
      var p = Math.min(1, Math.max(0, -r.top / total));
      var over = htrack.scrollWidth - innerWidth;
      if(over > 0) htrack.style.transform = 'translateX(' + (-over*p).toFixed(1) + 'px)';
    }
    addEventListener('scroll', function(){ if(!hTicking){ hTicking = true; requestAnimationFrame(hFrame);} }, {passive:true});
    addEventListener('resize', hFrame);
    hFrame();
  }

'''

NEW_FILTER = '''  // ---- Bedroom filter over the floor plan cards (markup 20) ----
  (function(){
    var grid = document.getElementById('plangrid');
    var out = document.getElementById('bedcount');
    if(!grid) return;
    var plans = [].slice.call(grid.querySelectorAll('.plan'));
    var btns = [].slice.call(document.querySelectorAll('[data-bedfilter]'));
    var LABEL = {all:'floor plan types', studio:'studio floor plans',
                 '1':'one bedroom floor plans', '2':'two bedroom floor plans',
                 '3':'three bedroom floor plans'};
    function show(want){
      var n = 0;
      plans.forEach(function(p){
        var hit = want === 'all' || p.dataset.bed === want;
        p.hidden = !hit;
        if(hit){ n++; p.classList.add('in'); }
      });
      btns.forEach(function(b){
        b.setAttribute('aria-pressed', b.dataset.bedfilter === want ? 'true' : 'false');
      });
      if(out){
        out.textContent = want === 'all'
          ? 'Showing all ' + n + ' floor plan types'
          : 'Showing ' + n + ' of ' + plans.length + ' ' + LABEL[want];
      }
    }
    btns.forEach(function(b){
      b.addEventListener('click', function(){ show(b.dataset.bedfilter); });
    });
    show('all');
  })();

'''

SWITCHER_JS = '''
<script>
/* Palette switcher. Four deep-colour options from the BSaR branding PDF,
   default C (Pantone Deep Purple 2617 C). Choice is remembered per browser. */
(function(){
  var KEY = 'the501_palette';
  var VALID = {A:1, B:1, C:1, D:1};
  var root = document.documentElement;
  var btns = [].slice.call(document.querySelectorAll('.pal [data-pal]'));
  function set(p, persist){
    if(!VALID[p]) p = 'C';
    root.setAttribute('data-palette', p);
    btns.forEach(function(b){
      b.setAttribute('aria-pressed', b.dataset.pal === p ? 'true' : 'false');
    });
    if(persist){ try { localStorage.setItem(KEY, p); } catch(e){} }
  }
  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch(e){}
  set(saved || 'C', false);
  btns.forEach(function(b){
    b.addEventListener('click', function(){ set(b.dataset.pal, true); });
  });
})();
</script>
'''


def run(h, sub, resub, cut_block):
    # the pinned scene is gone; so is the code that drove it
    h = sub(h, OLD_GALLERY, NEW_FILTER, 1, "gallery js out, filter js in")

    # the counter animation only ever fed the stats band, which markup 18 removed
    h = sub(h,
            "  var revealables = [].slice.call(document.querySelectorAll('.reveal, .reveal-img, .incentive'));\n"
            "  var counters = [].slice.call(document.querySelectorAll('[data-count]'));\n"
            "\n"
            "  function fmt(n, comma){\n"
            "    var s = String(n);\n"
            "    if(comma) s = s.replace(/\\B(?=(\\d{3})+(?!\\d))/g, ',');\n"
            "    return s;\n"
            "  }\n"
            "  function finishCounter(el){\n"
            "    el.textContent = fmt(+el.dataset.count, el.dataset.comma) + (el.dataset.suffix || '');\n"
            "  }\n"
            "  function revealAllNow(){\n"
            "    revealables.forEach(function(el){ el.classList.add('in'); });\n"
            "    counters.forEach(finishCounter);\n"
            "  }\n",
            "  var revealables = [].slice.call(document.querySelectorAll('.reveal, .reveal-img, .incentive'));\n"
            "\n"
            "  function revealAllNow(){\n"
            "    revealables.forEach(function(el){ el.classList.add('in'); });\n"
            "  }\n",
            1, "counter helpers out")
    h = sub(h,
            "    var cio = new IntersectionObserver(function(es){\n"
            "      es.forEach(function(e){\n"
            "        if(!e.isIntersecting) return;\n"
            "        var el = e.target, target = +el.dataset.count, comma = el.dataset.comma, suf = el.dataset.suffix || '';\n"
            "        cio.unobserve(el);\n"
            "        if(reduced){ finishCounter(el); return; }\n"
            "        var t0 = null;\n"
            "        function step(t){\n"
            "          if(!t0) t0 = t;\n"
            "          var p = Math.min((t - t0)/1400, 1);\n"
            "          el.textContent = fmt(Math.round(target * (1 - Math.pow(1 - p, 3))), comma) + suf;\n"
            "          if(p < 1) requestAnimationFrame(step); else finishCounter(el);\n"
            "        }\n"
            "        requestAnimationFrame(step);\n"
            "      });\n"
            "    }, {threshold:.6});\n"
            "    counters.forEach(function(el){ cio.observe(el); });\n"
            "\n",
            "",
            1, "counter observer out")

    # palette switcher goes last, after the main behaviour script
    h = sub(h,
            "      b.addEventListener('pointerleave', function(){ b.style.transform = ''; });\n"
            "    });\n"
            "  }\n"
            "})();\n"
            "</script>",
            "      b.addEventListener('pointerleave', function(){ b.style.transform = ''; });\n"
            "    });\n"
            "  }\n"
            "})();\n"
            "</script>\n" + SWITCHER_JS.rstrip(),
            1, "switcher js")

    return h
