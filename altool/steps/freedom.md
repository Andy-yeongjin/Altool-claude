# /altool freedom - 프롬프트로부터의 해방 모드

**사용법**

```text
/altool freedom {목표} --loops {횟수}
/altool freedom {목표} {횟수}회
/altool freedom
```

**목적**: 사용자가 매 단계 프롬프트로 운전하지 않아도, AI가 사용자가 지정한 루프 횟수만큼 웹 조사 -> 계획 -> 명세 -> 구현 -> 검증 -> 개선 -> 보고 흐름으로 이루어진 자율 개발 사이클을 수행한다.

Freedom은 `oneshot`의 대체가 아니라 상위 자율주행 모드다. `oneshot`은 한 번의 정해진 파이프라인이고, Freedom은 상태를 보고 다음 action을 고른다. 다만 채팅을 영구 점유하지 않도록 **반드시 루프 횟수 한도**를 가진다.

여기서 **각 루프는 action 하나가 아니라 자율 개발 사이클**이다. `loopBudget`은 같은 제품을 조사·구현·검증·재조사로 성숙시키는 반복 횟수다. 모든 루프는 반드시 research로 시작하고, 그 조사 결과와 현재 상태를 바탕으로 전체 제품의 완성형 목표를 정한다. 한 루프 안에서 여러 action(`plan`, `spec`, `run`, `analyze`, 필요한 `fix`, `browser`, `report`)을 수행할 수 있다. `currentAction`은 루프 내부에서 지금 수행 중인 세부 action일 뿐이며, `loopsCompleted`는 action 완료 때가 아니라 사이클 종료 때만 증가한다.

## 0. 시작 출력

```text
🥚 [al:freedom] {목표 또는 기존 목표} 시작... (loops: {N})
```

## 1. 무전기 초기화

`python altool/scripts/radio.py init "{목표}" --loops {N}`를 실행해 아래 파일을 보장한다.

```text
.altool/freedom/inbox.jsonl
.altool/freedom/outbox.jsonl
.altool/freedom/state.json
.altool/freedom/journal.md
```

목표가 비어 있으면 기존 `.altool/freedom/state.json`의 `goal`을 사용한다. 기존 목표도 없으면 사용법을 안내하고 중단한다.

루프 횟수 규칙:

- 사용자가 `--loops N`, `N회`, `N번`을 말하면 그 값을 사용한다.
- 루프 횟수가 없으면 기본값은 1회다.
- 루프 횟수는 1 이상이어야 한다.
- 각 루프는 하나의 의미 있는 개발 사이클이다. 반드시 `research`를 먼저 수행한 뒤, 조사 결과와 현재 상태에 따라 `plan -> spec -> run -> analyze -> fix -> browser -> report` 중 필요한 흐름으로 사용자가 맡긴 전체 제품의 완성형을 구현·검증한다.
- 루프 수는 같은 제품의 완성도를 반복적으로 끌어올리는 기준이다. 모든 루프는 동일한 제품 목표를 대상으로 한다.
- action 하나만 끝났다고 `loopsCompleted`를 올리지 않는다. `currentAction`만 갱신하고 outbox/journal에 진행 상황을 남긴다.
- `loopsCompleted`는 현재 사이클의 목표 산출물과 검증이 끝났을 때만 1 증가시킨다.
- `loopsCompleted >= loopBudget`이면 다음 루프를 시작하지 않고 완료 보고 후 채팅 제어권을 반환한다.
- 사용자가 큰 숫자를 주면 그대로 수행하되, 안전 경계·반복 실패·pause/stop은 루프 예산보다 우선한다.

로컬 루프 러너로 control-plane을 검증하거나 제한된 자동 루프를 실행할 때는 아래 명령을 사용한다.

```text
python altool/scripts/freedom_loop.py "{목표}" --loops {N} --interval 1
```

이 러너는 control-plane tick마다 radio inbox를 확인하고, state/outbox/journal/check 갱신 흐름만 검증한다. **주의: `/altool freedom`의 실제 실행은 이 러너만 돌리는 것이 아니다.** Claude Code는 아래 "Freedom 실제 루프 실행 규칙"에 따라 각 사이클 안에서 필요한 실제 Altool step들을 수행해야 한다. `freedom_loop.py`는 control-plane 테스트/디버그용이다.

## 1.5 Freedom 실제 루프 실행 규칙

`/altool freedom {목표} --loops N`을 받으면 Claude Code는 아래 루프를 직접 수행한다. 아래의 `cycle`이 사용자가 지정한 각 자율 개발 사이클이다.

