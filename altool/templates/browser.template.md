> 지침: 모든 내용은 반드시 한글로 작성합니다 (헌법 제0조).

# {기능명} — Browser Verification

> **Status**: Draft / Verified / Failed
> **작성일**: YYYY-MM-DD
> **대상 URL**: {http://localhost:3000 등}
> **검증 도구**: Playwright(MCP/로컬) / 기타 브라우저 자동화

---

## 1. 입력 자료

| 자료 | 경로 | 로딩 결과 |
| --- | --- | --- |
| Plan | `docs/01-plan/features/{기능명}.plan.md` | |
| Spec | `docs/02-spec/features/{기능명}.spec.md` | |
| Analyze | `docs/03-analyze/{기능명}.analyze.md` | |
| Fix | `docs/03-analyze/{기능명}.fix.md` | |
| Design | `designs/design.md` | |
| User Design Source | `designs/*.pen`, `designs/stitch/`, `designs/*.{png,jpg,jpeg,webp}`, `designs/*.{md,pdf}` | |
| 구현 | `{app/src/components/lib/tests}` | |

## 2. 서버 상태

| 항목 | 결과 | 증거 |
| --- | --- | --- |
| 서버 실행 | ✅ / ❌ | |
| 응답 URL | | |
| 빌드/테스트 선행 결과 | | |

### 2.1 서버 생명주기

| 항목 | 결과 | 증거 |
| --- | --- | --- |
| 서버 출처 | 기존 서버 사용 / browser step이 시작 | |
| Managed server | true / false | |
| PID / 포트 | | |
| 시작 명령 | | |
| 종료 결과 | 종료 완료 / skipped(existing server) / failed | |
| 종료 후 응답 확인 | 응답 없음 / 기존 서버 유지 / 확인 실패 | |

### 2.2 실행 도구 해석

| 항목 | 결과 | 증거 |
| --- | --- | --- |
| Windows `.cmd` 사용 | `npm/npx/next` bare command 없음 / N/A | |
| `playwright.config.ts` webServer | `node_modules\\.bin\\next.cmd` 또는 OS별 로컬 next 경로 사용 / N/A | |
| Playwright 패키지 해석 | 프로젝트 루트 `node`가 로컬 `node_modules`의 Playwright를 사용 / N/A | |
| REPL fallback 회피 | persistent REPL/global Playwright 미사용 / N/A | |

## 3. 화면 방문 결과

| 화면 | URL | 결과 | 증거 |
| --- | --- | --- | --- |
| 홈 | | ✅ / ⚠️ / ❌ | |

## 4. 사용자 행동 검증

| 시나리오 | 행동 | 기대 결과 | 실제 결과 | 판정 | 증거 |
| --- | --- | --- | --- | --- | --- |
| | 클릭/입력/이동 | | | ✅ / ⚠️ / ❌ | |

## 5. 반응형·디자인 검증

| 항목 | 기준 | 결과 | 증거 |
| --- | --- | --- | --- |
| 375px 반응형 | 겹침/잘림 없음 | | |
| desktop 레이아웃 | 주요 UI 겹침 없음 | | |
| 사용자 디자인 입력 | 있으면 Spec User Design Source 기준 구조·밀도·위계 반영 | | |
| Screen Recipes | `designs/design.md`의 화면 구조·섹션 순서·비례·밀도 계약 반영 | | |
| Capture-to-Implementation Map | 참조 캡처 C-__/S-__가 구현 section/component로 연결되어 최종 화면에 반영 | | |
| Component Extraction | nav/button/card/filter/form/media 외형 계약 반영 | | |
| 디자인 시스템 | `designs/design.md`의 시각 값·컴포넌트 계약·미디어 규칙 기준 반영, 없으면 Research/design_source 보완 필요 | | |
| CSS custom properties | `python altool/scripts/check.py css-vars --root .` 통과. CSS 파일이 없으면 `skipped(no css files)` | | |
| 폰트 | `designs/design.md`의 구현 font-family stack, 크기, 굵기, 행간 기준 반영. 참조 폰트 파일 복제 없음 | | |
| Generic AI/SaaS 회귀 | Research/Spec 근거 없는 split SaaS hero, floating trust card 묶음, 과한 그라디언트, glass panel, 추상 장식, 카드 그림자 남발 없음 | | |
| 참조 복제 금지 | 로고·카피·고유 이미지·식별 가능한 레이아웃 복제 없음 | | |
| 접근성 | 버튼/폼 사용 가능, 초점 이동 가능 | | |

### 5.1 참조 캡처 대조

> 픽셀 복제가 아니라 구조·비례·밀도·섹션 순서·컴포넌트 외형·미디어 사용·타이포 위계를 대조한다.

| Design Map | 참조 캡처 | 최종 스크린샷 | 대조 기준 | 판정 | 증거/메모 |
| --- | --- | --- | --- | --- | --- |
| Screen Recipe: {Home first view} | `docs/00-research/assets/{R-ID}/C-__.png` | `docs/03-analyze/assets/{기능명}/browser-final-home-desktop.png` | {섹션 순서, hero 비례, 다음 섹션 노출, CTA 위치} | Pass / Drift / N/A | |
| Component: {Product card} | `docs/00-research/assets/{R-ID}/C-__.png` | `docs/03-analyze/assets/{기능명}/browser-final-listing-desktop.png` | {이미지 비율, 정보 순서, shadow/border, quick action} | Pass / Drift / N/A | |
| Mobile behavior | `docs/00-research/assets/{R-ID}/C-__.png` 또는 N/A | `docs/03-analyze/assets/{기능명}/browser-final-mobile-375.png` | {모바일 접힘, 주요 CTA, overflow 없음} | Pass / Drift / N/A | |

## 6. 콘솔·네트워크

| 종류 | 결과 | 증거 |
| --- | --- | --- |
| Console error | 없음 / 있음 | |
| Network failure | 없음 / 있음 | |

## 7. 발견 이슈와 수정

| ID | 심각도 | 증상 | 원인 | 수정 | 재검증 |
| --- | --- | --- | --- | --- | --- |
| B-01 | Critical / Important / Minor | | | | |

## 8. Lesson 이벤트

| 이벤트 ID | 타입 | 요약 |
| --- | --- | --- |
| E-... / none | | |

## 9. 최종 판정

- **Browser Result**: Pass / Partial / Fail
- **남은 갭**:
  - 없음
- **다음 단계**:
  - `/altool report`
