# /altool analyze — Check 단계

**산출물**: `docs/03-analyze/{기능명}.analyze.md`

---

## 절차

`/altool analyze` 뒤 입력은 현재 feature 분석을 위한 추가 지시다. 기능명으로 해석하거나 `currentFeature`를 전환하지 않는다.

### 0. 템플릿 로딩 (MANDATORY)

`altool/templates/analyze.template.md`를 파일 읽기 도구로 읽고 그 절 구조를 아웃라인으로 사용한다.

### 1~3. 상류 문서 전체 로딩 + Context Anchor 복사

- 기능명은 `.altool/state/status.json`의 `currentFeature`에서 읽는다. `currentFeature`가 없으면 `/altool plan {기능 설명}` 먼저 실행을 안내하고 중단한다.
3계층 검증을 위해 전부 읽는다 (단일 문서 비교가 놓치는 갭을 잡기 위함):
- PRD → 전략 정합성 (올바른 문제를 풀었는가?)
- Plan → Requirements 이행 + Success Criteria
- Spec → 구조적 구현 일치
- Spec의 Context Anchor를 analyze 문서 헤더에 복사
- **코드 오류 검색**: `lesson.md` 전체를 읽지 않는다. 기능명·구현 경로·테스트·계약·오류코드 키워드로 `python altool/scripts/lesson.py search --query "{키워드}" --limit 7`를 실행하고 관련 코드 오류 이벤트만 추린다. 동일한 오류 패턴이 구현에 남아 있으면 갭으로 보고한다.
- **React/Next.js 보조 스킬**: `.claude/skills/vercel-react-best-practices/SKILL.md`가 있으면 waterfall, bundle, server/client boundary, rerender, hydration 등 성능 안티패턴을 추가 갭 후보로 검사한다. 없으면 `skipped(skill unavailable)`로 보고하고 계속한다.

### 4~5. Strategic Alignment Check

구조 갭 분석 전에 먼저 검증:
- 구현이 PRD의 핵심 문제(WHY)를 해결하는가?
- Plan의 Success Criteria 각각을 ✅ Met / ⚠️ Partial / ❌ Not Met으로 판정 + **증거(file:line 또는 테스트 결과) 필수**
- 핵심 설계 결정(아키텍처·데이터 모델·API)이 지켜졌는가?
- **전략적 불일치는 구조 매치율과 무관하게 Critical로 플래그. SC 위반은 자동 Critical.**

### 6~7. 독립 검증 에이전트 호출 (자기 채점 금지)

> **설계·구현을 작성한 세션이 스스로 채점하면 체크리스트가 구현 모양대로 해석되어 점수가 부풀려진다.**
> 갭 분석은 **독립 서브에이전트에 위임**한다.

1. **Agent 도구(general-purpose)로 검증 에이전트를 생성**하고 아래를 전달한다:
   - Spec 문서 경로 + Plan 문서 경로 + 구현 경로(src/ 등)
   - 아래 3축 정의와 Match Rate 공식
   - **관련 교훈 목록** (1~3단계에서 추린 것): "아래는 과거에 실제 발생한 결함 패턴이다. 각 교훈의 예방 규칙 위반 여부를 추가로 검사하라 — 설계와 일치하더라도 위반이면 갭으로 보고하라."
   - 지침: "너는 이 설계와 코드를 처음 본다. **갭을 찾는 것이 임무**다. 각 판정에 file:line 증거를 의무화하고, 애매하면 ✅가 아니라 ⚠️로 판정하라. 칭찬은 불필요하다."
2. 에이전트는 축별 점수 + 갭 목록(항목·파일·차이·수정 방향)을 구조화해 반환한다.
3. **메인 세션은 에이전트가 보고한 갭과 점수를 그대로 기록한다.** 임의로 점수를 올리거나 갭을 기각하지 않는다 (기각하려면 반증 증거를 문서에 남긴다).
4. Agent 도구를 사용할 수 없는 환경에서만 메인 세션이 직접 수행하되, 모든 판정에 file:line 증거를 의무화한다.

검증 3축 정의 (에이전트에게 전달):

