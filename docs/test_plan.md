# Test Plan — AC-FR01-01 Invalid Grid Size (Dual-Track TDD)

| 항목 | 내용 |
|------|------|
| **문서 버전** | 1.0 |
| **작성 기준** | `docs/PRD_MagicSquare.md` FR-01, Report 02 §2.3–2.4 |
| **샘플 AC** | **AC-FR01-01** (부 AC: **AC-FR01-05**) |
| **대표 입력** | `grid = None` |
| **기대 출력** | `{ "code": "UI_INVALID_SIZE", "message": "Grid must be 4x4." }` |
| **기술 스택** | Python 3.11+, pytest, pydantic, unittest.mock |
| **TDD 브랜치** | `feature/dual-track-tdd` → `red` → `green` → `refactoring` |

---

## 1. 목적 및 범위

### 1.1 목적

FR-01 Input Verification 중 **4×4 구조 검증(AC-FR01-01)** 을 Dual-Track TDD의 **첫 RED 슬라이스**로 고정한다.  
Boundary 계층은 에러 스키마 반환과 Domain resolver **미호출(AC-FR01-05)** 을, Domain 계층은 `MagicGrid.fromRaw` 진입점에서 동일 선행 조건(구조 불일치) 거부를 각각 검증한다.

### 1.2 In-Scope (본 계획서)

| Track | Test-ID | 대상 | 파일(예정) |
|-------|---------|------|------------|
| **Track A — Boundary** | UT-E01 | `BoundaryValidator` / solve 진입 API | `tests/boundary/test_validate_size.py` |
| **Track B — Domain** | DT-E01 | `MagicGrid.fromRaw` | `tests/entity/test_magic_grid.py` |

### 1.3 Out-of-Scope (본 슬라이스)

- AC-FR01-02~04 (빈칸 개수, 값 범위, 중복) — 후속 슬라이스
- **4×4 정상 입력** — AC-FR01-01 범위 외, **본 계획에 포함하지 않음**
- FR-02~FR-05 (빈칸 탐색, Solver, 판정 등)
- Integration (`IT-E01`) — UT-E01 Green 후 별도 슬라이스

---

## 2. pytest 단위 테스트 범위 및 우선순위

### 2.1 우선순위 매트릭스

| 우선순위 | Track | Test-ID | 시나리오 | RED 선행 조건 |
|----------|-------|---------|----------|---------------|
| **P0** | A | UT-E01-a | `grid = None` | pytest **FAILED** 확인 후 커밋 |
| **P0** | A | UT-E01-b | `grid = []` | 동일 |
| **P0** | A | UT-E01-c | `grid = [[]] * 4` | 동일 |
| **P1** | A | UT-E01-d | 3×4 행렬 | 동일 |
| **P1** | A | UT-E01-e | 4×3 행렬 | 동일 |
| **P1** | A | UT-E01-f | 5×5 행렬 | 동일 |
| **P0** | A | UT-E01-g | 모든 P0/P1 실패 입력 → **Domain resolver 호출 0회** | Mock/spy |
| **P0** | B | DT-E01-a | 3×3 → `DOMAIN_INVALID_GRID` | pytest **FAILED** 확인 후 커밋 |
| **P1** | B | DT-E01-b | `None` / `[]` / ragged row → Domain validation failure | 동일 |

### 2.2 실행 순서 (Dual-Track RED)

Report 02 §1.5.4 및 PRD §15.3에 따라 **한 Test-ID 단위로 Red → Green → Refactor** 를 수행한다.

```
1. UT-E01 RED (Boundary, tests/ only)
2. UT-E01 GREEN (src/boundary/ only, 최소 구현)
3. DT-E01 RED (Domain, tests/ only)
4. DT-E01 GREEN (src/entity/ only, 최소 구현)
5. REFACTOR (동작 불변, 커버리지 목표 충족)
6. develop merge (양 Track Green + 커버리지 게이트)
```