```text
for cycle in 1..N:
  1. radio pending 확인 및 처리
     - `python altool/scripts/radio.py cycle start --loop {cycle}` 실행
  2. Observe
  3. research 수행
     - 시작 전 `python altool/scripts/radio.py action start research --loop {cycle}` 실행
     - `altool/steps/research.md`를 읽고 실제 조사 산출물을 만든다
     - 기존 조사와 중복/새 발견을 분리한다
     - 다음 루프 후보는 확정 계획이 아니라 nextResearchQuestions로 남긴다
     - 완료 후 `python altool/scripts/radio.py action done research --loop {cycle} --summary "{요약}"` 실행
  4. 이번 사이클의 완성형 목표와 완료 기준 결정
     - 이번 research에서 확인한 유사 서비스·사용자 기대·페이지·기능·디자인 시스템 근거를 기준으로 전체 제품의 완성형 목표를 정한다
     - 기능·UX·디자인·품질 기준이 서로 연결된 end-to-end 제품 경험이 되도록 범위를 세운다
     - 후속 루프의 구체 작업은 미리 확정하지 않는다
  5. 필요한 action들을 순서대로 수행
     - 각 action 시작 전 radio pending 확인
     - 각 action 시작 시 `python altool/scripts/radio.py action start {action} --loop {cycle}` 실행
     - 선택된 action의 step 문서 읽기
     - 해당 step 실제 수행
     - 해당 step의 Step Check 실행
     - 각 action 완료 시 `python altool/scripts/radio.py action done {action} --loop {cycle} --summary "{요약}"` 실행
  6. 구현 사이클은 report 수행
     - browser 통과 후 다음 루프로 넘어가기 전에 반드시 `altool/steps/report.md`를 읽고 report action을 수행한다
     - `docs/04-report/{feature}.report.md`와 `{feature}.report.json` Step Check가 통과해야 한다
  7. 사이클 완료 기준을 만족하면 `python altool/scripts/radio.py cycle done --loop {cycle} --summary "{요약}"` 실행해 loopsCompleted를 갱신
  8. 다음 사이클로 넘어가기 전 radio pending 확인
```

중요:

