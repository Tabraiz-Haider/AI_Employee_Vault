# Step 17 — LinkedIn Victory Lap (Final Selector + Audit)

**Date:** 2026-02-18
**Status:** Implemented

## Changes

### 1. Robust selector chain for "Start a post"

```python
page.wait_for_selector("text=Start a post", timeout=15000)  # smart wait
start_post_btn = page.get_by_text("Start a post")           # text match
    .or_(page.get_by_role("button", name="Start a post"))   # role match
    .or_(page.locator("div.share-box-feed-entry__trigger")) # CSS fallback
    .or_(page.locator("button[aria-label*='Start a post']"))# ARIA fallback
```

Priority order: text content > ARIA role > CSS class > aria-label attribute.

### 2. Visual debugging

`headless=False` confirmed active — browser window is visible during
the entire automation so you can watch the mouse movement and clicks.

### 3. Post confirmation delay

```python
time.sleep(5)
```

After clicking Post, the browser stays open for 5 seconds so you can
see LinkedIn's "Post successful" confirmation popup.

### 4. Audit screenshot

```python
page.screenshot(path="post_confirmation.png")
```

Captures the browser state immediately after posting. Saved to
`post_confirmation.png` in the vault root as proof for audit trail.

## Files Modified

| File | Change |
|------|--------|
| `linkedin_poster.py` | Added role selector to chain, `time.sleep(5)` after Post click, `page.screenshot()` for audit |
| `.gitignore` | Added `post_confirmation.png` to ignored files |

## Previous step17 doc

`step17_linkedin_final_selector_fix.md` covered the initial text-based
selector switch. This doc covers the final additions (role fallback,
sleep for visual confirmation, screenshot audit).
