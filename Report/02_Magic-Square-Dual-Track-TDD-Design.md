# Magic Square 4×4 — Dual-Track UI + Logic TDD · Clean Architecture 설계

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_ (TDD 연습용) |
| 문서 버전 | 1.0 |
| 상위 문서 | [01_Magic-Square-Problem-Definition-Report.md](./01_Magic-Square-Problem-Definition-Report.md) |
| 목적 | 알고리즘 난이도보다 **레이어 분리 + 계약 기반 테스트 + 리팩토링** 훈련 |
| 범위 | 설계 · 계약 · 테스트 · 통합 계획 **만** (구현 코드 없음) |

---

# 1) Logic Layer (Domain Layer) 설계

## 1.1 도메인 개념

| 구분 | 이름 | 책임 (SRP) |
|------|------|------------|
| **Entity** | `MagicGrid` | 4×4 정수 격자 보유. 크기·빈칸 개수·값 범위·중복에 대한 **구조 검증**만 담당. 판정/해찾기는 위임. |
| **Value Object** | `CellValue` | 단일 칸 값 규칙: `0`(빈칸) 또는 `1~16`. 범위 위반 시 생성/검증 실패. |
| **Value Object** | `Position` | 1-index `(row, col)`. 경계 `1≤row,col≤4`. 빈칸 좌표·출력 좌표에 사용. |
| **Value Object** | `MagicConstant` | 4×4·1~16 완성 시 목표 합 **34** 단일 값 보장. |
| **Value Object** | `SolutionVector` | 도메인 내부 결과: 두 빈칸 좌표 + 두 누락 수 `(r1,c1,n1,r2,c2,n2)`. **출력 순서 규칙** 적용 후 UI에 전달. |
| **Domain Service** | `EmptyCellLocator` | `MagicGrid`에서 `0`인 칸을 **행 우선(row-major)** 스캔으로 정확히 2개 찾아 `Position` 쌍 반환. |
| **Domain Service** | `MissingValueFinder` | `1~16` 중 격자에 없는 정수 **정확히 2개**를 오름차순 `[small, large]`로 반환. |
| **Domain Service** | `MagicSquareJudge` | **완성 격자**(빈칸 없음)에 대해 행 4·열 4·주대각선·부대각선 합이 `MagicConstant`와 일치하는지 판정. |
| **Domain Service** | `PuzzleSolver` | 두 빈칸·두 누락 수에 대해 **배치 조합 2가지** 시도 후 `SolutionVector` 또는 **해 없음** 반환. |

**레이어 원칙**

- Domain은 UI·파일·DB에 **의존하지 않음**.
- 좌표는 Domain 내부에서 1-index `Position`으로 통일. UI는 변환만 담당하지 않음(동일 계약).

---

## 1.2 도메인 불변조건 (Invariants)

| ID | Invariant | 검증 가능 조건 |
|----|-----------|----------------|
| **D-STRUCT-01** | 격자 크기 | `int[4][4]` (또는 동등한 16칸) |
| **D-STRUCT-02** | 빈칸 개수 | `0`의 개수 **= 2** |
| **D-STRUCT-03** | 값 범위 | 모든 칸 ∈ `{0} ∪ {1,…,16}` |
| **D-STRUCT-04** | 비빈칸 유일성 | `0`이 아닌 값은 서로 다름 |
| **D-ORDER-01** | 빈칸 순서 | 첫 빈칸 = row-major 첫 `0`, 둘째 빈칸 = row-major 둘째 `0` |
| **D-MAGIC-01** | 매직 합 | 완성 격자의 각 행·열·주대각선·부대각선 합 = **34** |
| **D-SOLVE-01** | 누락 수 집합 | `{n1, n2} = {1..16} \ 격자의 비零 값}` 이고 &#124;집합&#124;=2 |
| **D-SOLVE-02** | 배치 시도 1 | `small`→첫 빈칸, `large`→둘째 빈칸 채운 격자가 `D-MAGIC-01` 만족 시 → 출력 `[r1,c1,small,r2,c2,large]` |
| **D-SOLVE-03** | 배치 시도 2 | 시도 1 실패 시 `large`→첫 빈칸, `small`→둘째 빈칸; 만족 시 → 출력 `[r1,c1,large,r2,c2,small]` |
| **D-SOLVE-04** | 해 없음 | 시도 1·2 모두 실패 시 도메인 실패(예외 또는 `Result.Failure`) — **임의 순서 출력 금지** |
| **D-OUT-01** | 출력 좌표 | `r1,c1,r2,c2 ∈ [1,4]`, `n1,n2 ∈ [1,16]`, `n1≠n2` |

