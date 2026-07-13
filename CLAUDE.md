# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Common Development Rules

### 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- Do not add case-specific rules or guidance to solve one observed failure; generalize the cause into a reusable principle, or leave it as a local note.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" -> "Write tests for invalid inputs, then make them pass"
- "Fix the bug" -> "Write a test that reproduces it, then make it pass"
- "Refactor X" -> "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```text
1. [Step] -> verify: [check]
2. [Step] -> verify: [check]
3. [Step] -> verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

### 5. UI Verification Harness

**New or changed pages must be clicked through in the browser.**

When creating or modifying any UI page:
- Run the available build/type check first.
- Open and verify the affected page in a real browser first, using the browser workflow in section 6.
- Click every primary user-facing control in the changed area:
  - buttons
  - links
  - tabs and filters
  - dropdowns
  - form inputs
  - submit and cancel actions
  - calendar/date interactions
- Verify the expected result after each interaction:
  - URL changes
  - modal open/close state
  - selected values
  - rendered list/card/table changes
  - persistence through the app's storage or API when data is saved
- For forms, submit at least one real test record and confirm it appears in both the UI and the app's persistence layer when applicable.
- For responsive areas, verify desktop and mobile when the changed area is visible in both.
- If the primary browser tool cannot control the page after retrying with a fresh snapshot, fall back to standalone Playwright with `headless: false` so the user can see the browser, and explicitly report that fallback.
- Report exactly what was tested and what passed.

### 6. Browser Operation

Verify UI in a real browser. Use the Playwright MCP server if it is available, or the project's own launch flow (for example the `/run` skill or `start.bat` + Playwright). Drive the actual page — DOM inspection alone is not verification.

Important notes:

- Ground locator choices in a DOM snapshot before interacting. Build locators from the snapshot, verify uniqueness (`count() === 1`) when it is not obvious, then perform the real user action (`click`, `fill`, `press`, role/text locators).
- UI verification is not complete until the changed controls have actually been clicked or operated in the browser and the resulting state has been checked. DOM inspection alone is not a substitute for clicking primary buttons, links, dropdowns, tabs, submit/cancel actions, and route-changing controls.
- Prefer stable, semantic locators for UI QA: `getByRole(...)`, `getByLabel(...)`, `getByText(...)`, or scoped `locator(...)`. Wait on navigation/state changes explicitly rather than fixed sleeps.
- When using standalone Playwright as the verification path, launch it with `headless: false` so the user can see the browser. Run it from the project working directory so it resolves the project-local `node_modules` and its pinned browser revision.
- Scope locators carefully. Some apps keep multiple route sections or hidden views in the DOM, so broad selectors can match hidden inputs/buttons. Prefer active-page and input-type selectors when uniqueness is not obvious.
- Before clicking/filling, verify locator count is exactly one when uniqueness is not obvious.
- If text entry via `fill()` fails, switch to a non-clipboard path such as focused keyboard presses or a page-side DOM/event helper, then verify the rendered value before saving. Do not loop on a failing input method.
- Use screenshots or DOM checks after interactions to confirm the visible result.

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

## 2. Project-Specific Rules

This repository packages the Altool Claude Code workflow: the `/altool` local command, command step documents, scripts, templates, and setup files for AI-assisted project development.