| 축 | 검사 내용 |
|----|----------|
| **Structural** | 파일 존재, 라우트 커버리지, 컴포넌트 목록 (Spec §5.3, §10.1 대조) |
| **Functional** | Spec §5.4 Page UI Checklist 항목별 구현 검증 + 플레이스홀더 검출(`TODO`, `console.log` 스텁, 목 배열) + 파일별 Depth Score(0~100, 60 미만 = SHALLOW) |
| **Contract** | Spec §4 ↔ 서버 route.ts ↔ 클라이언트 fetch 3-way 대조 (런타임 장애를 정적 검사로 검출) |

### 8. 런타임 검증 (v2.3.0)

서버 감지: `http://localhost:3000` 응답 확인.

- **서버 미실행 시**: L1~L3 생략, 사용자에게 경고 후 **정적 공식 사용**. (서버를 직접 실행하지 말고 `start.bat` 또는 `npm run dev` 실행을 안내)
- **서버 실행 중**:
  - **L1 — API 테스트**: Spec §8.1의 각 엔드포인트를 curl로 호출 — 상태코드·응답 형태·401 가드·400 검증 확인
  - **L2 — UI 액션 테스트**: `tests/e2e/{기능명}.spec.ts` 있으면 실행, 없으면 Spec §8.2에서 생성 후 Playwright 실행 (Playwright 미설치 시 생략 후 안내). Windows에서는 `npx playwright test`처럼 bare `npx`를 쓰지 말고 `npx.cmd playwright test` 또는 `node_modules\\.bin\\playwright.cmd test`를 사용한다. 프로젝트별 Playwright 검증은 프로젝트 작업 디렉터리에서 로컬 `node_modules`를 해석하는 `node`/Playwright로 실행하고, persistent Node REPL이나 외부 번들 런타임의 Playwright에 의존하지 않는다. Playwright(MCP/로컬) 또는 사용 가능한 브라우저 검증 도구로 대체 가능
  - **L3 — E2E 시나리오**: Spec §8.3의 멀티 페이지 사용자 여정 검증

### 9. Match Rate 계산 (4축 가중 공식)

```
런타임 실행 시: Overall = Structural×0.15 + Functional×0.25 + Contract×0.25 + Runtime×0.35
              (Runtime = L1×0.4 + L2×0.3 + L3×0.3)
정적 전용:     Overall = Structural×0.2 + Functional×0.4 + Contract×0.4
```

모든 축의 비율을 **개별 보고**하고 Gap 목록을 생성한다. 각 갭에는 파일 경로 + 설계와의 차이 + 수정 방향 기록 (iterate의 입력).

각 Critical/Important 갭은 `lesson.py append`로 `gap` 이벤트를 기록한다. 기록에는 `feature`, `phase: "analyze"`, `files`, `summary`, `cause` 또는 `preventionRule`(있을 때), `verification` 근거, `recurrenceRisk`, `recurrenceScope`, `recurrenceReason`을 포함한다.

**Altool 자산 감지 — 디자인 시스템 검증** (UI 기능이면 analyze 문서에 절 추가):
| 항목 | 기준 |
|------|------|
| 사용자 디자인 입력 있음 | `designs/`의 `.pen`, Stitch, 스크린샷, 디자인 문서가 있으면 Spec의 User Design Source와 구현 화면 구조·밀도·위계·컴포넌트 외형이 일치 |
| 디자인 시스템 있음 | 구현 화면의 색상·타이포·폰트 스택·간격·둥글기·그림자·컴포넌트 외형·미디어 사용이 `designs/design.md`의 규칙과 추적 가능하게 일치. 참조 폰트 파일 복제 없이 `design.md`의 구현 font-family stack 사용 |
| CSS custom properties | CSS 파일이 있으면 `var(--token)` 참조가 실제 정의(`--token:`)와 일치하는지 확인. 미정의 custom property는 해당 CSS 선언이 무효화될 수 있으므로 구현 갭 |
| 디자인 시스템 없음 | UI 작업이면 Research 또는 design_source로 돌아가 `design.md`를 생성해야 하므로 구현 완료 불가 |
| Generic AI/SaaS 회귀 | Research/Spec 근거 없는 대형 히어로, 과한 그라디언트, 추상 AI 장식, glassmorphism, 카드 그림자 남발 없음 |
| 참조 복제 금지 | 참조 브랜드의 로고·카피·고유 이미지·식별 가능한 레이아웃 복제 없음 |
| 반응형 | 375px 이상 정상 |

