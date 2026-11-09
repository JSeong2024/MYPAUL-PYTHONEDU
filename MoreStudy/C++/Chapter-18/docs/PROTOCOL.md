# TCP 메시지 계약

[← Chapter 18](../README.md) · [Coding Practice](../README.md#section-18-19)

## wire format

하나의 메시지는 **4바이트 길이 헤더 + payload**로 구성함.

| Offset | Length | Meaning |
|---:|---:|---|
| 0 | 4 bytes | Payload size, unsigned 32-bit, network byte order (big-endian) |
| 4 | `size` bytes | Payload bytes; 0~4096 bytes |

`PING`의 wire frame은 `00 00 00 04 50 49 4E 47` (16진수)임. 총 8바이트.

* TCP는 바이트 스트림이므로 `send()` 한 번에 대응하는 `recv()`가 한 번 호출된다는 보장은 없음.
* 4바이트 길이부터 정확히 수신하고 상한을 확인한 뒤 payload를 할당해야 함.
* 수신값이 4096을 넘으면 거부하고 연결을 정리함. 잘린 메시지도 실패로 처리함.
* payload는 널 종료 문자열이 아님. 문자열 변환 시 수신 바이트 수를 반드시 활용함.
* 메시지 길이는 **바이트 수**이며 UTF-8 글자 수가 아님.
* 이 수업용 계약은 압축·암호화·인증·체크섬을 제공하지 않음.

## 명령 계약

Advanced 프로그램은 `READ <device> <value>` 형태를 사용함. `device`는 영문·숫자·`_`·`-`로 된 1~16글자이고 `value`는 0~1000의 정수임. 공백·추가 토큰·오버플로를 허용하지 않음.

| Request | Reply | Reason |
|---|---|---|
| `READ A 20` | `OK` | 정상 측정값 |
| `READ pump-1 0` | `OK` | 경계값 허용 |
| `READ A 1001` | `ERR invalid reading` | 허용 범위 초과 |
| `READ A 1x` | `ERR invalid reading` | 숫자 전체 파싱 실패 |
| `READ A 3 ` | `ERR invalid reading` | 추가 공백 |

Pro의 명령은 `PING`, `UPPER <lowercase-ascii>`임. 응답은 각각 `PONG`, 대문자 문자열이고, 잘못된 명령에는 `ERR ...`를 반환함. 라이브러리 수준 입력 거부와 실제 프로토콜의 `ERR` 응답을 구분해야 함.

## 운영 시 확장 고려 사항

1. 프로토콜 버전과 유형 필드 추가
2. 요청 식별자, 응답 식별자, 중복 처리 방지 키
3. 절대 시간 제한(Deadline), 비정상적으로 느린 송신자 방어
4. 상호 인증·TLS·액세스 제어 및 로깅
5. 무한 재시도 방지와 Backpressure 설계
6. 프로토콜 오류의 명확한 분류 및 관측 지표
