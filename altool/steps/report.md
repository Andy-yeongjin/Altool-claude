# /altool report — 완료 보고서

**산출물**: `docs/04-report/{기능명}.report.md`

---

## 절차

`/altool report` 뒤 입력은 현재 feature 완료 보고서 작성 방식에 대한 추가 지시다. 기능명으로 해석하거나 `currentFeature`를 전환하지 않는다.

### 0. 템플릿 로딩 (MANDATORY)

`altool/templates/report.template.md`를 파일 읽기 도구로 읽고 그 절 구조를 아웃라인으로 사용한다.

### 1. Match Rate 확인

- 기능명은 `.altool/state/status.json`의 `currentFeature`에서 읽는다. `currentFeature`가 없으면 `/altool plan {기능 설명}` 먼저 실행을 안내하고 중단한다.
`.altool/state/status.json`의 matchRate < 90%면 경고 후 사용자에게 진행 여부 확인.
- UI가 있는 기능인데 `docs/03-analyze/{기능명}.browser.md`가 없으면 `/altool browser`를 먼저 실행하라고 안내하고 중단한다. 사용자가 명시적으로 브라우저 검증 생략을 지시한 경우에만 생략 사유를 보고서에 남기고 계속한다.

### 2. 상류 문서 전체 로딩

PRD→코드까지 전체 여정이 보고서에 반영되도록 모두 읽는다 (없는 것은 N/A):
- PRD — 원래 가치 제안 vs 실제 전달된 가치 비교
- Plan — 계획된 Requirements/Success Criteria vs 실제 결과
- Spec — 아키텍처 결정과 이탈 사항
- Analyze 문서 — 최종 Match Rate와 해소된 갭
- `docs/03-analyze/{기능명}.fix.md` — 개선 이력
- `docs/03-analyze/{기능명}.browser.md` — 실제 브라우저 기능·디자인 검증 결과

**Altool 확장**: `npm run build` 1회 실행해 최종 빌드 성공 여부 기록 (헌법 제10조). git 저장소면 `git status`로 변경 파일 수집.

### 3~7. 보고서 작성

템플릿 절 구조대로 작성. 핵심:
- **§1.2 전달된 가치**: 계획(Plan Executive Summary) 대비 실제 달성을 측정값과 함께 대조
- **§1.3 Success Criteria 최종 판정**: Plan의 SC 각각 ✅ 충족(증거) / ❌ 미충족(사유) + 충족률
- **§2 핵심 결정 기록(ADR)**: Plan→Spec 체인의 핵심 결정 — 지켜졌는가? 결과는? (**다음 개발 사이클을 위한 학습 기록** — 헌법 제12조 ADR과 동일한 목적)
- **§4.1 기능 요구사항 최종**: FR별 이행 상태
- **§4.2 이월 항목**: 다음 사이클로 이월된 항목 + 사유
- **§5 품질 지표**: 최종 Match Rate, 디자인 시스템 준수, 브라우저 기능·디자인 검증, 빌드 결과
- **§6 회고**: Keep / Problem / Try — 회고는 보고서에만 남긴다. Report 작성 중에는 `lesson.py append`를 실행하지 않는다. 사용자가 별도로 `/altool lesson ...`을 요청한 경우에만 수동 기록한다.

### 8. Executive Summary 출력 (MANDATORY)

보고서 완성 후 **Executive Summary 표를 응답에 직접 출력**한다.

### 9~10. 상태 갱신 + 완료 보고

`.altool/state/status.json`: `phase: "completed"`.
**문서 동기화** (Altool 공통 규칙): plan §9 Next Steps 잔여 항목과 analyze 문서 §8 다음 단계의 "보고서 작성" 항목을 `- [x]`로 갱신. 미래 작업(다음 사이클·배포)은 미체크 유지.

문서 상단 상태 동기화:
- plan 문서 상단 `상태`/`Status`를 `Completed`로 갱신한다.
- spec 문서 상단 `상태`/`Status`를 `Finalized`로 갱신한다.
- analyze/fix/browser 문서 상단 `상태`/`Status`를 최종 결과에 맞춰 `Resolved` 또는 `Verified`로 갱신한다.
- report 문서 상단 `상태`/`Status`는 `Completed`로 작성한다.
- 체크박스가 모두 완료되어도 상단 상태를 그대로 `Draft`로 두지 않는다.
- plan/spec/analyze/fix/browser 문서를 수정했으면 report Step Check만으로 끝내지 않는다. 수정된 문서의 소유 Step Check(`{기능명}.plan.json`, `{기능명}.spec.json`, `{기능명}.analyze.json`, `{기능명}.fix.json`, `{기능명}.browser.json`)도 최신 내용으로 갱신하고 각각 `check.py validate`를 통과시킨 뒤, report check의 `docs.synced` 증거에 갱신한 check 경로를 남긴다.

완료 전 `.altool/checks/{기능명}.report.json`을 작성하고 `python altool/scripts/check.py validate --json .altool/checks/{기능명}.report.json`를 실행한다. 실패하면 메시지를 보고 보완한 뒤 재검증하며, 최대 5회 실패 시 중지한다. 완료 보고에는 Step Check 요약을 포함한다:

| 항목 | 보고 기준 |
| --- | --- |
| `inputs.loaded` | PRD/plan/spec/analyze/fix/browser 문서 로딩 결과 |
| `lesson.search` | `skipped(document-only step)` |
| `event.capture` | `skipped(document-only step)` — Report 작성 중에는 lesson 이벤트를 append하지 않는다 |
| `verification` | 최종 빌드/status 확인 결과 |
| `state.updated` | phase=completed |
| `docs.synced` | plan/analyze/report 상태 동기화 결과, 수정된 소유 Step Check 재검증 경로 |
| `document.status` | plan=Completed, spec=Finalized, report=Completed 등 상단 Status 최종 동기화 |
| `artifacts.created` | `docs/04-report/{기능명}.report.md` |

```
🐣 [al:report] {기능명} 완료 — 산출물: docs/04-report/{기능명}.report.md
   최종 Match Rate: {N}% | 빌드: {성공/실패} | 반복: {iterationCount}회
   🐥 {기능명} 개발 사이클 완주
   다음: 새 기능 /altool plan {기능 설명} 또는 배포 (guides/neondb-guide.html → guides/vercel-guide.html)
```





