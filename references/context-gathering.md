# Context Gathering Reference

The diary cron gathers context from available sources before writing. Keep this reference portable: no private hostnames, IPs, usernames, chat IDs, or local absolute paths that only exist on one installation.

## Source List

1. Daily summary for the current local date — what happened, what was fixed.
2. Yesterday's diary entry — continuity and follow-up threads.
3. Agent identity/voice reference — tone and perspective guardrails.
4. Recent cron outputs/prompts — what scheduled jobs ran today.
5. Optional cross-agent shared status file or SSH target — ecosystem state from sibling agents.
6. Optional Topic Monitor context — only alerts that changed priorities, spawned action, contradicted assumptions, or became a continuity thread.

## Cross-Agent Context Rules

- Configure the shared status location in the local cron prompt or environment, not in the public skill doc.
- Use a short timeout for remote reads and skip gracefully if unavailable.
- Read a bounded amount of text, then summarize; do not paste full remote state into the diary.
- Treat sibling-agent context as background. The diary remains this agent's perspective, not a copy of another agent's notes.

## Notes

- Missing daily summaries or previous diary files are normal. Lower confidence instead of inventing continuity.
- Recent cron context should be summarized by effect, not copied as raw logs.
- Topic Monitor digests are not diary material unless they changed priorities or created an action thread.
