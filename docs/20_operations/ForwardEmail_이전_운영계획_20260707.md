# ForwardEmail 이전 운영계획

작성일: 2026-07-07  
대상: 010.Q 실서비스, Q메일 수신 포워딩

## 목적

Cloudflare Email Routing에 의존하던 연결메일 등록/포워딩 흐름을 ForwardEmail 기반으로 이전한다. Cloudflare Pages는 계속 웹 호스팅 용도로 사용하되, 메일 수신 MX와 alias 관리는 ForwardEmail을 기준으로 운영한다.

## 현재 코드 반영 상태

- `services/010/functions/api/register.js`
  - 신규/임시 가입 시 ForwardEmail alias를 생성 또는 갱신한다.
  - 기본 alias: `01012345678@q.co.kr`
  - OKQ/Founder 간편 수신 alias: `12345678@q.co.kr`
  - 대표 발급·저장 주소는 플랜과 관계없이 `01012345678@q.co.kr`이며, 8자리와 기호 포함 형태는 같은 주소로 연결되는 수신 호환 표기다.
  - 이름메일 alias: `kor_email`, `eng_email`이 `@q.co.kr`이면 함께 생성 또는 갱신한다.
  - 카카오 인증으로 최종 가입이 완료되면 11자리 기본 alias 생성 완료 후 해당 Q메일 주소로 웰컴메일을 발송한다.
  - 웰컴메일은 `새 Q메일 → 연결 이메일` 경로로 전달되므로, 수신 자체가 주소 발급과 포워딩 정상 여부를 확인한다.
- `services/010/functions/api/update-registration.js`
  - 카카오 인증 후 최종 가입 승격 시 동일하게 ForwardEmail alias를 생성 또는 갱신한다.
  - 초대·QR 임시 가입을 최종 활성화한 경우에도 대표 Q메일 주소로 동일한 웰컴메일을 발송한다.
- `services/010/functions/api/test-email-routing.js`
  - ForwardEmail 환경변수와 alias API 응답을 확인하는 진단 API로 변경했다.

## 필요한 환경변수

Cloudflare Pages의 010.Q 프로젝트 환경변수에 아래 값을 추가한다.

| 이름 | 용도 |
|---|---|
| `FORWARDEMAIL_API_KEY` | ForwardEmail API Basic Auth 토큰 |
| `WELCOME_EMAIL_FROM` | 웰컴메일 발신자. 선택값이며 기본값은 `Q <Q@q.co.kr>` |
| `WELCOME_EMAIL_APP_URL` | 웰컴메일의 프로필·대시보드 기준 URL. 선택값이며 기본값은 `https://010.q.co.kr` |

기존 `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `SESSION_SECRET`, `KAKAO_REST_API_KEY`는 그대로 유지한다.

## DNS 이전 절차

1. Cloudflare DNS에서 현재 `q.co.kr`의 MX/TXT/Email Routing 설정을 캡처한다.
2. ForwardEmail 계정에서 `q.co.kr` 도메인을 추가하고 검증한다.
3. Cloudflare DNS에서 기존 Cloudflare Email Routing MX를 제거한다.
4. ForwardEmail MX를 추가한다.

| Name | Type | Priority | Value |
|---|---|---:|---|
| `@` | MX | 0 | `mx1.forwardemail.net` |
| `@` | MX | 0 | `mx2.forwardemail.net` |

5. SPF TXT를 확인한다.

```text
v=spf1 a include:spf.forwardemail.net -all
```

이미 다른 SPF가 있으면 `include:spf.forwardemail.net`를 기존 SPF 안에 병합한다. SPF TXT는 한 도메인에 여러 개 두지 않는다.

6. ForwardEmail 대시보드에서 DKIM/DMARC/Return-Path 안내가 나오면 그대로 추가한다.
   - 웰컴메일 발송을 위해 `Q@q.co.kr` alias가 존재해야 한다. 다른 발신 주소를 사용할 때는 해당 alias를 만든 뒤 `WELCOME_EMAIL_FROM`에 지정한다.
   - ForwardEmail의 Outbound SMTP Configuration에서 DKIM, Return-Path, DMARC 검증을 모두 완료한다.
7. DNS 전파 후 `https://010.q.co.kr/api/test-email-routing`으로 환경변수를 확인한다.
8. 테스트 alias를 생성한다.

```json
{
  "alias": "01012345678",
  "recipient": "owner@example.com"
}
```

9. 실제 외부 메일에서 `01012345678@q.co.kr`로 발송해 수신 여부를 확인한다.

## 운영상 주의점

- Cloudflare Email Routing을 끄더라도 Cloudflare Pages, DNS, Workers/Pages Functions는 계속 사용한다.
- ForwardEmail은 alias 기반이므로, 가입/수정 시 alias 생성이 실패해도 DB 가입은 성공할 수 있다. 배포 직후에는 `test-email-routing`과 실제 수신 테스트를 반드시 수행한다.
- 웰컴메일 발송 실패는 가입 성공 응답을 막지 않는다. Cloudflare Pages Functions 로그의 `[WelcomeEmail]` 경고와 ForwardEmail Outbound Emails 기록을 함께 확인한다.
- 웰컴메일은 임시 저장에는 발송하지 않고, 카카오 인증과 active 전환 및 로그인 세션 생성이 모두 성공한 최종 가입에만 한 번 예약한다.
- 기존 Cloudflare Worker `code/email-worker`는 MX가 ForwardEmail로 전환되면 Q메일 수신 라우터 역할을 하지 않는다. 필요 시 보관용으로 두되 신규 수신 경로에는 포함하지 않는다.
- 기존 가입자 alias 일괄 생성은 별도 배치가 필요하다. 현재 코드 변경은 신규/수정 가입부터 적용된다.

## 참고

- ForwardEmail FAQ: https://forwardemail.net/en/faq
- ForwardEmail API: https://forwardemail.net/en/email-api
