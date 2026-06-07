# Q. Platform — 워크스페이스 마스터 가이드

> **Q. (큐닷) 1인 기업의 통합 작업 공간**
> 사람과 에이전트가 같은 좌표를 사용하기 위한 폴더 헌법

**위치:** `C:\Users\Won\Q_Platform`
**버전:** 1.0
**최종 갱신:** 2026-06-07

---

## 1. 한눈에 보는 폴더 맵

```
C:\Users\Won\Q_Platform\
│
├── README.md                        # 이 문서 (사람용)
├── AGENT_GUIDE.md                   # 에이전트용 네비게이션
├── publish.bat                      # docs → GitHub 통합 푸시
├── Q_Platform_setup.bat             # 최초 1회 셋업
│
├── docs\                            # ★ 정책·문서의 원본 (Single Source of Truth)
│   ├── 00_constitution\             # 헌법선언문
│   ├── 10_policy\                   # 정책기획서 (v2.1, v2.2, v2.3...)
│   ├── 20_operations\               # 운영규정 (명예자문위·펀드 등)
│   ├── 30_research\                 # 리서치·벤치마크
│   └── 90_archive\                  # 폐기·구버전 보관
│
├── design\                          # 디자인 산출물
│   ├── lp\                          # 랜딩 페이지 HTML
│   ├── messaging\                   # 카톡·메일·SMS 템플릿
│   └── brand\                       # 로고·색상·타이포
│
├── code\                            # 향후 에이전트가 작성할 코드
│
├── repos\                           # GitHub 클론 (publish.bat 대상)
│   └── q-policy-master\             # 정책 문서 공개 리포
│
└── scripts\                         # 보조 자동화 스크립트
```

---

## 2. 폴더 네이밍 규칙

| 규칙 | 예시 | 이유 |
|---|---|---|
| **숫자 접두사** | `00_`, `10_`, `20_` | 정렬 보장 (사람·에이전트 동일 순서) |
| **언더스코어 구분** | `00_constitution` | 공백 회피 (CLI·git 친화) |
| **버전 후미** | `v1.0`, `v2.2`, `v2.3` | 명시적 버전 관리 |
| **날짜 후미 (옵션)** | `_20260607` | 일자별 산출물 트래킹 |

---

## 3. 표준 작업 흐름 (Daily Workflow)

### 3-A. 새 문서 작성

```
1. docs\ 하위의 적절한 폴더 선택
   - 헌법 변경?  → 00_constitution\
   - 정책 추가?  → 10_policy\
   - 운영규정?   → 20_operations\
   - 리서치?     → 30_research\

2. 새 .md 파일 생성 (Cursor / Antigravity / VSCode)
   - 명명: 카테고리_제목_v버전.md

3. 작성 완료
```

### 3-B. GitHub 배포 (publish)

```cmd
cd /d C:\Users\Won\Q_Platform
publish.bat "커밋 메시지"
```

publish.bat 가 자동으로:
1. `docs\` → `repos\q-policy-master\docs\` 동기화 (변경분만)
2. `design\` → `repos\q-policy-master\design\` 동기화
3. `git add . && git commit -m "메시지" && git push`

→ **모든 변경이 한 줄 명령으로 GitHub 배포.**

### 3-C. 외부 협업자 공유

GitHub URL 공유:
- 정책 문서: https://github.com/qngel7/q-policy-master/tree/main/docs
- 헌법: https://github.com/qngel7/q-policy-master/tree/main/docs/00_constitution
- 디자인: https://github.com/qngel7/q-policy-master/tree/main/design

---

## 4. 에이전트 (Antigravity 등) 활용 가이드

### 에이전트가 알아야 할 우선순위

1. **항상 `docs\` 가 원본** — `repos\` 는 publish 산출물
2. **새 문서는 `docs\` 에 작성** — repo 폴더 직접 편집 금지
3. **명명 규칙 준수** — 숫자 접두사 + 카테고리 + 버전
4. **publish 는 항상 `publish.bat` 통해** — git 명령 직접 호출 지양

### 에이전트에게 줄 시스템 프롬프트 예시

```
당신은 Q. Platform 의 에이전트입니다.
모든 문서 작업은 C:\Users\Won\Q_Platform\docs\ 에 작성하세요.
폴더 카테고리: 00_constitution / 10_policy / 20_operations / 30_research / 90_archive
배포는 항상 C:\Users\Won\Q_Platform\publish.bat "메시지" 명령으로 수행하세요.
직접 git 명령을 호출하지 마세요.
상세 규칙: C:\Users\Won\Q_Platform\AGENT_GUIDE.md 참조.
```

---

## 5. 현재 보관 중인 문서 (v1.0 셋업 시점)

| 위치 | 문서 | 비고 |
|---|---|---|
| `docs\00_constitution\` | 큐닷_헌법선언문_v1.1.md | 최상위 규범 |
| `docs\10_policy\` | 큐닷_통합정책기획서_v2.2_패치노트.md | v2.1 기준 패치 |
| `docs\30_research\` | 보상체계_벤치마크_리서치.md | 한국 시장 실증 |
| `design\lp\` | 모바일_LP_비포애프터.html | D+0 카톡 클릭 후 화면 |
| `design\messaging\` | 카톡_메시지_템플릿.md | Scanner → 수신자 |

**원본 (v2.1 통합정책기획서)** 는 GitHub 에 이미 있음:
https://github.com/qngel7/q-policy-master/blob/main/큐닷_통합정책기획서_v2.1_20260524.md

---

## 6. 자주 쓰는 명령 한 줄 모음

| 작업 | 명령 |
|---|---|
| 폴더 열기 | `explorer C:\Users\Won\Q_Platform` |
| 헌법 보기 | `notepad C:\Users\Won\Q_Platform\docs\00_constitution\큐닷_헌법선언문_v1.1.md` |
| 변경 동기 + 푸시 | `cd /d C:\Users\Won\Q_Platform & publish.bat "메시지"` |
| 최신 pull | `cd /d C:\Users\Won\Q_Platform\repos\q-policy-master & git pull` |
| 깃 상태 | `cd /d C:\Users\Won\Q_Platform\repos\q-policy-master & git status` |

---

## 7. 트러블슈팅

| 증상 | 해결 |
|---|---|
| publish.bat 실행 시 git 인증 실패 | GitHub PAT 또는 SSH 키 설정 (Windows Credential Manager) |
| 한글 파일명 깨짐 | bat 파일 첫 줄 `chcp 65001` 확인 (이미 적용됨) |
| robocopy 권한 오류 | 관리자 권한으로 cmd 실행 |
| repo 폴더 미존재 | `Q_Platform_setup.bat` 재실행 |

---

## 8. 다음 확장 계획

| 우선순위 | 항목 | 비고 |
|---|---|---|
| ★★★ | `code\` 에 Cloudflare Worker (010Q메일 라우팅) | 인프라 시작 |
| ★★★ | `design\brand\` 에 로고·색상 토큰 정리 | 일관성 |
| ★★ | `repos\` 에 추가 리포 (`q-frontend`, `q-functions` 등) | 분리 |
| ★★ | `scripts\` 에 backup.bat (전체 백업) | 안전 |
| ★ | Antigravity 워크스페이스 설정 통합 | 에이전트 최적화 |

---

**원칙 한 줄:**
> **사람과 에이전트는 같은 폴더 맵을 본다.**

---

**관련 문서:**
- `AGENT_GUIDE.md` — 에이전트용 상세 지침
- `docs\00_constitution\큐닷_헌법선언문_v1.1.md` — 회사의 헌법
- https://github.com/qngel7/q-policy-master — 공개 리포지토리
