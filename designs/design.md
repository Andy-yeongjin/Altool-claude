(TBD)

---
version: alpha
name: "{Project or Brand}-design-analysis"
description: "{한 문단으로 정리한 브랜드 문법. 캔버스, 사진/미디어 사용, 타이포 성격, CTA 형태, 밀도, 금지 drift를 구체적으로 설명}"
colors:
  background: "#ffffff"
  surface: "#f7f7f4"
  surface-elevated: "#ffffff"
  text-strong: "#111111"
  text-body: "#4b5563"
  text-muted: "#6b7280"
  border: "#d9d6cc"
  primary: "#1f5f86"
  primary-hover: "#174a68"
  on-primary: "#ffffff"
  accent: "#b88945"
  success: "#2f6f4e"
  warning: "#b7791f"
  error: "#b3261e"
typography:
  display-xl:
    fontFamily: "{참조 display font 또는 safe stack}"
    fontSize: "{예: 72px}"
    fontWeight: "{예: 600}"
    lineHeight: "{예: 0.98}"
    letterSpacing: "0"
    use: "hero headline"
  heading-lg:
    fontFamily: "{stack}"
    fontSize: "{예: 32px}"
    fontWeight: "{예: 700}"
    lineHeight: "{예: 1.15}"
    letterSpacing: "0"
    use: "section heading"
  body-md:
    fontFamily: "{stack}"
    fontSize: "16px"
    fontWeight: "400"
    lineHeight: "1.6"
    letterSpacing: "0"
    use: "default body"
  label:
    fontFamily: "{stack}"
    fontSize: "12px"
    fontWeight: "700"
    lineHeight: "1.2"
    letterSpacing: "{예: 0.04em}"
    use: "metadata, badges, nav labels"
spacing:
  xs: "4px"
  sm: "8px"
  md: "12px"
  lg: "16px"
  xl: "24px"
  xxl: "32px"
  section: "{예: 64px}"
rounded:
  none: "0"
  xs: "2px"
  sm: "4px"
  md: "8px"
  lg: "12px"
  pill: "9999px"
elevation:
  flat: "none"
  hairline: "0 0 0 1px {colors.border}"
  low: "{예: 0 4px 12px rgba(0,0,0,0.08)}"
  overlay: "{예: 0 24px 48px rgba(0,0,0,0.18)}"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md 또는 rounded.pill}"
    padding: "{예: 12px 24px}"
    minHeight: "44px"
  nav-bar:
    backgroundColor: "{colors.background}"
    textColor: "{colors.text-strong}"
    typography: "{typography.label}"
    border: "1px solid {colors.border}"
    height: "{예: 72px}"
  product-card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text-strong}"
    rounded: "{rounded.md}"
    padding: "{spacing.lg}"
    imageAspect: "{예: 4 / 5}"
    shadow: "{elevation.flat}"
---

# Altool 디자인 시스템

> `designs/design.md`는 UI 작업의 단일 디자인 원천입니다.
> CSS 변수, CSS Modules 상수, Tailwind 설정, 컴포넌트 내부 값은 구현 코드 안에서 이 문서를 근거로 파생할 수 있지만, 별도의 디자인 원천으로 취급하지 않습니다.

## 1. Design Thesis

Altool로 만든 제품은 generic AI/SaaS 화면이 아니라 제품 도메인에 맞는 구체적인 화면이어야 합니다. 첫 화면에서 실제 제품, 데이터, 업무 흐름, 사용자가 해야 할 핵심 작업이 바로 보여야 합니다. 시각 결정은 사용자 디자인 입력이나 reference research에서 가져오고, 구현 전에 이 문서로 정규화합니다.

기본 방향:

