# Altool

**헌법 기반 통합 AI 개발 시스템** — 조사부터 검증·보고까지의 개발 사이클을 Claude Code 명령어 `/altool` 하나로 완주합니다.
외부 플러그인 설치가 필요 없습니다. 마크다운 엔진(`altool/`)과 bundled Claude Code local command가 프로젝트 안에서 동작합니다.

> 📖 **Claude Code 버전 기준 문서**는 이 README와 `CLAUDE.md`입니다. `guides/`의 HTML 문서도 `/altool` 기준의 보조 안내로 맞춥니다.

---

## 이게 뭔가요?

Altool은 세 가지를 모든 구현의 기준으로 삼아 개발 사이클을 돌립니다:

| 자산 | 파일 | 역할 |
|------|------|------|
| **프로젝트 헌법** | `constitution.md` | 개발 원칙 + 범용 디자인 품질 원칙 — 명세 우선, 보안, 반응형, 사용자 디자인 입력 우선 등 |
| **사용자 디자인 입력** | `designs/*.pen`, `designs/stitch/`, 스크린샷, 디자인 문서 | 화면 구조, 정보 밀도, 시각 위계, 컴포넌트 외형의 최우선 원천 |
| **디자인 시스템** | `designs/design.md` | 프로젝트 고유 색상·폰트·간격·컴포넌트·미디어 규칙의 단일 원천 |

핵심 특징:

- **외부 플러그인 불필요** — 개발 사이클 엔진과 보조 Claude Code 스킬을 repo에 내장 (사용자별 설치 불필요)
- **Research-first** — plan 전에 웹 조사 결과를 `docs/00-research/`에 누적하고, 만들 기능은 plan에서 확정
- **헌법·디자인 시스템 정책 내장** — 사용자 디자인 입력 우선, `design.md`를 구현 기준으로 사용, 없으면 Research/디자인 소스가 먼저 생성
- **독립 검증 에이전트** — 갭 분석을 별도 에이전트가 수행해 자기 채점 편향 차단
- **Match Rate 4축** — Structural/Functional/Contract/Runtime 가중 공식으로 일치율 측정
- **문서 상태 동기화** — 단계 완료 시 상류 문서의 체크박스·Status 자동 갱신 (문서만 열어도 진행 상황이 보임)
- **상태 + 이력** — `.altool/state/status.json`에 phase·matchRate·append-only history 기록

---

## 설치 및 사용

### 1. setup 실행

`setup.bat` 더블클릭 → 프로젝트를 만들 폴더 선택 → 필요한 파일이 자동 복사됩니다.
(`.claude/commands/altool.md` 로컬 커맨드와 `.claude/skills/` 보조 스킬이 함께 설치됩니다.)

### 2. Claude Code에서 프로젝트 열기

폴더를 연 뒤 대화창에 입력:

```
/altool setup
```

> 커맨드가 목록에 안 보이면 Claude Code를 재시작하거나 새 세션을 여세요.

### 3. (선택) 디자인 파일이 있다면 먼저

- **Pencil.dev**: `.pen` 파일을 `designs/`에 넣기
- **Stitch**: ZIP 압축 해제 후 `designs/stitch/`에 넣기

```
/altool design_source
```

색상·폰트·간격·컴포넌트 외형·미디어 규칙을 추출하고 `constitution.md`의 범용 디자인 품질 원칙을 기준으로 검토해 `designs/design.md`를 생성합니다.

### 4. 조사 후 기능 개발

조사를 먼저 여러 번 할 수 있습니다. 이 단계는 feature를 만들지 않습니다.

```
/altool research 쇼핑몰 상품 상세 페이지와 장바구니 UX 조사
```

조사 결과가 마음에 들면 plan에서 실제로 만들 기능을 말합니다.

```
/altool oneshot 사용자가 이메일과 비밀번호로 가입하고 로그인할 수 있는 인증 기능
```

`oneshot`은 웹 조사 → 계획 → 명세 → 구현 → 갭 분석(독립 에이전트) → 자동 개선 → 브라우저 검증까지 자동 완주합니다. PRD가 있으면 PRD가 기준 계약이고, research는 PRD를 더 잘 구현하기 위한 보강재로 사용됩니다.

