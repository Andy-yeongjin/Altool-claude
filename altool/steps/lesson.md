# /altool lesson - 개발 중 코드 오류 기록·조회

**사용법**:
```text
/altool lesson                  <- 최근 요약 lesson 조회
/altool lesson {검색어}          <- lesson index 검색
/altool lesson {코드 오류·해결}    <- code_error/fix 이벤트 수동 기록
```

**저장 구조**:

| 파일 | 역할 | 원천 여부 |
| --- | --- | --- |
| `~/.altool/events.jsonl` | 모든 lesson 이벤트의 append-only 원장 | Source of Truth |
| `~/.altool/lesson.index.json` | 현재 작업과 관련 이벤트를 찾는 검색 인덱스 | 파생물 |
| `~/.altool/lesson.md` | 사람이 읽는 교훈 요약 | 파생물 |

`lesson.md`를 직접 원천으로 읽거나 수정하지 않는다. 조회·기록·재생성은 항상 `altool/scripts/lesson.py` CLI로 수행한다.

---

## CLI

```text
python altool/scripts/lesson.py append --json-file .altool/tmp/lesson-event.json
python altool/scripts/lesson.py append --json '{"type":"code_error",...}'
python altool/scripts/lesson.py search --query "{기능명} {스택} {파일} {오류코드}" --limit 5
python altool/scripts/lesson.py rebuild-index
python altool/scripts/lesson.py render-lessons
```

> 테스트나 격리 실행이 필요하면 `ALTOOL_HOME` 환경 변수로 저장 위치를 바꿀 수 있다. 기본값은 `~/.altool`이다.

---

## 문서와 Lesson의 경계

`lesson`은 판단 로그나 회고 저장소가 아니다. 개발 중 실제 코드 작성·수정·검증 과정에서 발생한 코드 오류와 해결 규칙만 남긴다.

| 남길 곳 | 대상 |
| --- | --- |
| Plan | 요구사항, 범위, 성공 기준, 프로젝트 레벨 방향 |
| Spec | 아키텍처 3안 비교, 선택한 Option, API/데이터/UI 체크리스트 |
| Analyze/Fix | 발견한 코드 갭, 검증 결과, 실제 수정 이력 |
| Report | 최종 결과, ADR 요약, 회고 |
| Lesson event | 코드 작성·검증 중 발생한 코드 오류, 원인, 수정, 예방 규칙 |

Research/Plan/Spec/Report 같은 문서 작성 단계에서는 lesson 이벤트를 append하지 않는다. 일반적인 기본 선택, 아키텍처 판단, 회고는 각 문서에만 기록하고 Step Check의 `lesson.search`와 `event.capture`를 `skipped(document-only step)`로 둔다.

---

## 이벤트 타입

| 타입 | 기록 시점 |
| --- | --- |
| `code_error` | run/fix 중 코드·타입·빌드·런타임·테스트 오류가 발생한 경우 |
| `fix` | 원인이 규명된 코드 오류나 구현 갭을 실제로 해결한 경우 |
| `gap` | analyze/browser 검증에서 코드 구현과 기준 문서 사이의 차이가 발견된 경우 |
| `verification` | 코드 오류 수정 후 빌드·테스트·브라우저 검증 결과 |

이 외 타입은 사용하지 않는다. 예전 이벤트 파일에 다른 타입이 남아 있어도 인덱스·검색·lesson.md 렌더 대상에서 제외된다.

---

## 이벤트 스키마

필수:

```json
{
  "type": "code_error",
  "project": "프로젝트명",
  "feature": "기능명",
  "phase": "run",
  "summary": "한 줄 요약"
}
```

권장 필드:

```json
{
  "tags": ["nextjs", "contract", "build"],
  "files": ["src/app/api/projects/[projectId]/route.ts"],
  "symptom": "겉으로 보인 문제",
  "errorMessage": "오류 메시지 또는 핵심 로그",
  "cause": "규명된 원인",
  "change": "실제로 통한 수정",
  "preventionRule": "다음에 같은 상황을 피하는 한 줄 행동 규칙",
  "recurrenceRisk": "unknown | low | medium | high",
  "recurrenceScope": "unknown | one_off | feature | project | cross_project",
  "recurrenceReason": "재발 가능성 판단 근거",
  "verification": ["npm run build", "npm test"],
  "relatedEventIds": ["E-00001"],
  "promoteToLesson": true
}
```

CLI가 `id`, `timestamp`, `schemaVersion`을 자동 보강한다.

---

## 조회 모드

1. 인자 없음: `python altool/scripts/lesson.py render-lessons`로 `lesson.md`를 최신화한 뒤 최근 요약을 출력한다.
2. 검색어 있음: 현재 작업 키워드로 `search`를 실행한다.
   ```text
   python altool/scripts/lesson.py search --query "{검색어}" --limit 5
   ```
