# /altool research — 웹 조사 단계

**사용법**: `/altool research [조사 주제]`

**산출물**: `docs/00-research/R-0001-{조사주제}.research.md`
**UI 작업 추가 산출물**: 디자인 시스템이 없거나 비어 있거나 첫 non-empty line에 `TBD`가 있으면 `designs/design.md`

---

## 역할

`research`는 개발을 시작하기 전 시장·사용자·기능·페이지 구성을 조사하는 독립 단계다. 이 단계는 어떤 feature도 확정하지 않고, `.altool/state/status.json`의 `currentFeature`를 만들거나 바꾸지 않는다.

사용자는 마음에 들 때까지 여러 번 조사할 수 있다. 실제로 무엇을 만들지는 이후 `/altool plan {기능 설명}`에서 결정한다.

---

## 절차

### 0. 입력 확인

- `/altool research` 뒤 조사 주제가 비어 있으면 `사용법: /altool research {조사 주제}`를 안내하고 중단한다.
- 조사 주제는 문서 제목과 검색 키워드의 기준으로만 사용한다. 기능명으로 확정하지 않는다.

### 1. 템플릿 로딩 (MANDATORY)

`altool/templates/research.template.md`를 파일 읽기 도구로 읽고 그 절 구조를 문서 아웃라인으로 사용한다. 기억이나 추측으로 Research 문서를 생성하지 않는다.

### 2. 기존 조사와 입력 자산 확인

- `docs/00-research/*.research.md`가 있으면 최근 조사 목록을 읽고 중복 주제·이미 수집한 출처를 확인한다.
- `prd/*.md`, `prd/refs/*`, `constitution.md`, `designs/design.md`가 있으면 조사 관점 보정용으로 읽는다.
- `designs/claude-design/*.html`이 있으면 최우선 디자인 헌법으로 기록하고, 외부 사이트·`designs/design.md`·기타 사용자 디자인 입력보다 먼저 읽는다. Research는 이 HTML의 구조·밀도·위계·컴포넌트 외형을 대체하지 않고, 기능·UX·누락 위험 보강재로만 사용한다.
- `designs/` 안에 사용자가 넣은 `.pen`, `stitch/`, 스크린샷(`*.png`, `*.jpg`, `*.jpeg`, `*.webp`), 디자인 문서(`*.md`, `*.pdf`)가 있으면 외부 사이트보다 우선하는 사용자 디자인 입력으로 기록한다. Research는 이 디자인을 대체하지 않고, 기능·UX·누락 위험·페이지 구성 보강재로만 사용한다.
- PRD가 있으면 research는 PRD를 변경하거나 대체하지 않고, PRD를 더 잘 구현하기 위한 사용자 기대·누락 위험·UX 근거·리스크·구현 후보를 찾는 데 집중한다.
- UI/제품/사이트/앱을 조사하는데 `designs/design.md`가 없거나 비어 있거나 첫 non-empty line에 `TBD`가 있으면, research 단계에서 참조 사이트와 사용자 디자인 입력을 근거로 `design.md`를 생성한다. 이후 plan/spec/run은 research의 시각 관찰값을 직접 구현하지 않고 이 파일을 구현 기준으로 사용한다.
- 디자인 기준 우선순위는 `designs/claude-design/*.html` → `designs/` 사용자 디자인 입력(`.pen`, Stitch, 스크린샷, 디자인 문서) → `designs/design.md` → Research가 생성한 디자인 시스템 → AI 자체 판단 순서다.
- `constitution.md`의 디자인 품질 원칙은 모든 시각 원천에 항상 적용되는 상위 가드레일이다.
- Research는 문서/조사 단계이므로 `lesson.py search`와 `lesson.py append`를 실행하지 않는다.

### 3. 웹 조사 수행

웹 검색을 사용해 조사 주제와 가까운 실제 제품·서비스·문서·블로그·커뮤니티 글을 수집한다. Research의 목적은 자료 요약이 아니라 **다음 plan에서 바로 쓸 수 있는 판단 재료**를 만드는 것이다. PRD가 있을 때 이 판단 재료는 PRD 요구사항을 더 잘 구현하기 위한 보강 근거이며, PRD 범위를 임의로 넓히는 근거가 아니다.

최소 기준:

- 출처 8개 이상을 검토한다. `oneshot` quick research처럼 빠른 조사일 때도 5개 미만으로 낮추지 않는다.
- 실제 서비스/제품 3개 이상, UX/리서치/공식 문서 3개 이상, 사용자 목소리(커뮤니티·리뷰·앱스토어·이슈) 1개 이상을 포함한다.
- UI/제품/사이트/앱 조사라면 실제 서비스/제품 참조 중 최소 3개는 화면 캡처를 남긴다. 각 서비스당 핵심 화면 1~3장만 캡처하고, `docs/00-research/assets/{Research ID}/` 아래 저장한다.
- 법·보안·접근성·성능·플랫폼 정책처럼 도메인 리스크가 있는 주제는 해당 기준 출처 1개 이상을 포함한다.
- 각 출처의 URL과 접근일을 기록한다.
- 각 출처마다 `신뢰도(A/B/C)`, `최신성(current/stable/old)`, `핵심 근거`, `한계`를 기록한다.
- 특정 사이트의 문장·카피·로고·고유 이미지·식별 가능한 브랜드 스타일·정확한 레이아웃은 그대로 복제하지 않고, 기능 패턴·페이지 구조·사용자 기대·주의점을 추출한다.
- 외부 사이트 디자인 사례에서는 색상 팔레트, 브랜드 분위기, 타이포 스케일, 간격 리듬, 정보 밀도, 시각 위계, 테두리/그림자 강도, 둥글기, 컴포넌트 비례, 내비게이션 패턴, 인터랙션 affordance를 조사한다.
- UI/제품/사이트/앱 조사에서 캡처를 남겼다면, research는 감상 요약에서 끝나지 않고 **구현 가능한 추출물**을 만들어야 한다. 각 캡처에서 화면 순서, section 높이/폭 비례, 이미지와 텍스트의 배치 방식, nav 형태, CTA 위치, 카드 이미지 비율, 버튼/칩/폼 외형, 표면/구분선/그림자 사용, 모바일 접힘 방식을 추출해 `Screen Recipe`, `Component Extraction`, `Capture-to-Implementation Map`으로 기록한다.
- `Screen Recipe`는 특정 브랜드를 복제하기 위한 지문이 아니라, 새 제품에 적용할 화면 구조 계약이다. 문구·로고·고유 이미지·식별 가능한 고유 배치는 복제하지 않되, 페이지 구조·밀도·비례·섹션 순서·컴포넌트 외형 값은 구체적으로 가져온다.
- `Screen Recipe`에는 AI식 drift 금지 항목도 함께 쓴다. 예: 참조에 없는 split SaaS hero, 떠 있는 trust card 묶음, 과한 gradient overlay, glass panel, 추상 장식, 카드 중첩, reference density보다 느슨한 빈 화면.
- 폰트는 참조 사이트의 computed `font-family`, 역할별 크기·굵기·행간·자간, 제목/본문/메타/버튼의 사용 차이를 조사한다. 단, 참조 사이트의 폰트 파일을 복제하지 않는다.
- `design.md`는 GitHub `awesome-design-md` 스타일을 따른다. 즉 문서 상단에 `---`로 감싼 정밀 토큰 블록을 먼저 작성하고, 그 안에 `version`, `name`, `description`, `colors`, `typography`, `spacing`, `rounded`, `elevation`, `components`를 채운다. 아래 본문은 브랜드 문법과 구현 가이드다.
- `design.md`에는 참조 폰트 이름, 시각적 성격(geometric sans, grotesk, humanist, serif 등), 역할별 스케일, 구현에 사용할 안전한 폰트 스택을 기록한다. 구현 폰트는 시스템 폰트, 오픈 라이선스 폰트, 사용자가 제공한 폰트, 프로젝트에 이미 포함된 폰트만 사용한다.
- 동일 폰트를 사용할 수 없으면 시각 특성이 가까운 대체 폰트를 선택하고, `design.md`에 대체 사유를 남긴다.
- 캡처는 복제용이 아니라 레이아웃 구조, 정보 밀도, 컴포넌트 비율, 미디어 사용, 시각 위계를 분석해 `designs/design.md`로 정규화하기 위한 근거다. 캡처할 수 없는 출처는 실패 사유를 기록하고, HTML/문서/공개 이미지 등 대체 시각 근거를 남긴다.
- Research가 `designs/design.md`를 생성·보강한다면 `design.md`의 `Reference Source Map`에도 캡처 ID와 파일 경로를 반드시 남긴다. Research 문서에만 캡처 경로가 있고 `design.md`에는 출처명만 있으면 추적성 미완성으로 본다.
- 디자인 자유도는 "AI가 임의로 일반 SaaS/AI 미감을 만드는 것"이 아니다. 조사한 실제 서비스의 시각 패턴을 새 제품에 맞게 변환해 `design.md`로 정규화하는 것이다.
- 프로젝트에 Claude 디자인 HTML이나 사용자 디자인 입력이 있으면 Research는 그 디자인의 빈칸을 보강하는 용도로만 외부 사례를 사용한다. 화면 구조, 정보 밀도, 시각 위계, 색상·간격·타이포·둥글기·그림자는 `designs/claude-design/*.html`을 최우선으로 디자인 시스템에 변환한다.
- 프로젝트에 `designs/design.md`가 있고 첫 non-empty line에 `TBD`가 없으며 프로젝트 고유 내용이 있으면 기존 디자인 시스템을 구현 기준으로 유지하고, research 문서에는 보강 필요 지점만 기록한다. 사용자가 명시하지 않은 한 기존 디자인 시스템을 덮어쓰지 않는다.
- 프로젝트에 `designs/design.md`가 없거나 비어 있거나 첫 non-empty line에 `TBD`가 있으면 research 완료 전 파일을 생성한다. 생성된 `design.md`에는 GitHub `awesome-design-md` 스타일의 상단 정밀 토큰 블록, 참조 출처와 캡처 ID/경로, Design Thesis, Screen Recipes, Component Extraction, Capture-to-Implementation Map, 색상·타이포·폰트 스택·간격 값, 컴포넌트 계약, 페이지 구조, 미디어 규칙, 복제 금지 항목, Agent Implementation Guide를 기록하고 최상단 `TBD` 마커를 제거한다.
- 외부 디자인 사례가 프로젝트 디자인 시스템이나 `constitution.md`의 디자인 품질 원칙과 충돌하면 research 문서에 충돌을 기록하고, 디자인 시스템에는 프로젝트 기준으로 보정한 값을 반영한다.
- 이전 research가 있으면 중복 발견과 새 발견을 분리해 기록한다.