긴 프로젝트를 지정한 횟수만큼 자율 진행하려면 Freedom으로 시작합니다.

```
/altool freedom 쇼핑몰 만들어줘 --loops 10
/altool freedom 쇼핑몰 만들어줘 10회
/altool say 결제는 제외하고 장바구니까지만 해
/altool ask 지금 뭐하고 있어?
```

`/altool freedom`에서 각 루프는 action 하나가 아니라 자율 개발 사이클입니다. `loopBudget`은 같은 제품의 완성도 반복 횟수입니다. 모든 사이클은 먼저 research를 수행하고, 그 조사 결과로 전체 제품의 완성형 목표를 정합니다. 모든 구현 루프는 사용자의 전체 요청을 만족하는 end-to-end 제품 경험을 기준으로 하고, 후속 루프는 같은 제품을 다시 조사·관찰해 기능·UX·디자인·품질을 성숙시킵니다. 이후 필요한 `plan/spec/run/analyze/fix/browser/report` step을 실제 수행하며, 구현/UI 사이클은 browser 검증 뒤 report까지 완료해야 루프 완료로 기록합니다. 다음 루프의 구체 작업은 시작 시점에 미리 정하지 않고 다음 research에서 다시 결정합니다. 로컬 control-plane만 검증할 때는 `python altool/scripts/freedom_loop.py "쇼핑몰 만들어줘" --loops 5 --interval 1`을 사용할 수 있습니다.

Freedom 진행 상태는 `.altool/freedom/state.json`, `outbox.jsonl`, `journal.md`에 같이 기록됩니다. 각 action 시작/완료 때 `currentAction`이 갱신되고, 사이클 완료 때만 `loopsCompleted`가 증가합니다.
각 단계는 산출 문서의 체크박스와 상단 `상태`/`Status`를 함께 갱신합니다.

> `prd/` 폴더에 PRD(.md)를 넣으면 자동 감지, `prd/refs/`의 참고 문서(PDF·이미지 등)도 함께 읽습니다.
> 개발 완료 후에는 browser 단계의 스크린샷·검증 문서를 먼저 확인하고, 필요하면 `start.bat`으로 직접 실행해 볼 수 있습니다.

---

## 명령어

| Claude Code 명령어 | 설명 |
|--------|------|
| `/altool setup` | 초기 설치 + 세션 재개 |
| `/altool research [조사 주제]` | 웹 조사 → `docs/00-research/`, feature 생성 없음 |
| `/altool oneshot [기능 설명]` | 웹 조사 포함 7단계 자동 완주 (PRD·.pen 자동 감지) |
| `/altool freedom [목표] --loops N` | 무전기 inbox/outbox를 감시하며 지정 횟수만큼 자율 개발 사이클 진행 |
| `/altool say [내용]` | Freedom 루프에 방향 변경 전달 |
| `/altool ask [내용]` | Freedom 루프 상태 질문 |
| `/altool pause` / `/altool resume` / `/altool stop` | Freedom 일시정지·재개·중단 |
| `/altool outbox` | Freedom 응답과 진행 로그 확인 |
| `/altool guide` | 현재 단계 감지 + 다음 명령 안내 |
| `/altool design_source` | .pen/Stitch → design.md 생성 |
| `/altool lesson [내용]` | 바이브코딩 교훈 이벤트 기록·조회 — 전역 `~/.altool/events.jsonl`에 누적, index 검색으로 자동 회고 |
| `/altool plan {기능 설명}` | PRD를 기준으로 삼고 research로 보강해 개발 계획 생성 → `docs/01-plan/features/` |
| `/altool spec [추가 지시]` | 현재 plan 기준 구현 명세 (아키텍처 3안 비교) → `docs/02-spec/features/` |
| `/altool run [추가 지시]` | 현재 plan/spec 기준 코드 구현 (Depth-First + 빌드 검증) |
| `/altool analyze [추가 지시]` | 현재 기능 갭 분석 (독립 에이전트, 4축 Match Rate) → `docs/03-analyze/` |
| `/altool fix [추가 지시]` | 현재 기능 갭 발견 시 자동 개선 → 재검증 (최대 5회) |
| `/altool browser [추가 지시]` | 실제 브라우저 클릭·입력·반응형·레이아웃 검증 |
| `/altool report [추가 지시]` | 현재 기능 완료 보고서 → `docs/04-report/` |
| `/altool status` | 기능별 진행 현황 + 최근 이력 |

