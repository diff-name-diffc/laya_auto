"""Observer: turn a live page into the element table the decision model consumes.

Mirrors jev-ultrafast's ``snapshot.js`` semantics on top of Playwright-compatible
pages (spec §3.1/§3.2), with three extensions over the reference implementation:

* **L1 signals** (spec §2.1/§2.4 trigger ②): per-observation structural stats --
  element counts, unlabeled share, in-viewport counts -- plus a ``suspicious``
  flag. These are recorded in the trajectory and are the hook points for the
  optional VLM side path (not implemented; invariant: the main path never waits).
* **Challenge detection** (trigger ④): known bot-wall signatures are detected in
  the same single ``evaluate`` pass, so the loop can stop a challenged run at
  step 0 instead of burning the budget on captcha elements.
* **``in_viewport`` per element**: feeds the ≤250 action cap with a priority
  (on-screen elements first), which the reference implementation lacked.

Node identity: one stable id per element (``window.__abIds`` WeakMap + expando
property), stable across observations within a document. The id is the cache key
for any side-path enhancement and the anchor the executor resolves back to a
live element -- the model can never name a node that was not observed.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List

from .request_builder import DEFAULT_MAX_ACTIONS, cap_actions
from .validators import marker as _marker

# Runs in the page. Returns a JSON-serialisable observation in one round trip.
# __FLAGS__ is substituted by _observe_js(): {"occluded": bool, "chrome": bool}.
_OBSERVE_TEMPLATE = r"""
(() => {
  const FLAGS = __FLAGS__;
  if (!document.body) return null;
  const cache = window.__abIdsCache ||= {ids: new WeakMap(), next: 1};
  const identity = e => {
    if (!e.__abId) { e.__abId = cache.next++; }
    return e.__abId;
  };
  const safe = e => !['password','file','hidden'].includes((e.type || '').toLowerCase());
  const rectOf = e => e.getBoundingClientRect();
  const visible = e => {
    if (e.closest('[aria-hidden="true"],[inert]')) return false;
    const r = rectOf(e);
    if (r.width <= 0 || r.height <= 0) return false;
    if (r.bottom <= 0 || r.top >= innerHeight || r.right <= 0 || r.left >= innerWidth) return false;
    const s = getComputedStyle(e);
    return s.visibility !== 'hidden' && s.display !== 'none' && s.opacity !== '0';
  };
  const inViewport = e => {
    const r = rectOf(e);
    return r.top >= 0 && r.left >= 0 && r.bottom <= innerHeight && r.right <= innerWidth;
  };
  const SKIP_TAGS = ['STYLE','SCRIPT','NOSCRIPT','TEMPLATE'];
  const nameOf = (e, seen=new Set()) => {
    if (!e || seen.has(e)) return '';
    seen.add(e);
    const ref = (e.getAttribute('aria-labelledby') || '').split(/\s+/)
      .map(id => nameOf(document.getElementById(id), seen)).filter(Boolean).join(' ');
    return (ref || e.getAttribute('aria-label') ||
      [...(e.labels || [])].map(l => nameOf(l, seen)).filter(Boolean).join(' ') ||
      (['button','submit','reset'].includes((e.type||'').toLowerCase()) ? e.value : '') ||
      e.getAttribute('alt') ||
      (e.tagName === 'INPUT' ? '' : [...e.childNodes].map(n =>
        n.nodeType === 3 ? n.textContent :
        (n.nodeType === 1 && !SKIP_TAGS.includes(n.tagName)
         && n.getAttribute('aria-hidden') !== 'true') ? nameOf(n, seen) : ''
      ).join(' ').trim()) ||
      e.getAttribute('title') || e.getAttribute('placeholder') || '').trim().replace(/\s+/g, ' ');
  };
  const ROLES = ['button','link','checkbox','radio','switch','tab','menuitem','option',
                 'combobox','textbox','searchbox','spinbutton'];
  const roleOf = e => {
    const explicit = e.getAttribute('role');
    if (ROLES.includes(explicit)) return explicit;
    const t = e.tagName;
    if (t === 'BUTTON' || t === 'SUMMARY') return 'button';
    if (t === 'A') return e.getAttribute('href') ? 'link' : null;
    if (t === 'SELECT') return 'combobox';
    if (t === 'TEXTAREA' || e.isContentEditable) return 'textbox';
    if (t === 'INPUT') {
      const ty = (e.type || 'text').toLowerCase();
      if (['checkbox','radio'].includes(ty)) return ty;
      if (['button','submit','reset','image'].includes(ty)) return 'button';
      if (ty === 'search') return 'searchbox';
      if (ty === 'number') return 'spinbutton';
      if (['text','email','url','tel'].includes(ty)) return 'textbox';
    }
    return null;
  };
  const SELECTOR = 'a[href],button,input,textarea,select,summary,[contenteditable="true"],'
    + ROLES.map(r => '[role="' + r + '"]').join(',');
  const occluded = e => {
    const r = rectOf(e);
    const hit = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
    return !!hit && hit !== e && !e.contains(hit) && !hit.contains(e);
  };
  const actions = [];
  let nElements = 0, nUnlabeled = 0, nInViewport = 0;
  let nOccluded = 0, nChrome = 0, nAuth = 0;
  for (const e of document.querySelectorAll(SELECTOR)) {
    if (!safe(e) || !visible(e)) continue;
    if (e.matches(':disabled') || e.closest('[aria-disabled="true"]')) continue;
    const role = roleOf(e);
    if (!role) continue;
    // --- dirt filters: keep the candidate table to truly interactive controls
    // landmark chrome (nav/header/footer links) -- flagged, A/B-gated
    if (FLAGS.chrome
        && e.closest('nav,footer,aside,header,[role="navigation"],[role="banner"],[role="contentinfo"]')) {
      nChrome++; continue;
    }
    // dead links: no-ops that can only waste a decision
    if (e.tagName === 'A') {
      const href = e.getAttribute('href') || '';
      if (!href || href === '#' || href.startsWith('javascript:')
          || /^(mailto|tel):/i.test(href)) continue;
    }
    const rawName = nameOf(e);
    // auth-gated controls ("must be signed in to star") -- dead ends without login
    if (/must be signed in|sign in to |log in to /i.test(rawName)) { nAuth++; continue; }
    // covered right now (overlay/consent wall): unclickable this instant;
    // if the overlay is transient the element re-enters on a later observation
    if (FLAGS.occluded && occluded(e)) { nOccluded++; continue; }
    const node = identity(e);
    const label = (rawName || role).slice(0, 120);
    nElements++;
    if (!rawName) nUnlabeled++;
    const onScreen = inViewport(e);
    if (onScreen) nInViewport++;
    const base = {node, label, role, in_viewport: onScreen};
    for (const k of ['checked','selected','expanded']) {
      const v = e.getAttribute('aria-' + k);
      if (v !== null) base[k] = v;
    }
    if (['checkbox','radio'].includes((e.type||'').toLowerCase())) base.checked = String(e.checked);
    if (e.tagName === 'SELECT') {
      const cur = [...e.selectedOptions].map(o => o.label).join(', ');
      for (const o of e.options) {
        if (o.selected || o.disabled) continue;
        actions.push({...base, id: 'select:' + node + ':' + actions.length, kind: 'select',
                      value: o.value, current_value: cur, label: label + ' → ' + o.label});
      }
      continue;
    }
    const editable = !e.readOnly && e.getAttribute('aria-readonly') !== 'true' &&
      (['textbox','searchbox','spinbutton'].includes(role) ||
       (role === 'combobox' && ['INPUT','TEXTAREA'].includes(e.tagName)));
    const value = ('value' in e) ? String(e.value || '') :
      (e.isContentEditable || role === 'combobox') ? (e.innerText || '').trim() : '';
    actions.push({...base, id: (editable ? 'fill:' : 'click:') + node, kind: editable ? 'fill' : 'click',
                  value, current_value: value});
    if (editable) {
      actions.push({...base, id: 'click:' + node + ':open', kind: 'click', value, current_value: value,
                    label: 'Open ' + label});
    }
  }
  // visible text
  const words = [];
  let n, len = 0;
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while ((n = walker.nextNode()) && len < 6000) {
    const v = (n.textContent || '').trim().replace(/\s+/g, ' ');
    const parent = n.parentElement;
    if (!v || !parent || parent.closest('script,style,noscript,template') || !visible(parent)) continue;
    words.push(v); len += v.length;
  }
  const text = words.join('\n').slice(0, 6000);
  const height = document.documentElement.scrollHeight;
  // page-level controls
  actions.push({node: 0, id: 'wait', kind: 'wait', label: 'Wait for the page to update', role: 'wait'});
  if (scrollY + innerHeight < height - 2)
    actions.push({node: 0, id: 'scroll_down', kind: 'scroll', label: 'Scroll down', role: 'scroll', delta: 560});
  if (scrollY > 0)
    actions.push({node: 0, id: 'scroll_up', kind: 'scroll', label: 'Scroll up', role: 'scroll', delta: -560});
  // Submit the focused field. Offered whenever an editable field is present, so
  // submitting a query is a *decision the model makes*, not something the
  // harness does silently.
  const hasEditable = actions.some(a => a.kind === 'fill');
  if (hasEditable)
    actions.push({node: 0, id: 'press_enter', kind: 'enter',
                  label: 'Press Enter to submit the current field', role: 'enter'});
  // challenge detection (trigger ④): known bot-wall signatures
  const head = text.slice(0, 3000).toLowerCase();
  const challengeDom = !!document.querySelector(
    '#challenge-running, #cf-challenge, #cf-challenge-running, #challenge-form, ' +
    '.g-recaptcha, iframe[src*="recaptcha"], iframe[src*="/challenge"], iframe[src*="cdn-cgi"]'
  );
  const challengeUrl = /\/sorry(\/index)?/.test(location.pathname + location.search);
  const challengeText = ['unusual traffic', 'not a robot', 'complete the following challenge',
    'verify you are human', "verify you're human", 'confirm you are human',
    '确认您是真人', '请完成以下验证'].some(s => head.includes(s));
  const challenge = {hit: challengeDom || challengeUrl || challengeText,
                     dom: challengeDom, url: challengeUrl, text: challengeText};
  const semantics = actions.map(a => [a.id, a.kind, a.label, a.value, a.current_value]);
  return {url: location.href, title: document.title, text, actions,
          scroll: {y: scrollY, height}, count: actions.length, semantics,
          stats: {n_elements: nElements, n_unlabeled: nUnlabeled,
                  n_in_viewport: nInViewport, text_len: text.length,
                  n_occluded: nOccluded, n_chrome: nChrome, n_auth: nAuth},
          challenge};
})()
"""


def _observe_js(filter_occluded: bool, filter_chrome: bool) -> str:
    import json as _json
    return _OBSERVE_TEMPLATE.replace(
        "__FLAGS__", _json.dumps({"occluded": bool(filter_occluded),
                                  "chrome": bool(filter_chrome)}))


def observe(page, retries: int = 4, settle_ms: int = 300,
            max_actions: int = DEFAULT_MAX_ACTIONS,
            filter_occluded: bool = True, filter_chrome: bool = False) -> Dict[str, Any]:
    """Observe a page. Returns the observation dict (spec §3.2) with a marker.

    Retries through the two things that make an observation fail on the live
    web: ``document.body`` briefly absent mid-navigation, and a destroyed JS
    execution context during navigation. Waits use ``time.sleep`` (client-side),
    never ``page.wait_for_timeout`` (CDP round trip CloakBrowser advises against).

    Dirt filters (candidates must be truly interactive *right now*):
    ``filter_occluded`` drops elements whose centre is covered by an overlay at
    observation time; ``filter_chrome`` additionally drops landmark navigation
    chrome (nav/header/footer/aside links) -- off by default because it changes
    the candidate distribution the fine-tune was trained on; A/B before arming.
    """
    js = _observe_js(filter_occluded, filter_chrome)
    for attempt in range(retries):
        try:
            raw = page.evaluate(js)
        except Exception:  # noqa: BLE001 -- navigation/context churn
            if attempt == retries - 1:
                raise
            try:
                page.wait_for_load_state("domcontentloaded", timeout=3000)
            except Exception:  # noqa: BLE001
                pass
            time.sleep(settle_ms * (attempt + 1) / 1000.0)
            continue
        if raw is not None:
            raw["_filter"] = {"filter_occluded": filter_occluded,
                              "filter_chrome": filter_chrome}
            return _finalize(raw, max_actions)
        time.sleep(settle_ms * (attempt + 1) / 1000.0)
    raise RuntimeError("page has no body (still navigating?)")


_ELEMENT_KINDS = ("click", "fill", "select")


def _finalize(raw: Dict[str, Any], max_actions: int) -> Dict[str, Any]:
    """Cap the element table (viewport first), compute L1 signals + marker."""
    before = sum(1 for a in raw["actions"] if a.get("kind") in _ELEMENT_KINDS)
    capped = cap_actions(raw["actions"], max_actions)
    raw["actions"] = capped
    raw["dropped"] = max(0, before - sum(1 for a in capped if a.get("kind") in _ELEMENT_KINDS))
    raw["truncated"] = raw["dropped"] > 0
    raw["count"] = len(capped)
    stats = raw.get("stats") or {}
    n_elements = int(stats.get("n_elements") or 0)
    n_unlabeled = int(stats.get("n_unlabeled") or 0)
    text_len = int(stats.get("text_len") or 0)
    # §2.4 trigger ②: structure-suspicion heuristics. Both are cheap and
    # conservative; they arm the (optional) side path, never block the main one.
    suspicious = (
        (0 < n_elements < 3 and text_len > 800)          # big page, nothing interactive
        or (n_elements >= 8 and n_unlabeled / n_elements > 0.5)  # half the UI nameless
    )
    raw["signals"] = {
        "n_elements": n_elements,
        "n_unlabeled": n_unlabeled,
        "n_in_viewport": int(stats.get("n_in_viewport") or 0),
        "text_len": text_len,
        "n_occluded": int(stats.get("n_occluded") or 0),
        "n_chrome": int(stats.get("n_chrome") or 0),
        "n_auth": int(stats.get("n_auth") or 0),
        "suspicious": suspicious,
    }
    ch = raw.get("challenge") or {}
    raw["challenge"] = {"hit": bool(ch.get("hit")), "kind": (
        "url" if ch.get("url") else "dom" if ch.get("dom") else "text" if ch.get("text") else None)}
    raw["marker"] = _marker(raw)
    return raw


def compact_actions(actions: List[Dict[str, Any]], keep_controls: bool = True) -> List[Dict[str, Any]]:
    """Trim an action list for a request (drop page-level controls if asked)."""
    if keep_controls:
        return actions
    return [a for a in actions if a["kind"] in ("click", "fill", "select")]