### 10. Decision Record 검증

PRD→Plan→Spec 체인의 핵심 결정이 구현에서 지켜졌는지 확인, 이탈 플래그.

### 11. Checkpoint 5 — 처리 방침 결정

심각도별(Critical/Important, 확신도 ≥80%만) 이슈를 제시하고 Claude Code 대화 확인:
- "지금 모두 수정" → fix 진행
- "Critical만 수정" → Critical만 fix
- "그대로 진행" → 현재 상태 수용

(자동 파이프라인 호출 시: 갭이 1건이라도 있으면 "모두 수정"으로 자동 진행 — Match Rate와 무관)

### 12~13. 상태 갱신 + 보고

`.altool/state/status.json`: `phase: "check"`, `matchRate: {N}`. 빌드 성공 판정(SC류)은 상태의 `buildVerified` 필드를 독립 증거로 사용한다.
**문서 동기화** (Altool 공통 규칙): 검증을 통과한 항목만 spec §5.4 Page UI Checklist와 plan §4 Success Criteria에서 `- [x]`로 갱신. ❌/⚠️ 항목은 체크하지 않는다.
문서 상단 상태는 갭 결과와 일치시킨다:
- analyze 문서 상단 `상태`/`Status`: 미해소 갭 0건이면 `Analyzed`, 갭이 있으면 `GapsFound`.
- plan/spec 문서 상단 `상태`/`Status`: 미해소 갭 0건이면 `Analyzed`, 갭이 있으면 `NeedsFix`.
plan/spec 문서를 수정했으면 analyze Step Check만으로 끝내지 않는다. `.altool/checks/{기능명}.plan.json`과 `.altool/checks/{기능명}.spec.json`도 최신 내용으로 갱신하고 각각 `check.py validate`를 통과시킨 뒤, analyze check의 `docs.synced` 증거에 갱신한 check 경로를 남긴다.

완료 전 `.altool/checks/{기능명}.analyze.json`을 작성하고 `python altool/scripts/check.py validate --json .altool/checks/{기능명}.analyze.json`를 실행한다. 실패하면 메시지를 보고 보완한 뒤 재검증하며, 최대 5회 실패 시 중지한다. 완료 보고에는 Step Check 요약을 포함한다:

| 항목 | 보고 기준 |
| --- | --- |
| `inputs.loaded` | PRD/plan/spec/구현 경로/React 보조 스킬 로딩 결과 |
| `lesson.search` | analyze 시작 시 실행한 query와 결과 수 |
| `event.capture` | 기록한 `gap`/`verification` 이벤트 ID 또는 `skipped(no gap)` |
| `verification` | 정적 3축, L1/L2/L3 실행 또는 생략 사유 |
| `state.updated` | `.altool/state/status.json` phase=check, matchRate |
| `docs.synced` | plan/spec 체크박스와 관련 문서 상단 Status 동기화 결과, 수정된 소유 Step Check 재검증 경로 |
| `document.status` | analyze 및 plan/spec 문서 상단 Status=Analyzed/NeedsFix/GapsFound |
| `artifacts.created` | `docs/03-analyze/{기능명}.analyze.md` |

```
🐣 [al:analyze] {기능명} 완료 — 산출물: docs/03-analyze/{기능명}.analyze.md
   Structural {N}% | Functional {N}% | Contract {N}% | Runtime {N}% (또는 정적 전용)
   Overall Match Rate: {N}%
   디자인 기준: {디자인 시스템 통과 / 위반 N건}
```

- 미해소 갭 0건 → `다음 단계: /altool browser`
- 갭 존재 → `다음 단계: /altool fix` (Match Rate ≥90%여도)





