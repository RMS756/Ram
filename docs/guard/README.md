# REM Claude Code Guard Package

Place `CLAUDE.md` at the repository root.

Use `START_PROMPT.md` as the first prompt in the Claude Code session.

Purpose: force fail-closed behavior whenever the thesis specification is missing, conflicting, unverified, or unapproved.

The guard does not control Claude externally; it constrains the instructions Claude Code receives and the implementation behavior expected from the repository.
