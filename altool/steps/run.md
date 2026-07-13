# /altool run — Run 단계 (구현)

**산출물**: 소스 코드 (구현 가이드는 `altool/templates/run.template.md` 구조로 대화에 출력)

---

## 절차

`/altool run` 뒤 입력은 현재 feature 구현을 위한 추가 지시나 옵션이다. 기능명으로 해석하거나 `currentFeature`를 전환하지 않는다.

### 1~3. 상류 문서 전체 로딩 (Full Upstream Context Loading)

- 기능명은 `.altool/state/status.json`의 `currentFeature`에서 읽는다. `currentFeature`가 없으면 `/altool plan {기능 설명}` 먼저 실행을 안내하고 중단한다.
- `docs/02-spec/features/{기능명}.spec.md` 존재 확인 (필수). 없으면 spec 먼저 실행 제안.
- **Spec 문서를 요약이 아니라 전체를 읽는다** — 세션마다 완전한 아키텍처 컨텍스트로 시작해야 함.
- PRD(`docs/00-pm/` 또는 `prd/`) → WHY 추출, Plan → Context Anchor·Success Criteria·Requirements 추출.
- **코드 오류 검색**: `lesson.md` 전체를 읽지 않는다. 기능명·수정 예정 파일·프레임워크·패키지·오류코드로 `python altool/scripts/lesson.py search --query "{키워드}" --limit 5`를 실행하고, 관련 코드 오류 이벤트의 `preventionRule`만 `lesson: E-00000(...)` 1줄로 출력 후 구현에 반영한다.
- **React/Next.js 보조 스킬**: `.claude/skills/vercel-react-best-practices/SKILL.md`가 있으면 React/Next.js 구현 규칙으로 적용한다. 없으면 `skipped(skill unavailable)`로 보고하고 계속한다.
- **Altool 자산 감지**: `constitution.md`는 있으면 읽고 적용한다. `designs/claude-design/*.html`을 최우선 디자인 헌법으로 확인하고, 그 다음 `designs/` 사용자 디자인 입력(`*.pen`, `stitch/`, `*.png`, `*.jpg`, `*.jpeg`, `*.webp`, `*.md`, `*.pdf`)과 `designs/design.md`를 확인한다. Spec의 `User Design Source`가 있으면 그 화면 구조와 시각 기준을 1순위로 구현한다. Claude 디자인 HTML이 있으면 Spec보다 더 구체적인 시각 기준으로 적용하고, `designs/design.md`와 충돌하면 HTML을 우선한다. UI 작업은 `designs/design.md`를 구현 기준으로 사용한다. 이 파일이 없거나 비어 있거나 첫 non-empty line에 `TBD`가 있으면 run을 계속하지 말고 Research 또는 design_source로 돌아가 디자인 시스템을 먼저 생성한다. 디자인 시스템이 없다는 이유로 근거 없는 generic AI/SaaS 기본 미감(과한 그라디언트, 추상 장식, glassmorphism, 카드 그림자 남발)을 발명하지 않는다.
- UI 구현은 `designs/claude-design/*.html`의 DOM/CSS/컴포넌트 구조를 먼저 따르고, 그 다음 `designs/design.md`의 **Screen Recipes**와 **Capture-to-Implementation Map**을 따른다. 색상·폰트·버튼 값은 그 다음 적용한다. 캡처 기반 recipe가 있는데도 일반적인 split SaaS hero, floating trust card 묶음, 과한 gradient overlay, 카드 그림자 남발, reference보다 느슨한 빈 화면으로 구현하면 design drift다.
- `Capture-to-Implementation Map`의 각 행마다 대응하는 section/component를 코드에 만든다. 구현하지 않는 행이 있으면 plan/spec 범위 밖 사유를 run check의 `verification` 또는 `docs.synced` 증거에 남긴다.

### 4~5. Decision Record Chain + Success Criteria 표시

