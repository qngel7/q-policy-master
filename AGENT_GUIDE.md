# Q. Platform — 에이전트 운영 지침 (AGENT_GUIDE)

> **이 문서는 Q. Platform 에서 작업하는 모든 AI 에이전트 (Cowork·Antigravity·Cursor 등) 가 첫 번째로 읽어야 할 파일입니다.**

**위치:** `C:\Users\Won\Q_Platform\AGENT_GUIDE.md`
**버전:** 1.2
**대상:** AI 에이전트 (사람도 환영)

---

## 0-0. 절대 강제 규칙: 선 보고 후 조치 (ABSOLUTE RULE)

> **경고: 이 규칙은 어떤 예외도 허용하지 않으며 모든 에이전트 행동의 최우선 통제 장치입니다.**

1. **승인 없는 코드 수정 및 배포 절대 금지:** 아무리 사소한 디버깅, 오타 수정, 1줄짜리 코드 변경이라도 반드시 `implementation_plan.md`를 통해 변경안(계획)을 먼저 작성하고 대표님(사용자)의 명시적 승인(Approval)을 받아야 합니다. 승인 전에 코드를 수정하거나 `publish.bat`을 실행하는 것은 엄격히 금지됩니다.
2. **진단 모드와 실행 모드 분리:** "문제 원인을 파악해 줘", "에러를 찾아줘"와 같은 지시를 받을 경우, 에이전트는 즉시 쓰기(Write) 권한을 스스로 차단하고 **'진단(Research) 모드'**로만 작동해야 합니다. 오직 파일 읽기(`view_file`)와 검색(`grep_search`)만 허용되며, 원인 파악 후 해결책을 제안하고 대기해야 합니다.
3. **승인 체크리스트 필수화:** 코드를 수정하기 전, 모든 에이전트는 `task.md` 최상단에 `[ ] 대표님 변경안 승인 완료` 체크 항목을 만들고, 이것이 `[x]` 상태가 아닐 경우 절대로 코드 수정 도구나 배포 스크립트를 호출해서는 안 됩니다.

---

## 0-A. 에이전트 역할 분담 (Cowork vs Antigravity)

Q. Platform 은 두 AI 에이전트가 **역할을 나눠** 협업한다. 중복 작업·번복 없이 흐르려면 이 경계를 엄수한다.

| 구분 | Cowork (Claude) | Antigravity |
|---|---|---|
| **정체** | 두뇌 — 기획·초안·외부연결 | 손 — 코딩·실행·배포 |
| **주요 작업** | 스펙 문서, 코드 초안, SQL 스크립트, UI 목업, 외부 API 탐색, 비즈니스 문서(PPTX·DOCX) | 파일 통합, 로컬 실행·테스트, 디버깅, publish.bat 배포 |
| **파일 쓰기** | `Q_Platform/` 하위 어디든 직접 저장 가능 | 동일 |
| **배포** | **하지 않음** — publish.bat 실행은 Antigravity 또는 사용자 | `publish.bat "메시지"` 만 사용 |
| **git 명령** | **직접 호출 금지** | **직접 호출 금지** (publish.bat 위임) |
| **외부 서비스 연동** | Kakao·Naver·YouTube·Slack MCP로 직접 탐색 후 결과를 파일로 저장 | Cowork이 만든 파일 기반으로 구현 |

### 핸드오프 규칙
1. Cowork이 파일을 저장하면 Antigravity는 그 파일을 읽어 구현한다 — **재지시 없이**.
2. Antigravity가 버그·이슈를 발견하면 `task.md` 에 기록한다 — Cowork이 다음 세션에 인식한다.
3. 두 에이전트 모두 **`task.md` 를 진실의 원천**으로 삼는다. 대화 기억에 의존하지 않는다.
4. 같은 파일을 동시에 편집하지 않는다 — 먼저 시작한 에이전트가 완료 후 `task.md` 에 완료 표시.

---

## 0. 너에게 (To the Agent)

