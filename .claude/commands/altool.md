---
description: Run Altool local project workflow commands in Claude Code (setup, research, oneshot, freedom, plan, spec, run, analyze, fix, browser, report, status, etc.)
argument-hint: <command> [arguments]
---

# Altool Local Workflow

You are running the Altool local project workflow. Altool commands are repo-local and must operate from the current project root.

The user invoked: `/altool $ARGUMENTS`

Parse `$ARGUMENTS`: the first token is the Altool `<command>`, and any remaining text is that command's arguments. Map the command to the corresponding file/script below and **read that file before acting**. If `$ARGUMENTS` is empty or the command is unknown, show the supported `/altool` command list.

## Command Routing

| User command | Step file / action |
| --- | --- |
| `/altool setup` | `altool/steps/setup.md` |
| `/altool research <topic>` | `altool/steps/research.md` |
| `/altool oneshot <feature description>` | `altool/steps/oneshot.md` |
| `/altool freedom <goal> --loops N` | `altool/steps/freedom.md` |
| `python altool/scripts/freedom_loop.py <goal> --loops N` | Freedom control-plane smoke runner |
| `/altool say <text>` | `python altool/scripts/radio.py say <text>` |
| `/altool ask <text>` | `python altool/scripts/radio.py ask <text>` |
| `/altool pause` | `python altool/scripts/radio.py pause` |
| `/altool resume` | `python altool/scripts/radio.py resume` |
| `/altool stop` | `python altool/scripts/radio.py stop` |
| `/altool outbox` | `python altool/scripts/radio.py outbox` |
| `/altool guide` | `altool/steps/guide.md` |
| `/altool design_source` | `altool/steps/design_source.md` |
| `/altool lesson [text]` | `altool/steps/lesson.md` |
| `/altool plan <feature description>` | `altool/steps/plan.md` |
| `/altool spec [instructions]` | `altool/steps/spec.md` |
| `/altool run [instructions]` | `altool/steps/run.md` |
| `/altool analyze [instructions]` | `altool/steps/analyze.md` |
| `/altool fix [instructions]` | `altool/steps/fix.md` |
| `/altool browser [instructions]` | `altool/steps/browser.md` |
| `/altool report [instructions]` | `altool/steps/report.md` |
| `/altool status` | `altool/steps/status.md` |

## Rules

