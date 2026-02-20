# Step 17 — LinkedIn Final Selector Fix

**Date:** 2026-02-18
**Status:** Implemented

## Problem

The step 16 role-based selectors (`get_by_role("button", name="Start a post")`)
were still failing because LinkedIn's "Start a post" element is not always
rendered as a `<button>` — it can be a `<div>`, `<span>`, or other element
depending on the LinkedIn frontend version.

## Fix

### 1. Smart wait before clicking

```python
page.wait_for_selector("text=Start a post", timeout=15000)
```

This ensures the text is visible in the DOM before attempting to click,
regardless of what HTML element wraps it.

### 2. Text-based selector as primary

```python
page.get_by_text("Start a post")
```

Matches by visible text content — works regardless of the underlying
HTML element type (`<button>`, `<div>`, `<span>`, etc.).

### 3. Fallback selectors

```python
page.locator("div.share-box-feed-entry__trigger")
page.locator("button[aria-label*='Start a post']")
```

CSS class and ARIA attribute selectors kept as fallbacks via `.or_()`.

### 4. Visual debugging confirmed

`headless=False` was already set (line 57), so the browser window is
visible for observing mouse movement and click targets.

## Selector Priority (most to least robust)

| Priority | Selector | Why |
|----------|----------|-----|
| 1 | `get_by_text("Start a post")` | Matches visible text, element-agnostic |
| 2 | `div.share-box-feed-entry__trigger` | CSS class fallback |
| 3 | `button[aria-label*="Start a post"]` | ARIA attribute fallback |

## Files Modified

| File | Change |
|------|--------|
| `linkedin_poster.py:158-169` | Replaced role-based selectors with text-based + smart wait |