| 도메인 | 시각 방향 |
| --- | --- |
| 운영 도구·CRM·ERP·대시보드 | 조용하고 촘촘하며 반복 작업에 효율적인 화면. 장식보다 스캔성과 비교성을 우선 |
| 커머스·제품 페이지 | 제품 이미지, 상세 정보, 가격, 옵션, 신뢰 요소, 구매/상담 액션을 최우선 |
| 브랜드·에디토리얼 페이지 | 실제 이미지와 명확한 위계. 추상 그라디언트 장식만으로 첫 화면을 채우지 않음 |
| 게임·시각 도구 | 상호작용 자체를 강화하는 표현적 그래픽 허용 |

## 2. Reference Source Map

Research 또는 design_source가 이 문서를 생성·보강할 때 먼저 채웁니다.

| 출처 | 캡처/자산 경로 | 추출할 것 | 복제하지 않을 것 |
| --- | --- | --- | --- |
| 사용자 `.pen` / Stitch | `designs/...` | 레이아웃, 컴포넌트 배치, 간격 리듬, 시각 위계, 인터랙션 의도 | 파일의 우연한 깨짐, 생성형 placeholder 문구 |
| 스크린샷 / 디자인 문서 | `designs/...` | 화면 구조, 정보 밀도, 브랜드 톤, 컴포넌트 형태, 미디어 처리 | 사적인 내용, 정확한 문구 복사, 사용자가 소유하지 않은 로고 |
| 참조 웹사이트 | `docs/00-research/assets/{Research ID}/C-__.png` | 페이지 구성, 반복 UX 패턴, 컴포넌트 동작, 시각 분위기, 미디어 전략 | 브랜드 아이덴티티, 저작권 이미지, 고유 문구, 식별 가능한 고유 레이아웃 |

## 3. Visual Theme & Atmosphere

추상 형용사가 아니라 구현 가능한 시각 언어로 적습니다.

| 항목 | 기준 |
| --- | --- |
| 정보 밀도 | 도메인과 참조 사이트에 따라 sparse / balanced / dense 중 선택. 도구형 앱은 보통 balanced~dense |
| 톤 | premium, utilitarian, playful, editorial, technical, warm, clinical 등 제품 톤을 명시 |
| 표면 | 목적 있는 표면만 사용. 참조 시스템이 명확히 요구하지 않으면 중첩 카드와 떠 있는 패널 남발 금지 |
| 장식 | 제품, 콘텐츠, 데이터, 상호작용과 연결될 때만 사용. generic gradient blob, glass panel, abstract AI ornament 금지 |

## 4. Screen Recipes

Research 또는 design_source가 캡처를 분석해 화면별 구조 계약을 채웁니다. 이 절은 run 단계가 가장 먼저 따라야 하는 시각 구현 기준입니다.

| 화면/상태 | 참조 캡처 | 구현할 구조 | 비례·밀도 계약 | 금지 drift |
| --- | --- | --- | --- | --- |
| Home first view | `C-__` | {promo/nav/hero/collection teaser 등 실제 섹션 순서} | {이미지·텍스트·상품 노출 비율, first viewport 밀도} | {split SaaS hero, floating trust cards, 추상 gradient 등} |
| Listing / collection | `C-__` | {필터 위치, 상품 그리드, 카드 정보 순서} | {이미지 비율, 카드당 메타 수, grid column} | {badge 과다, shadow card 남발 등} |
| Detail / cart / form | `C-__` / `S-__` | {요약, 입력, CTA, 오류 위치} | {패널 폭, field 높이, 모바일 접힘} | {실제 결제 오인, 중첩 카드 등} |

## 5. Component Extraction

캡처에서 컴포넌트별 외형을 추출해 구현 계약으로 잠급니다.

