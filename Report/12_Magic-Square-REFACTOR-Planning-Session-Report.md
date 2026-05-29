# Magic Square 4×4 — REFACTOR Planning Session 보고서

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_ |
| 문서 버전 | 1.0 |
| 작성일 | 2026-05-29 (KST) |
| TDD phase | **REFACTOR (계획)** — `src/` 구조 변경 전 분석·슬라이스 설계 |
| Agent | Auto (Cursor) · code-reviewer 서브에이전트 |
| 브랜치 | `refactor/refactor` |
| 선행 Report | [11_Magic-Square-Golden-Master-Regression-Session-Report.md](./11_Magic-Square-Golden-Master-Regression-Session-Report.md) |
| SSOT | [02_Magic-Square-Dual-Track-TDD-Design.md](./02_Magic-Square-Dual-Track-TDD-Design.md), `.cursor/rules/magicsquare-*.mdc`, `docs/PRD_MagicSquare.md` |
| 목적 | ECB 역할·SRP·계약 gap 분석, 리팩토링 대상·테스트 선행·검증 방법 문서화 (코드 미변경) |

---

## 1) 작업 목표

- REFACTOR phase 진입 전 **대상 파일·테스트 갭·High 스멜** 정리
- ECB 매핑(프롬프트 domain/boundary/gui → 실제 `src/` 경로) 확정
- **code-reviewer** 전체 리뷰 결과 반영
- 리팩토링 **계획서**(우선순위·테스트 선행·회귀 검증) 산출
- 본 세션: **문서만** — `src/`·`tests/` 프로덕션/테스트 코드 변경 없음

---

## 2) ECB 파일 매핑 (프롬프트 → 실제)

| 프롬프트 역할 | ECB 목표 경로 | 현재 구현 | 비고 |
|---------------|---------------|-----------|------|
| domain.py | `src/control/solve_partial_magic_square.py` | `src/control/puzzle_solver.py` | rename 예정 |
| boundary.py | `src/boundary/ui_boundary.py` | 동명 (re-export) | 실체 `magic_square_boundary.py` |
| gui/main_window | `src/boundary/screen/main_window.py` | `src/boundary/screen/window.py` | `MagicSquareWindow` |
| (계획) | `src/entity/services/two_cell_solver.py` | **미존재** | Step A/B 추출 대상 |

**허용 의존:** `boundary → control → entity`  
**금지:** `entity → boundary|control`, Screen → Control 직접, Control → Boundary

---

## 3) pytest · 커버리지 현황 (세션 시점)

| 항목 | 결과 |
|------|------|
| `python -m pytest tests/ -q` | **73 passed** |
| RED 스켈레톤 `pytest.fail("RED:…")` | **0건** (Report 08 스켈레톤 → GREEN 완료) |
| Golden Master | GM-TC-01~05 PASS (`-m golden_master`) |
| 전역 커버리지 (참고) | **~67%** (REFACTOR 목표 80% 미달) |
| Screen (`boundary/screen/*`) | **0%** |

---

## 4) ECB 역할 적합성 요약

| 파일 (목표명) | 현재 역할 | 적합 | 핵심 근거 |
|---------------|-----------|------|-----------|
| `solve_partial_magic_square` | Control + Entity 알고리즘 혼재 | **부분** | `_try_placement`가 Domain 책임 |
| `ui_boundary` | Boundary re-export만 | **부분** | E001~E007·int[6] guard는 `magic_square_boundary` |
| `main_window` | Screen + Control 결합 | **부분** | `puzzle_solver` 직접 import (34, 44행) |

**판정:**

- `solve_partial` → **Control** (orchestration). 알고리즘은 **Entity** (`two_cell_solver`).
- `ui_boundary` → 본 파일 단독 must_not 위반 없음; Boundary SSOT 분산.
- `main_window` → 검증·Step A/B·magic 합 계산 없음; **249행** E00x code 결정만 UI 비즈니스 판단.

---

## 5) Critical · High 이슈 (code-reviewer + 세션 분석)

### 5.1 Critical

| Area | File:Line | Issue |
|------|-----------|-------|
| ECB / SRP | `puzzle_solver.py:14–66` | Control이 Step A/B·배치·int[6] 조립 수행 |
| ECB | `window.py:34–44` | Screen → Control 직접, `UIBoundary` 우회 |
| Contract | `magic_square_boundary.py:40–43` | `DomainInvalidGridError` 미매핑 |
| Contract | `magic_square_boundary.py:24–41` | UT-F01/F02 int[6] guard 없음 |
| SSOT | `error_codes.py` vs Report 02 | `INVALID_SIZE` vs `UI_INVALID_SIZE` (DEF-003) |
| Forbidden | `window.py:249` | `"UI_INTERNAL"` 하드코딩 |

### 5.2 High

| Area | Issue |
|------|-------|
| DRY | `input_validator.py` ↔ `grid_validator.py` 이중 D-STRUCT 검증 |
| Architecture | `ui_boundary.py` re-export vs `magic_square_boundary` 실체 분리 |
| Traceability | `test_d_sol_01` docstring "Step A" vs G1 Step B 기대값 |
| Coverage | Screen 0%, global 67% |

---

## 6) SRP 위반 요약 (함수·클래스·UI)

### 6.1 함수 다중 역할

