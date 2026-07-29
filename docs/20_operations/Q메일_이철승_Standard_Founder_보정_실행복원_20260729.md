# Q메일 이철승 Standard Founder 보정

> 작성일: 2026-07-29  
> 대상: 이철승 `LCS00000012`  
> 근거: Founder 회비 $100 납입  
> 등급: `standard`  
> 상태: 운영 사전점검·보정·최종검증·이메일 별칭·RP-5 전체 재검증 `PASS`, 앱 배포 전

## 0. 운영 사전점검 결과

2026-07-29 운영 Supabase에서
`preflight_leecheulseung_standard_founder_20260729.sql` 실행 결과:

- `result=PASS`
- Q-ID `LCS00000012`
- 실명 `이철승`
- 현재 플랜 `010q`
- `is_founder=false`
- `founder_tier` 열 없음
- 현재 `eng_email`, `kor_email` 모두 `NULL`
- RP-5 참가 상태 `candidate`
- 초대한도 10명, 필요 가입 5명, verified 0명
- 자격면제 `false`

회원·메일 충돌과 초대미션 승인 중복이 없으므로 Standard Founder 보정을
실행할 수 있다. 사전점검은 읽기 전용이며 회원 데이터는 변경하지 않았다.

### 운영 보정 트랜잭션 결과

2026-07-29 운영 Supabase에서
`promote_leecheulseung_standard_founder_20260729.sql` 실행 결과:

- `result=PASS`
- Q-ID `LCS00000012`, 실명 `이철승` 유지
- `plan=founder`
- `is_founder=true`
- `founder_tier=standard`
- 기존 `eng_name` 유지
- `eng_email=lcs@q.co.kr`
- `kor_email=이철승@q.co.kr`
- RP-5 참가 상태 `approved`
- 초대한도 10명, 필요 가입 0명, 자격면제 `true`

동일 트랜잭션에서
`RP-5-LCS-STANDARD-FOUNDER-PRE`와
`RP-5-LCS-STANDARD-FOUNDER-APPLY` 복원지점을 기록했다.

### 운영 최종검증 결과

2026-07-29 운영 Supabase에서
`verify_leecheulseung_standard_founder_20260729.sql` 실행 결과:

- `result=PASS`
- `OPEN-STAGE-2026-V1`
- 회원 `founder`, `is_founder=true`, `founder_tier=standard`
- `eng_email=lcs@q.co.kr`
- `kor_email=이철승@q.co.kr`
- 참가 상태 `approved`, 초대한도 10, 필요 가입 0, 자격면제 `true`
- Founder 미션면제 9명
- 비Founder 5명 미션 15명
- 초대미션 수동승인 장부 중복 없음
- PRE/APPLY 복원지점 확인

DB 회원 상태와 RP-5 참가자 정책은 최종검증을 통과했다.

### Forward Email 별칭 확정

2026-07-29 Forward Email 운영 화면에서 다음을 확인했다.

- `lcs@q.co.kr` 활성 유지
- `이철승@q.co.kr` 활성
- 두 별칭 모두 `msun21@naver.com`으로 전달
- 별도 IMAP 저장·비밀번호 생성 없음

따라서 Supabase의 `eng_email`, `kor_email` 기록과 실제 메일 전달 별칭이
일치한다.

### RP-5 전체 재검증 결과

2026-07-29 운영 Supabase에서 `verify_open_stage_rp5_v1.sql`을 다시 실행했다.

- `result=PASS`
- 캠페인 `active`
- operating/wiring 모두 `true`
- 초대한도 10명 적용 참가회원 24명
- Founder 미션면제 9명
- 비Founder 5명 미션 15명
- 수동 승인 대기 0명
- 활성 수동 승인 0명

이철승 유료 Founder 보정 후에도 RP-5 전체 정책·권한·장부 정합성이 유지된다.

## 1. 보정 원칙

- 대외 식별은 Q-ID `LCS00000012`를 사용한다.
- `account_id`는 DB 내부 조인과 잠금에만 사용하며 결과에 표시하지 않는다.
- 현재 `010q` 플랜을 `founder`로 변경한다.
- `is_founder=true`, `founder_tier='standard'`를 함께 기록한다.
- 운영 DB에 `founder_tier` 열이 없으면 적용 트랜잭션 안에서 해당 열만
  `ADD COLUMN IF NOT EXISTS`로 추가한다.
