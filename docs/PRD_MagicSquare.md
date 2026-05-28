# PRD — Magic Square 4x4 TDD Practice

## 1. Executive Summary
Magic Square 4x4 TDD Practice는 알고리즘 난이도 경쟁이 아니라, 불변식 기반 사고와 계약 기반 검증을 중심으로 한 훈련형 프로젝트다. 본 프로젝트는 4x4 입력과 `int[6]` 출력 계약을 고정하고, Boundary와 Domain을 분리한 Dual-Track TDD를 통해 설계 → 테스트(RED) → 최소 구현(GREEN) → 리팩토링(REFACTOR) 흐름을 반복적으로 체득하는 것을 목표로 한다.

- 이 프로젝트가 훈련하려는 핵심 역량:
  - 불변식 사고
  - 입력/출력 계약
  - Dual-Track TDD
  - 설계 → 테스트 → 구현 → 리팩토링 흐름

## 2. Background
Report/1 기준으로 본 과제의 표면 문제는 "4x4 마방진을 만든다"였으나, 실제 학습 현장의 불편은 다중 제약(행/열/대각선 합, 범위, 중복)을 동시에 추적하고 일관되게 판정하는 데 있다. 학습자는 종종 구현부터 시작해 완성 기준을 사후에 맞추며, 이 과정에서 검증 기준이 흔들리고 회귀 오류를 늦게 발견한다. 따라서 본 프로젝트는 퍼즐 풀이 자체보다, 검증 가능한 조건을 먼저 정의하고 반복 가능한 테스트 루프로 품질을 유지하는 학습 환경 구축에 초점을 둔다.

## 3. Problem Statement
이 프로젝트의 문제는 "마방진을 생성한다"가 아니라, "검증 가능한 불변식 조건을 만족하는 상태를 판정하고 보장한다"로 정의한다.  
핵심은 다음 두 가지다.

- 동일 입력에 대해 동일 판정을 제공하는 결정적(Deterministic) 동작
- 입력/출력 계약을 사전에 고정해 테스트 가능성을 확보하는 설계

즉, 본 프로젝트는 정답 탐색 중심의 알고리즘 과제가 아니라 계약 중심 품질 훈련 과제다.

## 4. Why Now / Why Chain
왜 지금 이 프로젝트를 수행해야 하는지에 대한 이유는 다음과 같다.

- 구현 먼저 시작하는 습관으로 인해 요구사항과 테스트 기준이 뒤늦게 정해진다.
- 테스트 기준이 모호하면 "거의 맞음"을 "완료"로 오인하기 쉽다.
- Boundary와 Domain 책임이 혼합되면 오류 원인 분석과 회귀 방지가 어려워진다.
- 리팩토링 이후 계약 불변식이 깨져도 조기 감지가 어렵다.
- 따라서 지금 단계에서 계약/불변식/레이어 경계를 명시한 PRD를 고정해야 이후 TDD 사이클의 품질 게이트가 작동한다.

## 5. Target Users
- TDD 학습자
- 코드 리뷰어
- Clean Architecture + ECB를 훈련하는 개발자

사용 환경:
- 콘솔 실행 또는 테스트 실행 중심
- 실제 UI/DB/Web 의존성은 범위 밖

## 6. Vision & Epic Goal
- Epic: **불변식 기반 사고 훈련 시스템 구축**

Vision:
- 학습자가 입력 계약과 도메인 불변식을 먼저 정의하고, 이를 Dual-Track TDD로 검증/구현/리팩토링하는 반복 루프를 수행하도록 돕는 훈련 시스템을 제공한다.

Decision Needed:
- `Report/4.UserJourney_Epic_to_TechnicalScenario_Report.md` 원문이 저장소에 없어, 현재는 `Report/05_Magic-Square-Level1-5-Alignment-Verification-Report.md`를 Epic/Journey의 대체 근거로 사용한다.

## 7. Persona
### Persona A — TDD 학습 개발자
- 알고리즘 정답 구현보다 테스트 주도 개발 습관을 먼저 체득하려는 사용자
- 실패 기준과 성공 기준을 코드보다 테스트로 먼저 고정하려는 학습자

