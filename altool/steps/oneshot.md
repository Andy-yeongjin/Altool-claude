# /altool oneshot — 기능 설명 → 구현 완료 전 자동 파이프라인

**사용법**: `/altool oneshot [기능 설명]`

**예시**:
```
/altool oneshot 사용자가 음식을 검색해서 끼니별로 기록하고 하루 칼로리를 확인하는 식단 기록 기능
```

기능 설명 하나로 웹 조사 → 개발 계획 → 구현 명세 → 구현 → 갭 분석 → 자동 개선 → 브라우저 검증까지 **7단계를 자동 완주**합니다.
각 단계는 `altool/steps/`의 해당 step을 **자동 파이프라인 모드**(Checkpoint 생략, 권장 옵션 자동 선택 — Altool 공통 규칙)로 실행합니다.
헌법·조건부 디자인 정책은 엔진에 내장되어 있으므로 별도 지시문 주입이 필요 없습니다. 디자인 기준 우선순위는 `designs/` 사용자 디자인 입력(`.pen`, Stitch, 스크린샷, 디자인 문서) → `designs/design.md` → Research가 생성한 디자인 시스템 → AI 자체 판단입니다. `constitution.md`의 디자인 품질 원칙은 모든 원천에 항상 적용합니다. oneshot의 research 단계는 UI 작업에서 디자인 시스템이 없거나 비어 있거나 첫 non-empty line에 `TBD`가 있으면 참조 사이트와 사용자 디자인 입력을 근거로 `design.md`를 먼저 생성하고 `TBD` 마커를 제거합니다. 이후 plan/spec/run은 Research의 시각 관찰값을 직접 구현하지 않고 이 디자인 시스템을 구현 기준으로 사용합니다.

---

## 실행 전 체크 (자동)

1. **기능 설명 확인**: 비어있으면 → 사용법 안내 후 중단.
2. **기능명 결정**: 기능 설명에서 짧은 한글 기능명을 도출한다 (공백은 하이픈).
3. **입력 자산 감지**: `🥚 [0/7] 입력 자산 감지 중...` 출력 후 탐색:

   | 자산 | 경로 | 필수 | 없을 때 |
   |------|------|------|---------|
   | 엔진 | `altool/` | 필수 | 중단 — setup.bat 안내 |
   | 선행 조사 | `docs/00-research/*.research.md` | 선택 | oneshot의 research와 함께 참고 |
   | 헌법 | `constitution.md` | 권장 | 1회 경고 후 계속 (Altool 자산 규칙) |
   | 디자인 시스템 | `designs/design.md` | UI 작업 필수 | research 단계에서 생성 |
   | 사용자 디자인 입력 | `designs/*.pen`, `designs/stitch/`, `designs/*.{png,jpg,jpeg,webp}`, `designs/*.{md,pdf}` | 선택 | research에서 디자인 시스템 생성 근거로 사용 |
   | PRD | `prd/*.md` | 선택 | — 표시 |
   | PRD 참고 | `prd/refs/*` (전부 읽음, PRD 우선) | 선택 | — 표시 |

   PRD·.pen·스크린샷·디자인 문서가 여러 개이고 적용 대상이 모호하면 → 멈추고 사용자에게 선택 요청 (단, `prd/refs/`는 전부 자동 읽기).

   감지 결과 보고:
   ```
   [0/7] 입력 자산 감지 완료
     Research: ✅/—  헌법: ✅/—  디자인 시스템: ✅/—  사용자 디자인 입력: ✅/—  PRD: ✅/—  PRD 참고: ✅/—
   ```

---

## 파이프라인 (7단계)