**Magic Constant 근거**

- 1~16 합 = 136 → 4행 평균 = **34** (고정 상수).

---

## 1.3 핵심 유스케이스 (도메인 관점)

| UC-ID | 이름 | 전제 | 결과 |
|-------|------|------|------|
| **UC-D01** | 격자 구조 검증 | `int[4][4]` 수신 | D-STRUCT-01~04 만족 시 `MagicGrid` 생성; 아니면 실패 |
| **UC-D02** | 빈칸 찾기 | 유효 `MagicGrid` | D-ORDER-01에 따른 `Position` 2개 |
| **UC-D03** | 누락 숫자 찾기 | 유효 `MagicGrid` | `small < large` 두 정수 |
| **UC-D04** | 마방진 판정 | 빈칸 없는 4×4 | `true` / `false` (D-MAGIC-01) |
| **UC-D05** | 퍼즐 해결 | 유효 `MagicGrid` (빈칸 2) | `SolutionVector` 6원 또는 D-SOLVE-04 실패 |
| **UC-D06** | 배치 시도 | 빈칸 2, `{small,large}` | 임시 완성 격자 → UC-D04 호출 |

**UC-D05 흐름 (순서 고정)**

1. UC-D01  
2. UC-D02 → `(r1,c1)`, `(r2,c2)`  
3. UC-D03 → `small`, `large`  
4. 시도 A: `(r1,c1)←small`, `(r2,c2)←large` → UC-D04 → 성공 시 D-SOLVE-02  
5. 시도 B: `(r1,c1)←large`, `(r2,c2)←small` → UC-D04 → 성공 시 D-SOLVE-03  
6. 둘 다 실패 → D-SOLVE-04  

---

## 1.4 Domain API (내부 계약)

> 표기: 시그니처 수준 설명만. **구현 코드 없음.**

| API | 입력 | 출력 | 실패 조건 |
|-----|------|------|-----------|
| `MagicGrid.fromRaw(int[][] raw)` | `raw` 4×4 | `MagicGrid` | 행·열≠4; 빈칸≠2; 값 범위 위반; 비零 중복 |
| `EmptyCellLocator.locate(MagicGrid g)` | 유효 `g` | `(Position first, Position second)` | 빈칸≠2 (fromRaw 이후 불가) |
| `MissingValueFinder.find(MagicGrid g)` | 유효 `g` | `(int small, int large)` | 누락 수≠2 (이론상 14개 채워진 경우만) |
| `MagicSquareJudge.isCompleteMagic(int[][] filled)` | 빈칸 없는 4×4 | `boolean` | 크기≠4×4 |
| `PuzzleSolver.solve(MagicGrid g)` | 유효 `g` | `int[6]` = `[r1,c1,n1,r2,c2,n2]` 1-index | D-SOLVE-04; fromRaw 실패 |
| `PuzzleSolver.solveRaw(int[][] raw)` | `raw` | 동일 | fromRaw 또는 solve 실패 |

**`int[6]` 의미 (고정)**

| 인덱스 | 필드 | 규칙 |
|--------|------|------|
| 0,1 | `r1,c1` | 첫 빈칸 (row-major) 1-index |
| 2 | `n1` | 첫 빈칸에 넣은 수 |
| 3,4 | `r2,c2` | 둘째 빈칸 1-index |
| 5 | `n2` | 둘째 빈칸에 넣은 수 |

**실패 타입 (Domain)**

| 코드 | 의미 |
|------|------|
| `DOMAIN_INVALID_GRID` | D-STRUCT-01~04 위반 |
| `DOMAIN_NO_SOLUTION` | D-SOLVE-04 |

---

## 1.5 Domain 단위 테스트 설계 (RED 우선)

### 1.5.1 정상 케이스

