> 지침: 모든 내용은 반드시 한글로 작성합니다. 출처 URL은 원문 그대로 기록합니다.

# {조사 주제} — Research

> **Research ID**: {R-0001}
> **작성일**: YYYY-MM-DD
> **상태**: Draft <!-- Step Check 통과 후 Done으로 갱신 -->
> **품질 점수**: {0~100}
> **Plan 준비도**: ready | partial | not-ready
> **요약**: {이번 조사에서 얻은 핵심 결론 한 줄}

---

## 1. 조사 질문

- {이번 조사가 답하려는 질문 1}
- {질문 2}
- {질문 3}

## 2. 조사 범위

| 구분 | 내용 |
| --- | --- |
| 포함 | {조사 대상} |
| 제외 | {이번 조사에서 다루지 않는 것} |
| 기준 사용자 | {대상 사용자} |

## 3. 출처

| ID | 유형 | 이름 | URL | 확인일 | 신뢰도 | 최신성 | 사용 이유 | 한계 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S-01 | 실제 서비스 | {서비스명} | {URL} | YYYY-MM-DD | A/B/C | current/stable/old | {왜 참고했는지} | {주의할 점} |
| S-02 | 문서/블로그/커뮤니티 | {이름} | {URL} | YYYY-MM-DD | A/B/C | current/stable/old | {왜 참고했는지} | {주의할 점} |

## 3.1 시각 캡처

> UI/제품/사이트/앱 조사라면 실제 서비스/제품 참조 중 최소 3개는 캡처한다. 캡처는 복제용이 아니라 레이아웃 구조, 정보 밀도, 컴포넌트 비율, 미디어 사용, 시각 위계를 `designs/design.md`로 정규화하기 위한 근거다.

저장 경로: `docs/00-research/assets/{Research ID}/`

| 캡처 ID | 출처 ID | 화면/상태 | 파일 경로 | 관찰한 시각 근거 | `design.md` 반영 |
| --- | --- | --- | --- | --- | --- |
| C-01 | S-01 | {홈/목록/상세/주문/대시보드 등} | `docs/00-research/assets/{Research ID}/C-01-...png` | {구조/밀도/비율/미디어/위계} | {반영할 디자인 규칙} |
| C-02 | S-02 | | | | |
| C-03 | S-03 | | | | |

캡처 불가 출처:

| 출처 ID | 사유 | 대체 시각 근거 |
| --- | --- | --- |
| {S-__ 또는 없음} | {로그인 필요/차단/동적 렌더 실패 등} | {공식 이미지/문서 설명/HTML 구조/텍스트 관찰 등} |

## 4. 출처 품질 매트릭스

| 항목 | 기준 | 결과 |
| --- | --- | --- |
| 총 출처 수 | 8개 이상 | {N}개 |
| 실제 서비스/제품 | 3개 이상 | {N}개 |
| 실제 서비스/제품 캡처 | UI 조사 시 3개 이상 | {N}개 / N/A |
| UX/리서치/공식 문서 | 3개 이상 | {N}개 |
| 사용자 목소리 | 1개 이상 | {N}개 |
| 리스크 기준 출처 | 필요 시 1개 이상 | {N/A 또는 N개} |
| A/B 신뢰도 비율 | 전체의 70% 이상 권장 | {N}% |

## 5. 품질 점수 산정

| 항목 | 배점 | 점수 | 근거 |
| --- | ---: | ---: | --- |
| Source Mix | 25 | {0~25} | {출처 유형 균형 근거} |
| Source Quality/Freshness | 20 | {0~20} | {신뢰도·최신성·한계 기록 근거} |
| Evidence Mapping | 20 | {0~20} | {주장과 출처 연결 근거} |
| Plan Readiness | 20 | {0~20} | {기능·페이지·데이터·리스크 후보 충분성} |
| Loop Value | 15 | {0~15} | {중복/신규 발견과 다음 조사 후보 근거} |
| **합계** | **100** | **{0~100}** | qualityScore |

## 6. 페이지·기능 인벤토리

| 영역 | 관찰된 페이지/기능 | 사용자 목적 | plan 반영 후보 |
| --- | --- | --- | --- |
| 탐색 | {예: 카테고리, 검색, 필터} | {목적} | High/Med/Low |
| 상세 | {예: 상품 상세, 리뷰, 추천} | {목적} | High/Med/Low |
| 전환 | {예: 장바구니, 결제, 가입} | {목적} | High/Med/Low |