- `freedom_loop.py`만 실행하고 끝내면 안 된다. 그것은 control-plane 테스트일 뿐이다.
- 사이클 시작 시 `.altool/freedom/state.json`의 `loop`를 현재 cycle 번호로 갱신한다.
- action 시작 시 `.altool/freedom/state.json`의 `currentAction`을 action명으로 갱신한다.
- action 완료 시 `currentAction`을 `null`로 되돌리고 outbox/journal에 완료 요약을 남긴다.
- 사이클 완료 시 `loopsCompleted`를 현재 cycle 번호 이상으로 갱신한다.
- 각 사이클은 반드시 `research` 산출물부터 만든다. `research` 없이 plan/spec/run으로 넘어가지 않는다.
- Freedom의 모든 구현 루프는 사용자의 전체 요청을 만족하는 end-to-end 제품 경험을 기준으로 한다. 후속 루프는 직전 루프에서 만든 같은 제품을 다시 조사·관찰해 기능·UX·디자인·품질을 성숙시킨다.
- 핵심 사용자 여정은 현재 루프의 완료 기준에 포함한다. `Out of Scope`는 안전 경계, 외부 연동, 실제 결제, 사용자 승인이 필요한 작업, 현재 제품의 보조 확장 후보에만 사용한다.
- 시간·안전·기술 제약이 있으면 현재 완성형 기준과 남은 확장 후보를 `Out of Scope`, report, `nextResearchQuestions`에 기록한다.
- 새 `currentFeature`는 사용자가 명시적으로 다른 제품이나 독립 기능을 요청한 경우에만 만든다. 후속 루프는 기존 `currentFeature`의 plan/spec/code/analyze/browser/report를 갱신해 같은 제품을 고도화한다.
- `research` 후 `plan`, `spec`, `run`, `analyze`, `fix`, `browser`, `report` 중 필요한 action을 선택하면 반드시 아래 Act 표의 step 문서를 읽고 실제 산출물을 만든다.
- 어떤 action에서든 Altool 소유 문서를 수정하면 그 문서의 소유 Step Check를 다시 작성하고 검증한다. 예를 들어 후속 루프의 `run` 중 `plan.md`에 addendum을 붙이면 `.altool/checks/{feature}.plan.json`을 갱신·검증하고, `spec.md`를 수정하면 `.altool/checks/{feature}.spec.json`을 갱신·검증한다. 현재 action의 `docs.synced`에는 갱신한 check 경로를 증거로 남긴다.
- 예: 루프 시작 시 `altool/steps/research.md`를 읽고 `docs/00-research/*.research.md`와 `.altool/checks/*.research.json`을 생성한다.
- 예: action이 `plan`이면 `altool/steps/plan.md`를 읽고 `docs/01-plan/features/*.plan.md`와 `.altool/checks/*.plan.json`을 생성한다.
- 예: action이 `spec`이면 `altool/steps/spec.md`를 읽고 `docs/02-spec/features/*.spec.md`와 `.altool/checks/*.spec.json`을 생성한다.
- run/analyze/fix/browser/report도 같은 방식으로 각 step 절차와 검증을 수행한다.
- 구현 또는 UI가 포함된 사이클은 `browser` 통과 후 `report`까지 완료해야 사이클 완료로 본다. browser 통과만으로 다음 루프를 시작하지 않는다.
- browser action은 참조 캡처와 최종 화면 스크린샷을 대조하고 browser Step Check의 `visual.reference_comparison`에 증거를 남긴다.
- browser action은 CSS 파일이 있는 UI 프로젝트에서 `python altool/scripts/check.py css-vars --root .`를 실행하고 `visual.css_custom_properties`에 통과 결과 또는 생략 사유를 남긴다.
- browser action이 직접 시작한 개발 서버는 action 종료 전에 반드시 종료한다. 기존 서버를 사용한 경우에는 종료하지 않고 browser Step Check의 `server.cleanup`에 `skipped(existing server)`로 남긴다.
- `docs/04-report/{기능명}.report.md`가 없거나 `.altool/checks/{기능명}.report.json`이 통과하지 않았으면 `loopsCompleted`를 올리지 않는다.
- 사용자가 "plan까지만", "research까지만"처럼 수행 범위를 명시하면 해당 범위까지만 수행하고 outbox에 stop/ack를 남긴다. 이 경우 구현 사이클 완료가 아니므로 report는 `skipped(user-limited cycle)`로 남기고, 일반적으로 `loopsCompleted`를 증가시키지 않는다.
- 각 사이클은 research와 정한 완료 기준까지 끝난 뒤 `loopsCompleted`를 1 증가시킨다. UI가 있는 기능은 browser와 report action 통과 전까지 사이클 완료로 보지 않는다.
- action 하나를 선택하거나 끝낸 것만으로 `loopsCompleted`를 올리지 않는다.
- 사용자가 "현재 루프까지만 하고 멈춰"라고 말하면 현재 action만 끝내는 것이 아니라 현재 사이클의 필수 검증과 정리까지 마친 뒤 다음 사이클에 진입하지 않는다.

## 2. 모든 action 전 inbox 확인

Freedom의 핵심 규칙이다. 아래 의미 있는 action을 시작하기 직전에 반드시 `python altool/scripts/radio.py pending`을 실행한다.

- 웹 조사
- research 문서 작성
- plan 작성
- spec 작성
- 파일 수정
- 의존성 설치
- 빌드/테스트
- 브라우저 검증
- analyze 작성
- fix 시작
- 다음 기능 후보 선택
- report 작성

pending 이벤트 처리:

| inbox type | 처리 |
| --- | --- |
| `stop` | outbox에 `stop` 기록 후 즉시 중단 |
| `pause` | outbox에 `ack` 기록 후 남은 사이클을 보류하고 중단. resume이 들어오면 다음 `/altool freedom`에서 이어간다 |
| `ask` | outbox에 `answer` 기록 후 계속 |
| `say` | 목표/제약/범위에 반영하고 outbox에 `ack` 기록 후 계속. "현재 루프까지만" 같은 지시는 현재 사이클 완료 후 중지 예약으로 해석한다 |
| `resume` | outbox에 `ack` 기록 후 계속 |

AI는 사용자에게 질문하지 않는다. 필요한 확인이 있으면 현재 안전 기준과 완료 기준에 맞는 선택을 하고 outbox에 이유를 남긴다.

## 3. Observe

다음 자산을 읽고 현재 상태를 판단한다.

- `CLAUDE.md`, `.claude/commands/altool.md`
- `constitution.md`
- `designs/design.md`
- `designs/*.pen`, `designs/stitch/`, `designs/*.{png,jpg,jpeg,webp}`, `designs/*.{md,pdf}`
- `prd/*.md`, `prd/refs/*`
- `.altool/state/status.json`
- `.altool/state/research.json`
- `.altool/freedom/state.json`
- `.altool/checks/*.json`
- `docs/`
- 코드 디렉터리: `src/`, `app/`, `pages/`, `components/`, `tests/`
- git status