### Persona B — 아키텍처 학습 개발자
- Clean Architecture/ECB 계층 분리 원칙을 실제 과제로 연습하려는 사용자
- Boundary 검증과 Domain 계산 책임을 분리해 유지보수성을 높이려는 학습자

### Persona C — 품질 검증자/리뷰어
- 요구사항-테스트-구현 간 추적성(Traceability)을 확인하려는 리뷰어
- 테스트 약화 없이 회귀 보호를 검증하려는 사용자

## 8. User Journey Summary
| Stage | Pain Point | Learning Outcome |
|---|---|---|
| 문제 인식 | "정답"에만 집중해 요구/계약이 비어 있음 | 문제를 불변식/계약 관점으로 재정의 |
| 계약 정의 | 입력/출력/실패 정책이 모호함 | 검증 가능한 계약 문장과 에러 정책 확정 |
| 도메인 분리 | 검증/계산/UI 책임이 섞임 | Boundary/Control/Domain 역할 분리 |
| Dual-Track TDD 진행 | UI와 Logic을 한 번에 섞어 변경 | Track A/B를 분리해 RED→GREEN 수행 |
| 회귀 보호 | 리팩토링 후 계약 파손 감지 지연 | Traceability + 커버리지 기준으로 회귀 조기 탐지 |

Decision Needed:
- Journey/Story/Scenario 상세 원문은 요청된 Report/4 부재로 인해 요약 근거(`Report/05`) 기반이다.

## 9. Scope

### 9.1 In-Scope
- 빈칸 좌표 탐색
- 누락 숫자 탐색
- 마방진 판정
- 두 조합 시도 후 결과 반환
- Boundary 계층 입력 검증
- 출력 계약 검증
- RED-GREEN-REFACTOR 흐름에 맞춘 테스트 가능성 확보

### 9.2 Out-of-Scope
- UI 화면 개발
- DB 저장/검색
- Web/API 서버 개발
- N×N 일반화
- 완전한 마방진 생성 알고리즘
- 사용자 인증/권한
- 네트워크 오류 처리
- QR 스캔
- 외부 서비스 연동

## 10. Functional Requirements

### FR-01 Input Verification
- Description: Boundary 계층에서 입력 행렬의 구조/값/중복/빈칸 규칙을 검증한다.
- Layer: Boundary
- Input: `int[][] grid`
- Processing Rules:
  - 4x4 여부 확인
  - `0` 개수 정확히 2개 확인
  - 값 범위 `0` 또는 `1~16` 확인
  - `0` 제외 중복 금지 확인
- Output:
  - 성공: Domain 호출 가능 상태
  - 실패: 정의된 에러 스키마 반환
- Acceptance Criteria:
  - AC-FR01-01: 4x4가 아니면 `UI_INVALID_SIZE` 반환
  - AC-FR01-02: 빈칸 개수가 2가 아니면 `UI_INVALID_EMPTY_COUNT` 반환
  - AC-FR01-03: 범위 위반 값이 있으면 `UI_INVALID_VALUE_RANGE` 반환
  - AC-FR01-04: 비영(0 제외) 중복이 있으면 `UI_DUPLICATE_VALUE` 반환
  - AC-FR01-05: AC-FR01-01~04 실패 시 Domain resolver를 호출하지 않음
- Error / Exception Policy: 에러 코드+고정 메시지 반환, 예외 전파 금지
- Related Business Rules: BR-01, BR-02, BR-03, BR-04
- Related Test Direction: UT-E01~UT-E05
- Component Candidate: `BoundaryValidator`

### FR-02 Blank Coordinate Discovery
- Description: row-major 기준 첫 번째/두 번째 빈칸 좌표를 찾는다.
- Layer: Domain
- Input: 유효한 4x4 `grid`
- Processing Rules:
  - 행 우선 스캔
  - 첫 발견 `0`을 first blank, 둘째 `0`을 second blank로 고정
- Output: `(r1, c1), (r2, c2)` (내부 표현, 최종 출력은 1-index)
- Acceptance Criteria:
  - AC-FR02-01: 빈칸은 정확히 2개여야 한다.
  - AC-FR02-02: 첫 번째 빈칸은 row-major 첫 `0`이어야 한다.
