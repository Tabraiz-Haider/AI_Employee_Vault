# Step 16 — LinkedIn Selector Fix

**Date:** 2026-02-18
**Status:** Implemented

## Problem

`linkedin_poster.py` was timing out trying to find the "Start a post" button.
The CSS-class-based selectors (`button.share-box-feed-entry__trigger`) were
brittle and broke when LinkedIn updated its DOM.

## Root Cause

- LinkedIn frequently changes CSS class names in its frontend.
- The page wasn't fully loaded before selector search began.
- 15s timeout was too short on slower connections.

## Fix

### 1. Added `networkidle` wait before interacting

```python
page.wait_for_load_state("networkidle", timeout=30000)
```

Ensures all network requests have settled before looking for elements.

### 2. Switched to role-based + text-based selectors (primary)

```python
page.get_by_role("button", name="Start a post")
page.get_by_role("textbox", name="Text editor")
page.get_by_role("button", name="Post", exact=True)
```

Role-based selectors are more resilient to DOM changes because they match
on ARIA roles and accessible names rather than CSS classes.

### 3. Kept CSS selectors as fallbacks via `.or_()`

The old CSS-class selectors are chained as fallbacks so the script works
across different LinkedIn frontend versions.

### 4. Increased timeouts to 30s

All element interaction timeouts raised from 15s to 30s to handle slow
page loads.

## Files Modified

| File | Change |
|------|--------|
| `linkedin_poster.py` | Updated selectors + added networkidle wait + 30s timeouts |
