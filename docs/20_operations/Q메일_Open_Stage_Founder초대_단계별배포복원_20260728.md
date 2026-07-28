# Q메일 Open Stage Founder 초대 단계별 배포·복원

> 작성일: 2026-07-28  
> 캠페인: `OPEN-STAGE-2026-V1`  
> 현재 단계: RP-1 설치·검증 `PASS` 완료 · RP-2 별도 승인 전 대기
> 기준 원칙: Q-ID는 대외 식별, `account_id`는 내부 식별

## 1. 목적

Open Stage Founder 초대 기능을 기존 가입·추천·회원 플랜과 분리하여 단계적으로 도입한다. 각 단계는 독립적으로 정지할 수 있어야 하며 문제가 생기면 직전 복원 지점으로 돌아가야 한다.

이번 RP-1에서는 Supabase 전용 테이블과 서버 전용 함수만 준비한다. 가입 API, 사용자 화면, 서대원 실제 초대 링크, Founder 승격은 연결하지 않는다.

## 2. 식별자 원칙

| 구분 | 식별자 |
|---|---|
| 초대 링크·화면·운영 검색 | Q-ID |
| 내부 외래키·권한·트랜잭션 | `account_id` |
| 감사 장부 | `account_id` + 사건 당시 Q-ID |

- Q-ID 이름이니셜 3자리는 정정될 수 있다.
- 뒤 8자리 회원 순번과 내부 `account_id`는 변경되지 않는다.
- 과거 Q-ID 링크는 `q_id_aliases`를 거쳐 현재 회원의 `account_id`로 해석한다.
- 일반 화면과 대외 API에 `account_id`를 노출하지 않는다.

## 3. RP-0 · 현재 복원 기준

대표님이 다음 배포 완료를 확인한 상태를 RP-0으로 지정한다.

```text
2026-07-28 · Q-ID 대외 식별 및 account_id 내부 식별 원칙 확정
```

### RP-0 상태

- Open Stage 전용 Supabase 테이블 없음
- Open Stage 전용 API·화면 없음
- 일반 `?ref=Q-ID` 추천 저장은 기존대로 동작
- 기존 `registrations`, `referrer_qid`, 플랜, 인증 동선 유지
- 초대장과 안내문 디자인은 확정 상태

### RP-0 파일 백업

보관 위치:

```text
_backups/open_stage/20260728_RP0/
```

검증 매니페스트:

```text
_backups/open_stage/20260728_RP0/manifest.sha256
```

| 파일 | SHA-256 |
|---|---|
| `AGENT_GUIDE.md` | `43DE00F31E2006D37D4A2180AFD46217B4256B27B43E0F306ABB7A1D408291CD` |
| `docs/10_policy/12_Q-ID_이름이니셜_정정_정책_v1.0.md` | `CF47639ED7681CD6D7C79FADDEB37A7236723B3471CA6FC4FD91F677A1C1FE48` |
| `services/010/index.html` | `815B008347CB54D252C8217DB02EAB2AAE257E4159EF037F3E6BFD824C7E4DCD` |
| `services/010/app.js` | `272B38133CE975196BA3F37726A57FD00DFB2410EC82553A7971FD9BCC97DEBF` |
| `services/010/functions/api/register.js` | `787F9A9F30993E281A903440B7D097D9FE2F42180E9D82BEE98638E384A9413D` |
| `services/010/functions/p.js` | `B74BEA26E1BB106AF62B80B8899813BBC12FB316BA693C2988D65A904E8EA6C4` |
| `services/010/db/add_qid_initial_correction.sql` | `1C0DCD7884C71203F3CD21D50E6E7F6610DEDEC68DA6DEFEF8739C6166366212` |
| `outputs/qmail_open_stage_invitation/qmail-open-stage-invitation.html` | `9D9FC522923D053E3A9258C6E7CCCFCB3B581AAB04D9B58E727723410697D3B4` |
| `outputs/qmail_open_stage_invitation/초대장_동봉메시지.md` | `FB8BC7B2271DE2B53243695E6020A72D8E46D8FD93BFC512F859C9D5265D56E3` |