| Test-ID | 설명 | 입력 요약 | 기대 | 보호 Invariant |
|---------|------|-----------|------|----------------|
| **DT-N01** | 표준 해 존재 — 시도 A 성공 | 유효 4×4, 2빈칸, A만 magic | `int[6]` 시도 A 순서 | D-SOLVE-02, D-OUT-01 |
| **DT-N02** | 시도 A 실패 · B 성공 | B만 magic인 퍼즐 | `n1> n2` 가능(첫 칸에 large) | D-SOLVE-03 |
| **DT-N03** | 빈칸 순서 | 빈칸 (2,3),(4,1) | `r1,c1`이 row-major 첫 0 | D-ORDER-01 |
| **DT-N04** | 누락 수 | 14개 채워진 격자 | `{n1,n2}` = 1..16 미사용 2개 | D-SOLVE-01 |
| **DT-N05** | 완성 판정 | 알려진 완성 4×4 | `isCompleteMagic=true` | D-MAGIC-01 |

### 1.5.2 비정상 케이스

| Test-ID | 설명 | 기대 | 보호 Invariant |
|---------|------|------|----------------|
| **DT-E01** | 3×3 | `DOMAIN_INVALID_GRID` | D-STRUCT-01 |
| **DT-E02** | 빈칸 1개 | `DOMAIN_INVALID_GRID` | D-STRUCT-02 |
| **DT-E03** | 빈칸 3개 | `DOMAIN_INVALID_GRID` | D-STRUCT-02 |
| **DT-E04** | 값 17 | `DOMAIN_INVALID_GRID` | D-STRUCT-03 |
| **DT-E05** | 값 -1 | `DOMAIN_INVALID_GRID` | D-STRUCT-03 |
| **DT-E06** | 비零 중복 (7,7) | `DOMAIN_INVALID_GRID` | D-STRUCT-04 |
| **DT-E07** | 해 없음 퍼즐 | `DOMAIN_NO_SOLUTION` | D-SOLVE-04 |

### 1.5.3 엣지 케이스

| Test-ID | 설명 | 기대 | 보호 Invariant |
|---------|------|------|----------------|
| **DT-X01** | 빈칸 (1,1),(4,4) 대각 | 좌표 1-index 정확 | D-OUT-01 |
| **DT-X02** | small=3, large=14 | 시도 순서 고정 | D-SOLVE-02→03 순서 |
| **DT-X03** | 이미 행합만 34·대각 실패 채움 | `DOMAIN_NO_SOLUTION` | D-MAGIC-01 |

### 1.5.4 RED 작성 순서 (권장)

1. DT-E01~E06 (구조)  
2. DT-N05 (판정)  
3. DT-N03, DT-N04  
4. DT-N01, DT-N02  
5. DT-E07, DT-X03  

---

# 2) Screen Layer (UI Layer) 설계 (Boundary Layer)

> UI = **입력/출력 경계**. 실제 화면·위젯 없음.

## 2.1 사용자/호출자 관점 시나리오

| Step | 행위 | 책임 레이어 |
|------|------|-------------|
| 1 | 호출자가 `int[4][4]` 제공 | UI Boundary |
| 2 | 크기·빈칸·범위·중복 **경계 검증** | UI (Domain 호출 전) |
| 3 | 검증 통과 시 Domain `solveRaw` 호출 | UI → Domain |
| 4 | 성공 시 `int[6]` 반환 | UI |
| 5 | 실패 시 **고정 Error schema** 반환 | UI |

**흐름 다이어그램**

```
[Caller] --int[4][4]--> [UI Boundary: validate] --ok--> [Domain: solve]
                              | fail                          |
                              v                               v
                         [Error schema]                  [int[6] | Domain Error]
```

---

## 2.2 UI 계약 (외부 계약)

### Input schema

| 필드 | 타입 | 규칙 |
|------|------|------|
| `grid` | `int[4][4]` | 필수 |
| `grid[r][c]` | `int` | `0` 또는 `1~16` |
| 빈칸 | — | `0` 정확히 **2개** |
| 중복 | — | `0` 제외 값 중복 **금지** |

### Output schema (성공)