## 7. 공통 패턴

- **패턴 1**: {여러 출처에서 반복된 구조/기능}
- **패턴 2**: {반복된 UX 기대}
- **패턴 3**: {반복된 데이터/상태 흐름}

## 8. 근거 매핑

| 주장/관찰 | 근거 출처 | 확신도 | plan 반영 |
| --- | --- | --- | --- |
| {주장 1} | S-01, S-03 | High/Med/Low | FR/SC/Risk/Out of Scope |

## 9. PRD 보강/충돌 메모

> PRD가 있으면 Research는 PRD 구현 보강재다. PRD를 덮어쓰지 않는다.

| 구분 | 내용 | 처리 제안 |
| --- | --- | --- |
| PRD 보강 | {PRD 요구사항을 더 잘 구현하기 위한 세부/리스크/UX 근거} | plan 반영 후보 |
| PRD 범위 밖 후보 | {좋지만 PRD에 없는 기능} | 다음 사이클/Out of Scope |
| PRD와 충돌 | {충돌 내용 또는 없음} | PRD 우선/사용자 확인 필요 |

## 10. 헌법/디자인 적용 메모

> 외부 사례는 기능과 시각 디자인의 조사 원천이다. 문장·카피·로고·고유 이미지는 복제하지 않는다.
> 가져올 수 있는 것: 페이지 구조, 정보 배치, 기능 흐름, 인터랙션 의도, 사용자 기대, 색상 팔레트, 브랜드 분위기, 타이포 스케일, 간격, 그림자, 둥글기, 컴포넌트 외형 값, 정보 밀도, 위계, 비례, 네비게이션 패턴.
> 폰트는 참조 사이트의 `font-family` 이름과 역할별 크기·굵기·행간·자간을 조사하되, 폰트 파일은 복제하지 않는다. 구현에는 시스템 폰트, 오픈 라이선스 폰트, 사용자 제공 폰트, 프로젝트 포함 폰트만 사용한다.
> `designs/`에 사용자가 넣은 `.pen`, Stitch, 스크린샷, 디자인 문서가 있으면 그 자산이 시각 기준 1순위다. Research는 외부 사례를 그 디자인의 빈칸을 보강하는 근거로만 사용한다.
> `designs/design.md`가 있고 첫 non-empty line에 `TBD`가 없으며 프로젝트 고유 내용이 있으면 기존 디자인 시스템을 구현 기준으로 유지한다. 파일이 없거나 비어 있거나 첫 non-empty line에 `TBD`가 있으면 Research 단계에서 참조 사이트와 사용자 디자인 입력을 근거로 `design.md`를 생성한다.
> Research가 `design.md`를 생성·보강하면 `Reference Source Map`에 캡처 ID와 파일 경로를 반드시 남긴다.

### 10.1 디자인 입력 우선순위

| 우선순위 | 입력 | 감지 경로 | 처리 |
| ---: | --- | --- | --- |
| 1 | 사용자 디자인 입력 | `designs/*.pen`, `designs/stitch/`, `designs/*.{png,jpg,jpeg,webp}`, `designs/*.{md,pdf}` | 화면 구조와 시각 기준의 원천 |
| 2 | 프로젝트 디자인 시스템 | `designs/design.md` | 사용자 디자인 입력과 참조 사이트 분석을 구현 가능한 디자인 명세로 정규화 |
| 3 | Research 기반 디자인 시스템 생성 | `docs/00-research/*.research.md` + 참조 사이트 | 디자인 시스템이 없거나 빈칸이 있을 때 `design.md` 생성·보강 근거 |
| 4 | AI 자체 판단 | 없음 | 위 입력으로도 결정되지 않는 세부만 보완 |

| 구분 | 외부 사례/관찰 | 프로젝트 기준 처리 |
| --- | --- | --- |
| 사용자 디자인 입력 | {없음 또는 .pen/Stitch/스크린샷/디자인 문서 경로} | {시각 기준 1순위 / 없음} |
| 디자인 시스템 | {기존 파일 있음/없음, 생성 또는 재사용 여부} | {`designs/design.md` 경로와 처리 요약} |
| 접근성/반응형 | {외부 UX 패턴} | constitution.md의 디자인 품질 원칙 유지 |
| 충돌 항목 | {있으면 기록, 없으면 없음} | 외부 사례 제외/보정/사용자 확인 |