1. Read the project root `CLAUDE.md` and the matching `altool/steps/*.md` file before executing a command.
2. This command and the matching step file are the complete runtime instructions for the command.
3. Keep workflow state and reports inside the current project, especially `.altool/` and `docs/`.
4. Store lesson events with `python altool/scripts/lesson.py append` only for code errors, implementation gaps, and their fixes during `/altool lesson`, run/analyze/fix/browser implementation, verification work, or natural-language code fix requests. Research/plan/spec/report are document-only steps and must not append lesson events.
5. Run `python altool/scripts/lesson.py search` before `/altool run`, `/altool analyze`, `/altool fix`, and `/altool browser`. Natural-language code fix requests do not require pre-fix lesson search; append only after an actual code error or implementation gap is fixed.
6. At the end of every Altool command, write `.altool/checks/{feature}.{step}.json`, run `python altool/scripts/check.py validate --json ...`, and report the Step Check summary including skipped reasons.
7. If any Altool-owned document is created or modified, refresh and validate that document's owning Step Check before completing the current command. For example, edits to `docs/01-plan/**/*.plan.md` require `.altool/checks/{feature}.plan.json`, edits to `docs/02-spec/**/*.spec.md` require `{feature}.spec.json`, research docs require `R-*.research.json`, analyze/browser/report docs require their matching checks. The current command's `docs.synced` evidence must list the refreshed check paths. After document-producing commands, run `python altool/scripts/check.py audit-docs --root .`; if it fails, refresh the stale owner check and retry.
8. Record code/type/build/test/runtime/browser failures caused by code, plus implementation gaps, as lesson events during run/analyze/fix/browser or natural-language code fixes; then assess recurrence with `recurrenceRisk` and `recurrenceScope`. Do not record architecture choices, retrospectives, normal feature changes, style/text tweaks, refactors-only, or external tool/environment issues as lessons.
9. Do not create or modify global prompt, skill, or command files while executing Altool commands.
10. If the command is unknown, show the supported `/altool` command list.
11. Treat `/altool research <topic>` as investigation only; it must not create or switch `currentFeature`. Treat `/altool plan <feature description>` and `/altool oneshot <feature description>` as new feature creation. For `/altool spec`, `/altool run`, `/altool analyze`, `/altool fix`, `/altool browser`, and `/altool report`, read `.altool/state/status.json` and use `currentFeature`; any trailing text is step-specific instruction, not a feature selector. If `currentFeature` is missing, tell the user to start with `/altool plan <feature description>`.
12. For `/altool oneshot <feature description>` or `/altool freedom <goal> --loops N`, if `designs/claude-design/*.html`, `designs/stitch/`, or `designs/*.pen` exists and `designs/design.md` is missing, empty, marked `TBD`, older than the Claude design HTML, or missing that HTML in its Reference Source Map, automatically run the `altool/steps/design_source.md` preflight before research. The user does not need to run `/altool design_source` separately.
13. For `/altool freedom <goal> --loops N`, read `altool/steps/freedom.md` and run the bounded loop described there. Each loop means one autonomous development cycle, not one action, and `loopBudget` is the number of maturity cycles for the same product. Every cycle starts with design_source preflight when needed, then research after inbox/observe, then chooses the whole product's complete-product goal from that research. Every implementation cycle works from an end-to-end product experience for the user's full request. Follow-up cycles re-observe the same product, research again, and mature its functionality, UX, visual design, edge cases, and quality. Core user journeys belong in the current cycle's completion criteria. Set only the current cycle's goal at cycle start; leave future candidates as `nextResearchQuestions` and product-wide quality/UX/edge-case/improvement questions. Use `python altool/scripts/radio.py cycle start --loop N`, `python altool/scripts/radio.py action start|done <action> --loop N`, and `python altool/scripts/radio.py cycle done --loop N` so `.altool/freedom/state.json`, outbox, and journal reflect the real cycle/action progress. Implementation/UI cycles run report after browser, and the next loop starts only after the report artifact and report Step Check pass. If the user explicitly limits the cycle to research/plan only, stop with an outbox note and mark report as skipped with the user-limited reason. `freedom_loop.py` is only a control-plane smoke/debug runner unless the user explicitly asks to test the runner.
14. Step Check JSON uses `status: done | skipped | failed`. `done` needs `evidence`; `skipped` and `failed` need `reason`. If validation fails, read the failure message, fix the missing work or check JSON, and retry up to 5 times.
15. Use `constitution.md`, `designs/claude-design/*.html`, `designs/design.md`, PRD files, `.pen`, Stitch, screenshots, design documents, and research artifacts when present. Missing optional assets disable only that asset's rule; they do not stop the command.
16. For UI work, `designs/claude-design/*.html` is the highest-priority design constitution. If one or more HTML files exist there, read them before `designs/design.md`, preserve their layout structure, density, hierarchy, component appearance, colors, spacing, typography, and interaction states as binding design rules, and only use `designs/design.md` to normalize or fill gaps that the HTML does not define. If multiple Claude design HTML files conflict, ask which one is authoritative before locking the visual plan.
17. If no Claude design HTML exists, `designs/design.md` is the single implementation design source. If it is absent, empty, or its first non-empty line contains `TBD`, `/altool research` or `/altool design_source` must create/fill it from user design inputs and/or reference-site research before plan/spec/run locks visual decisions. A completed project-specific `design.md` must remove the top `TBD` marker. CSS variables may be derived inside implementation code, but raw Research observations are not the final CSS source.
18. Keep document status synchronized. Completed steps update relevant checkboxes and top-level `상태`/`Status`; verified UI work must not leave upstream docs in `Draft`.
