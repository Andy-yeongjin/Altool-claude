# /altool spec — Spec 단계

**산출물**: `docs/02-spec/features/{기능명}.spec.md`

---

## 절차

`/altool spec` 뒤 입력은 현재 feature의 명세 작성 추가 지시다. 기능명으로 해석하거나 `currentFeature`를 전환하지 않는다.

### 0. 템플릿 로딩 (MANDATORY)

`altool/templates/spec.template.md`를 파일 읽기 도구로 읽고 그 절 구조를 아웃라인으로 사용한다. 기억으로 생성 금지.

### 1~2. Plan 문서 확인

- 기능명은 `.altool/state/status.json`의 `currentFeature`에서 읽는다. `currentFeature`가 없으면 `/altool plan {기능 설명}` 먼저 실행을 안내하고 중단한다.
- `docs/01-plan/features/{기능명}.plan.md` 존재 확인. **없으면 `/altool plan {기능 설명}` 먼저 실행을 제안**하고 사용자에게 진행 여부 확인.
- 있으면 전체를 읽고 요구사항·범위를 파악한다.
- 사용자가 입력한 추가 지시가 있으면 Plan 범위와 충돌하지 않는 선에서 아키텍처 3안, UI 체크리스트, 테스트 플랜에 반영한다.
- **Altool 자산 감지**: `constitution.md`는 있으면 읽고 적용한다. `designs/` 사용자 디자인 입력(`*.pen`, `stitch/`, `*.png`, `*.jpg`, `*.jpeg`, `*.webp`, `*.md`, `*.pdf`)이 있으면 화면 구조와 시각 기준의 1순위로 읽는다. `designs/design.md`가 있고 첫 non-empty line에 `TBD`가 없으면 프로젝트 디자인 시스템으로 적용한다. UI 작업인데 이 파일이 없거나 비어 있거나 `TBD` 마커가 있으면 Research 또는 design_source 단계로 돌아가 디자인 시스템을 먼저 생성하도록 명세에 기록하고, 임의 시각 값을 직접 명세화하지 않는다.

### 3. PRD 컨텍스트 로딩

`docs/00-pm/{기능명}.prd.md` 또는 `prd/*.md`가 있으면 읽고 아키텍처 결정에 시장·사용자 맥락을 반영한다.

### 4. Context Anchor 복사

