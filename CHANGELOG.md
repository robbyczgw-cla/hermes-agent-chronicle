# Changelog

All notable changes to this skill are documented here.

## Unreleased

### Added

- Added optional Topic Monitor context input with a strict relevance rule: include monitor events only if they changed priorities, spawned action, contradicted assumptions, or became a continuity thread.
- Added Diary vs Operational Memory separation so daily entries do not become config dumps or pseudo-skills.
- Added Source Attribution Footer for daily entries to prevent invented continuity and make confidence explicit.
- Added Quality Gates Before Saving for diary entries.
- Added `threads.md` to the storage layout and a Continuity Threads workflow for multi-day arcs.
- Added Monthly Synthesis guidance beyond raw PDF compilation.
- Added portable `references/context-gathering.md` for source selection and cross-agent context rules.

### Changed

- Reframed the skill around the active cron-prompt-driven workflow while keeping legacy scripts as reference-only.

### Privacy

- Public docs use generic cross-agent context wording. They intentionally avoid private hostnames, Tailscale IPs, chat IDs, credentials, and local installation-specific paths.