| 필드 | 타입 | 규칙 |
|------|------|------|
| `result` | `int[6]` | `[r1,c1,n1,r2,c2,n2]` |
| 좌표 | `int` | 각 `1~4` |
| 숫자 | `int` | `n1,n2 ∈ 1~16`, `n1≠n2` |

### Error schema

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `code` | `string` | Y | 아래 코드표 중 하나 |
| `message` | `string` | Y | **고정 문구** (2.4) |
| `field` | `string` | N | `grid`, `grid[row][col]` 등 |

| code | 조건 |
|------|------|
| `UI_INVALID_SIZE` | 행 또는 열 ≠ 4 |
| `UI_INVALID_EMPTY_COUNT` | 빈칸 개수 ≠ 2 |
| `UI_INVALID_VALUE_RANGE` | `0`·`1~16` 밖 |
| `UI_DUPLICATE_VALUE` | 비零 중복 |
| `DOMAIN_INVALID_GRID` | Domain 구조 실패 (UI 검증 통과 후 이중 방어) |
| `DOMAIN_NO_SOLUTION` | 해 없음 |

---

## 2.3 UI 레벨 테스트 (Contract-first, RED 우선)

**전제**: Domain은 **Mock** — `solveRaw`가 고정 `int[6]` 또는 Domain 오류를 반환한다고 가정.

| Test-ID | 시나리오 | Mock 설정 | 기대 |
|---------|----------|-----------|------|
| **UT-N01** | 유효 입력 | 성공 `int[6]` | 동일 배열 반환 |
| **UT-E01** | 4×5 | 호출 안 함 | `UI_INVALID_SIZE` |
| **UT-E02** | 빈칸 1 | 호출 안 함 | `UI_INVALID_EMPTY_COUNT` |
| **UT-E03** | 빈칸 3 | 호출 안 함 | `UI_INVALID_EMPTY_COUNT` |
| **UT-E04** | 값 0x99 | 호출 안 함 | `UI_INVALID_VALUE_RANGE` |
| **UT-E05** | (1,1)=5,(2,2)=5 | 호출 안 함 | `UI_DUPLICATE_VALUE` |
| **UT-E06** | Domain NO_SOLUTION | throw/Failure | `DOMAIN_NO_SOLUTION` + 고정 message |
| **UT-F01** | 반환 길이 | Mock `int[5]` | `UI_INTERNAL_CONTRACT` (내부 계약 위반 탐지) |
| **UT-F02** | 좌표 0-index 실수 탐지 | Mock `r1=0` | 경계 거부 또는 내부 오류 |

---

## 2.4 UX/출력 규칙

### 성공

- 반환: `int[6]` **만**. 추가 메타데이터 없음 (학습용 최소 계약).

### 에러 메시지 (문구 고정)

| code | message (정확히 일치) |
|------|------------------------|
| `UI_INVALID_SIZE` | `Grid must be 4x4.` |
| `UI_INVALID_EMPTY_COUNT` | `Grid must contain exactly 2 empty cells (0).` |
| `UI_INVALID_VALUE_RANGE` | `Cell values must be 0 or between 1 and 16.` |
| `UI_DUPLICATE_VALUE` | `Non-zero values must not duplicate.` |
| `DOMAIN_INVALID_GRID` | `Grid failed domain validation.` |
| `DOMAIN_NO_SOLUTION` | `No valid magic square completion for the two empty cells.` |
| `UI_INTERNAL_CONTRACT` | `Internal response contract violation.` |

**규칙**

- `message`는 위 표와 **완전 일치** (대소문자·구두점 포함).  
- 다국어·동적 포맷 **금지** (테스트 안정성).  
- `field`는 선택; 있을 경우 형식: `grid[2][3]` (0-index 표기는 **field에만**, 값 좌표는 출력 `int[6]`에서 1-index).

---

# 3) Data Layer 설계

## 3.1 목적 정의

| 항목 | 내용 |
|------|------|
| **필요성** | 동일 퍼즐 재실행·회귀 테스트 픽스처 재사용·세션 간 입력 복원 (학습용) |
| **범위** | 입력 `int[4][4]` 저장·로드; (선택) 마지막 `int[6]` 결과 저장 |
| **비범위** | RDB·ORM·동시성·클라우드 |