출처 신뢰도 기준:

| 등급 | 기준 |
| --- | --- |
| A | 공식 문서, 원 연구기관, 실제 제품/서비스의 현재 문서, 법/표준/플랫폼 정책 |
| B | 전문 블로그, 벤치마크 요약, 실무 사례, 앱스토어/마켓 리뷰 |
| C | 개인 의견, 오래된 커뮤니티 글, 출처가 불명확한 큐레이션 |

최신성 기준:

| 등급 | 기준 |
| --- | --- |
| current | 최근 18개월 이내이거나 현재 제품/공식 문서 |
| stable | 오래됐지만 UX 원칙·표준처럼 변동성이 낮은 자료 |
| old | 18개월 초과이고 현재성 검증이 필요한 자료 |

품질 점수는 100점 만점으로 계산하고 Research 문서 상단과 `.altool/state/research.json`에 기록한다.

| 항목 | 배점 | 기준 |
| --- | ---: | --- |
| Source Mix | 25 | 실제 서비스, 공식/리서치, 사용자 목소리, 리스크 출처의 균형 |
| Source Quality/Freshness | 20 | A/B 신뢰도 비율, 최신성 표기, 한계 명시 |
| Evidence Mapping | 20 | 주요 주장·패턴·plan 후보가 출처 ID와 연결됨 |
| Plan Readiness | 20 | 기능·페이지·데이터·리스크 후보가 plan으로 전환 가능함 |
| Loop Value | 15 | 중복/신규 발견과 다음 조사 후보가 명확함 |

`qualityScore`가 80 미만이면 `planReadiness`를 `ready`로 표기하지 않는다. 70 미만이면 조사 보완 후 Step Check를 다시 실행한다.

조사 우선순위:

1. 실제 경쟁/유사 서비스의 페이지 구조와 핵심 흐름
2. 사용자가 기대하는 기능 목록과 누락되기 쉬운 UX
3. 구현 시 필요한 데이터 구조·상태·외부 연동 후보
4. 법적·보안·접근성·성능 리스크
5. plan에 넘길 수 있는 구체적인 기능 후보

