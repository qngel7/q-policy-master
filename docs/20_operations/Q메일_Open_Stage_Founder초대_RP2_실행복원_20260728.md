# Q메일 Open Stage Founder 초대 RP-2 실행·복원

> 작성일: 2026-07-28
> 캠페인: `OPEN-STAGE-2026-V1`
> 승인 범위: 서대원 Seed → 기가입회원 기준시점 스냅샷 → Q-ID 개인 링크 → 3~5계정 자동롤백 검증
> 현재 상태: RP-2A~RP-2D 전체 `PASS` · RP-2 완료 · 라이브 연결은 RP-3 별도 승인 대기
> 기준 복원지점: RP-1 `PASS` · 커밋 `9d55947772ffcd69e26a790bebc245a6c9ac146f`

## 1. 이번 단계에서 바뀌는 것

- 서대원 현재 Q-ID를 확인하고 내부 `account_id`로 연결한 Seed 참가자 1건을 만든다.
- 실행 기준시각 이전에 가입된 `status='active'`, `enrollment_phase<>'test'` 회원을 기가입 초대회원으로 스냅샷 등록한다.
- 서대원은 세대 0, 기가입회원은 세대 1로 기록한다.
- 일반·OK-Q 기가입회원은 초대 인정 한도 10명, Open Founder 후보 기준 5명을 갖는다.
- 기존 `plan='founder'` 회원은 기존 플랜을 유지하고 재승격 대상에서는 제외한다.
- 각 참가자의 현재 Q-ID로 개인 링크를 생성하는 서버 전용 함수를 만든다.
- 캠페인 상태를 `draft`에서 `pilot`으로 전환하고 RP-2 체크포인트를 남긴다.

## 2. 이번 단계에서 바뀌지 않는 것

- `registrations`의 Q-ID, `referrer_qid`, 플랜, Founder 여부, 상태
- 010.Q 가입 화면과 가입 API
- 현재 `?ref=Q-ID` 추천 저장 방식
- 초대장·기가입회원 안내장의 운영 링크
- Founder 플랜 자동부여
- 실제 사용자 대상 초대 발송

따라서 RP-2 완료 후에도 개인 링크는 내부 확인용이다. 실제 발송은 가입 API 자동 장부 연결을 다루는 다음 단계 승인 후 시작한다.

## 3. 식별 및 스냅샷 원칙

- 대외 입력·표시·링크: Q-ID
- 내부 FK·중복 방지·트랜잭션: `account_id`
- Seed 입력 Q-ID: `SDW00000007`
- 서버는 현재 Q-ID 또는 `q_id_aliases`를 통해 Seed의 현재 Q-ID와 `account_id`를 확인한다.
- 스냅샷 기준시각은 `prepare_open_stage_rp2_v1.sql` 트랜잭션에서 `clock_timestamp()`로 한 번 고정한다.
- 기준시각 이후 가입자는 RP-2 기가입회원 스냅샷에 포함하지 않는다.
- 영구 테스트 계정 `TST00000004` 및 `enrollment_phase='test'` 계정은 제외한다.

## 4. RP-2 실행본 SHA-256

동일한 값은 `services/010/db/open_stage_rp2_manifest.sha256`에 기록한다.

| 파일 | SHA-256 |
|---|---|
| `preflight_open_stage_rp2_v1.sql` | `A8F9B9A89FC2386FEE84C3ABE5C0F81FAC977A2F3B4812314458EC67DDA05244` |
| `prepare_open_stage_rp2_v1.sql` | `E079803653A5B9588D081F08C58D1E680482E6A588D522B9371E0C2C3B033B65` |
| `run_open_stage_rp2_pilot_v1.sql` | `BD39197F39BDEFE2B9E24A724B55D85313DA14FE456F69FF83B53ACF6EAD62C9` |
| `verify_open_stage_rp2_v1.sql` | `016E5AF12BDAD540E0DE4DCBA6575035F0C1C95E911403FD32572E5D7E204BC7` |
| `rollback_open_stage_rp2_v1.sql` | `D059F72C465588B172CBA6600A3E6AE75B79E3E9A21ADE353545E630385EE5F2` |