- Error / Exception Policy: 구조 전제 위반 시 Domain validation failure
- Related Business Rules: BR-02, BR-05
- Related Test Direction: DT-N03
- Component Candidate: `BlankFinder`

### FR-03 Missing Number Discovery
- Description: `1..16` 중 입력에 없는 두 숫자를 찾고 오름차순으로 정렬한다.
- Layer: Domain
- Input: 유효한 4x4 `grid`
- Processing Rules:
  - 비어 있지 않은 숫자 집합 수집
  - 누락된 숫자 집합 계산
  - 누락 수는 정확히 2개
  - 결과는 오름차순 `[small, large]`
- Output: `(small, large)`
- Acceptance Criteria:
  - AC-FR03-01: 누락 숫자 개수는 정확히 2개다.
  - AC-FR03-02: 반환 순서는 오름차순이다.
- Error / Exception Policy: 누락 개수 불일치 시 Domain validation failure
- Related Business Rules: BR-06, BR-07
- Related Test Direction: DT-N04
- Component Candidate: `MissingNumberFinder`

### FR-04 Magic Square Validation
- Description: 완성된 4x4 격자가 마방진 조건(합 34)을 만족하는지 검증한다.
- Layer: Domain
- Input: 빈칸이 채워진 4x4 `grid`
- Processing Rules:
  - 행 4개 합 검사
  - 열 4개 합 검사
  - 주대각선/부대각선 합 검사
  - 모든 합이 34와 일치해야 true
- Output: `true/false`
- Acceptance Criteria:
  - AC-FR04-01: 행/열/대각선 합이 모두 34면 true
  - AC-FR04-02: 하나라도 다르면 false
- Error / Exception Policy: 크기 불일치 시 Domain validation failure
- Related Business Rules: BR-08, BR-09
- Related Test Direction: DT-N05, DT-X03
- Component Candidate: `MagicSquareValidator`

### FR-05 Two-Combination Solver and Result Formatting
- Description: 두 빈칸과 두 누락 숫자에 대해 small-first, reverse 순으로 시도하고 계약 형식으로 반환한다.
- Layer: Domain (+ Boundary 출력 계약 검증)
- Input: 유효한 4x4 `grid`
- Processing Rules:
  - Attempt 1: `small→first blank`, `large→second blank`
  - Attempt 1 성공 시 즉시 해당 순서로 반환
  - Attempt 1 실패 시 Attempt 2 수행
  - Attempt 2: `large→first blank`, `small→second blank`
  - Attempt 2 성공 시 reverse 순서로 반환
  - 둘 다 실패 시 정의된 실패 정책 반환
- Output:
  - 성공: `int[6] = [r1,c1,n1,r2,c2,n2]` (1-index)
  - 실패: `DOMAIN_NO_SOLUTION` (Boundary 에러 스키마로 매핑)
- Acceptance Criteria:
  - AC-FR05-01: Attempt 1 성공 케이스는 Attempt 2를 실행하지 않는다.
  - AC-FR05-02: Attempt 1 실패 후 Attempt 2 성공 시 reverse 결과를 반환한다.
  - AC-FR05-03: 두 시도 모두 실패 시 `DOMAIN_NO_SOLUTION`을 반환한다.
  - AC-FR05-04: 성공 반환은 길이 6, 좌표 1-index 규칙을 만족한다.
- Error / Exception Policy: 외부 계약은 에러 코드 기반 실패 응답으로 고정
- Related Business Rules: BR-10, BR-11, BR-12
- Related Test Direction: DT-N01, DT-N02, DT-E07, UT-E06
- Component Candidate: `Solver`, `ResultFormatter`

## 11. Business Rules / Domain Rules
- BR-01: 입력은 항상 4x4 정수 행렬이어야 한다.
- BR-02: 입력에서 빈칸(`0`)은 항상 정확히 2개여야 한다.
- BR-03: 각 셀 값은 항상 `0` 또는 `1..16` 범위여야 한다.
- BR-04: `0`을 제외한 숫자는 항상 중복되면 안 된다.
- BR-05: 첫 번째 빈칸은 항상 row-major 스캔에서 첫 `0`이다.
- BR-06: 누락 숫자 집합의 크기는 항상 2여야 한다.
- BR-07: 누락 숫자 반환 순서는 항상 오름차순이어야 한다.
- BR-08: 마방진 상수는 항상 34이다.
- BR-09: 완성 격자의 각 행/열/대각선 합은 항상 34여야 한다.
- BR-10: Solver는 항상 Attempt 1(small-first)을 먼저 수행해야 한다.
- BR-11: Attempt 1 실패 시에만 Attempt 2(reverse)를 수행해야 한다.
- BR-12: 성공 반환 형식은 항상 `int[6]`와 1-index 좌표 규칙을 만족해야 한다.