PRD가 있는 경우 추가 조사 관점:

1. PRD 요구사항을 구현할 때 놓치기 쉬운 UX/기능 세부
2. PRD 범위 안에서 더 좋은 구현을 위한 페이지·데이터·상태 후보
3. PRD 범위 밖이지만 다음 사이클 후보로 남길 만한 발견
4. PRD와 research가 충돌하는 지점과 PRD 우선 처리 사유

### 4. 산출물 경로 확정

- `docs/00-research/`를 생성한다.
- UI/제품/사이트/앱 조사라면 `docs/00-research/assets/{Research ID}/`를 생성해 캡처 이미지를 저장한다.
- 기존 `R-0001-*.research.md` 번호를 확인하고 다음 번호를 사용한다.
- 파일명은 `R-0001-{조사주제-slug}.research.md` 형식으로 만든다.
- 같은 파일명이 있으면 번호를 증가시킨다.

### 5. Research 문서 작성

템플릿의 모든 주요 절을 채운다. 특히 아래 내용은 반드시 포함한다.

- 조사 질문
- 출처 목록
- 시각 캡처 목록과 캡처 기반 관찰
- 출처 품질 매트릭스
- 페이지/기능 인벤토리
- 공통 패턴
- Design System Bootstrap: 기존 디자인 시스템 감지 결과, 생성·재사용·보강 여부, 참조 출처, 복제 금지 항목, `design.md` 생성 요약
- Design Token Block: `design.md` 상단 `---` 블록의 colors, typography, spacing, rounded, elevation, components가 참조 기반 값으로 채워졌는지
- Screen Recipes: 캡처 기반 화면별 구조 계약, 섹션 순서, 비례, 밀도, 금지 drift
- Component Extraction: 캡처 기반 nav/button/card/form/filter/media/cart 등 컴포넌트 외형 계약
- Capture-to-Implementation Map: 각 캡처/패턴이 plan/spec/run에서 어떤 화면·컴포넌트로 구현되어야 하는지
- Typography Source Mapping: 참조 폰트 이름, 역할별 타입 스케일, 구현 폰트 스택, 라이선스/대체 사유
- 사용자 디자인 입력: `designs/claude-design/*.html`, `designs/` 안의 `.pen`, Stitch, 스크린샷, 디자인 문서 감지 결과와 Research보다 우선한다는 처리 방침
- 근거 매핑
- 차별화 기회
- 리스크와 제약
- 중복/신규 발견
- plan에 넘길 후보 요구사항
- PRD 보강 포인트와 PRD 충돌/범위 밖 후보
- 헌법/디자인 적용 메모
- plan 준비도
- 품질 점수 산정 근거
- 다음 조사 후보
- 이번 조사에서 확정하지 않은 것

### 6. 조사 상태 갱신

`.altool/state/research.json`을 JSON으로 파싱해 갱신한다. 없으면 새로 만든다. 문자열 치환으로 수정하지 않는다.
Research 문서 작성과 Step Check가 통과하면 문서 상단 `상태`/`Status`를 `Done`으로 갱신한다. 작성 중 임시값인 `Draft`를 완료 산출물에 남기지 않는다.

예시:

```json
{
  "lastResearchId": "R-0001",
  "researchCount": 1,
  "updatedAt": "YYYY-MM-DD",
  "items": [
    {
      "id": "R-0001",
      "topic": "쇼핑몰",
      "file": "docs/00-research/R-0001-쇼핑몰.research.md",
      "sourceCount": 7,
      "visualCaptureCount": 3,
      "sourceMix": {
        "actualService": 3,
        "researchOrOfficial": 3,
        "userVoice": 1,
        "riskReference": 0
      },
      "qualityScore": 86,
      "planReadiness": "ready",
      "nextQueries": ["쇼핑몰 리뷰 UX", "장바구니 추천 UX"],
      "createdAt": "YYYY-MM-DD"
    }
  ]
}
```

### 7. Step Check

완료 전 `.altool/checks/R-0001.research.json`을 작성하고 `python altool/scripts/check.py validate --json .altool/checks/R-0001.research.json`를 실행한다. 실패하면 메시지를 보고 보완한 뒤 재검증하며, 최대 5회 실패 시 중지한다.

