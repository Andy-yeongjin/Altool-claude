# /altool fix — Fix 단계 (자동 개선)

**산출물**: 개선된 소스 코드 + `docs/03-analyze/{기능명}.fix.md` (iteration report)

---

## 절차

`/altool fix` 뒤 입력은 현재 feature의 갭 수정 범위나 우선순위에 대한 추가 지시다. 기능명으로 해석하거나 `currentFeature`를 전환하지 않는다.

### 1. 실행 조건 확인

- 기능명은 `.altool/state/status.json`의 `currentFeature`에서 읽는다. `currentFeature`가 없으면 `/altool plan {기능 설명}` 먼저 실행을 안내하고 중단한다.
- `docs/03-analyze/{기능명}.analyze.md`의 Gap 목록과 `.altool/state/status.json`의 `matchRate` 확인.
  - analyze 문서가 없으면 → `/altool analyze` 먼저 실행 안내 후 중단.
- **analyze 문서 §3에 미해소 갭이 0건이면** → `✅ 미해소 갭 없음 (Match Rate {N}%) — 개선 불필요. /altool browser로 실제 화면 검증을 진행하세요.` 출력 후 종료.
  - Match Rate ≥ 90%여도 **갭이 남아 있으면 수정한다** — 90%는 통과선이지 수정 면제선이 아니다 (Fix 공통 규칙).
- Checkpoint 5에서 "Critical만 수정"이 선택됐으면 Critical 갭만 대상으로 한다.

### 2~3. Gap 목록 기반 자동 수정

각 갭을 **하나씩** 수정한다:
- analyze 문서의 "수정 방향"을 따른다
- Functional 갭(SHALLOW 파일)은 run 단계의 Depth-First 기준으로 완성한다: TODO 제거, 실데이터 연결, Page UI Checklist 항목 충족
- Contract 갭은 Spec §4 스키마에 맞춰 서버·클라이언트 양쪽 정렬
- **설계 자체가 잘못된 경우** → 코드를 끼워 맞추지 말고 Spec 문서를 수정한 후 해당 갭을 갱신 (헌법 제9조: 명세-코드 동기화)
- **Altool 확장**: 수정 중에도 `designs/claude-design/*.html`이 있으면 최우선 디자인 헌법으로 사용하고, `designs/design.md`의 시각 값·컴포넌트 계약·미디어 규칙을 추적 가능하게 사용하며, TypeScript Strict와 보안 규칙을 준수
- **React/Next.js 보조 스킬**: `.claude/skills/vercel-react-best-practices/SKILL.md`가 있으면 React/Next 성능 갭 수정에 적용한다. 없으면 `skipped(skill unavailable)`로 보고하고 계속한다.

수정 완료 후 `npm run build` 성공 확인 (Altool 확장 — 실패 시 수정 후 재빌드).

### 4. 자동 재분석 (Auto re-Check)

`altool/steps/analyze.md`의 6~9번(정적 3축 + 런타임 + Match Rate 계산)을 다시 수행한다.

### 5. 반복 판정 

`.altool/state/status.json`: `iterationCount` +1, `matchRate` 갱신, `phase: "fix"`.

- **미해소 갭 0건** → 종료, browser 검증으로
- **갭 잔존 그리고 iterationCount < 5** → 수정·재분석·반복 판정 절차를 반복 (최대 5회)
- **갭 잔존 그리고 iterationCount ≥ 5** → 중단 후 안내:
  ```
  ⚠️ 최대 반복(5회) 후에도 갭 {N}건이 남았습니다 (Match Rate {N}%).
  남은 갭: {요약}
  선택 A (권장): 남은 갭을 직접 확인 후 개별 지시로 수정
  선택 B: 이 상태로 /altool browser 진행
  ```

> `/altool oneshot` 파이프라인에서 호출된 경우에도 fix 반복 한도는 5회다.

### 6. Lesson 이벤트 기록

해소한 코드 오류나 구현 갭마다 `python altool/scripts/lesson.py append`로 `fix` 이벤트를 기록한다. 수정 전 실제 코드 오류가 확인됐으면 별도 `code_error` 이벤트를 기록하고 `relatedEventIds`로 연결한다.

각 이벤트에는 `recurrenceRisk`, `recurrenceScope`, `recurrenceReason`을 포함한다. `promoteToLesson: true`는 승격 힌트일 뿐 기록 여부의 조건이 아니다. CLI가 `events.jsonl`에 append하고 `lesson.index.json`, `lesson.md`를 갱신한다. 수동 실행 시에는 사용자에게 기록 후보를 짧게 제안하고, oneshot 자동 모드에서는 기록 후 보고한다.

### 7. Fix Report 작성

`altool/templates/fix.template.md` 구조로 `docs/03-analyze/{기능명}.fix.md`를 작성/갱신한다:
- §1 Match Rate 추이 (회차별·축별)
- §2 해소된 갭 (analyze 문서의 갭 번호와 일치시킴)
- §3 회차별 상세 (수정 내용·파일·재분석 결과)
- §4 잔여 갭 (자동 수정 불가 사유 + 제안)

문서 동기화:
- 해소된 갭은 analyze 문서에 체크/Resolved로 반영한다.
- plan/spec 문서 상단 상태는 여전히 구현 검증 중이므로 `Implemented` 또는 `Fixing`으로 갱신한다. 미해소 갭 0건이면 `Implemented`, 갭이 남으면 `Fixing`을 사용한다.
- fix 문서 상단 `상태`/`Status`는 갭 0건이면 `Resolved`, 갭이 남으면 `Partial`로 쓴다.
- analyze/plan/spec 문서를 수정했으면 fix Step Check만으로 끝내지 않는다. 수정된 문서의 소유 Step Check(`{기능명}.analyze.json`, `{기능명}.plan.json`, `{기능명}.spec.json`)도 최신 내용으로 갱신하고 각각 `check.py validate`를 통과시킨 뒤, fix check의 `docs.synced` 증거에 갱신한 check 경로를 남긴다.

완료 전 `.altool/checks/{기능명}.fix.json`을 작성하고 `python altool/scripts/check.py validate --json .altool/checks/{기능명}.fix.json`를 실행한다. 실패하면 메시지를 보고 보완한 뒤 재검증하며, 최대 5회 실패 시 중지한다. 완료 보고에는 Step Check 요약을 포함한다:

| 항목 | 보고 기준 |
| --- | --- |
| `inputs.loaded` | analyze 문서/상태 파일/React 보조 스킬 로딩 결과 |
| `lesson.search` | fix 시작 시 갭/파일/스택 기준 검색 결과 또는 `skipped(no gap)` |
| `event.capture` | 기록한 `code_error`/`fix` 이벤트 ID |
| `verification` | 빌드와 재분석 결과 |
| `state.updated` | phase=fix, iterationCount, matchRate |
| `docs.synced` | analyze 갭 해소 표기와 관련 문서 상단 Status 갱신 결과, 수정된 소유 Step Check 재검증 경로 |
| `document.status` | fix/analyze/plan/spec 문서 상단 Status=Resolved/Partial/Implemented/Fixing |
| `artifacts.created` | `docs/03-analyze/{기능명}.fix.md` |

### 8. 완료 보고

```
🐣 [al:fix] {기능명} 완료 — Match Rate {이전}% → {현재}% ({iterationCount}회차)
   산출물: docs/03-analyze/{기능명}.fix.md
   다음 단계: /altool browser  (또는 남은 갭 안내)
```