실행 직전 해시가 다르면 파일을 실행하지 않고 운영 문서와 매니페스트를 먼저 갱신한다.

## 5. RP-2 직전 복원 기준

- Git 기준: `9d55947772ffcd69e26a790bebc245a6c9ac146f`
- Supabase 기준: `open_stage_release_checkpoints.checkpoint_code='RP-1'`
- 캠페인 상태: `draft`
- 참가자: 0
- 영구 초대 장부: 0
- RP-2 직전 파일 백업: `_backups/open_stage/20260728_RP2_PRE/`
- 백업 매니페스트: `_backups/open_stage/20260728_RP2_PRE/manifest.sha256`

가입 화면·가입 API·RP-1 SQL·초대문 10개 파일의 원본과 백업본 SHA-256을 대조한다.

## 6. 단계별 실행

### RP-2A · 사전점검

Supabase Production · Primary Database · role `postgres`에서 다음 파일만 실행한다.

```text
services/010/db/preflight_open_stage_rp2_v1.sql
```

마지막 결과에서 확인할 항목:

- `ready_for_rp2 = true`
- `campaign_status = draft`
- `seed_q_id = SDW00000007` 또는 별칭 해석 후 표시된 현재 Q-ID
- `seed_name = 서대원`
- `eligible_existing_members >= 3`
- `founder_candidates`, `existing_founders`, `excluded_test_accounts`
- `registrations_fingerprint`

이 결과 화면을 확인하기 전에는 RP-2B를 실행하지 않는다.

### RP-2B · Seed·기가입회원 스냅샷

사전점검 결과가 정상일 때 다음 파일을 실행한다.

```text
services/010/db/prepare_open_stage_rp2_v1.sql
```

처리 결과:

- Seed 1명
- 활성 비테스트 기가입회원 스냅샷
- 캠페인 `pilot`
- 영구 장부 0
- RP-2 체크포인트
- Q-ID 개인 링크 함수
- 3~5계정 자동롤백 파일럿 함수

### RP-2C · 설치 검증

```text
services/010/db/verify_open_stage_rp2_v1.sql
```

마지막 결과가 다음과 같아야 한다.

```text
PASS
RP-2 Seed·기가입회원 스냅샷·Q-ID 개인 링크 준비 완료 · 영구 장부 0 · 라이브 미연결
```

검증 내용:

- RP-2 기준시각 이전 회원원장 지문 불변
- Seed 정확히 1명
- 기가입 대상과 참가자 수 일치
- 테스트 계정 제외
- 기존 Founder 재승격 제외
- Q-ID 개인 링크에 `account_id` 미노출
- 내부 함수의 `anon`, `authenticated` 권한 차단
- 영구 장부 0

### RP-2D · 3~5계정 자동롤백 파일럿

```text
services/010/db/run_open_stage_rp2_pilot_v1.sql
```

표본은 기가입 활성계정 중 5개를 사용한다. 가능한 대상이 3~4개면 해당 수로 자동 축소한다. 회원 이름은 판정에 사용하지 않고 Q-ID를 표시한다.

마지막 단일 결과에서 다음을 확인한다.

- `final_result = PASS`
- `actual_sample_size = 3~5`
- `verified_rows = actual_sample_size`
- `sample_invitee_q_ids`에 사용된 Q-ID 표시
- 표본 5개이면 `would_qualify = true`
- `persistent_ledger_delta = 0`
- `persistent_ledger_rows = 0`

파일럿 함수는 실제 `open_stage_invite_ledger`에 INSERT하여 FK·중복·본인초대·상태 제약을 검사한 뒤, 하위 트랜잭션 예외 처리로 테스트 INSERT만 자동 롤백한다.

## 7. 개인 링크 조회

RP-2C가 `PASS`한 후 관리자 SQL Editor에서만 조회한다.

```sql
SELECT *
FROM public.open_stage_list_personal_links_v1(
  'OPEN-STAGE-2026-V1'
)
ORDER BY eligibility_generation, member_q_id;
```