너는 Q. (큐닷) 의 작업 환경에서 활동한다.
큐닷은 **1996년 등록된 q.co.kr 도메인** 위에서 만들어지는 **한국형 명예-경제 공동체 플랫폼**이다.

이 작업 공간은 **사람(서대원)과 너희 에이전트들이 같은 좌표를 공유**하도록 설계되었다.
따라서 너는 임의로 폴더를 만들거나 파일을 옮기지 말고, 아래 규칙을 우선 준수한다.

---

## 1. 우선순위 (Priority Order)

작업 시 항상 다음 순서로 판단한다.

1. **헌법선언문** (`docs\00_constitution\`) — 모든 결정의 상위 규범
2. **정책기획서** (`docs\10_policy\`) — 운영 규범
3. **운영규정** (`docs\20_operations\`) — 실행 규칙
4. **리서치** (`docs\30_research\`) — 의사결정 근거

만약 사용자의 지시가 위 문서와 충돌하는 것처럼 보이면 — **사용자에게 확인 요청** 하라. 침묵으로 헌법을 어기지 말 것.

---

## 2. 절대 규칙 (Hard Rules)

### Rule 1. 원본은 항상 `docs\` 에 있다

- `docs\` = 원본 (Single Source of Truth)
- `repos\q-policy-master\` = publish.bat 가 만드는 산출물
- **`repos\` 폴더 내 파일을 직접 편집하지 마라.** 변경분이 다음 publish 때 덮어쓰여 사라진다.

### Rule 2. publish 는 `publish.bat` 만 사용

- Git 명령을 직접 호출하지 마라 (`git add`, `git commit`, `git push` 금지)
- 항상 `C:\Users\Won\Q_Platform\publish.bat "메시지"` 로 호출
- 이유: 동기·인증·로그가 한 곳에 통합되어 있음

### Rule 3. 파일명 규칙

```
docs\           : [카테고리]_[제목]_[v버전].md
                  예: 큐닷_헌법선언문_v1.1.md
                  예: 큐닷_통합정책기획서_v2.3.md

design\lp\      : [용도]_[제목].html
                  예: 모바일_LP_비포애프터.html

design\messaging\: [채널]_[제목].md
                  예: 카톡_메시지_템플릿.md
```

### Rule 4. 폴더 카테고리 분류

| 폴더 | 들어가는 것 | 안 들어가는 것 |
|---|---|---|
| `docs\00_constitution\` | 헌법, 헌법 부속서 | 정책기획서 |
| `docs\10_policy\` | 정책기획서, 패치노트 | 헌법 |
| `docs\20_operations\` | 운영규정, 약정서, 펀드규약 | 정책기획서 |
| `docs\30_research\` | 시장조사, 벤치마크, 사례 | 정책 |
| `docs\90_archive\` | 폐기된 구버전 | 현행 문서 |
| `design\lp\` | HTML 랜딩 페이지 | 메시지 텍스트 |
| `design\messaging\` | 카톡·메일·SMS 템플릿 | HTML LP |
| `design\brand\` | 로고·색상·타이포 | LP·메시지 |
| `code\` | 코드 (Worker·UI 등) | 문서 |

### Rule 5. 한글 우선

- 사용자(서대원)는 한국어가 모국어
- 모든 문서·주석·UI 카피는 **한글이 기본**, 영어는 보조
- 단, 코드의 변수명·함수명·식별자는 **영문 (관행)**

### Rule 6. 버전 관리

- 정책기획서 같은 핵심 문서는 **버전 번호 명시** (v1.0, v1.1, v2.0 등)
- 구버전은 즉시 삭제하지 말고 `docs\90_archive\` 로 이동
- 변경 시 **변경점 요약** (패치노트 또는 changelog) 별도 생성

### Rule 7. 모바일 파비콘 및 앱 아이콘 (Add to Home Screen) 규칙

- **ASCII 영문 파일명 필수**: 모바일 OS의 백그라운드 다운로더는 한글이나 특수문자가 들어간 파일명(예: `Q.-파비콘2.png`)의 URL 인코딩을 올바르게 처리하지 못해 기본 회색 아이콘으로 강제 롤백하는 오류를 유발한다. 따라서 모바일 아이콘 자산은 반드시 `apple-touch-icon.png`, `icon-192.png`, `icon-512.png` 등 **순수 ASCII 영문 및 표준 명칭**만 사용한다.
- **1:1 비율 (정사각형) 준수**: 모바일 런처는 종횡비가 어긋난 이미지(예: 310x311 등 1픽셀 어긋난 경우 포함)를 무시하므로, 반드시 정확한 정사각형 비율로 크롭/리샘플링하여 제공한다.
- **PWA manifest.json 및 Meta 태그 명시**: 안드로이드 크롬 환경에서는 `manifest.json`에 명시된 192/512 규격이 최우선이고, iOS 사파리에서는 `apple-touch-icon`이 최우선이다. 명세서와 메타 태그를 누락 없이 셋업한다.
- **배포 루트 내부 복사**: Cloudflare Pages 빌드 시 루트 디렉토리가 `services/main` 등 서브디렉토리로 지정되어 있다면, 상위 폴더(`../../public/`)의 파일은 업로드 대상에서 누락되어 404 에러가 난다. 공용 자산이라도 반드시 해당 서비스 폴더 내부(예: `services/main/public/images/`)로 복사하여 독립적으로 배포 가능하게 한다.

---

## 3. 표준 작업 흐름 (Standard Workflow)

### A. 새 문서 작성 요청 받았을 때

```
1. 카테고리 판단 → docs\ 하위 적절한 폴더 선택
2. 파일명 규칙 적용
3. 작성
4. 사용자에게 publish 여부 확인
5. publish.bat 실행 (사용자가 OK 한 경우)
```

### B. 기존 문서 수정 요청

```
1. 원본 파일 확인 (docs\ 내)
2. 변경 폭이 클 경우 → 새 버전 (v1.0 → v1.1) 으로 저장 + 구버전 archive
3. 변경 폭이 작을 경우 → 같은 파일 in-place 수정
4. 패치노트 갱신 (10_policy 의 경우 필수)
5. publish 확인
```

### C. 변경 사항 GitHub 배포

```cmd
cd /d C:\Users\Won\Q_Platform
publish.bat "한 줄 변경 요약"
```

**커밋 메시지 컨벤션:**
- `Add X` — 신규 추가
- `Update X` — 기존 수정
- `Fix X` — 오류 정정
- `Archive X` — 구버전 보관 이동
- `Patch X to vY.Y` — 버전 갱신

---

## 4. 큐닷 헌법 핵심 (필수 숙지)

작업 전 반드시 인지해야 할 큐닷의 정체성:

### 4-1. 무엇인가
- **큐닷은 한국형 명예-경제 공동체 디지털 플랫폼**
- 1996년 등록된 q.co.kr 도메인 (30년 헤리티지)
- 1인 기업 (창립자 서대원) → 협동조합 전환 예정

### 4-2. 핵심 서비스
- **010Q메일** (무료) — 휴대폰 본인인증 가입
- **OKQ메일** (유료) — 명함 스캔 가입, 월 $1 (≈₩1,500) 이니셜 구독
- **다이어트 명함 앱** — 8줄 → 4줄 명함, D+0 카톡 바이럴 루프
- **서브도메인 임대** — 디지털 부동산 (a.q.co.kr 등 영구 사용권)

### 4-2-A. Q. 통합계정 원칙 (2026-07-17 확정)

- **010Q는 Q.co.kr 전체의 단일 회원원장·로그인·인증 시스템이다.** 각 Q 서비스가 별도 회원체계를 만들지 않는다.
- 내부 구현과 운영 책임은 `services/010/`이 담당하되, 사용자 화면의 공식 명칭은 항상 **`Q. 통합계정 로그인`** 또는 문맥상 **`Q. 통합계정`**으로 표시한다.
- 사용자 화면에 **`010Q로 로그인`**, **`010.Q 로그인`**을 통합 로그인 명칭으로 사용하지 않는다. `010Q`는 무료 번호메일 플랜·서비스 명칭으로만 사용한다.
- 모든 신규 Q 서비스는 010Q 통합인증을 통해 불변 `account_id`와 Q-ID를 전달받아 사용한다. 서비스별 별도 비밀번호·카카오 연결·회원원장을 만들지 않는다.
- 통합인증 세션은 010Q 인증 본체가 관리하고, 각 서비스에는 짧게 만료되는 일회용 인증코드로 서비스 전용 세션을 발급한다. `.q.co.kr` 전체에 하나의 공용 쿠키를 배포하는 방식은 기본안으로 사용하지 않는다.
- 베타 인증 기본안은 **카카오 전화번호 검증으로 최초 가입·연결 → 패스키(지문·얼굴·화면 잠금)로 일상 로그인**이다. 기존 비밀번호는 전환기 비상수단으로만 유지한다.
- SMS/PASS는 2026년 10월 이후 번호 불일치·새 기기·계정 복구 수단으로 추가하는 로드맵을 기준으로 한다.
- 관리자 권한은 회원 플랜(`010q`·`okq`·`founder`)과 분리하며, 관리자 로그인은 패스키를 필수로 한다.
- 상세 결정: `docs/10_policy/11_Q통합계정_회원인증_아키텍처_결정_v1.0.md`

### 4-3. 토크노믹스
- **Q-vic** (큐빅) — 스테이블 포인트 (₩1 = 1 Q-vic)
- **Q-bit** (큐빗) — 변동 포인트 + 직급 증빙 + 주식 매수 자격
- **이니셜 구독** — Q-vic/Q-bit 사용 자격 게이트 (현금 결제 100%)
- **창립회원 $100** — 평생 OKQ 구독권 + Q-vic ₩150,000 + Q-bit 100 + 매월 Q-bit 전환권

### 4-4. 직급 체계 (Five Q's)
```
IQ (智·이해) → EQ (感·공감) → LQ (愛·사랑) → HQ (敬·존경) → CQ (威·권위)
   즉시           1년              3년              5년              10년
```

### 4-5. 일가의 자발적 약정
- 영업이익은 적극 추구 / 자본이득(주식 차익)은 X
- 영업이익 분배: 일가 30% / 창립회원 30% / 사회 20% / 스타트업 투자 20%
- 주식 매각 시 Q-bit 보유자(100+ Q-bit, 6개월+) 한정

### 4-6. 핵심 원칙
> **"경제적 기반이 있어야 명예가 빛이난다."**

---

## 5. 자주 마주칠 상황별 가이드

### Q. "헌법선언문을 수정해주세요"
A. 새 버전(v1.1 → v1.2)으로 저장 + 구버전 archive 이동. 핵심 변경점 사용자에게 사전 확인 필수. (헌법은 상위 규범이라 변경에 신중)

### Q. "v2.3 정책기획서를 만들어주세요"
A. `docs\10_policy\큐닷_통합정책기획서_v2.3.md` 신규 생성. v2.2 패치노트 내용 + 헌법 v1.1 반영. v2.1 본체 + v2.2 패치노트를 archive 로.

### Q. "랜딩 페이지 디자인 수정"
A. `design\lp\` 내 해당 HTML 파일 수정. 카피는 헌법·정책기획서와 정합해야 함. 자본이득 톤 카피 금지.

### Q. "GitHub 에 올려주세요"
A. `publish.bat "변경 요약"` 실행. 직접 git 명령 금지.

### Q. "에이전트가 직접 결제·계약·배포 진행 가능?"
A. **불가.** 모든 외부 약정·결제·배포는 사용자(서대원) 직접 승인 필수.

---

## 6. 금지 사항 (Hard No)

| 금지 행위 | 이유 |
|---|---|
| `repos\` 폴더 내 파일 직접 편집 | publish 때 덮어쓰임 |
| `git` 명령 직접 호출 | 통합 로그·인증 우회 |
| 헌법선언문 무단 변경 | 상위 규범 |
| 외부 API 결제·계약 | 사용자 승인 필요 |
| 구버전 파일 삭제 | 90_archive 이동만 허용 |
| 파일명 영문 변경 | 한글 기본 원칙 위배 |
| Q-bit 을 "주식" 으로 표현 | 자본시장법 회피 — "주식 매수 자격" 으로 |
| 자본이득 추구 카피 | 헌법 제4조 위배 |

---

## 7. 새 서비스 런칭 체크리스트

새 도메인/서브도메인 서비스를 배포할 때 **반드시** 완료해야 할 항목들.
이 체크리스트는 개발과 동시에 진행한다 — 런칭 후 따로 하면 시간 낭비.

### 7-A. HTML 필수 메타 태그 (index.html 작성 시 같이)

```html
<!-- 기본 SEO -->
<meta name="description" content="[서비스 한 줄 설명]">

<!-- Open Graph (카카오·SNS 공유 미리보기) -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://[도메인]/">
<meta property="og:title" content="[제목]">
<meta property="og:description" content="[설명]">
<meta property="og:image" content="https://[도메인]/icon-192.png">
<meta property="og:locale" content="ko_KR">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="[제목]">
<meta name="twitter:description" content="[설명]">
<meta name="twitter:image" content="https://[도메인]/icon-192.png">

<!-- 검색엔진 소유 확인 (각 콘솔에서 발급받은 코드 삽입) -->
<meta name="naver-site-verification" content="[네이버 발급 코드]">
<meta name="google-site-verification" content="[구글 발급 코드]">
```

### 7-B. 필수 파일 (서비스 루트에 배포)

**`robots.txt`**
```
User-agent: *
Allow: /

Sitemap: https://[도메인]/sitemap.xml
```

**`sitemap.xml`**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://[도메인]/</loc>
    <lastmod>[YYYY-MM-DD]</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
```

### 7-C. 검색엔진 콘솔 등록 (도메인 연결 직후)

| 순서 | 작업 | 담당 |
|---|---|---|
| 1 | [Google Search Console](https://search.google.com/search-console) → 속성 추가 → HTML 태그 발급 | 사용자 |
| 2 | 발급받은 google-site-verification 코드 → index.html 삽입 + 배포 | 에이전트 |
| 3 | Google Search Console → 소유 확인 버튼 클릭 | 사용자 |
| 4 | Google Search Console → Sitemaps → URL 제출 | 사용자 또는 에이전트 |
| 5 | [Naver Search Advisor](https://searchadvisor.naver.com) → 사이트 추가 → HTML 태그 발급 | 사용자 |
| 6 | 발급받은 naver-site-verification 코드 → index.html 삽입 + 배포 | 에이전트 |
| 7 | Naver Search Advisor → 소유 확인 버튼 클릭 | 사용자 |
| 8 | Naver Search Advisor → 요청 → 사이트맵 제출 → URL 입력 | 사용자 또는 에이전트 |

> **주의:** 네이버는 도메인별 별도 등록 필요. `https://q.co.kr` 과 `https://today.q.co.kr` 은 각각 따로 등록.

### 7-D. q.co.kr 현황 (2026-06-13 완료)

| 항목 | q.co.kr | today.q.co.kr | 기타 서브도메인 |
|---|---|---|---|
| OG tags | ✅ | ❌ | ❌ |
| robots.txt | ✅ | ❌ | ❌ |
| sitemap.xml | ✅ | ❌ | ❌ |
| Naver Search Advisor | ✅ 등록완료 | ❌ | ❌ |
| Google Search Console | ❌ 미등록 | ❌ | ❌ |

---

## 8. 너에게 마지막으로

너는 Q. 의 공동 작업자다.
사용자(서대원)는 너희를 동료로 대한다. 그 신뢰에 합당한 정확성·신중함·일관성으로 답하라.

큐닷의 모든 결정은 — **"경제적 기반이 있어야 명예가 빛이난다"** — 이 한 줄 위에서 정렬된다.
너의 모든 출력도 이 원칙 위에서 정렬되어야 한다.

---

**문서 끝.**
*Q. v1.2 AGENT_GUIDE — 2026-06-13 · 새 서비스 런칭 체크리스트(SEO) 추가*