Research check JSON은 공통 `checks` 외에 root의 `quality` 객체를 포함해야 한다.

```json
{
  "schemaVersion": 1,
  "feature": "R-0001",
  "step": "research",
  "quality": {
    "score": 86,
    "planReadiness": "ready",
    "sourceCount": 9,
    "sourceMix": {
      "actualService": 3,
      "researchOrOfficial": 5,
      "userVoice": 1,
      "riskReference": 0
    },
    "nextQueryCount": 3
  },
  "checks": {}
}
```

`check.py`는 research에서 아래 조건을 직접 검증한다.

- `sourceCount >= 8`
- `sourceMix.actualService >= 3`
- `sourceMix.researchOrOfficial >= 3`
- `sourceMix.userVoice >= 1`
- `nextQueryCount >= 3`
- `quality.score < 70`이면 완료 불가
- `quality.score < 80`이면 `planReadiness: ready` 불가

| 항목 | 보고 기준 |
| --- | --- |
| `inputs.loaded` | 기존 research/PRD/refs/constitution/design 자산 확인 결과 |
| `lesson.search` | `skipped(research document step)` |
| `event.capture` | `skipped(research document step)` |
| `verification` | 웹 출처 수, 실제 서비스 수, URL 기록 확인 |
| `state.updated` | `.altool/state/research.json` 갱신 |
| `docs.synced` | 생성한 research 문서 |
| `document.status` | research 문서 상단 Status=Done |
| `artifacts.created` | `docs/00-research/R-0001-*.research.md` |
| `research.source_mix` | 실제 서비스/공식·리서치/사용자 목소리/리스크 기준 출처 비율 확인 |
| `research.source_quality` | 출처별 신뢰도 A/B/C와 한계 기록 |
| `research.freshness` | 출처별 최신성 current/stable/old 기록 |
| `research.duplicate_review` | 기존 research 대비 중복 발견과 새 발견 분리 |
| `research.evidence_map` | 각 주요 주장에 출처 ID 연결 |
| `research.visual_capture` | UI/제품/사이트/앱 조사면 실제 서비스/제품 3개 이상 캡처와 `docs/00-research/assets/{Research ID}/` 경로 연결. 비 UI 조사면 `skipped(non-UI research)`, 접근 실패면 실패 사유와 대체 근거 |
| `research.design_system` | UI 작업에서 `designs/design.md` 첫 non-empty line의 `TBD` 여부를 확인하고, 재사용했거나 생성·보강 후 `TBD` 마커를 제거했는지 확인. 생성·보강한 경우 `design.md` 상단 정밀 토큰 블록, Reference Source Map, Screen Recipes, Component Extraction, Capture-to-Implementation Map에 캡처 ID/경로와 구현 계약이 남았는지 증거 포함 |
| `research.design_tokens` | UI 작업이면 `design.md` 상단 `---` 토큰 블록에 colors, typography, spacing, rounded, elevation, components가 참조 기반 값으로 채워졌는지 확인 |
| `research.screen_recipe` | UI 작업이면 캡처 기반 화면별 구조 계약, 섹션 순서, 비례·밀도, 금지 drift가 research 문서와 `design.md`에 기록됐는지 확인 |
| `research.component_extraction` | UI 작업이면 nav/button/card/filter/form/media 등 컴포넌트 외형 계약이 캡처 ID와 연결돼 기록됐는지 확인 |
| `research.capture_map` | UI 작업이면 캡처/출처가 구현 section/component와 연결되어 plan/spec/run/browser에서 대조 가능하게 기록됐는지 확인 |
| `research.plan_readiness` | plan에 넘길 수 있는 후보 요구사항·페이지·데이터가 충분한지 평가 |
| `research.next_queries` | 다음 research 루프가 이어갈 질문 3개 이상 |

### 8. 완료 보고

사용자가 파일을 열지 않아도 볼 수 있도록 핵심 조사 결과를 짧게 출력한다.

```
🐣 [al:research] R-0001 완료 — 산출물: docs/00-research/R-0001-{조사주제}.research.md
   핵심 패턴: {3개}
   디자인 시스템: {재사용/생성/보강 제안}
   plan 후보: {3개}
   다음 단계: /altool plan {만들 기능 설명}
```