> 각 단계 시작 전 `🥚 [N/7] 단계명 시작...`, 완료 후 `🐣 [N/7] 단계명 완료` 출력 (필수).
> 각 하위 step의 Step Check를 수집한다. `skipped`/`failed` 항목은 이유를 남긴다. run/analyze/fix/browser 중 발생한 코드 오류와 구현 갭만 `lesson.py append` 기록 여부를 확인한다. research/plan/spec/report는 document-only step으로 append하지 않는다. 각 하위 step check는 `[al:check] ... 검증 중` / `[al:check] ... 통과` 형식으로 출력한다.
> 하위 step이 다른 Altool 문서(plan/spec/analyze/browser/report 등)를 수정했다면, 그 문서의 소유 Step Check도 갱신·검증된 상태여야 한다. oneshot 집계는 수정된 문서보다 오래된 소유 check를 완료 증거로 취급하지 않는다.
> **멈추는 경우는 두 가지뿐**: ① 7단계에서 개발 서버 미실행, ② fix 5회 후에도 미해소 갭 잔존.

| 단계 | 실행 | 비고 |
|------|------|------|
| [1/7] 웹 조사 | `altool/steps/research.md` 수행 | 입력 기능 설명과 PRD 기준으로 조사하고, `docs/00-research/`에 기록. PRD가 있으면 research는 PRD 구현 보강재로만 사용 |
| [2/7] 개발 계획 | `altool/steps/plan.md` 수행 | PRD를 기준 계약으로 두고, research와 refs·.pen은 보강 컨텍스트로 전달 |
| [3/7] 구현 명세 | `altool/steps/spec.md` 수행 | 아키텍처 Option C 자동 선택 |
| [4/7] 코드 구현 | `altool/steps/run.md` 수행 | Depth-First, 빌드 검증 포함 |
| [5/7] 갭 분석 | `altool/steps/analyze.md` 수행 | 독립 검증 에이전트 + 가능 시 런타임 검증 |
| [6/7] 자동 개선 | 미해소 갭 0건 → `🐣 [6/7] 패스` / 갭 존재 → `altool/steps/fix.md` 수행 (Match Rate ≥90%여도 갭이 있으면 수정) | **최대 5회**, 이후에도 미달 시 멈추고 선택지 제시 (A: 직접 확인 후 계속 / B: 이대로 7단계 진행) |
| [7/7] 브라우저 검증 | `altool/steps/browser.md` 수행 | Playwright(MCP/로컬) 브라우저 검증 |

### [7/7] 브라우저 기능·디자인 검증 + 자체 수정

`altool/steps/browser.md`를 읽고 그대로 수행한다. oneshot 내부에서는 자동 파이프라인 모드이므로 사용자가 별도로 승인하지 않아도 가능한 브라우저 도구로 실제 화면을 열고 클릭·입력·이동·반응형·레이아웃 깨짐을 검증한다.

browser step이 직접 시작한 개발 서버는 브라우저 검증이 끝나면 반드시 종료한다. 기존에 이미 떠 있던 서버를 사용한 경우에는 종료하지 않고 browser Step Check의 `server.cleanup`에 `skipped(existing server)`로 남긴다.

서버 미실행으로 browser step이 실패하면 oneshot도 완료 처리하지 않는다. 브라우저 검증에서 드러난 코드 오류와 구현 갭은 `browser.md` 기준으로 lesson 이벤트를 기록한다. npm/npm.ps1 같은 외부 도구·환경 문제는 lesson에 기록하지 않는다.

### Step Check 집계

각 단계 완료 후 아래 표를 누적하고, 최종 완료 보고에 포함한다.
최종 보고 전 `.altool/checks/{기능명}.oneshot.json`을 작성하고 `python altool/scripts/check.py validate --json .altool/checks/{기능명}.oneshot.json`를 실행한다. 실패하면 메시지를 보고 하위 step check 또는 집계 JSON을 보완한 뒤 재검증하며, 최대 5회 실패 시 중지한다.
이어 `python altool/scripts/check.py audit-docs --root .`를 실행한다. 실패하면 stale로 보고된 문서의 소유 Step Check를 갱신·검증한 뒤 oneshot check와 `audit-docs`를 다시 실행한다.

