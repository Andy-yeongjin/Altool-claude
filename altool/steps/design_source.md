# /altool design_source — 디자인 소스 기반 디자인 시스템 생성

**사용법**: `/altool design_source`

**목적**: 프로젝트의 디자인 소스(`designs/claude-design/*.html`, `.pen` 또는 Stitch)를 분석하여 단일 디자인 원천인 `designs/design.md`를 생성합니다.
생성된 디자인 시스템은 `constitution.md`의 범용 디자인 품질 원칙을 기준으로 검토합니다.

참조 사이트 조사만으로 디자인 시스템을 부트스트랩해야 하는 경우는 `/altool research`가 담당합니다. `design_source`는 사용자가 제공한 Claude 디자인 HTML, `.pen` 또는 Stitch 파일을 프로젝트 디자인 시스템으로 확정할 때 사용합니다.

> ⚠️ 이 커맨드는 **프로젝트 리드가 디자인 시스템을 확정할 때** 사용합니다.
> 생성된 `design.md`는 이후 모든 Altool 파이프라인에서 시각적 기준으로 사용됩니다.

---

## 실행 전 체크

### Step 0: 디자인 소스 감지 (자동 분기)

아래 순서대로 확인하여 **소스 타입**을 결정합니다:

| 우선순위 | 조건 | 소스 타입 | 분기 |
|---------|------|----------|------|
| 1 | `designs/claude-design/*.html` 파일 존재 | **Claude Design HTML** | → Claude HTML 모드 |
| 2 | `designs/stitch/` 폴더 존재 | **Stitch** | → Stitch 모드 |
| 3 | `designs/*.pen` 파일 존재 | **Pencil** | → Pencil 모드 |
| 4 | 모두 없음 | — | → 즉시 중단 |

모두 없으면 안내:
```
⚠️  디자인 소스가 없습니다.

  Claude 디자인 HTML 사용 시:
    Claude에서 만든 HTML을 designs/claude-design/ 폴더에 넣어주세요.

  Pencil.dev 사용 시:
    designs/ 폴더에 .pen 파일을 넣어주세요.

  Stitch 사용 시:
    Stitch에서 ZIP으로 내보낸 후 압축을 풀어
    designs/stitch/ 폴더에 파일을 넣어주세요.
    (code.html + DESIGN.md 파일이 있어야 합니다)
```

감지 완료 후 출력:
```
[0/6] 디자인 소스 감지 완료
  소스: [Claude Design HTML | Stitch | Pencil]
  경로: [designs/claude-design/*.html | designs/stitch/ | designs/*.pen]
```

### Step 1: 기존 designs/design.md 확인

이미 존재하면 첫 non-empty line을 확인한다.

- 첫 non-empty line에 `TBD`가 있으면 템플릿 상태로 보고 확인 없이 새 디자인 시스템으로 채운다.
- `TBD`가 없으면 사용자가 확정한 디자인 시스템일 수 있으므로 안내:
```
ℹ️  기존 designs/design.md가 있습니다. 덮어쓰시겠습니까?
A) 덮어쓰기 — 새로 생성
B) 취소
```

---

## 실행 순서 (5단계)

### [1/6] 디자인 소스 스캔

#### 🟣 Claude HTML 모드

`designs/claude-design/` 폴더의 모든 `.html` 파일을 읽습니다. 이 폴더의 HTML은 **가장 우선하는 디자인 헌법**입니다.

1. HTML의 DOM 구조를 읽고 페이지/섹션/컴포넌트 계층을 추출합니다.
2. `<style>`, 인라인 스타일, CSS custom properties, Tailwind class, class naming을 확인해 색상·타이포·간격·둥글기·그림자·상태 표현을 추출합니다.
3. 버튼, 카드, 입력, 탭, 네비게이션, 테이블, 모달, 배지, 빈 상태 등 반복 컴포넌트의 실제 크기·밀도·상태를 기록합니다.
4. 반응형 CSS, media query, container width, grid/flex 구조를 확인해 desktop/mobile Screen Recipe를 기록합니다.
5. 여러 HTML 파일이 있고 서로 색상·타이포·컴포넌트 규칙이 충돌하면 자동 병합하지 말고 어떤 HTML을 권위 기준으로 삼을지 사용자에게 확인합니다.