링크 형식:

```text
https://010.q.co.kr/?ref=<현재-Q-ID>&campaign=OPEN-STAGE-2026-V1
```

이 링크는 아직 실제 발송하지 않는다. 현재 가입 화면은 `ref`만 일반 추천인으로 보관하며 캠페인 장부 자동 기록은 다음 단계에서 연결한다.

## 8. 이상 발생 시 복원

사전점검 SQL이 실패하면 아무 데이터도 변경되지 않으므로 오류 화면을 보존하고 중단한다.

준비 SQL 실행 후 검증이 실패하면 다음 파일을 실행한다.

```text
services/010/db/rollback_open_stage_rp2_v1.sql
```

복원 동작:

- 캠페인 `paused`
- RP-2 내부 함수의 `service_role` 실행권 회수
- 영구 장부가 0이면 RP-2 배치 참가자를 `revoked`
- 영구 장부가 있으면 참가자와 장부를 보존하고 캠페인만 정지
- `registrations` 무변경
- 테이블·참가자·감사 장부 물리 삭제 없음

## 9. 금지사항

- RP-2A 확인 전 RP-2B 실행
- SQL 파일 일부만 선택 실행
- `SDW00000007`을 다른 사람 Q-ID로 임의 교체
- `enrollment_phase='test'` 계정을 실제 참가자에 포함
- 개인 링크 실사용자 발송
- 가입 API·화면 수동 수정
- `plan`, `is_founder`, `referrer_qid` 수동 변경
- 검증용 참가자나 장부 물리 삭제

## 10. RP-2 완료 기록란

```text
코드 배포일시:
배포 커밋:
사전점검 실행일시:
실행자 Q-ID:
seed_q_id:
eligible_existing_members:
existing_founders:
founder_candidates:
excluded_test_accounts:
registrations_fingerprint:
prepare 결과:
verify 결과:
campaign 상태:
participant 건수:
영구 ledger 건수:
파일럿 actual_sample_size:
파일럿 sample_invitee_q_ids:
파일럿 persistent_ledger_delta:
파일럿 persistent_ledger_rows:
RP-2 checkpoint_at:
비고:
```

## 11. RP-2A 사전점검 확정 기록

| 항목 | 결과 |
|---|---|
| 실행 결과 | `ready_for_rp2 = true` |
| 캠페인 | `OPEN-STAGE-2026-V1` |
| 캠페인 상태 | `draft` |
| Seed Q-ID | `SDW00000007` |
| Seed 이름 | `서대원` |
| 기가입 스냅샷 대상 | 24명 |
| 기존 Founder | 9명 |
| Founder 후보 | 15명 |
| 제외 테스트계정 | 1명 |
| 전체 registrations | 26명 |
| 회원원장 지문 | `8af606d87870554f1963a2c10abf684f` |
| DB 확인시각 | `2026-07-28 13:22:42.394523+00` |
| 한국시각 | `2026-07-28 22:22:42.394523+09` |

### RP-2A 검증 증빙

- 파일: `_backups/open_stage/20260728_RP2/rp2a-preflight-pass.png`
- SHA-256: `ADE2E6B6F7EC9E281542D21E38F015F2E376FD194A00117CC22D9A184706BB58`
- 매니페스트: `_backups/open_stage/20260728_RP2/manifest.sha256`
- 확인 환경: Supabase Production · Primary Database · role `postgres`

RP-2A는 통과했다. 다음 허용 작업은 `prepare_open_stage_rp2_v1.sql` 전체 실행이다. RP-2B 결과 확인 전 검증·파일럿 SQL을 이어서 실행하지 않는다.

## 12. RP-2B 준비 확정 기록