Plan의 `## Context Anchor` 표를 Spec 문서 상단(헤더 메타데이터와 ## 1. Overview 사이)에 복사한다. Plan에 없으면 생략.

### 5~7. 아키텍처 3안 생성 + Checkpoint 3

세 가지 설계안을 생성하고 트레이드오프 비교표(복잡도·유지보수성·공수·리스크)를 제시한다:

- **Option A — 최소 변경**: 기존 코드 최대 재사용. 빠르지만 결합도 위험
- **Option B — Clean Architecture**: 최고의 관심사 분리. 파일·리팩토링 많음
- **Option C — 실용 균형**: 과잉 설계 없는 적절한 경계. **권장 기본값**

Claude Code 대화 확인: **"3가지 설계안 중 어떤 걸 선택하시겠습니까?"** (권장안 포함)
(자동 파이프라인 호출 시 Option C로 자동 진행)

### 8~9. Spec 문서 작성

선택된 아키텍처로 템플릿 전체 절을 채워 작성한다. 핵심:
- **§2.1 아키텍처 3안 비교**: 비교표 + 선택 결과·근거 기록
- **§3 데이터 모델**: TypeScript 인터페이스 (Strict Mode, `any` 금지 — 헌법 제6조)
- **§4 API 명세**: 엔드포인트 목록 + 상세 스키마 + 에러 응답 (**analyze의 Contract 검증 기준**)
- **§5.4 Page UI Checklist (CRITICAL)**: 페이지별 필수 UI 요소를 빠짐없이 항목화 — 폼 필드·버튼·필터·배지·데이터 표시 요소를 구체적 옵션 값까지. **이 체크리스트가 없으면 analyze가 파일 존재만 검사하게 됨 (Functional 검증의 분모)**
- **§8 테스트 플랜**: L1(API)/L2(UI 액션)/L3(E2E) 테스트 시나리오 정의 — run에서 코드 작성, analyze에서 실행
- **사용자 디자인 입력 있음**: `.pen`, Stitch, 스크린샷, 디자인 문서에서 화면 구조, 정보 밀도, 시각 위계, 컴포넌트 외형을 명세 기준으로 잠근다. Research는 누락된 UX/기능/상태 보강과 디자인 시스템 정규화 근거로만 사용한다.
- **디자인 시스템 있음**: 모든 UI 컴포넌트의 시각적 수치(높이·색상·폰트·간격·그림자·둥글기)는 `designs/design.md`의 규칙으로 명시한다. 특히 Screen Recipes, Component Extraction, Capture-to-Implementation Map을 Design System Anchor에 잠그고 Page UI Checklist에 반영한다. 폰트는 참조 font-family와 구현 font-family stack, 대체 사유를 함께 잠근다. 코드 구현에서 CSS 변수를 쓰는 것은 허용하지만, 값과 역할은 `design.md`에서 추적 가능해야 한다. 필요한 화면 recipe나 컴포넌트 계약이 누락되면 spec에서 직접 발명하지 말고 디자인 시스템 보강 필요 항목으로 기록한다.
- **사용자 디자인 입력 없음 + 디자인 시스템 없음**: Research가 참조 사이트를 근거로 `designs/design.md`를 생성해야 한다. Spec은 research 문서와 생성된 디자인 시스템을 연결하고, 생성 전에는 UI 시각값을 확정하지 않는다.

### 10. Session Guide 생성

§10 구현 가이드 구조를 분석해 Module Map과 권장 세션 계획을 `§10.3 세션 가이드`로 작성한다. (`/altool run --scope module-N` 분할 구현용)

### 11. Design System Anchor

UI 기능이면 `## Design System Anchor` 절에 시각 기준을 잠근다. 먼저 `designs/` 사용자 디자인 입력이 있는지 확인하고, 있으면 그 자산의 경로와 적용 범위를 명시한다. 그 다음 `designs/design.md`의 Screen Recipes, Component Extraction, Capture-to-Implementation Map, 시각 값, 컴포넌트 계약, 미디어 규칙을 채운다. 이 파일이 없거나 비어 있거나 첫 non-empty line에 `TBD`가 있으면 관련 Research에서 디자인 시스템을 생성하도록 되돌리고, Spec 완료 전 `Design System Anchor`를 채운다. 이 절이 비어 있거나 Screen Recipe와 구현 대상 section/component 연결이 없으면 run이 generic AI/SaaS 스타일로 흐르므로 Spec 완료 전 반드시 보완한다.

### 12~13. 상태 갱신 + 보고

`.altool/state/status.json`: `phase: "spec"`.
**문서 동기화**: plan §9 다음 단계의 "구현 명세" 항목을 `- [x]`로 갱신 (문서 상태 동기화 규칙). spec 문서 상단 `상태`/`Status`를 `Specified`로, plan 문서 상단 상태를 `Specified`로 갱신한다.
plan 문서를 수정했으면 spec Step Check만으로 끝내지 않는다. `.altool/checks/{기능명}.plan.json`도 최신 내용으로 갱신하고 `check.py validate`를 통과시킨 뒤, spec check의 `docs.synced` 증거에 갱신한 check 경로를 남긴다.

완료 전 `.altool/checks/{기능명}.spec.json`을 작성하고 `python altool/scripts/check.py validate --json .altool/checks/{기능명}.spec.json`를 실행한다. 실패하면 메시지를 보고 보완한 뒤 재검증하며, 최대 5회 실패 시 중지한다. 완료 보고에는 Step Check 요약을 포함한다:

| 항목 | 보고 기준 |
| --- | --- |
| `inputs.loaded` | plan/PRD/constitution/designs 자산 로딩 결과 |
| `lesson.search` | `skipped(document-only step)` |
| `event.capture` | `skipped(document-only step)` — Spec 작성 중에는 lesson 이벤트를 append하지 않는다 |
| `verification` | plan 요구사항, 선택 아키텍처, API/UI/test 명세 정합성 검토 결과 |
| `state.updated` | `.altool/state/status.json` phase=spec |
| `docs.synced` | plan §9 동기화와 plan/spec 상단 Status 갱신 결과, 수정된 plan 소유 Step Check 재검증 경로 |
| `document.status` | plan/spec 문서 상단 Status=Specified |
| `artifacts.created` | `docs/02-spec/features/{기능명}.spec.md` |

```
🐣 [al:spec] {기능명} 완료 — 산출물: docs/02-spec/features/{기능명}.spec.md
   선택 아키텍처: Option {A/B/C}
   Page UI Checklist: {N}개 항목 (analyze의 Functional 검증 분모)
   다음 단계: /altool run
```