추출 완료 후 보고:
```
[1/6] Claude HTML 스캔 완료
  파일: [N]개 스캔
  페이지/화면: [N]개 발견
  컴포넌트: [N]종 발견
  색상/토큰: [N]개 발견
  반응형 규칙: [N]개 발견
```

#### 🔵 Pencil 모드

`designs/` 폴더의 모든 `.pen` 파일을 Pencil MCP 도구로 읽습니다.

1. 각 `.pen` 파일을 `open_document`로 열고
2. `batch_get`으로 전체 노드 구조를 파악하고
3. `search_all_unique_properties`로 아래 속성을 전수 추출합니다:

| 추출 속성 | designs/design.md 매핑 |
|-----------|----------------------|
| `fillColor` | 색상 팔레트 (Primary, Neutral, Semantic) |
| `textColor` | 텍스트 색상 |
| `strokeColor` | 보더 색상 |
| `strokeThickness` | 보더 두께 |
| `fontSize` | 타이포그래피 스케일 |
| `fontFamily` | 폰트 패밀리 |
| `fontWeight` | 폰트 굵기 |
| `cornerRadius` | 둥글기 (Border Radius) |
| `padding` | 간격 시스템 (Spacing) |
| `gap` | 간격 시스템 (Spacing) |

추출 완료 후 보고:
```
[1/6] .pen 스캔 완료
  파일: [N]개 스캔
  색상: [N]개 고유값 발견
  폰트 크기: [N]개 고유값 발견
  간격: [N]개 고유값 발견
  둥글기: [N]개 고유값 발견
```

#### 🟠 Stitch 모드

`designs/stitch/` 폴더에서 아래 파일을 읽습니다:

1. **`code.html`** — `tailwind.config` 스크립트 블록에서 아래를 추출합니다:
   - `theme.extend.colors` → 전체 색상 값 (이름 + hex 값)
   - `theme.extend.borderRadius` → 둥글기 값
   - `theme.extend.fontFamily` → 폰트 패밀리

2. **`DESIGN.md`** — 아래를 추출합니다:
   - 디자인 원칙 (Creative North Star, 컴포넌트 규칙)
   - 타이포그래피 스케일 (역할, 이름, 폰트, 크기)
   - 간격·그림자 규칙
   - Do/Don't 규칙

3. **`screen.png`** (선택) — 시각적 레이아웃 참고용으로 분석합니다.

추출 완료 후 보고:
```
[1/6] Stitch 스캔 완료
  색상 값: [N]개 (tailwind.config)
  타이포그래피: [N]개 역할 (DESIGN.md)
  둥글기: [N]개
  폰트 패밀리: [N]개
  디자인 원칙: [N]개 규칙
```

---

### [2/5] 디자인 시스템 정규화 (Normalization)

#### 🟣 Claude HTML 모드

HTML에서 추출한 실제 화면을 `design.md`의 규칙으로 정규화합니다. 이때 Claude HTML이 `designs/design.md`, Research 관찰값, 일반 AI 판단보다 우선합니다.

**화면 구조**: DOM 순서와 주요 section 비례를 Screen Recipes에 기록합니다. 구현 시 section 순서, 정보 밀도, 시각 위계가 HTML과 달라지면 design drift로 봅니다.

**색상**: CSS 변수와 실제 색상값을 역할 기반 팔레트로 정리합니다. 이름이 없으면 사용 위치를 기준으로 Primary/Surface/Text/Border/Semantic 역할을 부여합니다.

**타이포그래피**: CSS의 font-family, size, weight, line-height, letter-spacing을 역할별 스케일로 정리합니다. 외부/상용 폰트는 사용권을 확인할 수 없으면 안전한 대체 font-family stack을 함께 기록합니다.

