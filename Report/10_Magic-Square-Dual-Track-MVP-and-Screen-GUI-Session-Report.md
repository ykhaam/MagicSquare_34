# Magic Square 4×4 — Dual-Track MVP · Screen GUI Session 보고서

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_ |
| 문서 버전 | 1.0 |
| 작성일 | 2026-05-29 (KST) |
| TDD phase | **GREEN (MVP 통합)** + **Screen GUI (PyQt6)** |
| Agent | Auto (Cursor) |
| 브랜치 | `stabilize/green` |
| 선행 Report | [09_Magic-Square-AC-FR-01-01-Boundary-GREEN-Session-Report.md](./09_Magic-Square-AC-FR-01-01-Boundary-GREEN-Session-Report.md) |
| SSOT | `docs/PRD_MagicSquare.md` v0.2, [02_Magic-Square-Dual-Track-TDD-Design.md](./02_Magic-Square-Dual-Track-TDD-Design.md), `tests/boundary/ac_fr_01_01_constants.py`, `.cursor/rules/*.mdc` |
| 목적 | Track A/B 전 슬라이스 GREEN, Data/Integration 추가, PyQt6 Screen GUI 구현, G1 솔버 기대값 정정 기록 |

---

## 1) 작업 목표

- README 체크리스트 **Track A (A0-1~A8)** · **Track B (B1~B6)** 구현 완료
- Boundary: `InputValidator` 전체 검증, `MagicSquareBoundary`, `UIBoundary`
- Entity/Control: `MagicGrid.from_raw`, 서비스 3종, `puzzle_solver.solution`
- Data: `InMemoryMatrixRepository`, `InMemoryResultRepository`
- Integration: IT-N01, IT-N02, IT-E01, IT-E02, IT-E04
- Screen: PyQt6 데스크톱 UI (`boundary.screen`)
- **금지 준수:** 테스트 assert 완화·skip 없음; ECB 역방향 import 없음

---

## 2) 수행한 작업

| 순서 | 작업 내용 | 결과 |
|------|-----------|------|
| 1 | AC-FR-01-01 확장 GREEN (`InputValidator` 4×4 크기) | ✅ (Report 09 이후) |
| 2 | GREEN-A1 `MagicSquareBoundary` + `ErrorResponse` | ✅ 커밋 `e992982` |
| 3 | Track A 스켈레톤 → Full assert (U-IN, U-FLOW, U-OUT) | ✅ |
| 4 | Track B 스켈레톤 → Full assert (D-LOC, D-MIS, D-VAL, D-SOL) | ✅ |
| 5 | `test_magic_grid.py` (DT-E01~E07) 신규 | ✅ |
| 6 | Data/Integration 테스트·구현 | ✅ |
| 7 | MVP 통합 커밋 | ✅ `529f09f` |
| 8 | PyQt6 Screen GUI 보강 (`window.py`, 샘플·하이라이트) | ✅ (로컬, 미커밋 가능) |
| 9 | README 진행 현황·체크리스트 동기화 | ✅ |
| 10 | G1 솔버 기대값 수학 검증·정정 | ✅ (아래 §6) |

---

## 3) 레이어별 구현 요약

### 3.1 Boundary (`src/boundary/`)

| 모듈 | 역할 |
|------|------|
| `input_validator.py` | null → size → empty count → range → duplicate (short-circuit) |
| `error_codes.py` | PRD/Report 02 고정 code·message |
| `schemas.py` | `FailureResponse`, `ErrorResponse` |
| `magic_square_boundary.py` | `solve()` — 검증 실패 시 `ErrorResponse`, 성공 시 `resolve` |
| `ui_boundary.py` | `UIBoundary(execute=...)` — Control 진입 Mock/spy용 |
| `screen/` | PyQt6 GUI (§4) |

### 3.2 Entity (`src/entity/`)

| 모듈 | 역할 |
|------|------|
| `magic_grid.py` | `MagicGrid.from_raw()` — D-STRUCT-01~04 |
| `grid_validator.py` | `is_valid_structure()` |
| `services/blank_locator.py` | `find_blank_coords()` — row-major, 1-index |
| `services/missing_number_finder.py` | `find_not_exist_nums()` — 오름차순 |
| `services/magic_validator.py` | `is_magic_square()` — 합 34, 1..16 유일 |
| `exceptions.py` | `DomainInvalidGridError`, `UnsolvableDomainError` |