> **자동 파이프라인 모드에서는 아래 표 출력을 생략**하고 `📋 결정: {핵심 1줄} | 🎯 SC {N}개 추적` 한 줄 요약만 출력한다 (장황 방지). 표 전체 출력은 수동 실행 시에만.

구현 시작 전 대화에 출력:

```
📋 Decision Record Chain
[PRD] 타겟: {시장/사용자} — {근거}
[Plan] 아키텍처: {선택안} — {근거}
[Spec] 상태 관리: {선택 방식} — {근거}

📌 Context Anchor
WHY / WHO / RISK / SUCCESS / SCOPE 표 (Spec 문서에서)
```

Plan의 Success Criteria를 구현 체크리스트로 표시 — 각 기준이 구현 중 반드시 다뤄져야 한다.

### 6~8. --scope 파라미터 + Session Guide

- 추가 지시에 `--scope module-N`이 있으면 Spec §10.3 세션 가이드의 Module Map과 대조해 해당 모듈만 구현 범위로 필터.
- 그 밖의 추가 지시는 구현 방식 제약으로 반영하되, feature 선택자로 사용하지 않는다.
- `--scope`가 없으면 전체 Module Map 표시 + 세션 분할 권장 + 전체 구현 진행.

### 9~10. 범위 요약 + Checkpoint 4 — 구현 승인

```
생성 파일: N개 / 수정 파일: M개 / 예상 변경: ~X줄
```

Claude Code 대화 확인: **"이 범위로 구현을 시작해도 되겠습니까?"** — **승인 없이 구현 시작 금지.**
(자동 파이프라인 호출 시 승인 생략하고 진행)

### 11~13. 구현 — Depth-First 전략 (CRITICAL RULE)

> **깊게 구현하라, 넓게 펼치지 마라.**
> 안티패턴: 20개 파일 스켈레톤 → 각 30% 완성 (구조 매치 90%인데 기능적으로 빈껍데기)
> 올바른 패턴: **배치당 3~5개 파일을 완전히 구현** → Page UI Checklist 대조 검증 → 다음 배치

배치별 구현 사이클 (bottom-up):
```
① API route 구현 → ② L1 테스트(curl) → ③ Hook + Component 구현
→ ④ L2 테스트(Playwright) → ⑤ Page 통합 → ⑥ 전부 green이면 다음 배치
테스트 파일: tests/e2e/{기능명}.spec.ts (시나리오는 Spec §8 테스트 플랜)
```

파일별 완성 기준 (다음 파일 생성 전 확인):
- `// TODO`·플레이스홀더 주석 없음, `console.log` 스텁 핸들러 없음
- `[1,2,3].map` 하드코딩 목 배열 없음 (실데이터 또는 empty state)
- Page UI Checklist의 폼 필드·인터랙티브 요소 전부 존재 + 실제 핸들러
- 로딩 상태·에러 상태 구현, 데이터 페칭 연결

**코드 주석 규약** (명세 추적성): 파일 상단 `// Spec Ref: §{절} — {결정 근거}`, 핵심 로직 앞 `// Plan SC: {대응하는 성공 기준}`

**Altool 확장 준수 사항**:
| 항목 | 규칙 |
|------|------|
| 디자인 입력/디자인 시스템 | `designs/claude-design/*.html`이 있으면 최우선 디자인 헌법으로 읽고 화면 구조와 시각 기준 1순위로 구현한다. Spec의 User Design Source가 있으면 함께 확인한다. `designs/design.md`를 읽고 Screen Recipes, Component Extraction, Capture-to-Implementation Map을 구현하되 Claude HTML과 충돌하면 HTML을 우선한다. 그 다음 색상·타이포·폰트 스택·간격·둥글기·그림자·컴포넌트·미디어 규칙을 추적 가능하게 적용한다. CSS 변수는 코드 안에서 파생해도 되지만 값의 근거는 Claude HTML 또는 `design.md`에 있어야 한다. 참조 폰트 파일을 복제하지 말고 `design.md`에 잠긴 구현 font-family stack을 그대로 사용한다. 파일이 없거나 비어 있거나 첫 non-empty line에 `TBD`가 있으면 Research/design_source로 돌아가 생성 후 진행. 참조 브랜드의 로고·카피·고유 이미지·식별 가능한 고유 배치는 복제하지 않지만, 캡처에서 추출한 구조·비례·밀도·컴포넌트 외형 계약은 구현한다. |
| 보안 | API 키 하드코딩 금지, `.env` 격리, 세션 검증 (제6조·제11조) |
| 메인 화면 | 메인 화면 우선, 비인증 탐색 보장 (제15조) |
| 반응형 | 모바일 375px 이상 정상 표시 (제7조) |
| 로컬 DB | SQLite (제18조) |

