"""Browser observer: turn a live page into the element table Laya consumes.

The output is the same ``actions`` list that ``benchmark.browser_request``
expects, so an observation from a real page becomes a Laya request with no
adapter in between:

    {"id", "kind": "click"|"fill"|"select"|"wait"|"scroll",
     "label", "role", "node", "value"?, "current_value"?}

This mirrors jev-ultrafast's ``snapshot.js`` semantics, reimplemented on top of
Playwright so the loop is fully scriptable:

* only visible, enabled, non-covered interactive elements;
* one node per element, stable across observations via a JS-side id map;
* a ``marker`` (semantic hash) for staleness detection, not DOM mutation count,
  because animations change the DOM constantly and would invalidate every
  decision.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List

# Runs in the page. Returns a JSON-serialisable observation.
_OBSERVE_JS = r"""
(() => {
  if (!document.body) return null;
  const cache = window.__e2e ||= {ids: new WeakMap(), next: 1};
  const identity = e => {
    if (!e.__e2eId) { e.__e2eId = cache.next++; }
    return e.__e2eId;
  };
  const safe = e => !['password','file','hidden'].includes((e.type || '').toLowerCase());
  const visible = e => {
    if (e.closest('[aria-hidden="true"],[inert]')) return false;
    const r = e.getBoundingClientRect();
    if (r.width <= 0 || r.height <= 0) return false;
    if (r.bottom <= 0 || r.top >= innerHeight || r.right <= 0 || r.left >= innerWidth) return false;
    const s = getComputedStyle(e);
    return s.visibility !== 'hidden' && s.display !== 'none' && s.opacity !== '0';
  };
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
        n.nodeType === 1 && n.getAttribute('aria-hidden') !== 'true' ? nameOf(n, seen) : ''
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
  const actions = [];
  for (const e of document.querySelectorAll(SELECTOR)) {
    if (!safe(e) || !visible(e)) continue;
    if (e.matches(':disabled') || e.closest('[aria-disabled="true"]')) continue;
    const role = roleOf(e);
    if (!role) continue;
    const node = identity(e);
    const label = (nameOf(e) || role).slice(0, 120);
    const base = {node, label, role};
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
  const words = [], walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n, len = 0;
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
  // harness does silently. Without it a filled search box would have no way to
  // fire, and adding it implicitly would remove a real decision from the score.
  const hasEditable = actions.some(a => a.kind === 'fill');
  if (hasEditable)
    actions.push({node: 0, id: 'press_enter', kind: 'enter',
                  label: 'Press Enter to submit the current field', role: 'enter'});
  const semantics = actions.map(a => [a.id, a.kind, a.label, a.value, a.current_value]);
  return {url: location.href, title: document.title, text, actions,
          scroll: {y: scrollY, height}, count: actions.length, semantics};
})()
"""


def observe(page, retries: int = 4, settle_ms: int = 300) -> Dict[str, Any]:
    """Observe a Playwright page. Returns a page dict for the request builder.

    Retries through the two things that make an observation fail on the live web:

    * ``document.body`` is briefly absent mid-navigation;
    * clicking a link destroys the JS execution context, so ``evaluate`` raises
      ("Execution context was destroyed") rather than returning. Real Chrome
      navigations make this common, so it is retried, not treated as fatal.
    """
    for attempt in range(retries):
        try:
            raw = page.evaluate(_OBSERVE_JS)
        except Exception as exc:  # noqa: BLE001 -- navigation/context churn
            if attempt == retries - 1:
                raise
            try:
                page.wait_for_load_state("domcontentloaded", timeout=3000)
            except Exception:  # noqa: BLE001
                pass
            page.wait_for_timeout(settle_ms * (attempt + 1))
            continue
        if raw is not None:
            raw["marker"] = _marker(raw)
            return raw
        page.wait_for_timeout(settle_ms * (attempt + 1))
    raise RuntimeError("page has no body (still navigating?)")


def _marker(obs: Dict[str, Any]) -> str:
    """Semantic fingerprint: url + text + element semantics (no geometry)."""
    payload = {
        "url": obs["url"],
        "title": obs["title"],
        "text": obs["text"],
        "semantics": obs["semantics"],
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:32]


def compact_actions(actions: List[Dict[str, Any]], keep_controls: bool = True) -> List[Dict[str, Any]]:
    """Trim an action list for a request (drop page-level controls if asked)."""
    if keep_controls:
        return actions
    return [a for a in actions if a["kind"] in ("click", "fill", "select")]