**간격/밀도**: padding, gap, margin, container width, grid track, component height를 추출해 spacing scale과 화면별 밀도 규칙으로 기록합니다.

**컴포넌트 계약**: 버튼·카드·입력·네비게이션 등 반복 요소의 border, radius, shadow, hover/focus/active/disabled 상태를 실제 HTML 기준으로 잠급니다.

**상호작용**: HTML에 JS나 상태 class가 있으면 토글, 탭, 메뉴, 모달, validation, loading, empty/error/success 상태를 Component Contracts에 기록합니다.

#### 🔵 Pencil 모드

추출된 원시값을 `design.md` 안의 의미 있는 디자인 결정으로 정규화합니다.

**색상**: 유사한 색상을 그룹핑하여 역할 기반 팔레트로 구성합니다. Primary/Neutral/Semantic/Surface로 분류하고 각 색상의 사용 위치를 적습니다.

**타이포그래피**: 추출된 폰트 크기를 display/heading/body/caption/button 같은 역할로 매핑합니다.

**간격**: 추출된 padding/gap 값을 spacing scale과 사용 위치로 정리합니다.

**둥글기**: 추출된 cornerRadius를 표준 스케일(0/4/8/12/16/24/9999px)에 매핑.

**레이아웃**: navbar, sidebar, hero, card grid 등 반복 레이아웃 요소의 크기와 접힘 방식을 감지하여 Layout Principles에 등록합니다.

#### 🟠 Stitch 모드

Stitch의 tailwind.config 값은 이미 구조화되어 있어 `design.md`의 색상·타이포·간격·컴포넌트 계약으로 매핑합니다.

**색상**: `theme.extend.colors`의 키-값을 의미 이름, 값, 역할로 기록합니다.

**둥글기**: `theme.extend.borderRadius`의 값을 shape scale과 사용 위치로 기록합니다.

**폰트**: `theme.extend.fontFamily`에서 역할별 폰트 패밀리를 추출합니다.

**타이포그래피 스케일**: `DESIGN.md`의 타이포그래피 테이블을 기준으로 역할별 크기·굵기·행간을 정의합니다.

**폰트 사용권**: Claude HTML/`.pen`/Stitch가 폰트 이름을 제공하더라도 프로젝트에 폰트 파일이 포함되어 있거나 사용자가 제공했거나 오픈 라이선스임을 확인할 수 있는 경우에만 그대로 구현 폰트로 사용합니다. 확인할 수 없으면 시각 특성이 가까운 안전한 대체 폰트 스택을 `design.md`에 기록하고 대체 사유를 남깁니다.

**간격**: Stitch는 간격을 직접 제공하지 않는 경우가 있으므로 `DESIGN.md`의 컴포넌트 명세(padding, gap 언급)에서 추론하여 spacing scale과 사용 위치를 기록합니다.

정규화 완료 후 보고:
```
[2/5] 디자인 시스템 정규화 완료

  색상 매핑: [N]개
    primary: #81ecff → --color-primary
    surface: #0c0e17 → --color-surface
    ...

  둥글기 매핑: [N]개
    xl (0.5rem) → --radius-xl: 8px
    ...

  타이포 매핑: [N]개
  간격 스케일: [N]개 (추론 생성)
```

---

### [3/5] 디자인 품질 원칙 검토 (Quality Review)

`constitution.md`를 읽고, [2/5]에서 정규화된 디자인 시스템이 범용 디자인 품질 원칙을 해치지 않는지 검토합니다.

#### 검토 항목:

- 텍스트와 배경이 충분히 구분되어 사용자가 내용을 쉽게 읽을 수 있는가
- 클릭·터치·키보드 조작 대상이 실수 없이 사용할 수 있을 만큼 명확한 크기와 상태 표현을 갖는가
- 포커스, 오류, 성공, 로딩, 빈 상태 등 주요 상태가 시각적으로 구분되는가
- 화면 크기가 달라져도 텍스트와 UI가 겹치거나 잘리거나 조작 불가능한 상태가 되지 않는가
- 사용자 디자인 입력의 의도를 유지하면서도 접근성·반응형·명확성을 해치지 않는가

