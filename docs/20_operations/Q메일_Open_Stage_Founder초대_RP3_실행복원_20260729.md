# Q메일 Open Stage Founder 초대 RP-3 실행·복원 기록

> 작성일: 2026-07-29  
> 캠페인: `OPEN-STAGE-2026-V1`  
> Seed Q-ID: `SDW00000007`  
> 현재 상태: Supabase RP-3B 설치·읽기 전용 검증 `PASS`, 앱 배포 대기  
> RP-3 기준 복원 커밋: `58c094bf9f2d184b4a032a4dc92da3291b82c484`

## 1. RP-3의 범위

RP-3는 서대원 Seed 링크로 신규회원 1명의 가입 귀속만 실제 검증한다. 가입 활성화, 최종 Q-ID 발급, 추천인 Q-ID 저장, `verified` 초대 장부 기록을 하나의 DB 트랜잭션으로 처리한다. 첫 성공 직후 실가입 연결은 자동으로 다시 잠긴다.

이번 단계에서는 참가자 후보 추가, 초대 10명·가입 5명 집계, Open Founder 자격 확정, Founder 자동승격, 회원 플랜 변경을 하지 않는다.

대외 식별과 운영 화면에는 Q-ID만 사용한다. `account_id`는 서버 내부 인증·관계·트랜잭션에서만 사용하며 초대 링크, 앱 응답, 사용자 안내, 공개 검증 결과에 노출하지 않는다.

## 2. 복원 지점

### 앱 복원 기준

- 기준 커밋: `58c094bf9f2d184b4a032a4dc92da3291b82c484`
- 사전백업: `_backups/open_stage/20260729_RP3_PRE/`
- 백업 매니페스트: `_backups/open_stage/20260729_RP3_PRE/manifest.sha256`

사전백업 파일의 SHA-256:

| 파일 | SHA-256 |
|---|---|
| `services/010/app.js` | `272B38133CE975196BA3F37726A57FD00DFB2410EC82553A7971FD9BCC97DEBF` |
| `services/010/index.html` | `815B008347CB54D252C8217DB02EAB2AAE257E4159EF037F3E6BFD824C7E4DCD` |
| `services/010/functions/api/register.js` | `787F9A9F30993E281A903440B7D097D9FE2F42180E9D82BEE98638E384A9413D` |
| `services/010/package.json` | `CDAD56CAEBFA7E938081FEDFB01A168704B206B89D9F3D0C6B847FF5FF999EAC` |

### DB 복원 기준

- RP-2A~RP-2D 전체 `PASS`
- 캠페인 상태 `pilot`
- Seed `SDW00000007` 1명
- RP-2 체크포인트 확정 참가자 24명
- 영구 초대 장부 0건
- 실가입 연결 미설치 또는 잠김

## 3. 실행 파일과 해시

기준 파일: `services/010/db/open_stage_rp3_manifest.sha256`

| 실행 순서 | 파일 | SHA-256 |
|---:|---|---|
| 1 | `preflight_open_stage_rp3_v1.sql` | `5230C7D9296F147EF904500945E6B473BD39681A759D3BC9B15DC3268D5326C5` |
| 2 | `prepare_open_stage_rp3_v1.sql` | `B67E6F9B9030E6285F9A1450E20177EB44752EF2D3B9DBF64FE0C7AEF4141796` |
| 3 | `verify_open_stage_rp3_v1.sql` | `D7DFDFB876BCCDF3C45566D70A6E51CC86481B54279A2B8ED238B468DB7320C4` |
| 4 | `activate_open_stage_rp3_single_pilot_v1.sql` | `A18B2E05A3D8E6D3BBABB53597EAC3F97C91C64745689389DC7D37CCE8F8D50A` |
| 5 | `verify_open_stage_rp3_live_result_v1.sql` | `5A24AFDDD8F563BAAB69E2B367445DA403C82BF75D7151BE2D6D3051DDDA8D99` |
| 복원 | `rollback_open_stage_rp3_v1.sql` | `1C5911278076B459183D53ED812115892D45DDB42BBE7860BC47765E57BA71CB` |

