# /altool plan — Plan 단계

**사용법**: `/altool plan [기능 설명]`

**산출물**: `docs/01-plan/features/{기능명}.plan.md`

---

## 절차

`/altool plan` 뒤 입력은 새 feature 설명이다. 이 명령은 항상 새 개발 사이클을 시작하며 `currentFeature`를 새 feature로 갱신한다. 같은 이름의 산출물이 이미 있으면 기존 문서를 수정하지 말고 파일명과 feature key에 `-2`, `-3` suffix를 붙여 새로 생성한다.

`docs/00-research/*.research.md`가 있으면 선행 조사 입력으로 읽는다. Research는 후보와 근거일 뿐이며, 사용자가 plan에 입력한 기능 설명과 PRD를 최종 범위 결정의 기준으로 삼는다.

### 0. 템플릿 로딩 (MANDATORY)

`altool/templates/plan.template.md`를 파일 읽기 도구로 읽고 그 절 구조를 문서 아웃라인으로 사용한다. **기억이나 추측으로 Plan 문서를 생성하는 것은 금지.**

### 1. Research/PRD 자동 참조

- `docs/00-research/*.research.md`가 있으면 최근/관련 조사 문서를 읽고 Plan의 배경·요구사항 후보·리스크에 반영한다. Research의 출처 품질 매트릭스, 근거 매핑, Plan 준비도, 다음 조사 후보도 확인한다.
- `.altool/state/research.json`이 있으면 research ID, 파일 경로, sourceCount를 확인해 관련 조사 목록을 추린다.
- `docs/00-pm/{기능명}.prd.md`가 있으면 읽고 Plan의 컨텍스트로 사용.
- **Altool 자산 감지** (Altool 자산 감지 규칙): `prd/*.md`·`prd/refs/*`가 있으면 PRD·보조 컨텍스트로 읽는다 (충돌 시 PRD 우선). `designs/`의 사용자 디자인 입력(`*.pen`, `stitch/`, `*.png`, `*.jpg`, `*.jpeg`, `*.webp`, `*.md`, `*.pdf`)을 감지하고, `constitution.md`·`designs/design.md`가 있으면 읽고 강제 적용한다. UI 작업인데 디자인 시스템이 없으면 관련 research가 `designs/design.md`를 생성했는지 확인한다.
- PRD가 있으면 PRD를 기준 계약으로 삼고, Research는 PRD 구현을 더 잘하기 위한 보강재로만 사용한다. Research가 PRD에 없는 기능을 제안하면 자동으로 In Scope에 넣지 말고 후보/다음 사이클/Out of Scope에 기록한다.
- PRD와 Research가 충돌하면 PRD를 우선한다. 충돌 항목, 선택한 기준, 제외/보류 사유를 Plan §1.6 또는 §2.2에 기록한다.
- Plan은 문서 작성 단계이므로 `lesson.py search`와 `lesson.py append`를 실행하지 않는다.
- 디자인 기준 우선순위는 `designs/` 사용자 디자인 입력 → `designs/design.md` → Research가 생성한 디자인 시스템 → AI 자체 판단이다. `constitution.md`의 디자인 품질 원칙은 이 우선순위와 별개로 항상 적용한다.
- `designs/*.pen`이 있으면 Pencil MCP(batch_get)로 화면 구성을 읽고 UI 흐름에 반영한다. `designs/stitch/`가 있으면 Stitch 산출물의 구조와 디자인 의도를 읽는다. 스크린샷이나 디자인 문서가 있으면 레이아웃·밀도·위계·컴포넌트 외형의 직접 기준으로 반영한다.
- `designs/design.md`는 단일 디자인 시스템 원천이다. UI 작업에서 이 파일이 없거나 비어 있거나 첫 non-empty line에 `TBD`가 있으면 plan은 research 산출물에 디자인 시스템 생성 근거를 연결하고, 없을 경우 `/altool research` 또는 `/altool design_source`로 돌아가 생성하도록 기록한다.

### 2~4. 산출물 경로 확정

- `docs/01-plan/features/{기능명}.plan.md`가 없으면 → 해당 경로에 새로 작성한다.
- 이미 있으면 → `{기능명}-2.plan.md`, `{기능명}-3.plan.md`처럼 사용 가능한 다음 suffix를 골라 새 feature로 작성한다.
- suffix가 붙은 경우 `.altool/state/status.json`의 `currentFeature`와 check JSON의 `feature`도 같은 최종 feature key를 사용한다.

### 5. Checkpoint 1 — 요구사항 확인

기능에 대한 이해(문제·범위·제약)를 정리해 제시하고 Claude Code 대화 확인으로 확인: **"요구사항 이해가 맞나요? 빠진 건 없나요?"** 확인 후 진행.
(자동 파이프라인 호출 시 생략하고 진행 — 자동 파이프라인 Checkpoint 규칙)