---

## 프로젝트에 설치되는 파일

| 파일/폴더 | 용도 |
|----------|------|
| `altool/` | **엔진** — 단계별 절차(steps/) + 스크립트(scripts/) + 산출물 템플릿(templates/) |
| `CLAUDE.md` | Claude Code가 읽는 개발 원칙 + Altool 진입 안내 |
| `.claude/commands/altool.md` | `setup.bat`이 설치하는 Claude Code 로컬 커맨드 `/altool` |
| `.claude/skills/vercel-react-best-practices/` | React/Next.js 구현·리뷰·리팩터링 시 적용되는 Vercel 성능 최적화 스킬 |
| `constitution.md` | 프로젝트 헌법 (개발 원칙 + 범용 디자인 품질 원칙) |
| `designs/` | 사용자 디자인 입력 + 디자인 시스템 (design.md) |
| `prd/` | PRD 보관 폴더 (자동 감지) |
| `start.bat` / `end.bat` | 개발 서버 실행/종료 |
| `.gitignore` | `.altool/` 등 제외 (없을 때만 생성) |

---

## 기술 스택 (권장 기준)

Altool은 특정 스택을 강제하지 않습니다. plan/spec에서 요청 범위와 프로젝트 상태를 보고 정합니다. 일반적인 앱은 아래 기준을 우선하지만, 단일 정적 페이지처럼 단순한 요청이면 HTML/CSS/JS로도 구현할 수 있습니다.

| 영역 | 기술 |
|------|------|
| 일반 웹앱 | Next.js (App Router) + TypeScript |
| 단일 정적 페이지 | HTML/CSS/JS 허용 |
| Database | 필요할 때 SQLite(로컬) → NeonDB/Supabase 등은 ADR로 결정 |
| ORM | DB가 있을 때 Prisma 또는 Drizzle |
| Styling | 프로젝트 구조에 맞는 CSS 방식 + `designs/design.md` 기반 스타일 |
| Auth | 필요할 때 Auth.js 등으로 결정 |

---

## 자주 묻는 질문

**Q. 별도 플러그인이나 도구를 설치해야 하나요?**
아니요. Altool 엔진과 bundled Claude Code 커맨드·스킬이 함께 복사됩니다. 사용자별 플러그인 설치는 필요 없습니다.

**Q. 다른 AI 개발 워크플로우 도구와 뭐가 다른가요?**
대부분 외부 플러그인에 의존하거나 검증을 같은 AI가 스스로 합니다. Altool은 플러그인 없이 동작하고, 갭 분석을 독립 검증 에이전트에 분리하며, 문서 동기화·교훈(lesson) 누적으로 쓸수록 정확해집니다.

**Q. 헌법을 커스터마이징하고 싶어요**
프로젝트의 `constitution.md`를 직접 수정하면 됩니다.

**Q. altool/ 폴더만 다른 프로젝트에 복사해도 되나요?**
됩니다. `altool/` + `CLAUDE.md` + `.claude/commands/altool.md`가 있으면 Claude Code에서 동작합니다 (자산 감지형 — constitution.md 등이 없으면 해당 규칙만 비활성). 상세 명령 규칙은 `/altool` 커맨드와 `altool/steps/`에 둡니다.

---

## License

Original Altool source code, scripts, templates, and documentation are
licensed under the [MIT License](LICENSE).

Bundled third-party materials, including the Vercel React Best Practices skill,
the Digital Government Service UI/UX guideline PDF, and guide screenshots, keep
their original ownership and terms. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