---

## 3.2 인터페이스 계약

| 메서드 | 입력 | 출력 | 실패 |
|--------|------|------|------|
| `MatrixRepository.save(String id, int[][] grid)` | `id` 비공백, 유효 4×4 | `void` | `DATA_INVALID_ID`, `DATA_INVALID_GRID` |
| `MatrixRepository.load(String id)` | `id` | `int[4][4]` | `DATA_NOT_FOUND`, `DATA_CORRUPT` |
| `ResultRepository.save(String id, int[6] result)` | (선택) | `void` | `DATA_INVALID_RESULT` |
| `ResultRepository.load(String id)` | (선택) | `int[6]` | `DATA_NOT_FOUND` |

**저장 불변**

- 로드된 `grid`는 D-STRUCT-01~04를 만족하거나 `DATA_CORRUPT`.  
- 로드된 `result`는 길이 6, 각 좌표 1~4.

---

## 3.3 구현 옵션 비교

| 항목 | 옵션 A: InMemory | 옵션 B: File (JSON) |
|------|------------------|---------------------|
| 저장소 | `Map<String, Snapshot>` | `{id}.json` |
| 영속성 | 프로세스 종료 시 소실 | 디스크 유지 |
| 테스트 속도 |最快 | I/O 포함, 느림 |
| 형식 오류 | 해당 없음 | `DATA_CORRUPT` 필요 |
| 학습 포인트 | Repository 추상화 | 직렬화·경로·예외 |

**추천: 옵션 A (InMemory)** — 이유: TDD·레이어 분리·Domain/UI 트랙에 집중; Data는 **인터페이스 교체 연습**이 목적이며 영속성은 2단계에서 File 어댑터 추가로 확장 가능.

---

## 3.4 Data 레이어 테스트

| Test-ID | 시나리오 | 기대 |
|---------|----------|------|
| **DATA-T01** | save → load | 동일 4×4 (요소별相等) |
| **DATA-T02** | 없는 id load | `DATA_NOT_FOUND` |
| **DATA-T03** | corrupt JSON (File만) | `DATA_CORRUPT` |
| **DATA-T04** | save 후 4×4 아님 데이터 주입 방지 | 저장 시 검증 실패 |
| **DATA-T05** | (선택) result save/load | `int[6]` 동일 |

---

# 4) Integration & Verification

## 4.1 통합 경로 정의

**의존성 방향 (Clean Architecture)**

```
[Caller]
   ↓
[UI Boundary]  →  [Application Facade (선택)]  →  [Domain]
   ↓                                                      ↑
[Data Repository Interface] ─────────────────────────────┘
   ↑
[InMemory / File Adapter]
```

| 레이어 | 허용 의존 |
|--------|-----------|
| Domain | 없음 (순수) |
| Application (선택) | Domain, Repository **인터페이스** |
| UI | Domain 또는 Application; **Repository 직접 호출 금지** (학습 기본) |
| Data | Domain 타입만 사용; UI **금지** |

**기본 통합 경로 (Facade 없음)**

`Caller → UI.validate → Domain.solveRaw → UI return int[6]`

**확장 경로 (Facade 있음)**

`Caller → UI → App.solveAndPersist(id, grid) → Domain + MatrixRepository`

---

## 4.2 통합 테스트 시나리오

### 정상 (≥2)

| IT-ID | 경로 | 검증 |
|-------|------|------|
| **IT-N01** | UI→Domain, 알려진 퍼즐 | `int[6]` + 수동으로 채운 4×4가 D-MAGIC-01 |
| **IT-N02** | UI→Domain→InMemory save/load → 재실행 | 동일 `int[6]` |

### 실패 (≥3)

| IT-ID | 경로 | 검증 |
|-------|------|------|
| **IT-E01** | 3×4 입력 | `UI_INVALID_SIZE`, Domain 미호출 |
| **IT-E02** | 해 없음 퍼즐 | `DOMAIN_NO_SOLUTION` |
| **IT-E03** | corrupt file load (File adapter) | `DATA_CORRUPT`, Domain 미호출 |
| **IT-E04** | 빈칸 0개 + Domain | `UI_INVALID_EMPTY_COUNT` |

---

