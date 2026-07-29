# Q메일 Open Stage Founder 초대 RP-4 10/5 운영모드 실행·복원 기록

> 작성일: 2026-07-29  
> 캠페인: `OPEN-STAGE-2026-V1`  
> Seed Q-ID: `SDW00000007`  
> 첫 운영 후보 Q-ID: `GGS00000027`  
> 현재 상태: RP-4B DB 설치·읽기 검증 `PASS` · 운영 잠금 유지 · RP-4C 앱 배포 대기  
> RP-4 기준 복원 커밋: `fc0802b09219ad19714433cbd4d35a52889016b1`

## 1. 확정 운영정책

- Seed `SDW00000007`의 캠페인 링크로 직접 가입한 회원은 Open Founder `candidate`가 된다.
- 후보의 캠페인 링크를 통한 유효 가입은 최대 10명까지 인정한다.
- 5명 가입 시 참가 상태만 `qualified`로 자동 전환한다.
- `qualified` 달성만으로 회원 플랜을 `founder`로 바꾸지 않는다. Founder 확정은 관리자 확인 후 별도 처리한다.
- 후보가 초대한 피초대자는 일반회원으로 가입하며 새로운 후보가 되지 않는다.
- 캠페인 참가자가 아닌 일반회원의 친구초대는 캠페인 코드 없는 기존 일반 추천으로 처리한다.
- RP-3의 첫 실가입 회원 `GGS00000027`은 RP-4 설치 시 첫 운영 후보로 편입한다.

대외 식별, 개인 링크, 진행 화면, 증빙에는 Q-ID만 사용한다. `account_id`는 서버 내부 외래키와 원자적 트랜잭션에서만 사용한다.

## 2. 복원 지점

### 앱

- 기준 커밋: `fc0802b09219ad19714433cbd4d35a52889016b1`
- 사전백업: `_backups/open_stage/20260729_RP4_PRE/`
- 사전백업 매니페스트: `_backups/open_stage/20260729_RP4_PRE/manifest.sha256`

| 파일 | SHA-256 |
|---|---|
| `app.js` | `863EC6AA310E397E8D10CFBC680215ECD5E89DA478522A08B69A7257F12AAC0A` |
| `index.html` | `9C0B49F55179B150C49655A83AF9AA91DBDA643F28ACC155448CA6A9DAD8F877` |
| `register.js` | `936EBCB56EF1385432214E4C64B28EFC6F25A466E469165CB8EE0C6E1CFA4376` |
| `open-stage.js` | `6BB6A517B27FB2F7AA4D71C4345768F0B2BDFF3CF6D8799611BE659053D161B3` |
| `package.json` | `535041A49F3C2CFE99B6940CBB9D187C102DD23CF62A8EADF36F455D38D46DCD` |

### DB

- 캠페인 `pilot`
- `live_signup_wiring=false`
- `pilot_signup_limit=1`
- 회원원장 27명
- 참가자 24명
- `verified` 장부 1건
- RP-3 초대 사건 `SDW00000007 → GGS00000027`
- RP-3E 최종 결과 `PASS`

상세 기준은 `_backups/open_stage/20260729_RP4_PRE/restore_point.txt`에 고정했다.

## 3. 실행 파일과 해시

기준 매니페스트: `services/010/db/open_stage_rp4_manifest.sha256`

| 순서 | 파일 | SHA-256 |
|---:|---|---|
| 1 | `preflight_open_stage_rp4_v1.sql` | `B9526C8A29F2F974C962762C64131EFF0B369E94981BB11CD0FAFAC60B641D72` |
| 2 | `prepare_open_stage_rp4_v1.sql` | `9D8BA0CF04195CD7D447F5C2B12902C80F92438E36B445C05142512BE7A8BBFB` |
| 3 | `verify_open_stage_rp4_v1.sql` | `F4142A90A2A0511E760DE39FEC8F64E58C8C4E03FE485F9F5F0B6B240EC04D8E` |
| 4 | `activate_open_stage_rp4_operating_v1.sql` | `60C241A217A0D5C964A82618EF6ADAFDAB02B7B44FBFA40B6E9A19245737277C` |
| 5 | `verify_open_stage_rp4_operating_v1.sql` | `03CAD10075BF6FED0BBE488BD9A94DA1263004005358790A26EF49969A6CB96A` |
| 중지 | `pause_open_stage_rp4_v1.sql` | `3EC49E8D247D557D3879D47D6A316BA0DFF82FEA74C572DEF8C30DCBDBC63004` |
| 복원 | `rollback_open_stage_rp4_v1.sql` | `C60C509109E3B9A390A5DE0331EE3EFE95B67141809C7C1EB9C333953227837A` |