## 4. RP-1 · Supabase 기반 설치

### 생성되는 객체

- `open_stage_campaigns`
- `open_stage_participants`
- `open_stage_invite_ledger`
- `open_stage_release_checkpoints`
- `open_stage_resolve_member_v1(text)`
- `open_stage_record_checkpoint_v1(...)`
- `open_stage_set_campaign_status_v1(...)`

### RP-1 안전 상태

```text
campaign.status = draft
participants = 0
invite_ledger = 0
라이브 가입 연결 = 없음
사용자 화면 변경 = 없음
Founder 플랜 변경 = 없음
```

### RP-1 실행본 SHA-256

실제 Supabase SQL Editor에서 실행할 파일은 아래 해시와 일치해야 한다. 동일한 값은 `services/010/db/open_stage_v1_manifest.sha256`에도 기록했다.

| 파일 | SHA-256 |
|---|---|
| `create_open_stage_campaign_v1.sql` | `A2BBF3891A3C14AE849B0EBD348C5E964F27FDD8C867949601CA60536FC6D269` |
| `pause_open_stage_campaign_v1.sql` | `A9BFA927C5340C8496D0826E31E53FBDAE65922B0BBF87EC53822CF64589B3FB` |
| `verify_open_stage_campaign_v1.sql` | `AF26CC4297EF88C62A78B4E6777CBB52C518AF19BF80265B3F27C52DE496AC77` |
| `rollback_open_stage_campaign_v1.sql` | `6920CA21301438817036B5CE789395FFD23F6580DF4BCABCB48B044B32BC9D11` |

실행 직전 파일이 수정되었다면 해시를 다시 산출하고 운영 문서와 매니페스트를 함께 갱신한 뒤 실행한다.

## 5. Supabase 실행 순서

### 실행 전

1. Supabase 프로젝트와 `registrations` 테이블이 운영 프로젝트인지 확인한다.
2. `q_id_aliases` 테이블이 존재하는지 확인한다.
3. 현재 가입이 정상 동작하는지 확인한다.
4. RP-0 백업과 `manifest.sha256`이 존재하는지 확인한다.
5. RP-1 SQL 파일이 `open_stage_v1_manifest.sha256`과 일치하는지 확인한다.
6. SQL Editor에서 새 쿼리를 연다.

### 1단계 설치

다음 파일 전체를 실행한다.

```text
services/010/db/create_open_stage_campaign_v1.sql
```

이 파일은 하나의 트랜잭션으로 실행된다. 중간 오류가 발생하면 전체 설치가 롤백되어 기존 회원 데이터에 영향을 주지 않는다.

### 설치 검증

다음 파일 전체를 별도 쿼리로 실행한다.

```text
services/010/db/verify_open_stage_campaign_v1.sql
```

마지막 결과가 다음이어야 한다.

```text
PASS
RP-1 DB 기반 설치 완료 · 캠페인 draft/paused · 참가자 0 · 장부 0 · 라이브 미연결
```

검증 결과에서 다음을 확인한다.

- 캠페인 코드 `OPEN-STAGE-2026-V1`
- 캠페인 상태 `draft`
- 참가자 0건
- 장부 0건
- RP-0·RP-1 체크포인트 존재
- 네 테이블 모두 RLS 활성
- `anon`, `authenticated` 직접 권한 없음
- 활성 Q-ID 중복 0건
- 활성 Q-ID 8자리 순번 중복 0건

## 6. 이상 발생 시 즉시정지

다음 파일을 실행한다.

```text
services/010/db/pause_open_stage_campaign_v1.sql
```

처리 결과:

- 캠페인 상태가 `paused`로 변경
- 정지 시점의 회원·참가자·장부 건수 기록
- 기존 가입·추천·회원 플랜은 변경하지 않음
- 정지 체크포인트 자동 추가

RP-1은 라이브 동선과 연결되어 있지 않으므로 캠페인을 `paused`로 전환하는 것만으로 운영 영향이 차단된다.

## 7. RP-0 호환 복원

다음 파일의 기본 실행은 비파괴 복원이다.

```text
services/010/db/rollback_open_stage_campaign_v1.sql
```