### 6. Checkpoint 2 — 명확화 질문

미확정 요소(엣지 케이스, 에러 처리, 연동 지점, 호환성)를 정리해 질문 목록으로 제시하고 답변을 받은 후 문서를 생성한다.
(자동 파이프라인 호출 시 합리적 기본값으로 진행)

### 7. Plan 문서 생성

확정된 요구사항으로 템플릿 전체 절을 채워 작성한다. 핵심:
- **Research 반영**: 관련 research 문서의 출처 품질, 근거 매핑, 페이지/기능 인벤토리, 공통 패턴, 리스크, Plan 입력 후보를 선별해 §1.3 관련 문서와 §3 요구사항에 연결한다. 조사 결과와 다른 결정을 하면 사유를 남긴다.
- **디자인 입력 반영**: `designs/` 사용자 디자인 입력이 있으면 §1.3 관련 문서와 §4 성공 기준에 그 경로를 명시하고, 디자인 시스템보다 우선한다고 기록한다. 디자인 시스템이 research에서 생성되었으면 해당 research ID와 `designs/design.md` 경로를 명시한다.
- **PRD 우선**: PRD가 있으면 §2 In Scope와 §3 FR은 PRD 요구사항을 빠짐없이 반영한다. Research는 요구사항의 구현 세부, UX 보강, 리스크, 성공 기준을 강화하는 데 사용한다.
- **충돌 기록**: Research 제안이 PRD 범위를 넘거나 PRD와 충돌하면 §1.6 PRD/Research 대조 또는 §2.2 Out of Scope에 근거와 사유를 남긴다.
- **§2.1 포함(In Scope)**: 메인 화면 관련 항목을 최우선으로 (헌법 제15조)
- **§3.1 기능 요구사항**: FR-01부터 ID 부여, 우선순위 명시, Status는 `Pending`으로 시작. PRD가 있으면 모든 요구사항 빠짐없이 반영
- **§4 성공 기준**: analyze가 증거(file:line·테스트·측정값)로 판정 가능한 형태로 작성 (Match Rate 검증의 기준)
- **§6 영향 분석**: 변경 대상 리소스의 기존 사용처 전수 목록화 (신규 프로젝트면 명기 후 종료)
- **§7 아키텍처 방향**: 프로젝트 레벨 선택. 기본 스택 = Next.js(App Router) + TypeScript Strict + SQLite(로컬, 헌법 제18조)

### 8~9. 상태 갱신

`.altool/state/status.json`: `currentFeature`를 새 feature로 설정하고, 해당 feature의 `phase: "plan"`, `startedAt`을 기록한다. 기존 feature 항목과 `history`는 보존한다.
Plan 문서 작성과 Step Check가 통과하면 문서 상단 `상태`/`Status`를 `Planned`로 갱신한다. 작성 중 임시값인 `Draft`를 완료 산출물에 남기지 않는다.

### 10~11. Executive Summary + Context Anchor

- 문서 최상단에 `## Executive Summary` 4관점 표(Problem/Solution/Function·UX Effect/Core Value) 작성, 각 1~2문장
- Executive Summary·Requirements·Risks에서 추출해 `## Context Anchor` 표(WHY/WHO/RISK/SUCCESS/SCOPE)를 Executive Summary와 1장 사이에 작성 — **spec/run 단계로 전파됨**

### 12. 완료 보고 (MANDATORY)

문서 완성 후, 사용자가 파일을 열지 않아도 보도록 **Executive Summary 표를 응답에 직접 출력**한다.

완료 전 `.altool/checks/{기능명}.plan.json`을 작성하고 `python altool/scripts/check.py validate --json .altool/checks/{기능명}.plan.json`를 실행한다. 실패하면 메시지를 보고 보완한 뒤 재검증하며, 최대 5회 실패 시 중지한다. 완료 보고에는 Step Check 요약을 포함한다:

| 항목 | 보고 기준 |
| --- | --- |
| `inputs.loaded` | PRD/refs/constitution/design 자산 로딩 결과 |
| `verification` | Research/PRD 입력과 plan 범위가 대조되었는지 |
| `lesson.search` | `skipped(document-only step)` |
| `event.capture` | `skipped(document-only step)` — Plan 작성 중에는 lesson 이벤트를 append하지 않는다 |
| `state.updated` | `.altool/state/status.json` phase=plan |
| `docs.synced` | 생성/갱신한 plan 문서와 상단 Status=Planned |
| `document.status` | plan 문서 상단 Status=Planned |
| `artifacts.created` | `docs/01-plan/features/{기능명}.plan.md` |

```
🐣 [al:plan] {기능명} 완료 — 산출물: docs/01-plan/features/{기능명}.plan.md
   다음 단계: /altool spec
```





