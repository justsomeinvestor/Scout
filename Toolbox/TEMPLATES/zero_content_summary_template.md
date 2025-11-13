# Zero Content Summary Template

Use this template when a scraper runs successfully but finds zero new content (items_found=0 with ran=true).

---

## Template: [Source] Daily Summary

```markdown
# [Source] Summary — [YYYY-MM-DD]

**Status:** Scraper ran successfully
**Content Found:** 0 new items
**Data Source:** [X / YouTube / RSS / etc]
**Collection Time:** [HH:MM UTC]

---

## Summary

No new content from [Source] on [DATE].

### Possible Reasons
- **[SOURCE SPECIFIC]**: Typical weekend/holiday (weekends, major holidays)
- **[SOURCE SPECIFIC]**: Content posted but not yet indexed
- **Scheduled Maintenance**: Source may be undergoing updates

### What This Means
- ✅ Scraper ran successfully
- ✅ Data source is accessible
- ✅ No new content available for analysis
- This is **normal** and **not an error**

---

## Next Steps

Proceed with workflow:
- [ ] Continue to next data source
- [ ] Monitor for content availability tomorrow
- [ ] No action needed - no new content to process

---

**Source:** Auto-generated zero-content summary
**Generated:** [TIMESTAMP]
**Status Check:** Verified via scraper_status_[DATE].json
```

---

## Specific Examples by Source

### YouTube Template (Zero Videos)

```markdown
# YouTube Summary — 2025-10-27

**Status:** Scraper ran successfully
**Videos Found:** 0 new transcripts
**Channels Checked:** 19

---

## Summary

No new videos were published by tracked YouTube channels on October 27, 2025.

This is typical for weekend dates when creators often don't publish.

### Verification
- ✅ All 19 channels were scanned
- ✅ Cached videos were identified and skipped
- ✅ No new uploads found

---

## Recommendation

Proceed with next data source. Recheck Monday morning for weekend uploads.
```

### X/Twitter Lists (Zero Posts)

```markdown
# X Crypto List Summary — 2025-10-27

**Status:** Scraper ran successfully
**Posts Found:** 0 new posts
**List:** Crypto Traders
**Scroll Depth:** 150 posts checked

---

## Summary

No new posts from tracked crypto traders during the 24-hour collection window.

Possible reasons:
- Weekend (creators often post less)
- Major content already processed
- List members inactive today

### Verification
- ✅ Scraper scrolled 150+ posts
- ✅ Deduplication confirmed no missed content
- ✅ Previous session posts already archived

---

## Recommendation

Proceed with next list. No analysis needed - no new data available.
```

### RSS (Zero Articles)

```markdown
# Federal Reserve RSS Summary — 2025-10-27

**Status:** Scraper ran successfully
**Articles Found:** 0 new
**Feed:** Federal Reserve Announcements
**Feed Status:** ✅ Accessible

---

## Summary

Federal Reserve published no new announcements, press releases, or speeches on October 27, 2025.

This is typical for weekends when Fed does not typically publish.

---

## Recommendation

Proceed with next RSS provider. Monitor Monday for weekly publications.
```

---

## Rules for Zero-Content Summaries

### DO:
✅ Create the summary file (don't skip)
✅ Note that scraper ran successfully
✅ Mention zero items found
✅ Explain this is normal
✅ Specify collection parameters (channels checked, time period, etc)
✅ Proceed with workflow

### DON'T:
❌ Treat zero items as scraper failure
❌ Retry the scraper unnecessarily
❌ Skip the summary file
❌ Panic or report error
❌ Question if status is wrong
❌ Delete or manually edit the status file

---

## Verification

Before creating a zero-content summary, **always verify via status file**:

```python
# Pseudo-code
if status["ran"] == true and status["items_found"] == 0:
    # ✅ CORRECT - Create summary
    create_zero_content_summary()
else if status["ran"] == false:
    # ❌ WRONG - This is an error, not zero content
    stop_and_report_error()
```

---

**Version:** 1.0
**Created:** 2025-10-27
**Foolproof:** Yes, use decision tree from SCRAPER_STATUS_GUIDE.md
