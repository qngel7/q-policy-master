# Q메일 Open Stage Founder 초대 RP-5

> 작성일: 2026-07-29  
> 캠페인: `OPEN-STAGE-2026-V1`  
> 대외 식별: Q-ID  
> 내부 관계 식별: `account_id`  
> 상태: RP-5C 운영 DB 최종 검증 `PASS`, 앱 배포 전

## 0. RP-5A 운영 사전점검 결과

2026-07-29 운영 Supabase에서 `preflight_open_stage_rp5_v1.sql` 실행 결과:

- `ready_for_rp5=true`
- 캠페인 `active`
- `operating_mode_enabled=true`
- `live_signup_wiring=true`
- RP-2 기가입회원 스냅샷 참가자 23명
- 현재 Founder 참가자 8명
- 비Founder 5명 미션 대상 16명
  - 기가입 비Founder 15명
  - RP-3 신규 후보 `GGS00000027` 1명
- 수동 승인 대기 0명
- 정책 정규화 필요 0명
- RP-5 승인 함수 미설치 상태 확인

따라서 현재 참가자 정책은 이미 10/5 기준과 일치하며, RP-5 설치에서는
수동 승인·복원 감사기반과 Founder/비Founder 화면 구분을 추가한다.

### RP-5B 운영 DB 설치 결과

2026-07-29 운영 Supabase에서 `prepare_open_stage_rp5_v1.sql` 실행 결과:

- `result=PASS`
- 캠페인 `active` 유지
- 초대한도 10명 적용 참가회원 24명
- 비Founder 5명 미션 대상 16명
- 기존 Founder 미션면제 8명
- 수동 승인 함수 설치 `true`
- 자동 플랜 변경 없음
- Seed 수동 승인만 허용

`RP-5-INSTALL` 체크포인트와 참가자 정책 백업, 승인·복원 감사장부가
운영 DB에 생성되었다.

### RP-5C 운영 DB 최종 검증 결과

2026-07-29 운영 Supabase에서 `verify_open_stage_rp5_v1.sql` 실행 결과:

- `result=PASS`
- 캠페인 `active`
- operating/wiring 모두 `true`
- 초대한도 10명 적용 참가회원 24명
- 기존 Founder 미션면제 8명
- 비Founder 5명 미션 대상 16명
- 수동 승인 대기 0명
- 활성 수동 승인 0명
- 자동승격 없음

DB 정책·권한·백업·승인 감사기반 검증을 통과했다. 다음 단계는 앱 배포 후
기존 Founder와 비Founder 본인 화면의 문구·개인 이벤트 링크를 확인하는 것이다.

### 이철승 유료 Founder 보정 후 전체 재검증

2026-07-29 `LCS00000012` 이철승의 $100 Standard Founder 보정과
두 이름메일 확정 후 `verify_open_stage_rp5_v1.sql`을 다시 실행했다.

- `result=PASS`
- 초대한도 10명 적용 참가회원 24명
- 기존 Founder 미션면제 9명
- 비Founder 5명 미션 대상 15명
- 수동 승인 대기 0명
- 활성 수동 승인 0명

회원 보정 후에도 RP-5 정책·권한·감사장부 정합성이 유지된다.

## 1. 확정 정책

- 이벤트 참가회원은 가입 플랜과 관계없이 최대 10명의 유효 가입을 초대 실적으로 인정한다.
- 서대원 Seed는 초기 모집 운영자이므로 기존 Seed 한도를 유지한다.
- 현재 `plan='founder'` 회원도 10명까지 초대할 수 있지만 Founder 미션 대상은 아니다.
- `plan<>'founder'` 회원만 유효 가입 5명을 달성하면 `qualified`가 된다.
- 5명 달성만으로 회원 플랜을 자동 변경하지 않는다.
- `qualified` 회원은 운영자가 실적을 확인한 뒤 별도 수동 승인해야 Founder로 인정한다.
- 수동 승인 시에만 `registrations.plan='founder'`,
  `registrations.is_founder=true`, 참가 상태 `approved`가 된다.
- 승인과 복원은 모두 별도 감사장부와 체크포인트에 기록한다.

## 2. 회원별 동작

| 회원 구분 | 초대 한도 | 5명 미션 | 5명 달성 결과 | Founder 반영 |
|---|---:|---|---|---|
| Seed 운영자 | 기존 운영 한도 | 면제 | 해당 없음 | 기존 상태 유지 |
| 기존 Founder | 10명 | 면제 | 해당 없음 | 기존 상태 유지 |
| 기존 비Founder | 10명 | 적용 | `qualified` | Seed 수동 승인 |
| 초대로 가입한 비Founder 후보 | 10명 | 적용 | `qualified` | Seed 수동 승인 |

기존 Founder 화면에는 `n/10명 초대`가 표시되고, 비Founder 화면에만
`n/5명 가입`과 수동 승인 대기 상태가 표시된다.

## 3. 운영 DB 적용 순서

아래 순서를 바꾸지 않는다. 앱을 먼저 배포하면 아직 설치되지 않은
`open_stage_invite_status_v2` 호출이 실패할 수 있다.

1. `preflight_open_stage_rp5_v1.sql`
2. 결과 `ready_for_rp5=true` 확인 — 2026-07-29 `PASS`
3. `prepare_open_stage_rp5_v1.sql` — 2026-07-29 `PASS`
4. 결과 `PASS`, `manual_approval_function_installed=true` 확인 완료
5. `verify_open_stage_rp5_v1.sql` — 2026-07-29 `PASS`
6. 결과 `PASS` 확인 완료
7. `publish.bat`으로 앱 배포
8. 기존 Founder 1명과 비Founder 1명으로 화면 문구와 개인 캠페인 링크 확인