## 11. Design System Bootstrap

> 참조 사이트를 그대로 복제하지 않는다. 브랜드, 로고, 고유 카피, 식별 가능한 레이아웃, 고유 이미지는 사용하지 않는다.
> 대신 실제 서비스에서 반복되는 시각 패턴을 추출해 새 제품에 맞는 `designs/design.md`로 정규화한다.
> `design.md`가 이미 있더라도 첫 non-empty line에 `TBD`가 있으면 템플릿 상태로 보고 이번 research에서 프로젝트 고유 디자인 시스템으로 채운다. 사용자가 명시하지 않은 한 `TBD`가 없는 기존 디자인 시스템은 덮어쓰지 않는다.

### 11.1 디자인 시스템 상태

| 항목 | 상태 | 근거/경로 |
| --- | --- | --- |
| 기존 `design.md` | 없음/비어 있음/TBD 템플릿/확정됨 | `designs/design.md` 첫 non-empty line 확인 |
| 사용자 디자인 입력 | 있음/없음 | {`.pen`, Stitch, 스크린샷, 디자인 문서 경로} |
| Research 처리 | 재사용/생성/보강 제안 | {없거나 비어 있거나 TBD면 생성, 확정본이면 처리 요약} |

### 11.2 복제 금지

| 항목 | 금지 내용 | 처리 |
| --- | --- | --- |
| 브랜드/로고 | {참조 서비스의 고유 브랜드 요소} | 사용하지 않음 |
| 카피/문장 | {고유 문구/마케팅 카피} | 새 제품 문맥으로 재작성 |
| 고유 레이아웃 | {식별 가능한 화면 구성} | 구조 원리는 차용하되 배치는 재구성 |
| 고유 이미지 | {제품 이미지/사진/일러스트} | 사용하지 않음 |

### 11.3 참조 시각 패턴과 디자인 시스템 변환

| 항목 | 참조 출처 | 관찰 내용 | `design.md` 반영 |
| --- | --- | --- | --- |
| 정보 밀도 | S-__ / C-__ | {예: 카드당 메타 3개, KPI는 4개 이하} | {구현 기준} |
| 시각 위계 | S-__ / C-__ | {예: headline/meta/action의 크기 차이} | {구현 기준} |
| 타이포 스케일 | S-__ / C-__ | {예: 제목/본문/메타 크기감} | {역할별 폰트, 크기, 굵기, 행간} |
| 간격 리듬 | S-__ / C-__ | {예: 섹션/카드/행 간격} | {spacing scale과 사용 위치} |
| 테두리·그림자 | S-__ / C-__ | {예: 1px border 중심, shadow 최소} | {surface/elevation 규칙} |
| 둥글기 | S-__ / C-__ | {예: 작은 radius, pill chip만 full} | {shape scale과 사용 위치} |
| 컴포넌트 비례 | S-__ / C-__ | {예: sidebar 폭, 카드 aspect, 버튼 높이} | {컴포넌트 계약} |
| 내비게이션/상호작용 | S-__ / C-__ | {예: compact nav, inline filter, modal affordance} | {구현 기준} |

### 11.4 Screen Recipes

> 캡처를 보고 난 뒤의 감상 요약이 아니라, run 단계가 그대로 구현 기준으로 쓸 화면 구조 계약을 작성한다.
> 브랜드·문구·고유 이미지는 복제하지 않지만, 화면 구조·비례·밀도·섹션 순서·컴포넌트 외형은 구체적으로 추출한다.

| 화면/상태 | 참조 캡처 | 가져올 구조 | 비례·밀도 계약 | 금지 drift | `design.md` 반영 |
| --- | --- | --- | --- | --- | --- |
| Home first view | C-__ | {예: promo bar → compact nav → editorial product image → collection teaser} | {예: hero image가 first view의 60% 이상, 상품 섹션 일부 노출} | {예: split SaaS hero, floating trust cards, 추상 gradient} | {design.md Screen Recipe 이름} |
| Product listing | C-__ | {예: image-led product grid, filter 위치} | {예: image 65~75%, card meta 3~4줄} | {예: badge 과다, shadow card 남발} | {design.md Screen Recipe 이름} |
| Cart / checkout | C-__ / S-__ | {예: summary와 form의 관계, 오류 위치} | {예: summary 폭, form field 높이, 모바일 접힘} | {예: 실제 결제로 오해되는 카드 입력} | {design.md Screen Recipe 이름} |

