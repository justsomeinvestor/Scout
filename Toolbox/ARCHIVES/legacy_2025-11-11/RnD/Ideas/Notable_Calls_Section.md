# Notable Calls Section (Parked)

Idea: Surface high-conviction, time-boxed calls from Tier 1/2 influencers on X within the X Sentiment tab.

Why it could be valuable
- Adds context that raw sentiment can’t (thesis, triggers, invalidation, timeframe)
- Helps bridge quant signals and discretionary judgement

Inclusion criteria
- Source on Tier 1/2 whitelist
- Each item includes at least one: explicit trigger/level, timeframe, or risk control
- Fresh (<48h) or still active

Display spec
- Compact list beneath Sentiment Breakdown
- Format: "[timestamp] source — thesis | trigger | invalidation"
- Collapsible when many items; hide section if empty

Implementation notes
- Data source: front matter `xsentiment.influencer_consensus.notable_calls` (array of strings)
- Renderer should guard against empty/null values

Status: removed from UI for simplicity (Oct 14, 2025). Can be re-enabled if we start curating inputs.