## 12. Input / Output Contract

### 12.1 Input Contract
| Field / Item | Type | Rule | Valid Example | Invalid Example | Related Error Code 또는 Failure Policy |
|---|---|---|---|---|---|
| `grid` | `int[][]` | 4x4 고정 | `[[16,0,3,13],[5,11,10,8],[9,7,6,12],[4,14,0,1]]` | `[[1,2,3],[4,5,6],[7,8,9]]` | `UI_INVALID_SIZE` |
| `blank_count` | derived | `0` 개수 = 2 | 위 valid 예시의 `0` 2개 | `0` 1개 또는 3개 | `UI_INVALID_EMPTY_COUNT` |
| `cell_value` | `int` | `0` 또는 `1..16` | `0`, `1`, `16` | `-1`, `17` | `UI_INVALID_VALUE_RANGE` |
| `non_zero_uniqueness` | derived | `0` 제외 중복 금지 | `... [5,11,...], [..,7,..]` | `5`가 2회 등장 | `UI_DUPLICATE_VALUE` |

### 12.2 Output Contract (Success)
| Field / Item | Type | Rule | Valid Example | Invalid Example | Related Error Code 또는 Failure Policy |
|---|---|---|---|---|---|
| `result` | `int[6]` | 길이 6 고정 | `[1,2,2,4,3,15]` | `[1,2,2,4,3]` | `UI_INTERNAL_CONTRACT` |
| `r1,c1,r2,c2` | `int` | 좌표 1-index, 각 1~4 | `1,2,4,3` | `0,2,4,3` | `UI_INTERNAL_CONTRACT` |
| `n1,n2` | `int` | 누락 수 두 개, `1..16`, `n1!=n2` | `2,15` | `2,2` | `UI_INTERNAL_CONTRACT` |
| ordering | rule | `[r1,c1,n1,r2,c2,n2]` 순서 고정 | `[1,2,2,4,3,15]` | `[n1,r1,c1,...]` | `UI_INTERNAL_CONTRACT` |

## 13. Error / Failure Policy
| Case | Error Code | Message | Layer | Domain resolver 호출 여부 | Related Acceptance Criteria |
|---|---|---|---|---|---|
| 4x4가 아닌 입력 | `UI_INVALID_SIZE` | `Grid must be 4x4.` | Boundary | No | AC-FR01-01, AC-FR01-05 |
| 빈칸 개수 오류 | `UI_INVALID_EMPTY_COUNT` | `Grid must contain exactly 2 empty cells (0).` | Boundary | No | AC-FR01-02, AC-FR01-05 |
| 값 범위 위반 | `UI_INVALID_VALUE_RANGE` | `Cell values must be 0 or between 1 and 16.` | Boundary | No | AC-FR01-03, AC-FR01-05 |
| 0 제외 중복 숫자 | `UI_DUPLICATE_VALUE` | `Non-zero values must not duplicate.` | Boundary | No | AC-FR01-04, AC-FR01-05 |
| 두 조합 모두 실패 | `DOMAIN_NO_SOLUTION` | `No valid magic square completion for the two empty cells.` | Domain → Boundary mapping | Yes | AC-FR05-03 |

정책 고정:
- 입력 검증 실패 시 Domain resolver는 호출되지 않는다.
- 외부 계약(호출자 기준)은 예외 스택 노출 없이 에러 코드/메시지 기반 실패 응답을 사용한다.

Decision Needed:
- Domain 내부 실패 전달 방식을 예외(`throw`)로 통일할지, Result 객체로 통일할지 구현 정책 확정이 필요하다.

## 14. Non-Functional Requirements
- NFR-01 Coverage:
  - Domain Logic branch coverage는 95% 이상이어야 한다.
  - Boundary Validation branch coverage는 85% 이상이어야 한다.