### 2.3 pytest 구조 규칙

| 규칙 | 내용 |
|------|------|
| 프레임워크 | pytest 8+ |
| 패턴 | AAA (Arrange / Act / Assert) |
| Fixture scope | **function** (session 금지) |
| Marker | `@pytest.mark.ut_e01`, `@pytest.mark.dt_e01` (선택) |
| Parametrize | 경계값 케이스는 `@pytest.mark.parametrize`로 UT-E01 그룹화 |
| pydantic | 에러 응답 스키마 `ErrorResponse(code, message, field?)` 로 파싱·검증 |

---

## 3. 경계값 케이스 목록

AC-FR01-01 전용. 모든 케이스는 **동일 기대값**을 가진다.

| ID | 입력 (`grid`) | 구조 설명 | 기대 `code` | 기대 `message` | AC |
|----|---------------|-----------|-------------|----------------|-----|
| **BV-01** | `None` | 명시적 None | `UI_INVALID_SIZE` | `Grid must be 4x4.` | AC-FR01-01 |
| **BV-02** | `[]` | 빈 리스트 (행 0) | `UI_INVALID_SIZE` | `Grid must be 4x4.` | AC-FR01-01 |
| **BV-03** | `[[]] * 4` | 행 4, 열 0 (ragged) | `UI_INVALID_SIZE` | `Grid must be 4x4.` | AC-FR01-01 |
| **BV-04** | 3×4 행렬 (예: `[[1]*4]*3`) | 행 ≠ 4 | `UI_INVALID_SIZE` | `Grid must be 4x4.` | AC-FR01-01 |
| **BV-05** | 4×3 행렬 (예: `[[1,2,3]]*4`) | 열 ≠ 4 | `UI_INVALID_SIZE` | `Grid must be 4x4.` | AC-FR01-01 |
| **BV-06** | 5×5 행렬 (예: `[[0]*5]*5`) | 행·열 모두 ≠ 4 | `UI_INVALID_SIZE` | `Grid must be 4x4.` | AC-FR01-01 |

### 3.1 명시적 제외

| 입력 | 제외 사유 |
|------|-----------|
| **4×4 정상 입력** (예: RD-01) | AC-FR01-01 **범위 외** — FR-01 후속 AC 및 FR-02~05 슬라이스에서 다룸 |
| 빈칸 1/3개, 값 17, 중복 등 | AC-FR01-02~04 전용 |

### 3.2 Track별 기대 차이

| Track | 실패 표현 | 비고 |
|-------|-----------|------|
| **Boundary** | `ErrorResponse` (`UI_INVALID_SIZE`) | 예외 전파 금지 (PRD §13) |
| **Domain** | `DOMAIN_INVALID_GRID` 예외 또는 Result failure | Boundary 통과 후 이중 방어 또는 `fromRaw` 직접 호출 |

---

## 4. 예외 / 특이 케이스 목록

| ID | 케이스 | 입력 | 기대 동작 | 검증 포인트 |
|----|--------|------|-----------|-------------|
| **EX-01** | None 입력 | `None` | Boundary: `UI_INVALID_SIZE` | `TypeError` 미전파, 고정 message |
| **EX-02** | 빈 컨테이너 | `[]` | Boundary: `UI_INVALID_SIZE` | IndexError 미전파 |
| **EX-03** | Ragged row | `[[]]*4` | Boundary: `UI_INVALID_SIZE` | inner row length 0 처리 |
| **EX-04** | 비직사각형 | `[[1,2],[3,4,5]]` | Boundary: `UI_INVALID_SIZE` | 열 길이 불일치 |
| **EX-05** | 비-list 타입 | `"not_a_grid"` | Boundary: `UI_INVALID_SIZE` | duck-typing 거부 |
| **EX-06** | tuple of tuples | `((1,2,3,4),)*4` | Boundary: `UI_INVALID_SIZE` 또는 정책 확정 후 일관 거부 | DN: 타입 정책 — `int[][]` list only |
| **EX-07** | Domain 이중 방어 | Boundary Mock 통과 후 3×3 | Domain: `DOMAIN_INVALID_GRID` | Boundary 우회 시에도 Domain 차단 |
| **EX-08** | 입력 불변 (NFR-03) | 유효 형태지만 invalid size | 원본 `grid` 객체 변경 없음 | side-effect 없음 assert |

