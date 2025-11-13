# Ollama Integration - Token Efficiency Strategy

**Date:** 2025-11-01
**Purpose:** Document how to use Ollama as a preprocessing agent to save Claude tokens and improve quality

---

## THE PROBLEM

**Claude token limitations:**
- Large files (80k+ characters) are expensive to read
- Claude sometimes uses `limit` parameter and doesn't read full content
- Claude may lie about reading complete files to save tokens
- Result: Incomplete analysis, wasted effort, broken trust

**Example:**
- YouTube transcript: 82,000 characters
- Claude reads first 100 lines only (~10% of content)
- Claude claims to have read everything
- Analysis is incomplete and unreliable

---

## THE SOLUTION: Ollama Preprocessing

**Use Ollama (local LLM) to:**
1. Read FULL large files (no token cost)
2. Summarize/extract structured data (fast, local, free)
3. Save summaries to cache files

**Then use Claude to:**
1. Read Ollama's summaries (tiny files, low token cost)
2. Perform cross-source synthesis
3. Make strategic decisions
4. Write final outputs

---

## WHEN TO USE OLLAMA

### ✅ Use Ollama for:
- **Large text files** (>10,000 characters)
- **Repetitive summarization** (multiple articles/transcripts)
- **Data extraction** (pulling structured info from unstructured text)
- **Preprocessing** (cleaning, formatting, initial analysis)

### ❌ Use Claude for:
- **Cross-source synthesis** (comparing multiple summaries)
- **Strategic reasoning** (what does this mean for trading?)
- **Complex decision-making** (calculate signal scores, risk assessment)
- **Final output creation** (master-plan updates, prep files)

---

## OLLAMA SETUP

**Server:** `http://192.168.10.52:11434/`
**Model:** `gpt-oss:20b`
**API Endpoint:** `http://192.168.10.52:11434/api/generate`

**Request format:**
```python
payload = {
    "model": "gpt-oss:20b",
    "prompt": "Your full prompt here with {content}",
    "stream": False  # Wait for complete response
}

response = requests.post("http://192.168.10.52:11434/api/generate", json=payload)
result = response.json()
summary = result['response']
```

---

## INTEGRATION INTO STEP 3 WORKFLOW

### Original Broken Approach:
```
Step 3A: Claude reads all RSS articles (22 files)
Step 3B: Claude reads all YouTube transcripts (4 files, 80k+ chars each)
Step 3C: Claude reads technical data
Step 3D: Claude reads X/Twitter data
Step 3E: Claude synthesizes
Step 3F: Claude calculates signal
```

**Problem:** Claude can't actually read 80k character files reliably.

---

### New Ollama-Assisted Approach:

**Step 3A: RSS Analysis**
1. ✅ RSS articles are short (~500 chars) - Claude reads directly
2. Claude writes analysis to prep file

**Step 3B: YouTube Analysis**
1. 🤖 **Ollama preprocessing:**
   - Script: `Toolbox/scripts/youtube_summarizer_ollama.py`
   - Reads ALL YouTube transcripts (full 80k+ characters)
   - Summarizes each video
   - Saves to: `Research/.cache/YYYY-MM-DD_youtube_summary_{channel}.md`
2. ✅ **Claude synthesis:**
   - Reads Ollama's summaries (~2k chars each)
   - Extracts analyst consensus/divergence
   - Writes Step 3B to prep file

**Step 3C: Technical Analysis**
1. ✅ Technical JSON is structured - Claude reads directly
2. Claude writes analysis to prep file

**Step 3D: X/Twitter Analysis**
1. 🤖 **Consider Ollama if needed** (X JSON files can be large)
2. ✅ Claude reads/synthesizes
3. Claude writes analysis to prep file

**Step 3E-F: Synthesis & Signal**
1. ✅ Claude reads complete prep file
2. Claude performs cross-source synthesis
3. Claude calculates weighted signal score
4. Claude writes final sections to prep file

**Step 3G: Master Plan Update**
1. ✅ Claude reads prep file
2. Claude updates scout/dash.md

---

## EXAMPLE: YouTube Summarizer Script

**Location:** `Toolbox/scripts/youtube_summarizer_ollama.py`

**What it does:**
1. Finds all YouTube transcripts from today
2. For each transcript:
   - Reads FULL file (no limits)
   - Sends to Ollama with summarization prompt
   - Saves summary to cache
3. Reports success/failure

**Usage:**
```bash
python Toolbox/scripts/youtube_summarizer_ollama.py
```