### 3.3 Control (`src/control/`)

| 모듈 | 역할 |
|------|------|
| `puzzle_solver.py` | `solution()` — Step A (small→first) → Step B (reverse) |

### 3.4 Data (`src/data/`)

| 모듈 | 역할 |
|------|------|
| `matrix_repository.py` | `InMemoryMatrixRepository` save/load |
| `exceptions.py` | `DATA_NOT_FOUND`, `DATA_INVALID_GRID` 등 |

---

## 4) Screen GUI (PyQt6)

### 4.1 실행

```bash
python -m venv .venv
.\.venv\Scripts\pip install -e ".[gui]"
.\.venv\Scripts\python -m boundary.screen
# 또는: magicsquare-gui
```

`pyproject.toml`: optional extra `gui = ["PyQt6>=6.6"]`, script `magicsquare-gui`.

### 4.2 구성

| 파일 | 역할 |
|------|------|
| `screen/app.py` | `main()` 진입 |
| `screen/window.py` | `MagicSquareWindow` — 4×4 `QSpinBox`, 행·열 헤더 |
| `screen/constants.py` | `SAMPLE_PUZZLE` (PRD RD-01), 상태·스타일 상수 |
| `screen/__main__.py` | `python -m boundary.screen` |

### 4.3 기능

| 기능 | 설명 |
|------|------|
| **Solve** | `MagicSquareBoundary(resolve=solution)` 실제 Domain 연동 |
| **Load sample** | RD-01 샘플 퍼즐 로드 |
| **Clear** | 격자 0으로 초기화 |
| **성공** | 채운 칸 녹색 강조 + `[r1,c1,n1,r2,c2,n2]` 표시 |
| **실패** | `[code] message` 빨간색 표시 |

### 4.4 스크린샷 대조 (사용자 확인)

별도 실행 GUI(제목 `Magic Square 4x4`, 버튼 `풀기`)에서 `2, 2, 7, 3, 3, 10` 출력 사례가 있었음.

| 항목 | 스크린샷 예시 | 본 repo 솔버 (G1) |
|------|---------------|-------------------|
| (2,2) | 7 | **10** |
| (3,3) | 10 | **7** |
| 벡터 | `[2,2,7,3,3,10]` | **`[2,2,10,3,3,7]`** |
| 마방진 | ❌ (행 합 ≠ 34) | ✅ |

Report 07 placeholder `[2,2,7,3,3,10]`은 G1 격자와 **수학적으로 불일치** — D-SOL-01 테스트는 `[2,2,10,3,3,7]`로 정정함.

---

## 5) pytest 현황

| 명령 | 결과 |
|------|------|
| `python -m pytest tests/ -q` | **67 passed** (~0.2s) |

### 5.1 테스트 분포

| 경로 | 건수 | 내용 |
|------|------|------|
| `tests/boundary/` | 31 | AC-FR-01-01, validate_size, U-IN, U-FLOW, U-OUT |
| `tests/entity/` | 20 | User(8), magic_grid(7), D-LOC, D-MIS, D-VAL, D-SOL |
| `tests/data/` | 4 | DATA-T01, T02, T04, T05 |
| `tests/integration/` | 5 | IT-N01, IT-N02, IT-E01, IT-E02, IT-E04 |

### 5.2 README 체크리스트 (동기화)

- [x] RED-A0-1 ~ GREEN-A0-3
- [x] RED-A1 ~ GREEN-A8
- [x] RED-B1 ~ GREEN-B6
- [ ] REFACTOR / 커버리지 80%+ (후속)
- [ ] File JSON Repository · IT-E03 (후속)

---

## 6) G1 솔버 기대값 정정

**G1 격자:**

```text
[[16, 3, 2, 13],
 [5,  0, 11,  8],
 [9,  6,  0, 12],
 [4, 15, 14,  1]]
```

