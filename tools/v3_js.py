#!/usr/bin/env python3
"""Script layer of the v3 build. Imported by tools/apply_v3.py.

  markup 18  the map filter behaves the way Tyler specified on 8 September:
             everything is on at rest, the first chip click isolates that
             category, further clicks add categories, All restores everything
  markup 21  the bedroom filter keeps working against the retyped plan cards
  markup 8   the map site marker carries 1521
             the palette switcher drops to A and B, default B
  plus a null guard on the hero canvas so the same script survives on the
  register page, which runs a single still instead of the two-image cycle
"""

# --------------------------------------------------------------------------
#  Map filter (markup 18)
# --------------------------------------------------------------------------

OLD_MAPFILTER = '''  document.querySelectorAll('#mapfilter .chip').forEach(function(ch){
    var cat = ch.dataset.cat;
    var n = (data.pois[cat] || []).length;
    ch.querySelector('span').textContent = n;
    ch.addEventListener('click', function(){
      ch.classList.toggle('on');
      var on = ch.classList.contains('on');
      markers.forEach(function(m){
        if(m.g.dataset && m.g.dataset.cat === cat) m.g.classList.toggle('dim', !on);
      });
    });
  });'''

NEW_MAPFILTER = '''  /* ---- Category filter, markup 18 -------------------------------------
     Spec from the call of 8 September. The map rests with every category
     on. The first click on a category chip drops everything else and shows
     that category alone. Clicking further chips adds them. Clicking a lit
     chip removes it, and clearing the last one falls back to all. The All
     chip restores everything at any point. ------------------------------ */
  (function(){
    var chips = [].slice.call(document.querySelectorAll('#mapfilter .chip'));
    var allChip = null, cats = [];
    var selected = null;   /* null means "resting, everything on" */

    chips.forEach(function(ch){
      var cat = ch.dataset.cat;
      if(cat === 'all'){ allChip = ch; return; }
      cats.push(cat);
      var n = (data.pois[cat] || []).length;
      ch.querySelector('span').textContent = n;
    });
    if(allChip){
      var total = cats.reduce(function(s, c){ return s + (data.pois[c] || []).length; }, 0);
      allChip.querySelector('span').textContent = total;
    }

    function paint(){
      var resting = selected === null;
      markers.forEach(function(m){
        if(!m.g.dataset || !m.g.dataset.cat) return;
        var on = resting || selected.indexOf(m.g.dataset.cat) !== -1;
        m.g.classList.toggle('dim', !on);
      });
      chips.forEach(function(ch){
        var cat = ch.dataset.cat;
        var lit = cat === 'all' ? resting : (resting || selected.indexOf(cat) !== -1);
        ch.classList.toggle('on', lit);
        ch.setAttribute('aria-pressed', lit ? 'true' : 'false');
      });
    }

    chips.forEach(function(ch){
      ch.addEventListener('click', function(){
        var cat = ch.dataset.cat;
        if(cat === 'all'){ selected = null; paint(); return; }
        if(selected === null){
          /* first click out of rest: this category only */
          selected = [cat];
        } else {
          var i = selected.indexOf(cat);
          if(i === -1) selected.push(cat);
          else selected.splice(i, 1);
          if(!selected.length) selected = null;
        }
        paint();
      });
    });
    paint();
  })();'''


# --------------------------------------------------------------------------
#  Site marker and palette switcher
# --------------------------------------------------------------------------

OLD_MARKER_TEXT = "  el('text', {y:6}, sm).textContent = '501';"
NEW_MARKER_TEXT = "  el('text', {y:5}, sm).textContent = '1521';"

OLD_SWITCHER = '''/* Palette switcher. Four deep-colour options from the BSaR branding PDF,
   default C (Pantone Deep Purple 2617 C). Choice is remembered per browser. */
(function(){
  var KEY = 'the501_palette';
  var VALID = {A:1, B:1, C:1, D:1};'''

NEW_SWITCHER = '''/* Palette switcher. The two blues from the BSaR branding PDF, default B
   (Pantone Blue 072 C). The purple options came out on 10 September.
   Choice is remembered per browser. */
(function(){
  var KEY = 'q1521_palette';
  var VALID = {A:1, B:1};'''

OLD_SWITCHER_SET = '''  function set(p, persist){
    if(!VALID[p]) p = 'C';'''
NEW_SWITCHER_SET = '''  function set(p, persist){
    if(!VALID[p]) p = 'B';'''

OLD_SWITCHER_INIT = "  set(saved || 'C', false);"
NEW_SWITCHER_INIT = "  set(saved || 'B', false);"


# --------------------------------------------------------------------------
#  Hero canvas guard: the register page runs a single still
# --------------------------------------------------------------------------

OLD_HERO_GUARD = '''  function startHero(){
    if(reduced || !cv.getContext) return;'''
NEW_HERO_GUARD = '''  function startHero(){
    if(!cv || !imgs[0] || !imgs[1]) return;
    if(reduced || !cv.getContext) return;'''


# --------------------------------------------------------------------------
#  Bedroom filter label set: the plans are typed now, not named
# --------------------------------------------------------------------------

OLD_BEDLABEL = '''    var LABEL = {all:'floor plan types', studio:'studio floor plans',
                 '1':'one bedroom floor plans', '2':'two bedroom floor plans',
                 '3':'three bedroom floor plans'};'''
NEW_BEDLABEL = '''    var LABEL = {all:'floor plan types', studio:'studio floor plan types',
                 '1':'one bedroom floor plan types', '2':'two bedroom floor plan types',
                 '3':'three bedroom floor plan types'};'''


def run(h, sub, resub, cut_block):
    h = sub(h, OLD_MAPFILTER, NEW_MAPFILTER, 1, "map filter behaviour, markup 18")
    h = sub(h, OLD_MARKER_TEXT, NEW_MARKER_TEXT, 1, "map site marker, markup 8")
    h = sub(h, OLD_SWITCHER, NEW_SWITCHER, 1, "palette switcher header")
    h = sub(h, OLD_SWITCHER_SET, NEW_SWITCHER_SET, 1, "palette default B")
    h = sub(h, OLD_SWITCHER_INIT, NEW_SWITCHER_INIT, 1, "palette init B")
    h = sub(h, OLD_HERO_GUARD, NEW_HERO_GUARD, 1, "hero canvas guard")
    h = sub(h, OLD_BEDLABEL, NEW_BEDLABEL, 1, "bedroom filter labels")
    return h