- NFR-02 Deterministic Execution:
  - 동일 입력은 항상 동일 출력(또는 동일 에러 코드)을 반환해야 한다.
- NFR-03 No Side Effects:
  - 입력 행렬은 함수 실행 후 변경되지 않아야 한다(불변 입력 정책).
- NFR-04 Performance:
  - 4x4 기준 단일 실행은 50ms 이내여야 한다(일반 개발 환경 기준).
- NFR-05 Maintainability:
  - Boundary/Domain 책임을 분리해야 한다.
  - 설명 없는 매직 넘버를 금지한다.
  - 하드코딩 문자열을 금지하고 명명된 상수/에러 맵을 사용해야 한다.

## 15. Dual-Track TDD Strategy

### 15.1 Track A — Boundary / UI Contract TDD
- 입력 검증 테스트
- 출력 형식 테스트
- 실패 응답 테스트
- Domain resolver 미호출 테스트

### 15.2 Track B — Domain / Logic TDD
- 빈칸 탐색 테스트
- 누락 숫자 탐색 테스트
- 마방진 검증 테스트
- small-first 성공 테스트
- small-first 실패 후 reverse 성공 테스트
- 두 조합 모두 실패 테스트

### 15.3 Parallel Progression Rules
- UI RED와 Logic RED를 분리한다.
- UI GREEN과 Logic GREEN을 각각 최소 구현으로 처리한다.
- REFACTOR 단계에서만 구조 개선을 수행한다.
- 모든 Domain을 먼저 구현하고 나중에 Boundary를 붙이는 방식을 금지한다.
- 테스트를 약화하거나 삭제해서 통과시키는 것을 금지한다.

## 16. Test Plan / QA

### 16.1 Normal Scenarios
- TS-N01: small-first 성공
- TS-N02: small-first 실패 후 reverse 성공

### 16.2 Exception Scenarios
- TS-E01: 4x4가 아닌 입력
- TS-E02: 빈칸 개수 오류
- TS-E03: 값 범위 오류
- TS-E04: 중복 숫자 오류
- TS-E05: 두 조합 모두 실패

### 16.3 Boundary Scenarios
- TS-B01: 최소값 1 처리
- TS-B02: 최대값 16 처리
- TS-B03: `0`은 빈칸으로만 처리
- TS-B04: 출력 좌표 1-index 검증
- TS-B05: 반환 배열 길이 6 검증

### 16.4 Representative Test Data
- RD-01 small-first 성공 행렬:
  - `[[16,0,3,13],[5,11,10,8],[9,7,6,12],[4,14,0,1]]`
- RD-02 reverse 성공 행렬:
  - `[[16,0,3,13],[5,11,10,8],[9,7,6,12],[4,14,15,0]]`
- RD-03 invalid size 행렬:
  - `[[1,2,3],[4,5,6],[7,8,9]]`
- RD-04 invalid blank count 행렬:
  - `[[16,2,3,13],[5,11,10,8],[9,7,6,12],[4,14,0,1]]` (빈칸 1개)
- RD-05 duplicate value 행렬:
  - `[[16,0,3,13],[5,11,10,8],[9,7,6,12],[4,14,16,0]]`
- RD-06 invalid range 행렬:
  - `[[16,0,3,13],[5,11,10,8],[9,7,6,12],[4,14,17,0]]`

## 17. Architecture Overview, High-Level
- Boundary Layer:
  - 입력 검증
  - 오류 응답 생성
  - 출력 포맷 계약 검증
- Domain Layer:
  - 순수 마방진 로직
  - 불변식 검증
  - 조합 시도 및 판정
- Control / Application Layer:
  - Boundary와 Domain 흐름 조정
  - 필요 시에만 포함(본 프로젝트 MVP에서는 선택)

의존 방향:
- Boundary → Control → Domain
- Domain은 Boundary를 몰라야 한다.
- Domain은 UI, DB, Web, 파일 시스템에 의존하지 않아야 한다.