검토 결과 품질 원칙을 명확히 위반하는 값은 사용자 디자인 원천의 의도를 해치지 않는 범위에서 보정합니다. 특정 기관 스타일이나 고정 수치로 강제 교정하지 않습니다.

검토 및 보정 완료 후 보고:
```
[3/6] 디자인 품질 원칙 검토 완료

  ✅ 통과 항목:
    - 읽기 쉬운 대비와 정보 위계 확인
    - 조작 가능한 인터랙션 크기와 상태 표현 확인
    - 반응형 흐름 확인

  🔧 보정된 항목:
    - {필요 시 보정 내용}
```

보정 항목이 없으면 바로 다음 단계로 진행합니다.

---

### [4/5] design.md 생성

정규화된 디자인 시스템을 바탕으로 `designs/design.md`를 작성합니다.

**필수 포함 섹션**:

1. Design Thesis
2. Reference Source Map 또는 Source Mapping
3. Visual Theme & Atmosphere
4. Color Palette & Roles
5. Typography Rules
6. Layout Principles
7. Component Contracts
8. Media Rules
9. Depth & Elevation
10. Responsive Behavior
11. Do / Don't
12. Agent Implementation Guide

**작성 규칙**:
- 각 색상·타이포·간격·둥글기·그림자 값은 `이름 | 값 | 역할 | 사용 위치` 형식의 테이블로 정리
- Typography Rules에는 참조/원본 font-family, 구현 font-family stack, 대체 사유, 역할별 크기·굵기·행간·자간을 기록
- 디자인 소스에서 실제로 사용된 컴포넌트만 상세 명세를 작성하고, 사용되지 않은 컴포넌트는 기본값으로 채움
- 문서 상단에 소스 타입 명시: "이 문서는 [Claude Design HTML | Stitch | .pen 파일] 기반으로 자동 생성되었습니다"
- 생성 완료한 `design.md`의 첫 non-empty line에는 `TBD`가 없어야 한다. 기존 템플릿의 `(TBD)` 마커는 제거한다.
- Claude HTML 모드: `designs/claude-design/*.html`의 DOM/CSS/컴포넌트 규칙을 Reference Source Map, Screen Recipes, Component Contracts, Capture-to-Implementation Map에 최상위 디자인 헌법으로 기록
- Stitch 모드: `DESIGN.md`의 디자인 원칙(Creative North Star, Do/Don't)을 design.md의 Rules 섹션에 그대로 포함

---

### [5/5] 디자인 프리뷰 HTML 생성

`guides/design-preview.html`을 생성합니다. 브라우저에서 열면 디자인 시스템 전체를 시각적으로 확인할 수 있는 단일 HTML 파일입니다.

> `guides/` 디렉토리가 없으면 생성합니다.

**필수 조건**:
- `designs/design.md`에 적힌 값과 컴포넌트 계약을 HTML/CSS로 시각화
- 외부 라이브러리 없이 순수 HTML + CSS + 인라인 JS로 구성 (단일 파일)
- 프리뷰 내부 CSS는 `design.md`에서 파생한 값임을 주석으로 기록

**포함 섹션** (designs/design.md 구조 순서대로):

#### 1. Color Palette
- Primary 50~900: 각 색상을 정사각 칩으로 나열, 이름 + HEX값 표시
- Neutral(Gray) 50~900: 동일
- Semantic: Success, Warning, Danger, Info — 각각 기본색 + light 배경색
- Background & Surface: bg, bg-secondary, bg-tertiary, surface, overlay

#### 2. Typography
- 폰트 패밀리: sans, mono 각각 샘플 텍스트 렌더링
- 폰트 크기: text-xs ~ text-4xl 을 실제 크기로 "The quick brown fox" 렌더링
- 폰트 굵기: normal, medium, semibold, bold 비교
- 줄 높이: tight, normal, relaxed 비교

#### 3. Spacing
- space-0 ~ space-20: 각 간격을 시각적 바(bar)로 표현, 이름 + px값 표시

#### 4. Layout
- 컨테이너 너비: sm, md, lg, xl을 비율 바로 표현
- 브레이크포인트: sm, md, lg, xl 표시
- Navbar 높이, Sidebar 너비 시각화

#### 5. Buttons
- 종류별(Primary, Secondary, Ghost, Danger, Danger-outline) × 사이즈별(xs, sm, md, lg, xl) 매트릭스
- 각 버튼에 hover, disabled 상태도 표시

#### 6. Form Elements
- Text Input: default, focus, error, disabled 상태
- Textarea, Select, Checkbox, Radio, Toggle
- Label + Helper text + Error message 조합

#### 7. Cards
- 기본 카드, 클릭 가능 카드 (호버 그림자)

#### 8. Badges & Tags
- Default, Primary, Success, Warning, Danger 뱃지

#### 9. Alerts
- Info, Success, Warning, Danger 인라인 알림

#### 10. Shadows
- shadow-xs ~ shadow-xl: 동일 크기 박스에 각 그림자 적용

#### 11. Border Radius
- radius-none ~ radius-full: 동일 박스에 각 둥글기 적용

#### 12. Z-Index & Transitions
- z-index 체계를 계층 다이어그램으로 표현
- 트랜지션: fast, base, slow, spring 버튼으로 체감 비교

**스타일 규칙**:
- 페이지 자체의 레이아웃도 `designs/design.md`의 값과 컴포넌트 계약을 사용
- 각 섹션은 앵커 링크가 있는 목차(TOC)로 이동 가능
- 상단에 "이 페이지는 designs/design.md를 기준으로 생성된 디자인 시스템 프리뷰입니다." 안내 표시
- 반응형: 모바일에서도 확인 가능

생성 완료 후 보고:
```
[5/5] 디자인 프리뷰 생성 완료
  → guides/design-preview.html
  브라우저에서 열어 디자인 시스템을 확인하세요.
```

### Step Check

완료 전 `.altool/checks/design_source.design_source.json`을 작성하고 `python altool/scripts/check.py validate --json .altool/checks/design_source.design_source.json`를 실행한다. 실패하면 메시지를 보고 보완한 뒤 재검증하며, 최대 5회 실패 시 중지한다. 완료 보고에는 Step Check 요약을 포함한다:

| 항목 | 보고 기준 |
| --- | --- |
| `inputs.loaded` | 디자인 소스와 constitution.md 로딩 결과 |
| `lesson.search` | 디자인 소스 키워드 검색 결과 또는 `skipped(not applicable)` |
| `event.capture` | `skipped(document/design-system step)` — 코드 오류 lesson을 append하지 않는다 |
| `verification` | 디자인 품질 원칙 검토 결과 |
| `state.updated` | `skipped(no feature phase)` |
| `docs.synced` | design.md 갱신 결과 |
| `document.status` | design.md 최상단 `TBD` 제거 확인 또는 `skipped(design system assets)` |
| `artifacts.created` | design.md, design-preview.html |

---

## 완료 보고

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 디자인 시스템 생성 완료
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 디자인 소스: [Claude Design HTML (designs/claude-design/*.html) | Stitch (designs/stitch/) | Pencil (.pen [N]개)]
📊 생성된 디자인 값 수:
  색상: [N]개
  타이포: [N]개
  간격: [N]개
  레이아웃: [N]개
  기타: [N]개

📄 생성된 파일:
  ✅ designs/design.md (디자인 시스템 명세)
  ✅ guides/design-preview.html (시각 프리뷰)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 다음 단계
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. guides/design-preview.html을 브라우저에서 열어 디자인 시스템을 확인하세요
2. designs/design.md를 검토하고 필요한 부분을 수정하세요
3. 확정 후 /altool research 또는 /altool oneshot 으로 기능 개발을 시작하세요

⚠️ designs/design.md는 파이프라인 실행 전에 확정해야 합니다.
   파이프라인 실행 중에는 수정하지 마세요 (헌법 제16조).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