### 빌드 검증 (Altool 확장 — 완료 보고 전 필수)

`npm run build` 성공까지 확인. 실패 시 수정 후 재빌드. 서버는 직접 실행하지 않는다 (`start.bat`이 있으면 그것을, 없으면 `npm run dev`를 안내).

코드·타입·빌드·테스트·런타임·브라우저 검증에서 코드 오류가 발생하면 `lesson.py append`로 이벤트를 남기고 재발 가능성을 평가한다:
- 코드 오류가 발생하면 `code_error`
- 실제 코드 수정으로 해결했으면 `fix`
- 수정 후 검증 결과는 `verification`

이벤트에는 `recurrenceRisk`, `recurrenceScope`, `recurrenceReason`을 포함한다. 외부 도구/환경 문제, 명령 사용법 문제, 단순 오타·실행 전에 바로 고친 import 누락은 기록하지 않는다.

### 14~15. 상태 갱신 + 보고

`.altool/state/status.json`: `phase: "run"`, **`buildVerified: true`** (빌드 성공 확인 후에만).
**문서 동기화** (Altool 공통 규칙): plan §2.1 포함(In Scope)의 구현된 항목 체크, plan §3.1 FR Status를 `Pending` → `✅ 완료`로, spec §11.2 Implementation Order의 완료 항목 체크. 빌드까지 통과한 구현이면 plan/spec 문서 상단 `상태`/`Status`를 `Implemented`로 갱신한다.
plan/spec 문서를 수정했으면 run Step Check만으로 끝내지 않는다. `.altool/checks/{기능명}.plan.json`과 `.altool/checks/{기능명}.spec.json`도 최신 내용으로 갱신하고 각각 `check.py validate`를 통과시킨 뒤, run check의 `docs.synced` 증거에 갱신한 check 경로를 남긴다.

완료 전 `.altool/checks/{기능명}.run.json`을 작성하고 `python altool/scripts/check.py validate --json .altool/checks/{기능명}.run.json`를 실행한다. 실패하면 메시지를 보고 보완한 뒤 재검증하며, 최대 5회 실패 시 중지한다. 완료 보고에는 Step Check 요약을 포함한다:

| 항목 | 보고 기준 |
| --- | --- |
| `inputs.loaded` | spec/plan/PRD/자산/React 보조 스킬 로딩 결과 |
| `lesson.search` | run 시작 시 실행한 query와 결과 수 |
| `event.capture` | `code_error`/`fix`/`verification` 이벤트 ID 또는 `skipped(no code error)` |
| `verification` | 빌드·테스트 명령과 결과 |
| `state.updated` | `.altool/state/status.json` phase=run, buildVerified |
| `docs.synced` | plan/spec 체크박스와 상단 Status=Implemented 동기화 결과, 수정된 plan/spec 소유 Step Check 재검증 경로 |
| `document.status` | plan/spec 문서 상단 Status=Implemented |
| `artifacts.created` | 구현 파일 목록 |

```
🐣 [al:run] {기능명} 완료
   구현 파일: {목록} | 빌드: ✅ npm run build 성공
   브라우저 확인: start.bat(없으면 npm run dev) 실행 후 http://localhost:3000
   다음 단계: /altool analyze
```