DB 설치 전 참가자 정책은 `open_stage_rp5_participant_backup`에 저장된다.
설치 체크포인트는 `RP-5-INSTALL`이다.

## 4. 승인 대기 명단 확인

`list_open_stage_founder_approval_queue_v1.sql`을 실행한다.

명단에는 아래 조건을 모두 충족한 회원만 표시된다.

- 현재 플랜이 Founder가 아님
- 캠페인 참가 상태가 `qualified`
- verified 가입 5명 이상
- 기존 Founder 자격면제 대상이 아님
- 아직 활성 수동 승인 이력이 없음

대외 운영 화면과 조회 결과에는 Q-ID를 사용하고 `account_id`는 노출하지 않는다.

## 5. Founder 수동 승인

`run_open_stage_founder_manual_approval_v1.sql`에서 `TARGET_Q_ID`를 실제
대상 Q-ID로 바꾸고 승인 메모를 확인한 뒤 실행한다.

승인 함수:

```sql
SELECT *
FROM public.open_stage_founder_approve_v1(
  'OPEN-STAGE-2026-V1',
  '대상_Q-ID',
  'SDW00000007',
  '5명 유효가입 확인 후 Open Founder 수동 승인'
);
```

함수는 다음 조건을 다시 검증한다.

- 캠페인 기간과 상태가 유효함
- 승인자가 캠페인 Seed임
- 대상자가 비Founder `qualified` 회원임
- 유효 가입이 실제로 5명 이상임
- 초대한도 10명·필요인원 5명 정책이 일치함

조건이 하나라도 다르면 전체 승인이 롤백된다.

## 6. 개별 오승인 복원

`run_open_stage_founder_manual_reversal_v1.sql`에서 대상 Q-ID와 복원 사유를
확인한 뒤 실행한다.

복원 함수는 승인장부에 저장된 이전 `plan`과 `is_founder` 값을 되돌리고
참가 상태는 5명 달성 상태인 `qualified`로 유지한다.

승인 후 다른 절차로 참가 상태가 `claimed`가 되었다면 자동 복원을 거부한다.
이 경우 후속 권리관계를 먼저 확인한다.

## 7. RP-5 전체 복원

1. 활성 수동 승인 건을 모두 개별 복원한다.
2. `rollback_open_stage_rp5_v1.sql`을 실행한다.
3. 앱 코드를 RP-4 배포 커밋으로 함께 복원한다.

활성 승인이 한 건이라도 남아 있으면 전체 복원 SQL은 자동 중단한다.
회원 가입정보와 추천 장부는 삭제하지 않는다. 승인 감사장부와 참가자 백업도
전체 복원 후 보존한다.

## 8. 파일

- `services/010/db/preflight_open_stage_rp5_v1.sql`
- `services/010/db/prepare_open_stage_rp5_v1.sql`
- `services/010/db/verify_open_stage_rp5_v1.sql`
- `services/010/db/list_open_stage_founder_approval_queue_v1.sql`
- `services/010/db/run_open_stage_founder_manual_approval_v1.sql`
- `services/010/db/run_open_stage_founder_manual_reversal_v1.sql`
- `services/010/db/rollback_open_stage_rp5_v1.sql`
- `services/010/db/open_stage_rp5_manifest.sha256`

## 9. 확정 초대장 연결

2026-07-29 기준 초대 버튼에 사용하는 최종 디자인은 특정 초대인 명의가
들어간 초기안이 아니라 아래의 시기 초대형 프리런칭 초대장이다.

- 승인 원본:
  `outputs/qmail_open_stage_invitation/Q메일_프리런칭_초대장_카카오.png`
- 운영 공개 파일:
  `services/010/public/images/qmail-prelaunch-invitation-2026.png`
- SHA-256:
  `9617E81DE1F78015C358DCFD78252B2E88B3683F1B6029BF748CEF39C344D2EE`
- 동봉 문구 원본:
  `outputs/qmail_open_stage_invitation/초대장_동봉메시지.md`

`Open Stage 초대`, Founder 초대 이벤트, Open Founder 후보 화면은 모두
`shareMemberInvitation()`을 호출한다. 공유 순서는 다음과 같다.

1. 카카오 JavaScript SDK가 준비됐으면 승인 초대장 이미지·확정 문구·개인
   캠페인 링크로 카카오 피드 공유
2. 카카오 SDK를 쓸 수 없으면 Web Share의 이미지 파일 공유
3. 파일 공유도 불가능하면 확정 동봉 메시지와 개인 링크 공유
4. 공유 API가 없으면 전체 메시지를 클립보드 또는 복사창으로 제공

개인 링크의 `ref` Q-ID와 `campaign=OPEN-STAGE-2026-V1`는 유지하고,
링크 미리보기 캐시 분리를 위해 공유 시 `share_v=RP5`만 추가한다.
가입 API는 `ref`와 `campaign`만 해석하므로 초대 귀속에는 영향이 없다.

HTML의 OG·Twitter 미리보기도 같은 승인 이미지와 확정 핵심 문구를 사용한다.
이미지 URL에는 `v=20260729-rp5-1`을 붙인다. 이는 배포 직전 존재하지 않던
새 정적 파일의 첫 요청이 SPA HTML로 캐시되는 경우를 우회하기 위한 자산
버전값이며 초대장 이미지 내용이나 초대 귀속에는 영향을 주지 않는다.
기존에 발송한 URL에서 예전 `VIP Invitation` 카드가 남으면 배포 후 카카오
URL 메타정보 관리 도구에서 해당 시험 URL의 캐시만 초기화한다.

로컬 전체 테스트 결과: `npm test` PASS, 이철승 보정 및 확정 초대장 연결 포함
Open Stage 39/39 PASS.