| 배치 | (2,2) | (3,3) | 2행 합 | 3행 합 | 마방진 |
|------|-------|-------|--------|--------|--------|
| A | 7 | 10 | 31 | 37 | ❌ |
| B | **10** | **7** | **34** | **34** | ✅ |

**솔버 출력 (Step A):** `[2, 2, 10, 3, 3, 7]`

U-OUT Mock 테스트는 `execute` 반환값 검증용으로 `[2,2,7,3,3,10]` 고정 Mock 유지 — Domain 로직과 분리됨.

---

## 7) Git 커밋 이력 (본 세션)

| 커밋 | 메시지 |
|------|--------|
| `8d2bb36` | feat(boundary): AC-FR-01-01 INVALID_SIZE via InputValidator |
| `e992982` | feat(boundary): GREEN-A1 MagicSquareBoundary invalid size |
| `529f09f` | feat: complete Dual-Track MVP — Boundary, Entity, Control, Data, IT, GUI |

**로컬 미커밋 (GUI 보강):** `screen/window.py`, `constants.py`, `__main__.py`, `README.md`, `pyproject.toml` scripts

---

## 8) ECB · 계약 준수

| 규칙 | 상태 |
|------|------|
| `entity` → `boundary` import 금지 | ✅ |
| `boundary` → `control` → `entity` 방향 | ✅ |
| Boundary invalid 시 Domain/execute 0회 | ✅ U-FLOW, IT-E01 |
| Entity Track Domain Mock 금지 | ✅ |
| 고정 error message (Report 02 §2.4) | ✅ |
| Forbidden: `print`, magic number 34/4/2 in new code | ✅ `entity.constants` SSOT |

---

## 9) 미완료 · 후속

| 항목 | 상태 |
|------|------|
| `stabilize/refactoring` 브랜치 | 미생성 |
| 커버리지 Entity 95% / Boundary 85% / 전체 80% | 미측정 |
| File JSON `MatrixRepository` (IT-E03, DATA-T03) | 미구현 |
| `develop` ← `stabilize/green` merge PR | 사용자 수동 (push/PR 본문 제공) |
| 한글 UI (`풀기`, `결과 (...)`) 스크린샷 형식 | 선택 후속 |
| U-OUT Mock 벡터 vs G1 실솔버 정렬 | Mock 계약 유지 vs 문서 정정 선택 |

---

## 10) Traceability (Report 02)

| Report 02 ID | 구현·테스트 |
|--------------|-------------|
| UT-E01~E05, UT-N01 | Boundary `InputValidator` / `UIBoundary` |
| DT-E01~E07 | `MagicGrid.from_raw`, `solution` |
| D-VAL, D-LOC, D-MIS, D-SOL | entity services + control |
| DATA-T01~T05 | `tests/data/` |
| IT-N01, IT-E01~E04 | `tests/integration/` |
| Screen (학습용) | `boundary.screen` — Report 02 “위젯 없음” API 경계의 **선택 데모** |

---

## 11) 참고 문서

- [docs/PRD_MagicSquare.md](../docs/PRD_MagicSquare.md)
- [docs/test_plan.md](../docs/test_plan.md)
- [Report/07_Magic-Square-Dual-Track-TDD-RED-Design-Report.md](./07_Magic-Square-Dual-Track-TDD-RED-Design-Report.md)
- [Report/08_Magic-Square-Dual-Track-TDD-RED-Skeleton-Session-Report.md](./08_Magic-Square-Dual-Track-TDD-RED-Skeleton-Session-Report.md)
- [Report/09_Magic-Square-AC-FR-01-01-Boundary-GREEN-Session-Report.md](./09_Magic-Square-AC-FR-01-01-Boundary-GREEN-Session-Report.md)
- [README.md](../README.md)

---

## 문서 이력

| 버전 | 날짜 | 변경 |
|------|------|------|
| 1.0 | 2026-05-29 | Dual-Track MVP · Data/IT · PyQt6 Screen GUI · G1 정정 — 최초 작성 |

---

*본 문서는 TDD GREEN(MVP 통합) 및 Screen GUI 세션 산출물이며, REFACTOR·develop merge 명세가 아닙니다.*