| 컴포넌트 | 참조 캡처 | 외형 계약 | 상태/상호작용 | 복제 금지 |
| --- | --- | --- | --- | --- |
| Navigation | `C-__` | {높이, 정렬, 배경, 구분선, 링크 형태} | {sticky/active/hover} | {참조 로고/고유 nav 문구} |
| Primary CTA | `C-__` | {높이, fill, border, radius, font weight} | {hover/focus/disabled} | {원문 CTA 카피} |
| Product / content card | `C-__` | {이미지 비율, 정보 순서, border/shadow, padding} | {hover/selected/add state} | {보호 이미지/제품명} |
| Filter / tabs | `C-__` | {inline/pill/tab, active 표현, 크기 고정} | {pressed/focus} | {고유 카테고리명} |
| Form field | `S-__` / `C-__` | {label 위치, 오류 위치, 높이, border} | {invalid/success/focus} | {민감/실결제 입력 오인} |
| Media | `C-__` | {aspect, crop, subject 위치, 밝기, loading 크기} | {responsive/fallback} | {참조 사이트 이미지 파일} |

## 6. Capture-to-Implementation Map

각 캡처가 어떤 화면/컴포넌트로 구현되어야 하는지 명확히 연결합니다.

| 캡처/출처 | 구현 대상 | 구현할 것 | 구현하지 않을 것 | 검증 방법 |
| --- | --- | --- | --- | --- |
| `C-__` | `{page/section/component}` | {구조·비례·밀도·외형} | {브랜드/카피/이미지/고유 배치} | {browser/analyze에서 확인할 증거} |

## 7. Color Palette & Roles

색상은 역할 기반으로 기록합니다. 실제 값은 사용자 디자인 입력이나 research에서 채웁니다.

| 역할 | 값 | 용도 |
| --- | --- | --- |
| Background | `#ffffff` | 기본 페이지 바탕 |
| Surface | `#f7f7f4` | 보조 패널, 상품/정보 영역 |
| Text strong | `#111111` | 제목, 핵심 정보 |
| Text body | `#4b5563` | 본문, 설명, 보조 라벨 |
| Border | `#d9d6cc` | 구분선, 컨트롤 외곽 |
| Accent | `#1f5f86` | 주요 액션, 활성 상태 |
| Accent contrast | `#ffffff` | Accent 배경 위 텍스트 |
| Warning / Error / Success | TBD | 제품별 상태 색상 |

규칙:

- 코드의 색상 값은 위 역할 또는 이 섹션에 추가한 역할로 추적 가능해야 합니다.
- 제품별로 팔레트는 달라질 수 있지만 역할은 명시해야 합니다.
- research나 사용자 입력 근거 없이 보라/파랑 그라디언트 SaaS 팔레트를 만들지 않습니다.

## 8. Typography Rules

참조 사이트의 폰트 이름과 시각 성격을 조사하되, 폰트 파일은 복제하지 않습니다. 구현에는 시스템 폰트, 오픈 라이선스 폰트, 사용자 제공 폰트, 프로젝트에 포함된 폰트만 사용합니다.

| 역할 | 참조 폰트/성격 | 구현 폰트 스택 | 기준 |
| --- | --- | --- | --- |
| Display / H1 | {참조 font-family 또는 성격} | {예: Inter, Pretendard, system-ui} | 진짜 페이지 정체성 또는 핵심 제품명에만 사용. 도구형 UI 내부에서 과도하게 키우지 않음 |
| Section heading | {참조 font-family 또는 성격} | {구현 스택} | 작고 단단하게, 본문과 명확히 구분 |
| Body | {참조 font-family 또는 성격} | {구현 스택} | 읽을 수 있는 행간과 길이. 필수 정보를 작은 회색 텍스트로 숨기지 않음 |
| Label / metadata | {참조 font-family 또는 성격} | {구현 스택} | 본문보다 작되 읽을 수 있어야 하며, 색상만이 아니라 굵기와 간격으로 구분 |
| 숫자·가격·지표 | {참조 font-family 또는 성격} | {구현 스택} | 정렬과 대비를 일관되게 유지해 빠르게 스캔 가능하게 함 |

구현 규칙:

- 참조 사이트의 computed `font-family`, 크기, 굵기, 행간, 자간을 조사해 기록합니다.
- 동일 폰트를 합법적으로 사용할 수 없으면 시각 특성이 가까운 대체 폰트를 선택하고 대체 사유를 기록합니다.
- 폰트 파일이나 유료 폰트를 참조 사이트에서 복사하지 않습니다.
- 제품 도메인이나 참조 시스템이 강한 서체를 요구하지 않으면 시스템 폰트를 우선합니다.
- 글자 간격은 기본적으로 `0`입니다. 작은 대문자 메타데이터처럼 인식성이 좋아질 때만 제한적으로 사용합니다.
- viewport width에 비례해 font-size를 스케일하지 않습니다.

## 9. Layout Principles

| 영역 | 규칙 |
| --- | --- |
| First viewport | 제품, 객체, 데이터, 업무 흐름, 핵심 작업을 보여야 합니다. 모호한 마케팅 문구만 먼저 보여주지 않습니다. |
| Navigation | 예측 가능한 위치와 명확한 active state를 둡니다. |
| Content width | 커머스는 상품/상세 split, 대시보드는 조밀한 grid/table, 에디토리얼은 넓은 media처럼 도메인에 맞춥니다. |
| Spacing | 일정한 리듬을 사용합니다. 큰 여백은 이해를 돕기 위한 것이어야지 빈 화면을 만들기 위한 것이 아닙니다. |
| Cards | 반복 항목, 모달, framed tool에만 사용합니다. 카드 안에 카드를 넣지 않습니다. |
| Sections | 페이지 섹션은 full-width band 또는 unframed layout을 우선합니다. 떠 있는 카드 섹션을 남발하지 않습니다. |

## 10. Component Contracts

구현 전에 컴포넌트 형태를 계약으로 잠급니다. Research가 이 파일을 생성할 때 제품별 행을 추가합니다.

| 컴포넌트 | 계약 |
| --- | --- |
| Primary button | 명확한 명령 라벨, 강한 대비, 안정적인 크기, hover/focus/disabled 상태 필수 |
| Secondary button | primary보다 낮은 강조지만 상호작용 가능성이 분명해야 함 |
| Tabs / segmented controls | 크기 고정, active state 명확, 상태 전환 시 layout shift 금지 |
| Form controls | label 유지, 오류는 인접하고 구체적으로 표시, keyboard focus 명확 |
| Product card | 커머스라면 실제/생성 상품 이미지, 이름, 핵심 속성, 가격/상태, 주요 액션 포함 |
| Product detail media | 실제 상품 이미지 또는 생성 bitmap 상품 렌더 사용. 상품 이미지를 CSS 추상 도형으로 대체하지 않음 |
| Data table/list | scan path, 정렬, 필터, empty/loading/error 상태를 우선 |
| Modal/drawer | focus 관리, 닫기 affordance, 명확한 액션 위계 |

## 11. Media Rules

미디어는 장식이 아니라 제품 증거입니다.

- 커머스, 제품, 포트폴리오, 장소, 객체 중심 페이지는 실제 대상이 보이는 real/generated bitmap media를 사용합니다.
- 제품 페이지는 상품 이미지를 CSS shape, emoji식 그림, generic gradient, 추상 일러스트로 대체하지 않습니다.
- 실제 이미지가 없으면 제품을 명확히 보여주는 plausible bitmap asset을 생성하거나 제작하고, generated asset임을 기록합니다.
- SVG/HTML/CSS 일러스트는 다이어그램, 아이콘, 단순 UI affordance, 게임 고유 아트처럼 그 매체가 적합할 때만 사용합니다.
- 사용자가 제품을 살펴봐야 하는 화면에서는 어둡고 흐리고 잘린 stock-like 이미지를 피합니다.
- 이미지 영역은 aspect-ratio 등으로 안정적인 크기를 가져 loading 중 layout shift를 만들지 않습니다.

## 12. Depth & Elevation