## 18. Component Candidates
| Component | Responsibility | Layer | Input | Output | Related FR | Related Test |
|---|---|---|---|---|---|---|
| `BoundaryValidator` | 입력 계약 검증 및 에러 코드 매핑 | Boundary | `int[][]` | 검증 성공/실패 | FR-01 | UT-E01~UT-E05 |
| `BlankFinder` | row-major 빈칸 2개 탐색 | Domain | 유효 grid | 두 빈칸 좌표 | FR-02 | DT-N03 |
| `MissingNumberFinder` | 누락 숫자 2개 도출 및 정렬 | Domain | 유효 grid | `(small, large)` | FR-03 | DT-N04 |
| `MagicSquareValidator` | 행/열/대각선 합 34 검증 | Domain | 완성 grid | `bool` | FR-04 | DT-N05, DT-X03 |
| `Solver` | Attempt1/Attempt2 실행, 실패 정책 적용 | Domain | 유효 grid | 성공 `int[6]` 또는 실패 코드 | FR-05 | DT-N01, DT-N02, DT-E07 |
| `ResultFormatter` | 1-index + `int[6]` 형식 보장 | Boundary/Control | 도메인 결과 | 계약 출력 | FR-05 | UT-F01, UT-F02 |

## 19. Risks & Ambiguities
| Risk | Impact | Decision / Mitigation |
|---|---|---|
| 1-index와 0-index 혼동 | 좌표 오류로 오답 반환 | 출력 계약에 1-index 고정, TS-B04 필수 |
| row-major 첫 번째 빈칸 정의 누락 | Solver 순서 비결정성 발생 | BR-05/FR-02로 명시, DT-N03로 검증 |
| small-first vs reverse 데이터 혼동 | 잘못된 분기 테스트로 회귀 발생 | RD-01/RD-02를 분리 고정 |
| 입력 행렬 변경 여부 불명확 | 부작용으로 상위 호출자 상태 오염 | NFR-03으로 "입력 불변" 정책 고정 |
| 두 조합 실패 정책 누락 | 호출자 실패 처리 불가 | Section 13에 `DOMAIN_NO_SOLUTION` 고정 |
| 34 상수 하드코딩 | 규칙 변경/해석 불일치 위험 | 명명 상수 사용 및 BR-08에 계약 고정 |
| Boundary와 Domain 책임 혼합 | 테스트 분리 불가, 유지보수성 저하 | ECB 의존 방향 고정, Track 분리 강제 |