각 단계는 SQL 파일 전체를 독립된 Supabase SQL Editor 탭에서 실행한다. 일부 줄만 선택 실행하거나 여러 단계 파일을 한 번에 붙여 넣지 않는다.

## 4. 단계별 실행 게이트

### RP-3A · 읽기 전용 사전점검

지금 허용되는 작업은 `services/010/db/preflight_open_stage_rp3_v1.sql` 전체 실행뿐이다.

기대 결과:

- `ready_for_rp3=true`
- `campaign_status=pilot`
- `seed_q_id=SDW00000007`
- `rp2_checkpoint_participant_count=24`
- `participant_count=24`
- `ledger_count=0`
- `rp3_function_already_installed=false`

결과 화면을 저장하고 `_backups/open_stage/20260729_RP3/`의 증빙 목록에 기록한다. 값이 하나라도 다르면 즉시 중단하며 준비·활성화·복원 SQL을 실행하지 않는다.

### RP-3B · DB 기반 설치와 설치 검증

RP-3A 결과 확인 후에만 다음 순서로 진행한다.

1. `prepare_open_stage_rp3_v1.sql` 전체 실행
2. `verify_open_stage_rp3_v1.sql` 전체 실행
3. 검증 결과 `PASS`, `live_signup_wiring=false`, `pilot_signup_limit=1`, 체크포인트 기준 참가자 24명, 장부 0건 확인

설치 직후에도 실제 초대 링크는 닫혀 있다. 검증 결과가 다르면 초대하지 않고 `rollback_open_stage_rp3_v1.sql`로 캠페인을 정지한다.

### RP-3C · 앱 배포

RP-3B 검증 `PASS` 후 대표님이 저장소의 `publish.bat`로 배포한다. 배포 후 `https://010.q.co.kr/`에서 새 `app.js` 캐시 버전과 일반 가입 화면의 정상 로드를 확인한다.

아직 1인 파일럿 링크는 보내지 않는다. 상단 메뉴나 기존 가입완료 화면에서 만들어지는 일반 추천 링크는 RP-3 실가입 링크로 사용하지 않는다.

### RP-3D · 1인 파일럿 잠금 해제

DB 설치와 앱 배포를 모두 확인한 뒤 `activate_open_stage_rp3_single_pilot_v1.sql` 전체를 실행한다. 결과에서 `live_signup_wiring=true`, `pilot_signup_limit=1`, 장부 0건을 확인한다.

선정한 신규회원 1명에게만 다음 링크를 직접 보낸다.

`https://010.q.co.kr/?ref=SDW00000007&campaign=OPEN-STAGE-2026-V1`

파일럿 중에는 다른 사람에게 링크를 보내지 않는다. 신규회원은 `010Q` 또는 `OKQ`로 정상 가입해야 하며 테스트계정, 기존회원, Seed 본인 계정은 사용할 수 없다.

### RP-3E · 실가입 결과검증

가입 직후 `verify_open_stage_rp3_live_result_v1.sql` 전체를 실행한다.

통과 조건:

- 최종 결과 `PASS`
- 장부 `verified` 정확히 1건
- 초대자 사건 Q-ID `SDW00000007`
- 신규회원 상태 `active`와 최종 Q-ID 발급
- 신규회원 `referrer_qid=SDW00000007`
- `live_signup_wiring=false` 자동 복귀
- 설치 체크포인트 참가자 24명과 참가자 지문 무변경
- 신규 참가자 생성 0건
- Founder 자동승격·플랜 변경 0건

결과가 `PASS`여도 RP-3는 1인 검증 완료 상태일 뿐이다. 추가 초대는 후속 단계의 별도 승인과 재활성화 없이는 진행하지 않는다.

## 5. 장애 시 중단·복원