| 파일:줄 | 역할 1 | 역할 2 |
|---------|--------|--------|
| `puzzle_solver:solution` 14–43 | 오케스트레이션 | 구조 검증 + Step A/B 결정 |
| `puzzle_solver:_try_placement` 46–66 | 배치·magic 판정 | int[6] 조립 |
| `window:__init__` 41–49 | UI 초기화 | Boundary/Control 결합 |
| `window:_init_ui` 51–127 | 레이아웃 | `_cells` 데이터 구조 |
| `window:_on_solve_clicked` 236–249 | Boundary 호출·라우팅 | `UI_INTERNAL` code 생성 |

### 6.2 UI 비즈니스 판단

| 파일:줄 | 내용 |
|---------|------|
| `window:249` | `"UI_INTERNAL"` code·message Screen에서 결정 |

---

## 7) 테스트 갭 · 선행 RED 목록

| Layer | Missing | Suggested Test-ID |
|-------|---------|-------------------|
| Boundary | wrong-length execute return | **UT-F01** |
| Boundary | 0-index coordinates | **UT-F02** |
| Boundary | `DomainInvalidGridError` mapping | **UT-E07** |
| Entity | `two_cell_solver` 추출 후 | **DT-N01~03**, **D-SOL-01~04** |
| Screen | UIBoundary wiring, 표시 | **UT-GUI-01~04** (신규) |
| SSOT | error code rename | **UT-E01**, GM-TC-03~05 |

**리팩토링 전 테스트 없이 금지:** Boundary guard·E006/E007, `two_cell_solver` 추출, Screen ECB wiring.

---

## 8) 리팩토링 대상 목록 (우선순위)

| 순번 | 대상 | 문제 | 기법 | 우선순위 |
|------|------|------|------|----------|
| 1 | `magic_square_boundary.py` | int[6] guard 없음 | Contract Guard | P0 |
| 2 | `magic_square_boundary.py` | E006/E007 미매핑 | Exception Mapping | P0 |
| 3 | `error_codes.py` | DEF-003 code drift | SSOT 정렬 | P0 |
| 4 | `window.py` + error_codes | UI_INTERNAL 하드코딩 | Extract Constant | P0 |
| 5 | `window.py` | Control 직접 import | Dependency Inversion → UIBoundary | P0 |
| 6 | `puzzle_solver.py` | Domain 알고리즘 혼재 | Extract Module → `two_cell_solver` | P0 |
| 7 | `puzzle_solver.py` | 중복 `MagicGrid.from_raw` | Remove Duplication | P0 |
| 8 | `input_validator.py` | grid_validator 중복 | Shared Kernel / Adapter | P1 |
| 9 | `ui_boundary.py` | SSOT 분산 | Move Class / Consolidation | P1 |
| 10 | `window.py` | 긴 `_init_ui`, 루프 중복 | Extract Method/Class | P1 |
| 11 | `puzzle_solver.py` | 파일명 | Rename → solve_partial | P1 |
| 12 | `window.py` | 파일명 | Rename → main_window | P2 |
| 13 | `magic_grid.py` | literal `4` | Replace Magic Number | P2 |
| 14 | `test_d_sol_01` | docstring drift | Rename Test / Doc | P2 |

---

## 9) 권장 슬라이스 순서 (P0 → P1)

```text
[P0-1] UT-F01/F02 RED → GREEN (Boundary guard)
[P0-2] UT-E07 RED → GREEN (DomainInvalidGridError)
[P0-3] DEF-003 + UI_INTERNAL_CONTRACT RED → GREEN
[P0-4] two_cell_solver RED → GREEN + Control thin
[P0-5] UT-GUI RED → GREEN (Screen UIBoundary)
[P1-*] validator SSOT, ui_boundary consolidate, rename, layout extract
[P2-*] coverage ≥80%, doc fix
```

---

## 10) 리팩토링 후 검증

### 10.1 회귀 명령

```bash
python -m pytest tests/ -q
python -m pytest -m golden_master -v
python -m pytest tests/boundary/ tests/integration/ -v
python -m pytest tests/ --cov=src --cov-fail-under=80
```

### 10.2 기능 불변 기준

- 입·출력 계약: 4×4 grid, `int[6]` 1-index, E001~E007 message byte-exact
- Golden Master baseline diff 없음 (또는 승인 갱신)
- GUI 수동: Sample → Solve → G1 `[2,2,10,3,3,7]`; invalid → `[code] message`

---

## 11) Traceability

| Report 02 | 본 계획 |
|-----------|---------|
| UT-F01, UT-F02 | P0-1 |
| UT-E01, DEF-003 | P0-3 |
| DT-N01~03, D-SOL | P0-4 |
| IT-N01, IT-E01~E04 | 회귀 suite |
| GM-TC-01~05 | golden_master marker |
| REFACTOR coverage 80% | P2 exit |

---

## 12) 미착수 · 후속

| 항목 | 상태 |
|------|------|
| `src/` refactor 구현 | ⏳ 본 Report 이후 슬라이스별 Red-Green-Refactor |
| `stabilize/refactoring` 브랜치 merge → develop | ⏳ |
| File JSON / IT-E03 | 백로그 |

---

## 문서 이력

| 버전 | 날짜 | 변경 |
|------|------|------|
| 1.0 | 2026-05-29 | REFACTOR 계획·ECB·SRP·code-reviewer 종합 — 최초 작성 |

---

*본 문서는 TDD REFACTOR **계획** 산출물이며, 프로덕션 코드 변경을 포함하지 않습니다.*