## 20. Engineering Principles
Report/3 및 Cursor Rules(.cursorrules, .cursor/rules/*.mdc) 요약:

- EP-01: Python은 PEP8(Black 88) 준수
- EP-02: 모든 공개 함수/메서드는 type hints 필수
- EP-03: 테스트 프레임워크는 pytest 사용
- EP-04: 테스트는 AAA 패턴을 따른다
- EP-05: Coverage 목표 준수 (Domain 95%+, Boundary 85%+, Global 80%+)
- EP-06: ECB 레이어 분리 (`boundary → control → entity`)
- EP-07: RED-GREEN-REFACTOR 순서를 위반하지 않는다
- EP-08: `print()` 디버깅을 금지한다
- EP-09: bare `except`를 금지한다
- EP-10: 테스트 약화/삭제/skip/xfail로 통과시키는 행위를 금지한다
- EP-11: 설명 없는 매직 넘버 사용을 금지한다

## 21. Traceability Matrix
| Concept / Invariant | Business Rule | Feature ID | Acceptance Criteria | Test Case Candidate | Component |
|---|---|---|---|---|---|
| 4x4 입력 | BR-01 | FR-01 | AC-FR01-01 | UT-E01, TS-E01 | BoundaryValidator |
| 빈칸 2개 | BR-02 | FR-01, FR-02 | AC-FR01-02, AC-FR02-01 | UT-E02, UT-E03, TS-E02 | BoundaryValidator, BlankFinder |
| 값 범위 0 또는 1~16 | BR-03 | FR-01 | AC-FR01-03 | UT-E04, TS-E03 | BoundaryValidator |
| 중복 금지 | BR-04 | FR-01 | AC-FR01-04 | UT-E05, TS-E04 | BoundaryValidator |
| row-major 첫 번째 빈칸 | BR-05 | FR-02 | AC-FR02-02 | DT-N03 | BlankFinder |
| 누락 숫자 2개 | BR-06 | FR-03 | AC-FR03-01 | DT-N04 | MissingNumberFinder |
| 누락 숫자 오름차순 | BR-07 | FR-03 | AC-FR03-02 | DT-N04, TS-B01/TS-B02 | MissingNumberFinder |
| 마방진 상수 34 | BR-08 | FR-04 | AC-FR04-01 | DT-N05 | MagicSquareValidator |
| 행/열/대각선 합 | BR-09 | FR-04 | AC-FR04-01, AC-FR04-02 | DT-N05, DT-X03 | MagicSquareValidator |
| small-first 시도 | BR-10 | FR-05 | AC-FR05-01 | DT-N01, TS-N01 | Solver |
| reverse 시도 | BR-11 | FR-05 | AC-FR05-02 | DT-N02, TS-N02 | Solver |
| int[6] 반환 | BR-12 | FR-05 | AC-FR05-04 | UT-F01, TS-B05 | ResultFormatter |
| 1-index 좌표 | BR-12 | FR-05 | AC-FR05-04 | UT-F02, TS-B04 | ResultFormatter |

## 22. Open Questions / Decision Needed
- DN-01: `Report/4.UserJourney_Epic_to_TechnicalScenario_Report.md` 원문 부재. `Report/05` 대체 사용을 유지할지, 원문 복구 후 재동기화할지 결정 필요.
- DN-02: Domain 내부 실패 표현을 예외 기반으로 통일할지, Result 기반으로 통일할지 결정 필요(외부 계약은 에러 코드 응답으로 고정).
- DN-03: Control/Application 레이어를 MVP부터 명시적으로 둘지, Boundary→Domain 직결로 시작할지 결정 필요.

## 23. Appendix

### 23.1 참고 문서 목록
- `Report/01_Magic-Square-Problem-Definition-Report.md`
- `Report/02_Magic-Square-Dual-Track-TDD-Design.md`
- `Report/03_Magic-Square-Cursorrules-and-Phase03-Kickoff-Report.md`
- `Report/04_Magic-Square-Cursor-Rules-Migration-Report.md`
- `Report/05_Magic-Square-Level1-5-Alignment-Verification-Report.md` (Report/4 대체 근거)
- `.cursorrules`
- `.cursor/rules/magicsquare-project.mdc`
- `.cursor/rules/magicsquare-tdd-testing.mdc`
- `.cursor/rules/magicsquare-forbidden.mdc`
- `.cursor/rules/magicsquare-ecb-architecture.mdc`
- `.cursor/rules/magicsquare-python-code-style.mdc`

### 23.2 Cursor Rules 요약
- SSOT: 규칙 상세는 `.cursor/rules/*.mdc`
- 계약 충돌 시: Report/02 우선
- TDD 사이클: `spec → red → green → refactoring → develop`
- 금지: print 디버깅, bare except, 테스트 약화, ECB 역전, RED 없는 src 변경

### 23.3 대표 Gherkin Scenario 요약
- GS-01 (Normal): Given 유효 4x4와 빈칸 2개, When small-first가 magic 만족, Then `int[6]`를 small-first 순서로 반환
- GS-02 (Fallback): Given 유효 4x4, When small-first 실패 후 reverse 성공, Then reverse 순서 `int[6]` 반환
- GS-03 (Boundary Fail): Given invalid size/blank/range/duplicate, When validate 실행, Then 에러 코드 반환 및 Domain 미호출
- GS-04 (No Solution): Given 두 시도 모두 실패 퍼즐, When solve 실행, Then `DOMAIN_NO_SOLUTION` 반환

### 23.4 향후 RED Test ID 후보
- `RED-BND-VAL-001`: invalid size
- `RED-BND-VAL-002`: invalid blank count
- `RED-BND-VAL-003`: invalid value range
- `RED-BND-VAL-004`: duplicate non-zero
- `RED-DOM-BLK-001`: row-major blank order
- `RED-DOM-MISS-001`: missing two numbers
- `RED-DOM-MISS-002`: ascending order
- `RED-DOM-VAL-001`: magic validation true
- `RED-DOM-VAL-002`: magic validation false
- `RED-DOM-SOL-001`: small-first success
- `RED-DOM-SOL-002`: reverse success
- `RED-DOM-SOL-003`: no solution