기본 처리:

- 캠페인 `paused`
- 변경 RPC의 `service_role` 실행권 회수
- `registrations`, 추천관계, 회원 플랜 보존
- 캠페인 테이블과 장부 보존
- 복원 체크포인트 기록

### 테이블 완전 제거

기본값에서는 실행되지 않는다. 다음 조건을 모두 충족한 경우에만 파일 하단의 확인문을 수동 변경한다.

1. 참가자 0건
2. 초대 장부 0건
3. 검증 결과 보관 완료
4. 대표님이 완전 제거를 별도로 승인

```sql
v_confirmation text := 'DROP_OPEN_STAGE_V1';
```

참가자나 장부가 한 건이라도 있으면 제거 블록은 예외를 발생시키고 중단한다.

## 8. 단계별 진행 기준

| 복원 지점 | 기능 | 다음 단계 진입 조건 |
|---|---|---|
| RP-0 | 식별 원칙 배포 완료 | 백업·해시 기록 |
| RP-1 | DB 기반, 라이브 미연결 | SQL 검증 PASS |
| RP-2 | 서대원 Seed Pilot 3~5건 | 추천 귀속·장부 수동 대조 |
| RP-3 | 기가입회원 후보 등록 | 기존 데이터 무변경 확인 |
| RP-4 | 10명·5명 자동 집계 | 자동값과 수동 검산 일치 |
| RP-5 | 승인·수락 | 별도 승인 후 활성화 |

각 단계는 별도 구현계획과 대표님 승인을 받은 뒤 진행한다.

## 9. RP-2 전 금지사항

- `services/010/app.js` 캠페인 연결
- `services/010/functions/api/register.js` 캠페인 장부 연결
- 서대원 Seed 참가자 운영 DB 등록
- 실회원 대상 캠페인 링크 발송
- 10명·5명 조건 외부 공지
- `plan=founder` 또는 `is_founder` 자동 변경

## 10. RP-1 완료 기록

| 항목 | 확정 기록 |
|---|---|
| 코드 배포 | `2026-07-28T10:18:16+09:00` |
| 배포 커밋 | `f5c466ba28501373071bd7892123d9af08b0d2c8` |
| 배포문 | `2026-07-28 · Open Stage Founder 초대 RP-0 및 Supabase 1단계 기반` |
| Supabase 실행일 | `2026-07-28` |
| 실행자 Q-ID | 제출 화면에서 확인되지 않아 미기록 |
| create SQL SHA-256 | `A2BBF3891A3C14AE849B0EBD348C5E964F27FDD8C867949601CA60536FC6D269` |
| create SQL 결과 | 성공 — 검증 SQL이 설치 객체와 RP 체크포인트를 확인 |
| verify SQL 결과 | `PASS` |
| 캠페인 상태 | RP-1 체크포인트 `draft`; 검증 허용 안전상태 `draft/paused` |
| registrations 건수 | RP-1 DB 체크포인트에 기록됨; 제출 화면에는 수치 미표시 |
| participants 건수 | `0` |
| ledger 건수 | `0` |
| RP-0 확인 | 확인 완료 |
| RP-1 확인 | 확인 완료 |
| 라이브 연결 | 없음 |

정확한 Supabase 실행시각과 당시 `registrations_count`는 운영 DB의 `open_stage_release_checkpoints`에서 `checkpoint_code='RP-1'`로 조회한다.

### RP-1 검증 증빙

- 파일: `_backups/open_stage/20260728_RP1/supabase-rp1-verification-pass.png`
- 증빙 SHA-256: `DD3CCCCCFA28CD20AFF3016DBDB12B90C22B34A1970EDD28580999A8B39CEABD`
- 증빙 매니페스트: `_backups/open_stage/20260728_RP1/manifest.sha256`
- 화면 확인 내용: Supabase Production · Primary Database · role `postgres`에서 검증 SQL 마지막 결과 `PASS`

RP-1은 완료되었다. RP-2의 서대원 Seed Pilot, 실제 초대 귀속, 실회원 등록은 별도 변경안 승인 전까지 시작하지 않는다.
