# Scraper Status Guide - For AI Operators

**TL;DR:** Check the status file. If scraper "ran" is true but "items_found" is 0, that's NOT an error - it just means no new content published today.

---

## Status File Location

```
Research/.cache/scraper_status_YYYY-MM-DD.json
```

Example: `Research/.cache/scraper_status_2025-10-27.json`

Each scraper writes here on completion. One file per day contains ALL scrapers' status.

---

## Status File Format

```json
{
  "YouTube": {
    "ran": true,
    "items_found": 0,
    "error": null,
    "timestamp": "2025-10-27T10:30:45.123456",
    "message": "No new content found"
  },
  "X_Crypto": {
    "ran": true,
    "items_found": 5,
    "error": null,
    "timestamp": "2025-10-27T10:35:12.654321",
    "message": "Scraper completed successfully"
  },
  "RSS": {
    "ran": false,
    "items_found": 0,
    "error": "Connection timeout after 30 seconds",
    "timestamp": "2025-10-27T10:40:00.987654",
    "message": "Connection timeout after 30 seconds"
  }
}
```

---

## How to Interpret Each Scraper's Status

### Scenario A: Everything Good (Zero Content)

```json
"YouTube": {
  "ran": true,
  "items_found": 0,
  "error": null,
  "message": "No new content found"
}
```

**Meaning:** Scraper ran successfully. YouTube published no new videos today.
**Action:** ✅ PROCEED - This is normal. Create "no new videos" summary file.
**Confidence:** 100% safe to treat as success.

---

### Scenario B: Everything Good (Content Found)

```json
"X_Crypto": {
  "ran": true,
  "items_found": 5,
  "error": null,
  "message": "Scraper completed successfully"
}
```

**Meaning:** Scraper ran successfully. Found 5 new crypto posts.
**Action:** ✅ PROCEED - Create summary with these 5 posts.
**Confidence:** 100% success.

---

### Scenario C: Scraper Failed to Run

```json
"RSS": {
  "ran": false,
  "items_found": 0,
  "error": "Connection timeout after 30 seconds",
  "message": "Connection timeout after 30 seconds"
}
```

**Meaning:** Scraper crashed or never completed.
**Action:** ❌ STOP - This is an error.
- Check network connection
- Check RSS feeds are accessible
- Retry scraper if transient (connection timeout)
- Report if persistent

**Confidence:** 100% this is an ERROR.

---

### Scenario D: Scraper Missing from Status File

```
"Federal_Reserve" is not in the status file at all
```

**Meaning:** This scraper either:
- Never ran
- Was skipped
- Status write failed (very rare, wrapped in try/except)

**Action:** ❌ STOP - This is an error.
- Check scraper started
- Check no permission errors
- Investigate why it's missing

**Confidence:** 99% this is an ERROR.

---

## Decision Tree (Use This!)

```
┌─ Does status file exist for today?
│  ├─ NO → ❌ ERROR: No scraping ran at all
│  └─ YES ↓
├─ Is scraper entry present in status file?
│  ├─ NO → ❌ ERROR: Scraper didn't reach completion
│  └─ YES ↓
├─ Check "ran" field
│  ├─ "ran": false → ❌ ERROR: Scraper crashed/failed
│  └─ "ran": true ↓
└─ Check "items_found"
   ├─ 0 → ✅ OK: No new content today (NORMAL)
   └─ >0 → ✅ OK: Found content (SUCCESS)
```

---

## Code Examples: How to Check Status

### Python - Check if Scraper Ran

```python
import json
from pathlib import Path
from datetime import datetime

status_file = Path("Research/.cache") / f"scraper_status_{datetime.now().strftime('%Y-%m-%d')}.json"

if not status_file.exists():
    print("❌ No scraper status file found - no scraping ran")
    exit(1)

status_data = json.loads(status_file.read_text())

if "YouTube" not in status_data:
    print("❌ YouTube scraper missing from status file")
    exit(1)

youtube_status = status_data["YouTube"]

if not youtube_status["ran"]:
    print(f"❌ YouTube scraper failed: {youtube_status['error']}")
    exit(1)

if youtube_status["items_found"] == 0:
    print("✅ YouTube scraper ran successfully - no new videos today")
    # This is NORMAL - create summary with "no new videos"
else:
    print(f"✅ YouTube found {youtube_status['items_found']} new videos")
    # Process the videos

exit(0)
```

### Bash - Quick Check

```bash
#!/bin/bash
TODAY=$(date +%Y-%m-%d)
STATUS_FILE="Research/.cache/scraper_status_${TODAY}.json"

# Check file exists
if [ ! -f "$STATUS_FILE" ]; then
    echo "❌ Status file missing"
    exit 1
fi

# Check YouTube ran
if grep -q '"YouTube"' "$STATUS_FILE"; then
    RAN=$(grep -A 1 '"YouTube"' "$STATUS_FILE" | grep '"ran"' | grep 'true')
    if [ -n "$RAN" ]; then
        echo "✅ YouTube scraper ran"
    else
        echo "❌ YouTube scraper failed"
        exit 1
    fi
else
    echo "❌ YouTube not found in status"
    exit 1
fi

exit 0
```

---

## What Each Scraper Writes

| Scraper | Status Key | Items Field Meaning |
|---------|-----------|-------------------|
| YouTube | `YouTube` | Number of new transcripts found |
| X Lists | `X_Technicals` | New posts in Technicals list |
| X Lists | `X_Crypto` | New posts in Crypto list |
| X Lists | `X_Macro` | New posts in Macro list |
| X Bookmarks | `X_Bookmarks` | New bookmarked posts |
| RSS | `RSS` | Total articles found across all feeds |
| Bookmarks (standalone) | `Bookmarks` | Bookmarked posts from X |

---

## Foolproof Guarantees

✅ **Status write never breaks the scraper**
- Wrapped in try/except
- If status write fails, scraper still succeeds
- Status is bonus clarity, not required for scraper function

✅ **Zero content (0 items) is valid**
- Not distinguished from error
- Must check `"ran": true` to verify success
- If `ran=true` and items=0: normal, proceed
- If `ran=false` and items=0: error, stop

✅ **Backward compatible**
- Existing verification scripts work with OR without status file
- Status file is additive enhancement

---

## Common Questions

**Q: How do I know if "0 items" means "nothing published" vs "scraper failed"?**
A: Check the `"ran"` field. If `"ran": true`, scraper succeeded (nothing published). If `"ran": false`, scraper failed.

**Q: What if status file doesn't exist?**
A: No scraping ran at all. This is an ERROR. Stop and investigate.

**Q: What if scraper entry is missing?**
A: Scraper didn't complete (possible crash during execution). This is an ERROR. Stop and investigate.

**Q: Should I retry if a scraper failed?**
A: Yes for transient errors (timeouts, network). No for permission errors (will fail again). Check error message in status file.

**Q: Can I edit the status file manually?**
A: No. Status files are auto-generated. Editing breaks the system. Always use the scraper to generate status.

**Q: What if I'm not sure?**
A: Follow the decision tree above. If still unsure, STOP and report the status. Don't guess.

---

## Status Write Behavior

Each scraper:
1. Runs its collection logic
2. Records how many items found
3. Writes status file with: `ran=true, items_found=X`
4. If crashes during execution: `ran=false, error=exception message`

Status file is ALWAYS written (unless filesystem is down - rare).

---

**Version:** 1.0
**Last Updated:** 2025-10-27
**Foolproof Level:** Maximum (verified with decision tree)