### 11.5 Component Extraction

> 컴포넌트별로 “무엇처럼 보이는가”를 추상 형용사 대신 구현 가능한 외형 계약으로 기록한다.

| 컴포넌트 | 참조 캡처 | 추출한 외형 | 상태/상호작용 | 구현 계약 | 복제 금지 |
| --- | --- | --- | --- | --- | --- |
| Navigation | C-__ | {높이, 정렬, 링크 형태, 배경/구분선} | {sticky/active/hover} | {구현할 nav 구조} | {브랜드 로고/고유 카피} |
| Primary CTA | C-__ | {shape, fill, border, height, weight} | {hover/focus/disabled} | {버튼 계약} | {원문 CTA} |
| Product card | C-__ | {이미지 비율, 정보 순서, 가격 위치, border/shadow} | {hover/add state} | {카드 계약} | {참조 제품 이미지} |
| Filter / chip | C-__ | {inline/pill/tab, active 표현} | {pressed/focus} | {필터 계약} | {고유 카테고리명} |
| Form field | S-__ / C-__ | {label 위치, 오류 위치, 높이, border} | {invalid/success/focus} | {폼 계약} | {실제 결제 입력 오인} |
| Media | C-__ | {사진 크롭, aspect, subject 위치, 밝기} | {loading/responsive} | {generated/owned media 규칙} | {보호 이미지} |

### 11.6 Capture-to-Implementation Map

> 각 캡처가 코드에서 어떤 section/component로 바뀌어야 하는지 명확히 연결한다.
> 이 표가 비어 있으면 캡처는 단순 참고 이미지로만 남아 구현에 반영되지 않는다.

| 캡처/출처 | 구현 대상 | 구현할 것 | 구현하지 않을 것 | 검증 방법 |
| --- | --- | --- | --- | --- |
| C-__ | `{page/section/component}` | {구조·비례·밀도·컴포넌트 외형} | {브랜드/카피/이미지/고유 배치} | {browser/analyze에서 볼 증거} |
| S-__ | `{page/section/component}` | {UX 흐름·상태·리스크} | {범위 밖 기능} | {테스트/브라우저 증거} |

### 11.7 `designs/design.md` 작성 구조

> `design.md`는 CSS 변수 파일의 보조 문서가 아니라 구현자가 읽는 단일 디자인 원천이다.
> GitHub `awesome-design-md`처럼 상단에는 정밀 토큰 블록을 두고, 본문에는 브랜드 문법과 구현 계약을 쓴다.

0. **Design Token Block**: 문서 최상단 `---` 블록에 `version`, `name`, `description`, `colors`, `typography`, `spacing`, `rounded`, `elevation`, `components`를 작성
   - `colors`: semantic color name, hex, role이 추적 가능해야 함
   - `typography`: token name, fontFamily, fontSize, fontWeight, lineHeight, letterSpacing, use
   - `spacing`: base scale과 section/card/form spacing
   - `rounded`: shape scale과 사용 위치
   - `elevation`: flat/hairline/low/overlay 등 shadow와 border depth
   - `components`: button/nav/card/input/filter/media 등 바로 코드로 옮길 component token
1. **Design Thesis**: 이 제품/사이트가 어떤 시각 언어로 보여야 하는지 한 문단으로 정의
2. **Reference Source Map**: 참조 사이트별로 차용한 구조·밀도·컴포넌트·미디어 원칙과 복제 금지 항목 기록. UI research 캡처가 있으면 캡처 ID와 파일 경로를 포함
3. **Visual Theme & Atmosphere**: 분위기, 밀도, 화면 리듬, 디자인 철학
4. **Screen Recipes**: 화면별 구조 계약, 섹션 순서, 비례, 밀도, 금지 drift
5. **Component Extraction**: nav, CTA, card, filter, form, media 등 컴포넌트별 외형 계약
6. **Capture-to-Implementation Map**: 캡처/출처가 구현 section/component로 연결되는 표
7. **Color Palette & Roles**: 의미 이름, 값, 역할. CSS 변수명이 아니라 색의 역할을 우선 기록
8. **Typography Rules**: 역할별 폰트, 크기, 굵기, 행간, 사용 위치
   - 참조 `font-family`, 폰트 성격, 구현 폰트 스택, 라이선스/대체 사유를 포함