## 4. Decide

각 사이클은 먼저 research를 완료한 뒤, 현재 상태와 조사 결과를 보고 후속 action을 하나씩 고른다. action 선택 근거는 `.altool/freedom/journal.md`와 outbox `progress`에 남긴다.

| action | 선택 기준 |
| --- | --- |
| `research` | 모든 사이클의 필수 시작 action. 목표와 유사 사례, 기능 후보, UX 패턴, 사용자 기대, 리스크를 조사 |
| `plan` | 이번 research 기준의 완성형 목표가 정해졌고, plan이 없거나 현재 research·사용자 지시·구현 상태와 불일치함 |
| `spec` | plan이 있고, spec이 없거나 현재 plan·research·design.md·구현 상태와 불일치함 |
| `run` | spec이 있고, 구현이 없거나 현재 spec·research·design.md와 구현이 불일치함 |
| `analyze` | 구현 후 갭 검증이 필요함 |
| `fix` | analyze에서 갭이 발견됨 |
| `browser` | UI/런타임/디자인을 실제 브라우저에서 확인해야 함. UI가 있는 구현 사이클은 report 전 필수 |
| `report` | browser 통과 후 구현 사이클을 닫기 위한 필수 완료 보고 |
| `stop` | 안전 경계 또는 반복 실패 한도 도달 |

넓은 목표는 현재 루프의 research 기준으로 하나의 완성형 제품 경험으로 정리한다. 단, 루프별 작업을 시작 시점에 미리 확정하지 않는다. 다음 루프의 실제 목표는 다음 루프 시작 시 다시 inbox 확인, Observe, research를 수행한 뒤 같은 제품 전체를 기준으로 결정한다. 현재 루프 종료 시에는 `nextResearchQuestions`와 전체 제품을 더 완성하기 위한 품질·UX·엣지 케이스·확장 후보만 남긴다.

기존 plan/spec이 있어도 새 research, 사용자 지시, 구현 관찰, browser 결과가 문서와 달라졌으면 새 feature 문서를 만들지 말고 같은 `currentFeature`의 기존 문서를 갱신한다. 갱신 후 해당 owner Step Check를 다시 작성하고 검증한다. 새 `currentFeature`는 사용자가 명시적으로 다른 제품이나 독립 기능을 요청한 경우에만 만든다.

## 5. Act

선택한 action은 기존 step을 재사용한다.

| Freedom action | 사용할 절차 |
| --- | --- |
| `research` | `altool/steps/research.md` |
| `plan` | `altool/steps/plan.md` |
| `spec` | `altool/steps/spec.md` |
| `run` | `altool/steps/run.md` |
| `analyze` | `altool/steps/analyze.md` |
| `fix` | `altool/steps/fix.md` |
| `browser` | `altool/steps/browser.md` |
| `report` | `altool/steps/report.md` |

Research는 PRD와 사용자 디자인 입력을 덮어쓰지 않는다. 디자인 기준 우선순위는 `designs/` 사용자 디자인 입력(`.pen`, Stitch, 스크린샷, 디자인 문서) → `designs/design.md` → Research가 생성한 디자인 시스템 → AI 자체 판단이다. `constitution.md`의 디자인 품질 원칙은 모든 원천에 항상 적용한다. 외부 사이트에서 가져올 수 있는 것은 페이지 구조, 정보 배치, 기능 흐름, 인터랙션 의도, 사용자 기대, 색상, 브랜드 분위기, 타이포, 간격, 그림자, 둥글기, 컴포넌트 외형 값, 밀도, 위계, 네비게이션 패턴이다. `designs/design.md`가 있고 첫 non-empty line에 `TBD`가 없으며 프로젝트 고유 내용이 있으면 기존 디자인 시스템을 재사용하고, 없거나 비어 있거나 `TBD` 마커가 있으면 첫 research에서 참조 사이트와 사용자 디자인 입력을 근거로 이 파일을 생성한 뒤 `TBD`를 제거한다. 후속 action은 Research의 시각 관찰값을 직접 구현하지 않고 생성·재사용된 디자인 시스템을 구현 기준으로 사용한다. 단, 문장·카피·로고·고유 이미지·식별 가능한 레이아웃은 그대로 복제하지 않는다. 디자인 시스템이 없다는 이유로 근거 없는 generic AI/SaaS 기본 미감을 새로 만들지 않는다.