문제 발생 시 새 가입 데이터를 삭제하거나 기존 Q-ID·추천인·플랜을 일괄 복구하지 않는다.

1. `rollback_open_stage_rp3_v1.sql` 전체 실행
2. 캠페인 `paused`, `live_signup_wiring=false`, service role 함수 실행권 회수 확인
3. 이미 정상 가입된 회원과 초대 장부는 감사기록으로 보존
4. 앱 문제가 원인이면 RP-3 사전백업 또는 기준 커밋의 앱 파일로 복원 후 대표님 배포
5. 장애 시각, 증상, 실행 SQL, 결과 화면을 `_backups/open_stage/20260729_RP3/`에 기록

복원 SQL은 캠페인 연결을 멈추는 비파괴 복원이다. 테이블·회원·장부를 삭제하지 않는다.

## 6. 현재 결론

로컬 파일 작성과 자동검사는 완료되었으나 운영 DB와 앱에는 아직 RP-3가 적용되지 않았다. 따라서 지금은 초대장을 발송하지 않는다. 다음 단일 작업은 RP-3A 읽기 전용 사전점검 실행과 결과 화면 확인이다.

## 7. RP-3A 1차 안전중단 및 교정 기록

- 1차 실행 결과: `P0001: RP-2 확정 참가자는 25명이어야 합니다. 현재: 24`
- 데이터 변경: 없음. 사전점검은 읽기 전용이며 예외 발생 전에 DML을 수행하지 않았다.
- 원인: RP-2 사전점검의 기가입 대상 24명에 Seed가 이미 포함되어 있었으나 RP-3 계획에서 Seed를 다시 더해 25명으로 기록했다.
- 확정 기준: RP-2 준비·검증 SQL은 활성 비테스트 회원 24명 전체와 Open Stage 참가자 24명이 동일해야만 통과하며, RP-2C가 이미 `PASS`했다.
- 교정: RP-3 SQL 전체에서 참가자 수 25 하드코딩을 제거하고 RP-2 또는 RP-3 설치 체크포인트의 `participant_count`를 참조한다.
- 증빙: `_backups/open_stage/20260729_RP3/rp3a-preflight-safe-stop-participant-count.png`
- 증빙 SHA-256: `12122B00FCBF187F2C5001203E55A5D61547EE3A42AD013BB39C8470E74AB9A9`
- 교정본 재실행 결과: `ready_for_rp3=true`, `campaign_status=pilot`, Seed `SDW00000007`, RP-2 체크포인트 참가자 24, 현재 참가자 24, 장부 0, 전체 가입 26, RP-3 함수 미설치.
- PASS 증빙: `_backups/open_stage/20260729_RP3/rp3a-preflight-pass.png`
- PASS 증빙 SHA-256: `78117007111B100AE2135F400DD491E438F78A6DCC0E0F6B599479561DDAF9AF`
- RP-3B 준비 결과: `campaign_status=pilot`, `live_signup_wiring=false`, `pilot_signup_limit=1`, 참가자 24, 장부 0.
- RP-3B 준비 증빙: `_backups/open_stage/20260729_RP3/rp3b-prepare-installed-locked.png`
- RP-3B 준비 증빙 SHA-256: `851E7C6FCCEE368AA8A6DE3FEAAE743957929D45244FE5A8995A3DC90E252387`
- RP-3B 설치 검증 결과: `PASS`, `pilot`, `live_signup_wiring=false`, `pilot_signup_limit=1`, 회원원장 26, 참가자 24, 장부 0, 복원 커밋 일치.
- RP-3B 검증 증빙: `_backups/open_stage/20260729_RP3/rp3b-verification-pass.png`
- RP-3B 검증 증빙 SHA-256: `789A43819CDCD07F789029EB2B916EC438D20761E97764036C9194E7B771478F`
- 현재 다음 작업: 대표님이 `publish.bat`로 앱을 배포하고 배포 식별값을 확인한다. 활성화 SQL은 아직 실행하지 않는다.