- 영문이름메일 필드 `eng_email`에는 `lcs@q.co.kr`을 기록한다.
- 한글이름메일 필드 `kor_email`에는 `이철승@q.co.kr`을 기록한다.
- 실제 영문 실명을 받지 않았으므로 `eng_name`은 추정하거나 변경하지 않는다.
- Q-ID, 전화번호, 추천인, 인증정보는 변경하지 않는다.
- 결제일을 확인하지 않은 상태이므로 구독 시작·종료일은 생성하지 않는다.
- Q-bit/Q-vic은 별도 자산 원장 검증 없이 발행하지 않는다.

## 2. RP-5 참가자 정책 동기화

회원 플랜만 Founder로 바꾸고 오픈스테이지 참가자를 그대로 두면
RP-5 검증에서 `Founder + 5명 미션` 불일치가 발생한다.

같은 트랜잭션에서 참가자 상태를 아래와 같이 맞춘다.

- 초대한도: 10명 유지
- 필요 가입: 5명에서 0명으로 변경
- 자격미션: 면제
- 참가 상태: `approved`
- 초대미션 수동승인 장부: 생성하지 않음

이 보정은 5명 초대미션 보상이 아니라 과거 $100 납입회원의 회원등급
정정이기 때문이다.

보정 후 다른 회원 변동이 없다면 RP-5 집계는 다음과 같이 변한다.

- Founder 미션면제: 8명 → 9명
- 비Founder 5명 미션: 16명 → 15명
- 초대한도 10명 참가회원: 24명 유지

## 3. 실행 순서

운영 Supabase SQL Editor에서 아래 순서를 바꾸지 않는다.

1. `preflight_leecheulseung_standard_founder_20260729.sql`
2. 결과 `PASS`, Q-ID `LCS00000012`, 이름 `이철승`, 현재 플랜 `010q` 확인
   - `founder_tier_column_exists=false`여도 정상이며 적용 SQL에서 안전하게 추가한다.
3. `promote_leecheulseung_standard_founder_20260729.sql`
4. 결과 `PASS`, 플랜 `founder`, 등급 `standard`, 두 이름메일 확인
5. `verify_leecheulseung_standard_founder_20260729.sql`
6. 결과 `PASS`, 참가 상태 `approved`, 한도 10, 필요인원 0, 면제 `true` 확인
7. 관리자 이메일 별칭 동기화를 실행해 `lcs`와 `이철승` 별칭을 연결메일로 확정
8. 기존 `verify_open_stage_rp5_v1.sql`을 다시 실행해 RP-5 전체 정책 `PASS` 확인
9. 그 다음에만 `publish.bat`을 실행한다.

## 4. 복원지점

적용 SQL은 한 트랜잭션에서 아래 체크포인트를 기록한다.

- 적용 직전: `RP-5-LCS-STANDARD-FOUNDER-PRE`
- 적용 완료: `RP-5-LCS-STANDARD-FOUNDER-APPLY`

문제 발생 시에만
`rollback_leecheulseung_standard_founder_20260729.sql`을 실행한다.

복원 SQL은 PRE 스냅샷의 아래 필드만 되돌린다.

- 회원: `plan`, `is_founder`, `founder_tier`, `eng_email`, `kor_email`
- 참가자: 상태·한도·필요인원·면제·승인시각

회원가입, Q-ID, 추천인, 초대장부, 구독·토큰 필드는 삭제하거나 덮어쓰지 않는다.
DB 복원 후에는 관리자 이메일 별칭 동기화를 다시 실행한다.

## 5. 파일

- `services/010/db/preflight_leecheulseung_standard_founder_20260729.sql`
- `services/010/db/promote_leecheulseung_standard_founder_20260729.sql`
- `services/010/db/verify_leecheulseung_standard_founder_20260729.sql`
- `services/010/db/rollback_leecheulseung_standard_founder_20260729.sql`
- `services/010/tests/leecheulseung-standard-founder.test.mjs`

로컬 Open Stage 회귀검증: 38/38 PASS.