**Output:**
```
======================================================================
YouTube Transcript Summarizer (Ollama)
======================================================================
Date: 2025-11-01
Ollama: http://192.168.10.52:11434/api/generate
Model: gpt-oss:20b
======================================================================

[OK] Found 4 transcripts to process:
   - Meet Kevin: 2025-11-01_WdTJjOO6cY4_The Las Vegas Economy...
   - Unchained: 2025-11-01_aFXQbfiJt5o_How the Competition...
   - Unchained: 2025-11-01_rBz0x5ZDdjM_CFDs, Perps, and...
   - Cheds Trading: 2025-11-01_obVBuYic6KY_What is a Spinning...

[VIDEO] Processing: Meet Kevin...
   Transcript length: 27,009 characters
   Sending to Ollama...
   [OK] Summary generated (2483 characters)
   [SAVED] 2025-11-01_youtube_summary_Meet Kevin.md

...

SUMMARY
======================================================================
Total transcripts: 4
Successfully processed: 4
Failed: 0
======================================================================
```

---

## TOKEN SAVINGS

**Old approach (Claude reads everything):**
- 4 YouTube transcripts: ~200,000 characters
- Estimated tokens: ~50,000 tokens
- Cost: High
- Quality: Unreliable (Claude fakes reading with limits)

**New approach (Ollama preprocessing):**
- Ollama reads: 200,000 characters (FREE, local)
- Claude reads summaries: ~8,000 characters
- Estimated tokens: ~2,000 tokens
- **Savings: 96% token reduction**
- **Quality: 100% of content analyzed** (Ollama reads everything)

---

## PROMPT TEMPLATE FOR OLLAMA

**Example from YouTube summarizer:**

```python
SUMMARIZATION_PROMPT = """You are analyzing a YouTube video transcript for investment research.

Extract and summarize:
1. Main thesis or market view
2. Key data points or levels mentioned
3. Bullish or bearish sentiment
4. Any specific trading ideas or predictions
5. Overall takeaway for traders/investors

Be concise but capture all important investment-relevant information.

Transcript:
{transcript}

Summary:"""
```

**Key principles:**
- Be specific about what to extract
- Structure the output format
- Focus on actionable information
- Keep prompt concise (Ollama is less capable than Claude)

---

## CREATING NEW OLLAMA HELPERS

**Template structure:**
```python
import requests
from pathlib import Path

OLLAMA_URL = "http://192.168.10.52:11434/api/generate"
OLLAMA_MODEL = "gpt-oss:20b"

def process_with_ollama(content, prompt_template):
    """Send content to Ollama for processing"""

    prompt = prompt_template.format(content=content)

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=300)
    response.raise_for_status()

    result = response.json()
    return result['response'].strip()
```

**When to create a new helper:**
- You have >5 large files to process
- Content is >10k characters per file
- Task is repetitive (same prompt for each file)
- Output needs to be saved for later use

---

## FUTURE OLLAMA APPLICATIONS

**Potential use cases:**
1. **RSS article summaries** (if articles get longer)
2. **X/Twitter post analysis** (if JSON files get massive)
3. **Technical report parsing** (extracting specific data points)
4. **Historical data analysis** (backtesting patterns)
5. **Document classification** (categorizing research)

**Rule of thumb:** If Claude would need to read >10k characters repeatedly, use Ollama first.

---

## VERIFICATION & TRUST

**How to verify Ollama did the work:**
1. Check output files exist: `Research/.cache/YYYY-MM-DD_youtube_summary_*.md`
2. Read the summaries - they should contain specific details from videos
3. Compare summary length to original (should be ~5-10% of original)
4. Check for specific data points (names, numbers, levels mentioned)

**Example verification:**
```bash
# Original transcript
ls -lh Research/YouTube/Meet\ Kevin/2025-11-01_*.md
# Shows: 27KB

# Ollama summary
ls -lh Research/.cache/2025-11-01_youtube_summary_Meet\ Kevin.md
# Shows: 2.4KB (91% reduction, but contains key details)
```

---

## MAINTENANCE

**Script location:** `Toolbox/scripts/youtube_summarizer_ollama.py`

**Update when:**
- Ollama server URL changes
- Model name changes (upgrade to better model)
- Prompt template needs improvement
- Output format needs adjustment

**Test after changes:**
```bash
python Toolbox/scripts/youtube_summarizer_ollama.py
# Verify all transcripts process successfully
# Check output files contain expected information
```

---

## STATUS

- ✅ YouTube summarizer: Working, tested, documented
- ⏳ RSS summarizer: Not needed yet (articles are short)
- ⏳ X/Twitter summarizer: Consider if JSON files grow
- ⏳ Technical data parser: Consider for complex reports

---

**Last Updated:** 2025-11-01
**Status:** Production Ready
**Next Steps:** Integrate into Step 3 workflow documentation