- `prepare_open_stage_rp2_v1.sql` 전체 실행 성공
- Seed: `SDW00000007`, 역할 `seed`, 세대 0, 상태 `approved`
- Seed 초대한도: 캠페인 총한도 1,000, 재자격 기준 0, `qualification_exempt=true`
- 기가입회원: 역할 `candidate`, 세대 1
- 기존 Founder: 상태 `approved`, 기준 0, `qualification_exempt=true`
- Founder 후보: 상태 `candidate`, 초대한도 10, 기준 5, `qualification_exempt=false`
- Q-ID 개인 링크가 `?ref=<Q-ID>&campaign=OPEN-STAGE-2026-V1` 형식으로 생성됨
- 마지막 결과의 10개 행은 `LIMIT 10` 미리보기이며 전체 참가자 수 검증은 RP-2C에서 수행

### RP-2B 검증 증빙

- 파일: `_backups/open_stage/20260728_RP2/rp2b-prepare-personal-links.png`
- SHA-256: `3A9B7A2506F638354E15732B90EE2998DE17484653DA8A4AC367B1293266241C`
- 매니페스트: `_backups/open_stage/20260728_RP2/manifest.sha256`
- 확인 환경: Supabase Production · Primary Database · role `postgres`

RP-2B는 완료되었다. 다음 허용 작업은 읽기 전용 `verify_open_stage_rp2_v1.sql` 전체 실행이다. 검증 결과 확인 전 파일럿 SQL은 실행하지 않는다.

## 13. RP-2C 검증 확정 기록

- `verify_open_stage_rp2_v1.sql` 전체 실행 성공
- 최종 결과: `PASS`
- 확인 메시지: `RP-2 Seed·기가입회원 스냅샷·Q-ID 개인 링크 준비 완료 · 영구 장부 0 · 라이브 미연결`
- 영구 초대 장부: 0건
- 가입 API·초대장 링크·실서비스 가입 동선: 미연결

### RP-2C 검증 증빙

- 파일: `_backups/open_stage/20260728_RP2/rp2c-verification-pass.png`
- SHA-256: `D39F6A8A51133D3C2A09EBC8960C8304D5D935A8E1EBC6744E1812291582A3F4`
- 매니페스트: `_backups/open_stage/20260728_RP2/manifest.sha256`
- 확인 환경: Supabase Production · Primary Database · role `postgres`

RP-2C는 통과했다. 다음 허용 작업은 `run_open_stage_rp2_pilot_v1.sql` 전체 실행이다. 이 파일럿은 유효한 기가입회원 3~5명을 자동 선정하여 초대 귀속·5명 기준·장부 제약을 검사하고, 하위 트랜잭션에서 만든 임시 장부를 자동 롤백한다.

## 14. RP-2D 자동롤백 파일럿 확정 기록

| 항목 | 결과 |
|---|---|
| 최종 결과 | `PASS` |
| Seed Q-ID | `SDW00000007` |
| 요청 표본 | 5명 |
| 실제 표본 | 5명 |
| 표본 Q-ID | `ACB00000011`, `BNB00000009`, `CYS00000025`, `HSU00000010`, `JMO00000001` |
| 검증 장부 | 5건 |
| Open Founder 기준 | 5명 |
| 기준 충족 판정 | `true` |
| 영구 장부 증감 | 0건 |
| 영구 장부 잔존 | 0건 |

파일럿에서 만든 테스트 장부 5건은 하위 트랜잭션에서 자동 롤백되었다. 따라서 표본 회원의 실제 초대 실적·Founder 자격·회원 플랜은 변경되지 않았다.

### RP-2D 검증 증빙

- 파일: `_backups/open_stage/20260728_RP2/rp2d-pilot-pass.png`
- SHA-256: `4FDCF0BA686AC41A75C24C9E4A4E147F34F526063E3BC6D2472F5717CEC2EDF3`
- 매니페스트: `_backups/open_stage/20260728_RP2/manifest.sha256`
- 확인 환경: Supabase Production · Primary Database · role `postgres`

RP-2는 완료되었다. Supabase에는 Seed·기가입회원 스냅샷과 Q-ID 개인 링크 생성 기반만 준비되어 있으며, 영구 초대 장부는 0건이다. 실제 초대장 링크, 가입 API, 초대 귀속, 5명 달성 자동승격은 연결하지 않았다. 해당 라이브 연결은 RP-3 계획·승인·복원지점 확정 후에만 진행한다.