---

## 5. Domain resolver 호출 횟수 검증 전략 (Mock / Spy)

### 5.1 대상

Boundary solve 진입 API (예: `MagicSquareBoundary.solve(grid)`)가 내부에서 호출하는 **Domain resolver** — `PuzzleSolver.solveRaw` 또는 Control 계층의 `domain.solve_raw`.

### 5.2 Mock 전략 (Track A — UT-E01)

| 항목 | 전략 |
|------|------|
| 도구 | `unittest.mock.patch` 또는 `pytest-mock` (`mocker`) |
| 대상 | Domain resolver 함수/메서드 (예: `src.entity.puzzle_solver.PuzzleSolver.solve_raw`) |
| 설정 | Mock이 고정 `int[6]` 반환하도록 configure — **호출 여부만 관심** |
| Assert | `mock_solve_raw.assert_not_called()` — BV-01~BV-06 전 케이스 |
| Assert (호출 횟수) | `assert mock_solve_raw.call_count == 0` |
| Spy (대안) | `wraps=real_func` 로 patch 후 `call_count == 0` — Green 단계에서 real Domain 존재 시 |

### 5.3 검증 시나리오 매핑

| Test | Arrange | Act | Assert |
|------|---------|-----|--------|
| UT-E01-g-None | `patch("...solve_raw")` | `boundary.solve(None)` | `code == UI_INVALID_SIZE`, `call_count == 0` |
| UT-E01-g-Empty | 동일 Mock | `boundary.solve([])` | 동일 |
| UT-E01-g-Ragged | 동일 Mock | `boundary.solve([[]]*4)` | 동일 |
| UT-E01-g-3x4 | 동일 Mock | 3×4 입력 | 동일 |

### 5.4 Anti-pattern (금지)

- Boundary `UT-*` 테스트에서 **real Domain** 호출 — Track A 오염
- Mock 없이 "에러만 반환" assert — AC-FR01-05 미충족
- `call_count >= 0` 등 약한 assert — 호출 0회 명시 필수

### 5.5 Track B (DT-E01) — Mock 불필요

Domain 단위 테스트는 `MagicGrid.fromRaw` **직접 호출**. resolver spy는 Boundary 통합 슬라이스(`IT-E01`)에서 재검증.

---

## 6. 커버리지 목표

Report 02 §4.4 · PRD NFR-01 · EP-05 기준.

| 레이어 | 측정 대상 | Branch 목표 | 본 슬라이스 최소 목표 |
|--------|-----------|-------------|------------------------|
| **Domain** | `src/entity/` (`MagicGrid`, exceptions) | **≥ 95%** | `fromRaw` size-validation 분기 100% |
| **Boundary** | `src/boundary/` (`BoundaryValidator`, error map) | **≥ 85%** | size-validation + error mapping 분기 100% |
| **Global** | `src/` 전체 | **≥ 80%** | 슬라이스 merge 시 누적 충족 |

### 6.1 merge 게이트 (RG-05)

- UT-E01 + DT-E01 **전부 Green**
- Boundary size-validation 모듈 branch **≥ 85%**
- Domain `MagicGrid` structure branch **≥ 95%** (슬라이스 범위 내)
- RED 테스트 삭제·skip·xfail **금지** (RG-03)

---

## 7. pytest-cov 측정 전략

### 7.1 설치

```bash
pip install pytest-cov
# 또는 dev 의존성 일괄
pip install -e ".[dev]" pytest-cov
```

### 7.2 기본 실행 (전체)

```bash
pytest --cov=src --cov-report=term-missing
```

