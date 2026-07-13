# /altool setup — 초기 설치 + 세션 재개

처음 실행 시 필요한 도구를 설치하고, 기존 프로젝트면 현재 상태를 복원합니다.
**별도 플러그인 설치가 필요 없습니다** — Altool 엔진(`altool/`)과 bundled Claude Code local commands가 프로젝트 내부에서 동작합니다.

---

## 모드 판단

`.altool/state/status.json` 또는 `docs/` 폴더가 존재하면 → **세션 재개 모드**, 없으면 → **초기 설치 모드**.

---

## 초기 설치 모드

아래 단계를 순서대로 직접 실행한다. 설명만 하지 말고 반드시 실행할 것.

**1단계 — Node.js 확인:**
```bash
node --version
```
없으면 winget으로 설치 후 재확인:
```bash
winget install OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements
```

**2단계 — 로컬 전용 원칙 확인:**

- 전역 Claude Code prompt/skill/command 설치를 수행하지 않는다.
- 프로젝트 내부 `CLAUDE.md`, `altool/`, `.claude/commands/`, `.claude/skills/`, `.altool/`만 사용한다.
- 필요한 외부 도구는 프로젝트의 `package.json`에 이미 있거나, 해당 단계에서 사용자에게 명시한 뒤 로컬 devDependency로만 추가한다.

**3단계 — Altool 자산 확인:**

| 자산 | 확인 | 없을 때 |
|------|------|---------|
| `altool/` 엔진 폴더 | 필수 | Altool setup.bat 재실행 안내 후 중단 |
| `.claude/commands/` | 필수 | Altool setup.bat 재실행 안내 후 중단 |
| `.claude/skills/vercel-react-best-practices/` | 권장 | React/Next.js 성능 보조 스킬 비활성 안내 후 계속 |
| `constitution.md` | 권장 | "헌법 검증이 비활성화됩니다" 안내 후 계속 |
| `designs/claude-design/` | 권장 | 폴더 생성. Claude가 만든 HTML을 여기에 넣으면 최우선 디자인 헌법으로 사용 |
| `designs/design.md` | 권장 | "디자인 시스템 기준이 비활성화됩니다. 디자인 소스가 있다면 /altool design_source 실행" 안내 후 계속 |
| `designs/` 사용자 디자인 입력 | 선택 | `claude-design/*.html`은 oneshot/freedom에서 `design_source` 자동 실행, `.pen`/Stitch는 `/altool design_source`, 스크린샷/디자인 문서는 plan/spec에서 직접 참조 |
| `prd/` 폴더 | 선택 | 생성 |

**4단계 — 완료 안내:**

완료 전 `.altool/checks/setup.setup.json`을 작성하고 `python altool/scripts/check.py validate --json .altool/checks/setup.setup.json`를 실행한다. 실패하면 메시지를 보고 보완한 뒤 재검증하며, 최대 5회 실패 시 중지한다. 완료 안내에는 Step Check 요약을 포함한다:

| 항목 | 보고 기준 |
| --- | --- |
| `inputs.loaded` | CLAUDE.md/altool 엔진 확인 결과 |
| `lesson.search` | `skipped(not applicable)` |
| `event.capture` | `skipped(setup step)` — 코드 오류 lesson을 append하지 않는다 |
| `verification` | Node.js 확인 결과 |
| `state.updated` | 초기 설치는 `skipped(no active feature)` |
| `docs.synced` | `skipped(no feature docs)` |
| `document.status` | `skipped(no feature docs)` |
| `artifacts.created` | 필요한 폴더/자산 확인·생성 결과 |

```
🐣 Altool 초기 설치 완료!

다음 중 하나로 시작하세요:
  • /altool research [조사 주제]             ← 먼저 조사
  • /altool oneshot [만들고 싶은 기능 설명]  ← 한 번에 자동 개발
  • /altool design_source                          ← Claude HTML/.pen/Stitch로 디자인 시스템을 만들 때
  • /altool guide                           ← 뭘 해야 할지 모르겠다면
```

---

## 세션 재개 모드

1. `altool/steps/status.md`의 절차를 수행해 현황과 최근 이력을 출력한다.
2. 마지막 phase 기준 다음 단계 명령을 안내한다.
3. `CLAUDE.md`(프로젝트 루트)의 현재 개발 상태 섹션이 있으면 최신 상태로 갱신한다.
4. `.altool/checks/setup.resume.json`을 작성하고 `python altool/scripts/check.py validate --json .altool/checks/setup.resume.json`를 실행한다. 실패하면 메시지를 보고 보완한 뒤 재검증하며, 최대 5회 실패 시 중지한다. 완료 안내에는 Step Check 요약을 포함한다. setup/resume 중 오류·차단은 안내에 남기며 lesson 이벤트로 기록하지 않는다.