SQL은 한 파일 전체를 독립된 Supabase SQL Editor 탭에서 실행한다. 여러 파일을 합치거나 일부 줄만 선택 실행하지 않는다.

## 4. 단계별 실행 게이트

### RP-4A · 읽기 전용 사전점검

첫 작업은 `preflight_open_stage_rp4_v1.sql` 전체 실행뿐이다.

기대 결과:

- `ready_for_rp4=true`
- `campaign_status=pilot`
- `live_signup_wiring=false`
- `pilot_signup_limit=1`
- 초대자 `SDW00000007`
- 첫 후보 예정자 `GGS00000027`
- `ledger_status=verified`
- 회원원장 27명, 참가자 24명, 장부 1건
- `rp4_function_already_installed=false`

값이 다르면 중단한다. 사전점검은 읽기 전용이므로 실패해도 데이터를 변경하지 않는다.

### RP-4B · DB 설치 후 계속 잠금

RP-4A `PASS` 확인 후 아래 두 파일을 순서대로 실행한다.

1. `prepare_open_stage_rp4_v1.sql`
2. `verify_open_stage_rp4_v1.sql`

통과 조건:

- 최종 결과 `PASS`
- 캠페인 `pilot`
- `operating_mode_enabled=false`
- `live_signup_wiring=false`
- 운영 배치 한도 100, 기준 장부 1
- 회원원장 27명 그대로
- 참가자 25명, 장부 1건
- `GGS00000027`이 `candidate`, 진행률 0/5, 초대한도 10
- `campaign_open=false`, `can_invite=false`
- 회원 플랜·Q-ID·RP-3 장부 무변경

설치 직후에는 링크를 보내도 Open Stage 귀속이 열리지 않는다.

### RP-4C · 앱 배포

RP-4B 검증 `PASS` 후 대표님이 저장소 루트의 `publish.bat`를 실행한다.

배포 확인:

- `https://010.q.co.kr/` 응답 정상
- `app.js?v=20260729-open-stage-rp4`
- 로그인 후보의 상단 메뉴에 `Open Founder n/5`
- 일반회원은 기존 `친구 초대`
- 공개 API 응답과 화면에 `account_id` 없음

앱 배포 전에는 RP-4D 운영 활성화를 실행하지 않는다.

### RP-4D · 운영 100건 배치 활성화

앱 배포 확인 후 `activate_open_stage_rp4_operating_v1.sql` 전체를 실행한다.

기대 결과:

- `PASS`
- 캠페인 `active`
- `operating_mode_enabled=true`
- `live_signup_wiring=true`
- 운영 배치 한도 100
- `GGS00000027` 진행률 0/5, 남은 인정 인원 10
- 개인 링크에 `ref=GGS00000027`과 캠페인 코드 포함

### RP-4E · 운영 상태 읽기 검증

활성화 직후 신규 가입을 만들기 전에 `verify_open_stage_rp4_operating_v1.sql`을 실행한다.

결과 `PASS` 후부터 초대를 시작한다.

- Seed 초대: `https://010.q.co.kr/?ref=SDW00000007&campaign=OPEN-STAGE-2026-V1`
- 후보 초대: 로그인 후 상단 `Open Founder n/5` 또는 가입완료 화면의 `친구 초대하기`
- 일반회원 초대: 기존 일반 친구초대

Seed 링크 가입자는 새 후보가 된다. 후보 링크 가입자는 일반회원이며 해당 후보의 인정 가입수에만 반영된다.

## 5. 자동 집계와 한도

- 후보별 장부 `verified`가 5건이 되면 참가 상태를 `qualified`로 바꾸고 체크포인트를 남긴다.
- 10건이 되면 그 후보의 캠페인 링크로는 더 가입할 수 없다.
- RP-4 시작 기준 장부 1건 이후 신규 `verified` 100건이 쌓이면 `live_signup_wiring=false`로 자동잠금한다.
- 한 피초대자는 한 번만 귀속되며 자기초대, 테스트계정, 기존 참가자, 중복귀속을 차단한다.