## 4.3 회귀 보호 규칙

| 규칙 ID | 내용 |
|---------|------|
| **RG-01** | `int[6]` 길이·순서·1-index **변경 금지** |
| **RG-02** | Error `code`·`message` 표 **변경 시** UI 테스트 전부 업데이트 후 merge |
| **RG-03** | RED 테스트 **삭제 금지**; Green 후에만 Refactor |
| **RG-04** | Domain Invariant ID (D-*) 는 테스트 ID (DT-*)에 매핑 유지 |
| **RG-05** | develop merge 조건: Domain + UI Boundary 테스트 **전부 Green** |

---

## 4.4 커버리지 목표

| 레이어 | 목표 | 측정 범위 |
|--------|------|-----------|
| Domain Logic | **≥ 95%** branch | `MagicGrid`, Locator, Finder, Judge, Solver |
| UI Boundary | **≥ 85%** branch | validate*, error mapping, response shape |
| Data | **≥ 80%** branch | Repository 구현체, save/load 예외 |

**미달 시**: merge 금지 (CI 정책으로 명시).

---

## 4.5 Traceability Matrix (필수)

| Concept (Invariant) | Rule | Use Case | Contract | Test | Component |
|---------------------|------|----------|----------|------|-----------|
| D-STRUCT-01 | 4×4만 허용 | UC-D01 | `fromRaw` | DT-E01, UT-E01 | `MagicGrid` |
| D-STRUCT-02 | 빈칸=2 | UC-D01 | Input schema | DT-E02~03, UT-E02~03 | UI + `MagicGrid` |
| D-STRUCT-03 | 0 또는 1~16 | UC-D01 | Input schema | DT-E04~05, UT-E04 | UI + `CellValue` |
| D-STRUCT-04 | 비零 중복 금지 | UC-D01 | Input schema | DT-E06, UT-E05 | UI + `MagicGrid` |
| D-ORDER-01 | row-major 빈칸 | UC-D02 | `int[6]` r,c | DT-N03, DT-X01 | `EmptyCellLocator` |
| D-MAGIC-01 | 합=34 | UC-D04 | `isCompleteMagic` | DT-N05, IT-N01 | `MagicSquareJudge` |
| D-SOLVE-01 | 누락 2수 | UC-D03 | solve output n | DT-N04 | `MissingValueFinder` |
| D-SOLVE-02 | small→첫, large→둘째 | UC-D05 | `int[6]` | DT-N01 | `PuzzleSolver` |
| D-SOLVE-03 | 반대 배치 | UC-D05 | `int[6]` | DT-N02 | `PuzzleSolver` |
| D-SOLVE-04 | 해 없음 | UC-D05 | `DOMAIN_NO_SOLUTION` | DT-E07, UT-E06, IT-E02 | `PuzzleSolver` |
| D-OUT-01 | 1-index 좌표 | UC-D05 | Output schema | UT-F02, IT-N01 | UI + Domain |
| 저장 4×4 | load 동일 | — | `MatrixRepository` | DATA-T01, IT-N02 | Data adapter |
| Error 문구 고정 | RG-02 | — | Error schema | UT-E01~06 | UI Boundary |

---

## 설계 체크리스트

- [x] Logic / UI Boundary / Data 레이어 분리
- [x] 입력 `int[4][4]` · 출력 `int[6]` 계약 고정
- [x] 빈칸 2개 · row-major · small/large 시도 순서 명시
- [x] RED 우선 테스트 목록 (Domain / UI / Data)
- [x] Traceability Matrix 포함
- [x] 구현 코드 없음

---

## 3줄 요약

1. **범위**: 4×4·빈칸 2개·누락 수 2개를 채워 마방진(합 34)을 만드는 **Domain 해결** + **UI 경계 검증** + **선택적 Repository 저장**.  
2. **첫 TDD 슬라이스**: `DT-E01~E06` (구조) → `MagicSquareJudge` → `PuzzleSolver` (`DT-N01~N02`).  
3. **열린 질문**: Application Facade 도입 시점(저장 연동 시 vs UI→Domain 직결 유지).

---

*본 문서는 TDD·Clean Architecture 설계 산출물이며, 구현 명세서·소스 코드가 아닙니다.*
