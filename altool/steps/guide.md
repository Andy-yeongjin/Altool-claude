# /altool guide — 현재 단계 감지 + 다음 명령 안내

처음 사용자도 이 명령 하나로 어디서부터 시작해야 할지 알 수 있습니다.

---

## Step 1: 상태 수집

1. `.altool/state/status.json`이 있으면 **그것을 우선 사용** (phase·matchRate·최근 이력).
2. 없으면 파일 존재로 역산:

```
[ ] constitution.md / designs/design.md — Altool 자산
[ ] prd/ (내용 있음)                — PRD
[ ] designs/claude-design/*.html    — 최우선 Claude 디자인 헌법
[ ] designs/*.pen, designs/stitch/  — 디자인 시스템 생성용 소스
[ ] designs/*.{png,jpg,jpeg,webp,md,pdf} — 사용자 디자인 입력
[ ] docs/00-research/               — 웹 조사
[ ] docs/01-plan/  docs/02-spec/  — 계획·명세
[ ] src/ 또는 app/                  — 구현
[ ] docs/03-analyze/  docs/04-report/ — 분석·보고서
[ ] .altool/freedom/                — Freedom 무전기/자율 루프
```

## Step 2: 단계 판단 → 다음 명령

> 헌법·디자인 참조는 엔진에 내장되어 있어 **명령어만 입력하면 됩니다** (긴 지시문 복사 불필요).

| 조건 | 현재 상태 | 다음 실행 |
|------|----------|----------|
| `altool/` 없음 | 설치 전 | Altool setup.bat 실행 안내 |
| `designs/claude-design/*.html` 있음 | Claude 디자인 헌법 있음 | `/altool design_source`로 정규화하거나 `/altool oneshot`/`freedom` 자동 정규화로 진행 |
| 디자인 소스(.pen/Stitch) 있음 + design.md 없음 | 디자인 시스템 미확정 | `/altool design_source` |
| 스크린샷/디자인 문서 있음 | 사용자 디자인 입력 있음 | `/altool research {조사 주제}` 또는 `/altool plan {기능 설명}` |
| 00-research 없음 + 01-plan 없음 | 조사 필요 | `/altool research {조사 주제}` 또는 자동 진행 `/altool oneshot [기능설명]` |
| 긴 목표를 지정 횟수만큼 맡기고 싶음 | 자율 루프 필요 | `/altool freedom {목표} --loops N` |
| .altool/freedom ✅ | Freedom 진행 중 | `/altool outbox` 또는 `/altool say/ask/pause/resume/stop` |
| 00-research ✅, 01-plan 없음 | 계획 필요 | `/altool plan {기능 설명}` |
| 01-plan ✅, 02-spec 없음 | 계획 완료 | `/altool spec` |
| 02-spec ✅, 소스코드 미완 | 명세 완료 | `/altool run` |
| 소스코드 ✅, analyze 문서 없음 | 구현 완료 | `/altool analyze` |
| analyze ✅, 미해소 갭 존재 | 개선 필요 | `/altool fix` (Match Rate ≥90%여도) |
| analyze ✅, 미해소 갭 0건 + browser 문서 없음 | 정적/런타임 분석 통과 | `/altool browser` |
| browser ✅, 미해소 갭 0건 | 실제 화면 검증 통과 | `/simplify` (코드 정리, 선택) → `/altool report` |
| report ✅ | 🐥 사이클 완료 | 다음 기능 `/altool oneshot …` 또는 배포 가이드 |

## Step 3: 출력 형식

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🥚 현재 단계: [N단계. 단계명]   (기능: {기능명})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 완료된 산출물:
  ✅ [파일/단계명]

다음 단계: [설명 1~2줄]

실행 명령어:
┌─────────────────────────────────────
│ /altool {명령}
└─────────────────────────────────────

참고: [주의사항 또는 선택 단계]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 특수 상황

- `constitution.md` 없음 → "헌법 검증이 비활성 상태입니다. Altool setup.bat으로 구성하면 활성화됩니다." 안내 후 계속.
- `designs/claude-design/*.html` 있음 → 이 HTML을 최우선 디자인 헌법으로 안내하고, `designs/design.md`보다 먼저 적용한다. `design.md`가 없거나 오래됐으면 `/altool design_source`로 정규화하도록 안내한다.
- `designs/design.md` 없음 + `.pen`/Stitch 있음 → "디자인 소스가 있다면 `/altool design_source`로 디자인 시스템을 먼저 확정하세요." 안내 후 계속.
- 스크린샷/디자인 문서만 있으면 `design_source`를 요구하지 않는다. plan/spec가 해당 자산을 User Design Source로 직접 참조한다.
- research는 여러 번 반복할 수 있으며 `currentFeature`를 바꾸지 않는다.
- Freedom은 긴 목표를 사용자가 지정한 루프 횟수만큼 자율 진행하는 모드이며, 사용자는 `/altool say/ask/pause/resume/stop/outbox`로 무전기처럼 개입한다.
- 기능이 여러 개면 → 기능별 표로 정리하고 `currentFeature` 기준으로 안내. 기능 전환은 새 `/altool plan {기능 설명}`으로 시작한다.

## Step Check

출력 전 `.altool/checks/guide.guide.json`을 작성하고 `python altool/scripts/check.py validate --json .altool/checks/guide.guide.json`를 실행한다. 실패하면 메시지를 보고 보완한 뒤 재검증하며, 최대 5회 실패 시 중지한다. 출력 마지막에 Step Check 요약을 포함한다:

| 항목 | 보고 기준 |
| --- | --- |
| `inputs.loaded` | status/docs/assets 탐색 결과 |
| `lesson.search` | `skipped(not applicable)` |
| `event.capture` | `skipped(no code error)` |
| `verification` | `skipped(guide only)` |
| `state.updated` | guide가 상태 파일을 생성/수정했는지 |
| `docs.synced` | `skipped(guide only)` |
| `document.status` | `skipped(guide only)` |
| `artifacts.created` | `skipped(guide only)` |