9. **Layout Principles**: 컨테이너, 그리드, 섹션 리듬, 반응형 전환, 여백 철학
10. **Component Contracts**: 버튼, 카드, 네비게이션, 입력, 테이블, 탭, 모달, 상품 갤러리 등 컴포넌트별 모양·상태·사용 위치
11. **Media Rules**: 사진, 영상, 생성 이미지, 아이콘, 제품 이미지, 썸네일, 빈 상태 이미지 사용 규칙
12. **Depth & Elevation**: shadow, border, surface hierarchy, hover/active feedback
13. **Responsive Behavior**: 모바일/태블릿/데스크톱에서 접힘과 우선순위
14. **Do / Don't**: AI스럽게 흐르는 패턴과 참조 복제 위험을 명시적으로 금지
15. **Agent Implementation Guide**: run 단계가 바로 따를 구현 요약

### 11.8 생성/갱신 산출물 요약

| 산출물 | 처리 | 요약 |
| --- | --- | --- |
| `designs/design.md` | 생성/재사용/보강 제안 | {상단 Design Token Block, Design Thesis, 참조 맵, Screen Recipes, Component Extraction, Capture-to-Implementation Map, 캡처 ID/경로, 시각 값, 폰트 스택과 대체 사유, 컴포넌트 계약, 미디어 규칙, Do/Don't 요약. 생성·보강 완료 시 최상단 TBD 제거} |

### 11.9 Generic AI/SaaS 회피 기준

- 참조에 없는 큰 hero, 과한 그라데이션, 과도한 카드 그림자, 추상적인 AI 장식, 불필요한 glassmorphism을 임의 생성하지 않는다.
- 참조 서비스의 실제 정보 밀도와 조작 흐름을 우선한다.
- 새 제품의 브랜드 표현은 만들되, 참조 시각 패턴을 `design.md`로 정규화한 범위 안에서 변주한다.

## 12. 중복/신규 발견

| 구분 | 내용 | 근거 |
| --- | --- | --- |
| 기존 research와 중복 | {없음 또는 중복 내용} | {기존 R-ID/S-ID} |
| 이번에 새로 발견 | {새 발견} | {S-ID} |
| 이전 판단을 뒤집는 발견 | {없음 또는 변경 내용} | {S-ID} |

## 13. 차별화 기회

| 기회 | 근거 | 적용 난이도 | 우선순위 |
| --- | --- | --- | --- |
| {기회} | {출처/관찰 근거} | High/Med/Low | High/Med/Low |

## 14. 리스크와 제약

| 리스크 | 원인 | 대응 방향 |
| --- | --- | --- |
| {리스크} | {왜 생기는지} | {plan/spec에서 다룰 방법} |

## 15. Plan 입력 후보

> 여기 적힌 항목은 확정 요구사항이 아니다. `/altool plan`에서 사용자가 만들 기능을 말하면 필요한 것만 선별한다.

### 15.1 후보 기능

- {후보 기능 1}
- {후보 기능 2}
- {후보 기능 3}

### 15.2 후보 페이지

- {페이지 1}
- {페이지 2}

### 15.3 후보 데이터

- {데이터 모델/필드 후보}

## 16. Plan 준비도

| 항목 | 상태 | 근거 |
| --- | --- | --- |
| 기능 후보가 충분한가 | ready/partial/not-ready | {근거} |
| 페이지 후보가 충분한가 | ready/partial/not-ready | {근거} |
| 데이터 후보가 충분한가 | ready/partial/not-ready | {근거} |
| 리스크가 식별되었는가 | ready/partial/not-ready | {근거} |

## 17. 다음 조사 후보

- {다음 research query 1}
- {다음 research query 2}
- {다음 research query 3}

## 18. 이번 조사에서 확정하지 않은 것

- {아직 결정하지 않은 범위/기능/기술}

## Version History

| Version | Date | Changes | Author |
| --- | --- | --- | --- |
| 0.1 | YYYY-MM-DD | 최초 작성 | Altool |