## 6. 장애 시 중지·복원

### 즉시 중지

`pause_open_stage_rp4_v1.sql`을 실행한다.

- 캠페인 `paused`
- `operating_mode_enabled=false`
- `live_signup_wiring=false`
- 기존 회원·참가자·장부·플랜 보존

### 비파괴 복원

`rollback_open_stage_rp4_v1.sql`을 실행한다.

- 신규 캠페인 귀속 잠금
- RP-4 service role 함수 권한 회수
- 운영 중 발생한 실제 가입·참가자·장부·플랜은 삭제하지 않음
- 앱은 RP-4 사전백업 또는 기준 커밋을 이용해 복원 후 대표님이 다시 배포

실가입 사건은 감사와 수동 판정을 위해 보존한다. 일괄 삭제나 Q-ID·추천인·플랜 되돌리기는 하지 않는다.

## 7. 로컬 검증 결과

- JavaScript 문법검사 통과
- 전체 `npm test` 통과: 인증·SSO·메일·이름메일·웰컴메일·가입·Q-ID 회귀검사 통과
- RP-2·RP-3·RP-4 Open Stage 회귀검사 24건 통과
- RP-4 SQL 7개 파일의 SHA-256을 매니페스트에 고정했다.
- 앱·API·테스트 최종 해시는 `_backups/open_stage/20260729_RP4/source_manifest.sha256`에 고정했다.

현재 운영 DB에는 RP-4 사전점검만 수행했으며 데이터 변경은 없다. 운영 앱에는 아직 RP-4가 배포되지 않았다.

## 8. RP-4A 실행 기록

- 실행 결과: `ready_for_rp4=true`
- 캠페인: `OPEN-STAGE-2026-V1`, 상태 `pilot`
- 잠금: `live_signup_wiring=false`, `pilot_signup_limit=1`
- RP-3 사건: 초대자 `SDW00000007`, 첫 후보 예정자 `GGS00000027`, 장부 `verified`
- 회원원장 27명, 참가자 24명, 장부 1건
- RP-4 함수 미설치 확인
- 증빙: `_backups/open_stage/20260729_RP4/rp4a-preflight-pass.png`
- 증빙 SHA-256: `42A0004398092EC8293B86275C5989621A163719E21431F7118605A48C6D529B`
- 판정: RP-4B DB 설치 진행 가능. 앱 배포와 운영 활성화는 아직 금지.

## 9. RP-4B 설치 기록

- 캠페인 `pilot`
- `operating_mode_enabled=false`, `live_signup_wiring=false`
- 운영 배치 한도 100, 시작 기준 verified 장부 1건
- 회원원장 27명 유지
- 참가자 25명, 장부 1건
- 첫 후보 `GGS00000027`, 상태 `candidate`
- 후보 진행률 0/5, 최대 인정 10명
- 증빙: `_backups/open_stage/20260729_RP4/rp4b-prepare-installed-locked.png`
- 증빙 SHA-256: `2291DF8CF22F4EB028904DB6375404C69FDFE73ABF015C441350ED27C468B7B0`
- 판정: 설치 결과값 정상·운영 잠금 유지. `verify_open_stage_rp4_v1.sql` 읽기 검증 전까지 앱 배포 금지.

## 10. RP-4B 설치 검증 기록

- 최종 결과 `PASS`
- 캠페인 `pilot`
- operating·wiring 모두 `false`
- 운영 한도 100, 기준 장부 1
- 회원원장 27명, 참가자 25명, 장부 1건
- `GGS00000027` 후보 0/5·초대한도 10
- `campaign_open=false`, `can_invite=false`
- Founder 플랜 자동변경 없음
- 증빙: `_backups/open_stage/20260729_RP4/rp4b-verification-pass.png`
- 증빙 SHA-256: `6315390735D2C41DB34C7A86557792876B57CB843C9004CC574051D79DB6D1B9`
- 판정: RP-4C 앱 배포 가능. 운영 활성화와 실제 초대는 아직 금지.