### 7.3 슬라이스별 실행 (권장)

**Track A — Boundary only**

```bash
pytest tests/boundary/test_validate_size.py \
  --cov=src/boundary \
  --cov-report=term-missing \
  --cov-fail-under=85
```

**Track B — Domain only**

```bash
pytest tests/entity/test_magic_grid.py \
  --cov=src/entity \
  --cov-report=term-missing \
  --cov-fail-under=95
```

**Dual-Track 통합 (merge 전)**

```bash
pytest tests/boundary/ tests/entity/ \
  --cov=src/boundary \
  --cov=src/entity \
  --cov-report=term-missing \
  --cov-report=html:htmlcov
```

### 7.4 측정 범위 설정 (pyproject.toml 권장 추가)

```toml
[tool.coverage.run]
source = ["src"]
branch = true
omit = ["tests/*"]

[tool.coverage.report]
fail_under = 80
show_missing = true
```

### 7.5 해석 가이드

| `--cov-report` | 용도 |
|----------------|------|
| `term-missing` | CI/로컬 — 미커버 라인 즉시 확인 |
| `html` | Refactor 단계 — 분기 시각화 |
| `--cov-fail-under=N` | merge gate 자동화 |

---

## 8. Traceability

| Concept | Business Rule | FR | AC | Test-ID | Scenario |
|---------|---------------|-----|-----|---------|----------|
| 4×4 입력 | BR-01 | FR-01 | AC-FR01-01 | UT-E01, DT-E01 | BV-01~BV-06 |
| Domain 미호출 | — | FR-01 | AC-FR01-05 | UT-E01-g | Mock call_count == 0 |
| 에러 message 고정 | RG-02 | FR-01 | AC-FR01-01 | UT-E01 | Report 02 §2.4 표 일치 |
| TS-E01 | — | FR-01 | AC-FR01-01 | UT-E01-d | 3×4 등 invalid size |

---

## 9. RED → GREEN 체크리스트

### RED (`red` 브랜치, `tests/` only)

- [ ] UT-E01: BV-01~BV-06 parametrize — **전부 FAILED**
- [ ] UT-E01-g: Domain resolver `assert_not_called` — **FAILED** (Boundary 미구현)
- [ ] DT-E01: 3×3 및 None/[] — **FAILED**
- [ ] `pytest` 실행 결과 Red 확인 후 커밋

### GREEN (`green` 브랜치, `src/` only)

- [ ] `BoundaryValidator` — size check 최소 구현
- [ ] `MagicGrid.fromRaw` — D-STRUCT-01 최소 구현
- [ ] pydantic `ErrorResponse` — code/message 검증 통과
- [ ] **전부 PASSED**, Mock call_count == 0

### REFACTOR (`refactoring` 브랜치)

- [ ] ERROR_MESSAGES 상수화 (매직 스트링 금지)
- [ ] size validation 함수 추출 (동작 불변)
- [ ] `--cov-fail-under` 게이트 통과
- [ ] `develop` merge

---

## 10. 부록 — pydantic 에러 스키마 (계약)

테스트 Arrange/Assert에서 사용할 응답 모델 (구현 시 `src/boundary/schemas.py` 등).

| Field | Type | Required | Rule |
|-------|------|----------|------|
| `code` | `str` | Y | `UI_INVALID_SIZE` 등 코드표 고정 |
| `message` | `str` | Y | Report 02 §2.4 문구 **완전 일치** |
| `field` | `str \| None` | N | 예: `grid`, `grid[0]` |

---

## 11. 참고 문서

- `docs/PRD_MagicSquare.md` — FR-01, §12.1, §13, §15, §16.2 TS-E01
- `Report/02_Magic-Square-Dual-Track-TDD-Design.md` — UT-E01, DT-E01, §2.4 message 표
- `.cursor/rules/magicsquare-tdd-testing.mdc` — Red/Green/Refactor 브랜치 규칙