| 단계 | inputs.loaded | lesson.search | event.capture | verification | state.updated | docs.synced | document.status | artifacts.created |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| research | done/skipped(reason) | skipped(reason) | skipped(reason) | done/skipped(reason) + research 품질 체크 | done/skipped(reason) | done/skipped(reason) | Status=Done | done/skipped(reason) |
| plan | done/skipped(reason) | skipped(document-only step) | skipped(document-only step) | N/A | done/skipped(reason) | done/skipped(reason) | Status=Planned | done/skipped(reason) |
| spec | done/skipped(reason) | skipped(document-only step) | skipped(document-only step) | N/A | done/skipped(reason) | done/skipped(reason) | Status=Specified | done/skipped(reason) |
| run | done/skipped(reason) | done/skipped(reason) | E-.../skipped(no event) | done/skipped(reason) | done/skipped(reason) | done/skipped(reason) | Status=Implemented | done/skipped(reason) |
| analyze | done/skipped(reason) | done/skipped(reason) | E-.../skipped(no event) | done/skipped(reason) | done/skipped(reason) | done/skipped(reason) | Status=Analyzed/GapsFound | done/skipped(reason) |
| fix | done/skipped(no gap) | done/skipped(no gap) | E-.../skipped(no gap) | done/skipped(no gap) | done/skipped(no gap) | done/skipped(no gap) | Status=Resolved/Partial/skipped(no gap) | done/skipped(no gap) |
| browser | N/A | done/skipped(reason) | E-.../skipped(no issue) | done/skipped(reason) | N/A | done/skipped(reason) | Status=Verified | screenshot/result |

`event.capture`는 사건이 없을 때만 `skipped(no event)`로 둔다. 오류·실패·우회·갭이 있었는데 이벤트가 없다면 해당 단계로 돌아가 보완한다.
research 하위 check에는 `research.source_mix`, `research.source_quality`, `research.freshness`, `research.duplicate_review`, `research.evidence_map`, `research.visual_capture`, `research.design_system`, `research.design_tokens`, `research.screen_recipe`, `research.component_extraction`, `research.capture_map`, `research.plan_readiness`, `research.next_queries`도 포함한다.
browser 하위 check에는 `visual.reference_comparison`, `visual.css_custom_properties`, `server.cleanup`을 포함한다. `visual.reference_comparison`은 참조 캡처와 최종 화면 스크린샷의 구조·비례·밀도·컴포넌트 외형 대조 결과여야 한다. `visual.css_custom_properties`는 `python altool/scripts/check.py css-vars --root .` 통과 결과 또는 `skipped(no css files)`여야 한다. `server.cleanup`은 직접 시작한 서버의 종료 증거 또는 `skipped(existing server)`여야 한다.
`oneshot` check JSON에는 `checks` 객체와 `children` 배열을 포함한다. `children`에는 research/plan/spec/run/analyze/fix/browser check 파일 경로를 넣는다. 갭이 없어 fix를 건너뛰면 fix 항목은 `skipped(no gap)`로 남긴다.

---

## 완료 보고

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🐣 /altool oneshot 완료! (조사 → 계획 → 명세 → 구현 → 갭 분석 → 개선 → 브라우저 검증)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 산출물:
  ✅ docs/00-research/R-0001-{조사주제}.research.md
  ✅ docs/01-plan/features/{기능명}.plan.md
  ✅ docs/02-spec/features/{기능명}.spec.md
  ✅ [구현 파일 목록]
  ✅ docs/03-analyze/{기능명}.analyze.md — Match Rate: {N}%
  ✅ 브라우저 검증: 기능 {N}건 / 디자인 {N}건 / 수정 {N}건
  ✅ Step Check: research/plan/spec/run/analyze/fix/browser 요약
  ✅ Lesson Events: {E-00001, E-00002 또는 none}

💬 다음:
  • 수정 요청: 대화로 바로 ("로그인 버튼 색 바꿔줘")
  • 완료 보고서: /altool report
  • 다음 기능: /altool oneshot [기능 설명]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```