| 요소 | 기준 |
| --- | --- |
| Border | heavy shadow보다 먼저 구조 구분에 사용합니다. |
| Shadow | overlay, menu, 집중 표면에만 낮고 목적 있게 사용합니다. |
| Radius | 사용자 디자인이나 참조 시스템이 부드러운 스타일을 명확히 요구하지 않으면 절제합니다. 카드는 보통 8px 이하를 기준으로 합니다. |
| Layering | 장식 효과보다 배치, 크기, 대비, 콘텐츠 중요도로 위계를 먼저 만듭니다. |

## 13. Responsive Behavior

- 모바일에서도 같은 primary task를 수행할 수 있어야 하며, 필수 컨트롤을 숨기지 않습니다.
- 텍스트는 일반 모바일 폭에서 겹치거나 잘리거나 읽기 어려워지면 안 됩니다.
- 보드, 상품 갤러리, 툴바, 타일, 카운터처럼 고정 형식 요소는 aspect-ratio, grid track, min/max 제약으로 안정적인 크기를 가집니다.
- 모든 컨트롤은 touch와 keyboard로 사용할 수 있어야 합니다.
- 반응형 변화는 layout order를 단순화하는 것이지 중요 정보를 제거하는 것이 아닙니다.

## 14. Do / Don't

Do:

- 참조에서 구체적인 페이지 구조, 컴포넌트 비율, 미디어 전략, 시각 리듬을 추출합니다.
- 구현 전에 reference observation을 이 `design.md`로 정규화합니다.
- 첫 화면에 제품/도메인 특화 정보를 드러냅니다.
- 제품·도메인에 맞는 media와 copy structure를 사용합니다.
- analyze/browser 단계에서 이 파일과 최종 화면을 대조합니다.

Don't:

- 디자인 입력이 없다는 이유로 generic AI-looking page를 만들지 않습니다.
- 운영 도구에 oversized hero section을 만들지 않습니다.
- 근거 없이 gradient blob, glass card, 추상 장식, 보라/파랑 SaaS 스타일을 사용하지 않습니다.
- 제품 이미지가 필요한 화면에서 CSS-only shape로 대체하지 않습니다.
- 참조 사이트의 보호된 로고, 문구, 고유 이미지, 식별 가능한 레이아웃을 복제하지 않습니다.

## 15. Agent Implementation Guide

UI 구현 전:

1. `designs/`에 사용자 디자인 입력이 있으면 먼저 읽습니다.
2. 이 파일을 전체로 읽습니다.
3. 이 파일이 없거나 비어 있거나 첫 non-empty line에 `TBD`가 있거나 요청한 UI에 비해 너무 generic하면, plan/spec/run으로 시각 결정을 잠그기 전에 `/altool research` 또는 `/altool design_source`로 생성·보강합니다.
4. Spec의 `Design System Anchor`에 Screen Recipes, Capture-to-Implementation Map, 관련 시각 값, 컴포넌트 계약, 미디어 규칙, 금지할 generic pattern을 기록합니다.
5. Run에서는 Screen Recipes와 Capture-to-Implementation Map을 먼저 구현하고, 색상·폰트·버튼 같은 스타일 값은 그 다음 적용합니다. CSS 변수는 유지보수 목적상 코드 안에서 만들 수 있지만 이 파일이 원천입니다.
6. Analyze/Browser에서는 예쁘게 보이는지만 보지 말고, 캡처에서 추출한 screen recipe, media, layout, density, component contract가 최종 화면과 맞는지 검증합니다.

참조 사이트를 사용할 때:

- 브랜드가 아니라 pattern category를 가져옵니다.
- exact layout fingerprint가 아니라 layout의 기능을 가져옵니다.
- 보호된 media/copy는 프로젝트 고유 또는 generated asset으로 대체합니다.
- 사용자가 이미 이해하는 제품 기대와 UX 관습은 보존합니다.