## 6. Verify

각 하위 action의 Step Check를 실행한다. Freedom 자체도 `.altool/checks/freedom.freedom.json`을 작성하고 검증한다.

필수 check:

| 항목 | 의미 |
| --- | --- |
| `inputs.loaded` | CLAUDE.md, Altool skill, Observe 자산, freedom state, docs/code/git 상태 로딩 결과 |
| `lesson.search` | 하위 구현 action의 lesson search 결과 요약 또는 `skipped(no implementation action)` |
| `event.capture` | 하위 구현 action에서 기록한 code_error/gap/fix 이벤트 요약 또는 `skipped(no code event)` |
| `verification` | 하위 action Step Check와 Freedom 상위 검증 결과 |
| `state.updated` | `.altool/freedom/state.json`과 필요한 `.altool/state/status.json` 갱신 |
| `docs.synced` | plan/spec/analyze/browser/report 문서와 상태 동기화 결과, 그리고 수정된 Altool 문서의 소유 Step Check 갱신·검증 결과. 문서 수정이 없으면 `skipped(no feature docs)` |
| `document.status` | 관련 문서 상단 Status 동기화 결과 또는 `skipped(no document status)` |
| `artifacts.created` | 생성/갱신한 freedom, docs, check 산출물 목록 |
| `inbox.watch` | action 전 inbox 확인 |
| `research.required` | 실제 `/altool freedom` 사이클 시작 시 research 산출물과 research Step Check를 먼저 완료 |
| `cycle.state` | 사이클 시작/완료 시 `loop`, `loopsCompleted`가 실제 진행과 일치 |
| `action.state` | 각 action 시작/완료 시 `currentAction`이 설정되고 완료 후 해제 |
| `report.required` | 구현/UI 사이클은 report 문서와 report Step Check 완료. 사용자 범위 제한 지시가 있으면 `skipped(user-limited cycle)` |
| `outbox.updated` | ack/answer/progress/warning/stop 기록 |
| `action.selected` | 다음 action 선택 근거 |
| `lesson.capture` | 코드 오류/구현 갭 lesson 처리 |
| `loop.progress` | 사이클 진행 로그 |
| `visual.reference_comparison` | browser action의 참조 캡처와 최종 화면 스크린샷 대조 결과 또는 `skipped(no browser action)` |
| `visual.css_custom_properties` | browser action의 CSS custom property 검증 결과 또는 `skipped(no browser action/no css files)` |
| `server.cleanup` | browser action이 시작한 서버 종료 증거 또는 `skipped(existing server)` |

검증은 최대 5회 반복한다.

```text
[al:check] freedom.freedom 검증 중... (attempt {N}/5)
python altool/scripts/check.py validate --json .altool/checks/freedom.freedom.json
python altool/scripts/check.py audit-docs --root .
```

`audit-docs`가 실패하면 stale로 보고된 문서의 소유 Step Check를 갱신·검증한 뒤 Freedom check와 `audit-docs`를 다시 실행한다.

## 7. Learn

run/analyze/fix/browser 또는 자연어 코드 수정 중 코드 오류, 빌드 실패, 테스트 실패, 런타임 오류, 브라우저 오류, 구현 갭이 있으면 `lesson.py append`로 기록한다.

research/plan/spec/report 문서 작성 판단은 lesson에 기록하지 않는다.

## 8. Record

각 사이클과 주요 action마다 아래를 남긴다.

- `.altool/freedom/state.json`: 목표, 상태, `loopBudget`, `loopsCompleted`, 현재 사이클 번호, 현재 action, 제약
- `.altool/freedom/journal.md`: 사람이 읽는 진행 로그
- `.altool/freedom/outbox.jsonl`: 사용자에게 보이는 진행/답변/경고
- `.altool/checks/freedom.freedom.json`: Freedom 상위 검증

완료 출력:

```text
🐣 [al:freedom] 루프 {N} 완료 - 다음 사이클: {continue 또는 stop}
```

루프 예산을 모두 사용한 경우:

```text
🐣 [al:freedom] {loopsCompleted}/{loopBudget} 루프 완료 - 지정된 루프 횟수에 도달했습니다.
```

## 9. 안전 경계

Freedom은 아래 작업을 수행하지 않는다. 필요하면 outbox에 `warning`을 남긴다.

- 실제 결제/송금/구매
- 외부 배포
- 계정 생성
- 권한 변경
- 데이터 삭제
- 비밀키 생성/조회/전송
- 유료 API 사용