3. `/altool run/analyze/fix`는 `lesson.md` 전체를 읽지 않는다. 반드시 `search` 결과 중 관련 코드 오류 이벤트 상위 N개만 작업 맥락에 반영한다. 자연어 코드 수정은 수정 전 search를 요구하지 않고, 실제 코드 오류/갭을 고친 경우 append만 적용한다.

## 기록 모드

1. 입력 내용을 코드 오류면 `code_error`, 해결 내용이면 `fix` 이벤트로 정리한다.
2. 재발 가능성은 기록 여부를 결정하는 조건이 아니다. `recurrenceRisk`, `recurrenceScope`, `recurrenceReason` 필드로 평가한다.
3. JSON payload를 만든 뒤 CLI로 append한다.
   ```text
   python altool/scripts/lesson.py append --json-file .altool/tmp/lesson-event.json
   ```
4. append 후 CLI가 `lesson.index.json`과 `lesson.md`를 자동 갱신한다.
5. 완료 보고:
   ```text
   [al:lesson] 기록 완료 - E-00000 (code_error)
   ```

완료 전 `.altool/checks/global.lesson.json`을 작성하고 `python altool/scripts/check.py validate --json .altool/checks/global.lesson.json`를 실행한다. 실패하면 메시지를 보고 보완한 뒤 재검증하며, 최대 5회 실패 시 중지한다. 완료 보고에는 Step Check 요약을 포함한다:

| 항목 | 보고 기준 |
| --- | --- |
| `inputs.loaded` | events/index/lesson 파생물 확인 결과 |
| `lesson.search` | 조회 모드 query와 결과 수 또는 기록 모드 `skipped(record mode)` |
| `event.capture` | 기록 모드의 이벤트 ID 또는 조회 모드 `skipped(read only)` |
| `verification` | JSON append/search/render 성공 여부 |
| `state.updated` | `skipped(global lesson only)` |
| `docs.synced` | `skipped(global lesson only)` |
| `document.status` | `skipped(global lesson only)` |
| `artifacts.created` | events.jsonl/index/lesson.md 생성·갱신 결과 |

---

## 자동 회고 연동

| 시점 | 동작 |
| --- | --- |
| **research/plan/spec/report 시작 시** | document-only step이므로 search/append하지 않는다 |
| **run 시작 시** | 수정 예정 파일, 프레임워크, 패키지, 오류코드로 `lesson.py search` 실행. 관련 이벤트의 `preventionRule`만 구현 체크에 반영 |
| **analyze 시작 시** | 기능명, 구현 경로, 테스트/계약 키워드로 `search` 실행. 관련 코드 오류 예방 규칙을 독립 검증 에이전트에게 전달하고, 위반 시 갭으로 보고 |
| **fix 시작 시** | 갭, 수정 대상 파일, 스택, 오류코드로 `search` 실행. 관련 코드 오류 예방 규칙을 수정 체크에 반영 |
| **자연어 코드 수정 시** | 수정 전 search는 요구하지 않는다. 실제 코드 오류나 구현 갭을 고친 경우에만 append한다 |
| **run·fix 중 코드 오류 발생 시** | 코드·타입·빌드·런타임·테스트 오류가 있으면 `code_error` 이벤트를 append하고 재발 가능성을 평가한다 |
| **fix에서 코드 오류/갭 수정 시** | 해결한 코드 오류나 갭별로 `fix` 이벤트를 append한다 |
| **report 회고 작성 시** | append하지 않는다. 회고는 report 문서에만 남기고, 사용자가 별도로 요청하면 `/altool lesson ...`으로 수동 기록한다 |

기록 기준:

- 기록한다: 코드 작성·검증 중 발생한 코드 오류, 타입 오류, 빌드 실패, 테스트 실패, 런타임 오류, 브라우저 검증에서 드러난 코드 문제, 구현 갭.
- 기록할 때 평가한다: `recurrenceRisk`는 `unknown | low | medium | high`, `recurrenceScope`는 `unknown | one_off | feature | project | cross_project` 중 하나로 둔다.
- `lesson.md` 승격 기준: `promoteToLesson: true` 또는 `recurrenceRisk`가 `medium/high`인 이벤트를 사람용 요약으로 렌더한다.
- 기록하지 않는다: Research/Plan/Spec/Report 작성 중 나온 모든 일반 결정과 회고, 아키텍처 선택, 요구사항 변경, 단순 명령 사용법, 외부 도구/환경 문제, 실행 전에 바로 고친 오타, 사용자 요구 변경으로 인한 정상 방향 전환.


