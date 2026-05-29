# MagicSquare_

4×4 **마방진(Magic Square)** TDD 연습 프로젝트입니다.  
**Phase 01~02** 문제 정의·Dual-Track 설계, **Phase 03** 구현 착수, **Phase 04** Cursor 규칙(`.mdc`) 이중 레이어까지 문서화했습니다.

저장소: [ykhaam/MagicSquare_xx](https://github.com/ykhaam/MagicSquare_xx)

---

## Phase 요약

| Phase | 내용 | Report | Prompting | 상태 |
|-------|------|--------|-----------|------|
| **01** | 관찰 · Why · 문제 정의 · Invariant I1~I5 | [01](./Report/01_Magic-Square-Problem-Definition-Report.md) | [01](./Prompting/01_Magic-Square-Problem-Definition-Prompt.md) | ✅ |
| **02** | Dual-Track(UI+Logic) TDD · Clean Architecture 설계 | [02](./Report/02_Magic-Square-Dual-Track-TDD-Design.md) | [02](./Prompting/02_Magic-Square-Prompt.md) | ✅ |
| **03** | `.cursorrules` YAML · ECB `User` · TDD 구현 착수 | [03](./Report/03_Magic-Square-Cursorrules-and-Phase03-Kickoff-Report.md) | [03](./Prompting/03_Magic-Square-Phase03-Cursorrules-Prompt.md) | 🔄 진행 중 |
| **04** | Cursor 규칙 `.cursor/rules/*.mdc` 마이그레이션 | [04](./Report/04_Magic-Square-Cursor-Rules-Migration-Report.md) | [04](./Prompting/04_Magic-Square-Cursor-Rules-Migration-Prompt.md) | ✅ |

---

## Phase 01 — 문제 정의 (요약)

> 학습자가 제시한 4×4 격자가 마방진 규칙을 **모두 만족하는지 일관되게 판정**하고, **명확한 피드백**을 제공하는 연습 환경을 정의·보장한다.

- 가정: 학습·퍼즐형 · 값 1~16 · 행·열·대각선 합 동일  
- Invariant: **I1~I5** — [Report 01 §7](./Report/01_Magic-Square-Problem-Definition-Report.md#73-핵심-invariant)

---

## Phase 02 — TDD 설계 (현재 구현 계약)

알고리즘 난이도보다 **레이어 분리 · 계약 기반 테스트 · 리팩토링** 훈련이 목적입니다.  
상세: [Report 02](./Report/02_Magic-Square-Dual-Track-TDD-Design.md)

### 입·출력 계약 (고정)

| 구분 | 규칙 |
|------|------|
| **입력** | `int[4][4]` · `0` = 빈칸 · 빈칸 **정확히 2개** · 값 `0` 또는 `1~16` · 비零 중복 금지 |
| **출력** | `int[6]` = `[r1,c1,n1,r2,c2,n2]` · 좌표 **1-index** |
| **해 찾기** | 누락 수 2개를 row-major 첫·둘째 빈칸에 배치 시도 (작은→첫, 큰→둘째 → 실패 시 반대) |
| **매직 합** | 완성 시 행·열·대각선 합 = **34** |

### 레이어

| 레이어 | 역할 |
|--------|------|
| **Domain (Logic)** | `MagicGrid`, `PuzzleSolver`, `MagicSquareJudge` 등 — UI·저장소 무의존 |
| **UI (Boundary)** | 입력 검증 · `int[6]` 반환 · 고정 Error schema |
| **Data** | `MatrixRepository` save/load — InMemory 추천 (File 확장 가능) |

### Phase 02 불변 (일부)

| ID | 요약 |
|----|------|
| D-STRUCT-01~04 | 4×4, 빈칸 2, 값 범위, 비零 유일 |
| D-MAGIC-01 | 완성 격자 합 = 34 |
| D-SOLVE-02~04 | 배치 시도 순서 · 해 없음 처리 |
| D-OUT-01 | 출력 좌표 1-index |

전체: [Report 02 §1.2](./Report/02_Magic-Square-Dual-Track-TDD-Design.md#12-도메인-불변조건-invariants)

---

## Phase 03 — 구현 착수 (요약)

- 루트 `.cursorrules` YAML 완성 → Phase 04에서 `.mdc`로 이전·슬림화
- ECB **entity** 샘플: `User` + pytest 8건 Green  
- 상세: [Report 03](./Report/03_Magic-Square-Cursorrules-and-Phase03-Kickoff-Report.md)

---

## Phase 04 — Cursor Rules 마이그레이션 (요약)

| 항목 | 내용 |
|------|------|
| SSOT | `.cursor/rules/magicsquare-*.mdc` (5파일) |
| 인덱스 | `.cursorrules` (~40줄, `rules_index`) |
| alwaysApply | project, forbidden, tdd-testing |
| globs | python-code-style (`**/*.py`), ecb-architecture (`src/**`, `tests/**`) |

상세: [Report 04](./Report/04_Magic-Square-Cursor-Rules-Migration-Report.md)

---

## Git 브랜치 전략

```
main                    ← 마일스톤 스냅샷 (안정)
develop                 ← 통합 (merge 후 Green 목표)
spec                    ← 수용 조건·설계 문서
feature/dual-track-tdd  ← Dual-Track RED 설계·스켈레톤 (병합 완료 시 develop)
  → red                 ← 실패 테스트만 (tests/)
    → green             ← 최소 구현만 (src/)
      → refactoring     ← 동작 유지 구조 개선
        → develop
```

| 브랜치 | 용도 | 변경 허용 | 원격 |
|--------|------|-----------|------|
| `main` | 문서·동작 스냅샷 | 문서·릴리스 | `origin/main` |
| `develop` | TDD 통합 | merge from `refactoring` | `origin/develop` |
| `spec` | 설계·PRD·규칙 | `Report/`, `docs/`, `.cursor/` | `origin/spec` |
| `feature/dual-track-tdd` | Dual-Track RED 묶음 (레거시) | — | `origin/feature/dual-track-tdd` |
| **`red`** | **현재 RED 슬라이스** | **`tests/`만** | `origin/red` (push 후) |
| **`green`** | **현재 GREEN 슬라이스** | **`src/`만** | `origin/green` (push 후) |
| **`refactoring`** | **리팩터 슬라이스** | 구조·이름 (계약 동일) | `origin/refactoring` (push 후) |

> **참고:** 이전 작업 브랜치 `stabilize/green`은 **`green`으로 통일**합니다. AC-FR-01-01 Boundary GREEN은 `green`에서 이어갑니다.

TDD 사이클: `spec → red → green → refactoring → develop` (**동시에 red/green/refactoring 3분기 금지**)

```bash
# 예: 다음 GREEN 슬라이스
git checkout green
python -m pytest <node id> -v   # RED 확인 → src/ 최소 수정 → PASS
git checkout -b refactoring     # REFACTOR 시에만
```

---

## 저장소 구조

```
MagicSquare_/
├── README.md
├── .cursorrules              # 규칙 인덱스 · contract 요약
├── .cursor/rules/            # magicsquare-*.mdc (실행 규칙 SSOT)
├── pyproject.toml
├── src/
│   ├── boundary/             # InputValidator, schemas (Track A)
│   ├── control/              # (예정) PuzzleSolver 진입
│   └── entity/               # User · services (Track B)
├── tests/
│   ├── boundary/             # UT-* · AC-FR-* (Mock 허용)
│   └── entity/               # DT-* · D-* (Mock 금지)
├── Report/
│   ├── 01_Magic-Square-Problem-Definition-Report.md
│   ├── 02_Magic-Square-Dual-Track-TDD-Design.md
│   ├── 03_Magic-Square-Cursorrules-and-Phase03-Kickoff-Report.md
│   └── 04_Magic-Square-Cursor-Rules-Migration-Report.md
└── Prompting/
    ├── 01_Magic-Square-Problem-Definition-Prompt.md
    ├── 02_Magic-Square-Prompt.md
    ├── 03_Magic-Square-Phase03-Cursorrules-Prompt.md
    └── 04_Magic-Square-Cursor-Rules-Migration-Prompt.md
```

---

## 문서 바로가기 (Report 01~04)

| 문서 | 설명 |
|------|------|
| [Report/01](./Report/01_Magic-Square-Problem-Definition-Report.md) | STEP 1~5 · I1~I5 · 열린 질문 |
| [Report/02](./Report/02_Magic-Square-Dual-Track-TDD-Design.md) | Logic / UI / Data / Integration · Traceability |
| [Report/03](./Report/03_Magic-Square-Cursorrules-and-Phase03-Kickoff-Report.md) | `.cursorrules` YAML · `User` entity · Phase 03 kickoff |
| [Report/04](./Report/04_Magic-Square-Cursor-Rules-Migration-Report.md) | `.mdc` 5파일 · 슬림 `.cursorrules` |
| [Prompting/01](./Prompting/01_Magic-Square-Problem-Definition-Prompt.md) | Turn 01~02 · 문제 정의 워크숍 |
| [Prompting/02](./Prompting/02_Magic-Square-Prompt.md) | Turn 03~18 · Dual-Track 설계 |
| [Prompting/03](./Prompting/03_Magic-Square-Phase03-Cursorrules-Prompt.md) | Turn 19~27 · `.cursorrules` · `User` |
| [Prompting/04](./Prompting/04_Magic-Square-Cursor-Rules-Migration-Prompt.md) | Turn 28~32 · `.mdc` 마이그레이션 |

---

## 진행 현황

| 단계 | 내용 | 상태 |
|------|------|------|
| STEP 1~5 | 문제 정의 (Report 01) | ✅ |
| Dual-Track 설계 | Report 02 · Prompting 02 | ✅ |
| Cursor Rules `.mdc` | Report 04 · 5× `.mdc` | ✅ |
| `.cursorrules` · `User` entity | Report 03 · Phase 03 kickoff | ✅ |
| **AC-FR-01-01** | `InputValidator` · `test_ac_fr_01_01_*` 9건 | ✅ GREEN (`green`) |
| **`red`** | 실패 테스트 **3건/커밋** (`tests/` only) | 🔄 `red` 브랜치 · **다음: RED-A1** |
| **`green`** | 최소 구현 슬라이스 (`src/` only) | 🔄 **현재 작업 브랜치** |
| **`refactoring`** | 구조 정리 (계약 동일) | ⏳ |
| `develop` / `main` merge | MVP 마일스톤 | ⏳ |

상세 GREEN 세션: [Report 09](./Report/09_Magic-Square-AC-FR-01-01-Boundary-GREEN-Session-Report.md)

---

1. **`red` 브랜치**에서 아래 **RED 묶음(3건/커밋)** 다음 미체크만 커밋 → `green`에서 **GREEN 1 node/커밋**
2. Track A·B **동시 RED/GREEN 금지** — 한 트랙씩 `red` → `green` → `refactoring` → `develop`
3. RED 잔여 2건 묶음은 **마지막 슬라이스 예외** (총 건수 % 3 ≠ 0일 때만)
4. 계약 충돌 시 Report **02 우선** · AI 규칙은 **04 + `.mdc`**

---

## TDD RED / GREEN To-Do (체크리스트)

> **RED:** `git checkout red` · **`tests/`만** · **3 test(또는 parametrize 3 id) = 1 커밋**  
> **GREEN:** `git checkout green` · **`src/`만** · **1 node id = 1 커밋** · REFACTOR = 동작 동일  
> **Track A/B 동시 RED·GREEN 금지**  
> SSOT: [Report 02 §1.5.4](./Report/02_Magic-Square-Dual-Track-TDD-Design.md#154-red-작성-순서-권장) · [docs/test_plan.md](./docs/test_plan.md)

### 매 슬라이스 (공통)

**RED (`red` 브랜치)**

- [ ] 묶음 내 3건 `pytest` → **FAIL** 확인 후 `tests/`만 커밋
- [ ] `git checkout green`

**GREEN (`green` 브랜치)**

- [ ] `python -m pytest <node id> -v` → **FAIL** (이미 PASS면 `src/` 수정 금지)
- [ ] `src/` 최소 수정 · Boundary는 `FailureResponse`/`ErrorResponse` (throw 금지)
- [ ] 동일 node id **PASS** · Conventional Commit 1건

---

### Track A — Boundary (Mock 허용)

#### RED 묶음 — 3건/커밋 (`red` 브랜치)

| ID | 커밋 | 테스트 3건 (node id 요약) | 상태 |
|----|------|---------------------------|------|
| **RED-A0-1** | AC-FR-01-01 ① | `test_none_grid_returns_failure_with_invalid_size_code` · `[empty_list]` · `[four_empty_rows]` | ✅ |
| **RED-A0-2** | AC-FR-01-01 ② | `[size_3x4]` · `test_none_grid_message_matches_prd_section_8_1_exactly` · `test_none_grid_returns_exact_invalid_size_code_string` | ✅ |
| **RED-A0-3** | AC-FR-01-01 ③ | `test_none_grid_returns_pydantic_failure_response_type` · `test_ac_fr_01_01_scope_excludes_later_acceptance_criteria` · `test_ac_fr_01_01_scope_module_covers_only_null_and_size_tags` | ✅ |
| **RED-A1** | UT-E01 ① | `test_none_grid_returns_invalid_size_failure` · `test_empty_list_returns_invalid_size_failure` · `test_ragged_four_rows_returns_invalid_size_failure` | ⏳ |
| **RED-A2** | UT-E01 ② | `test_three_by_four_grid_returns_invalid_size_failure` · `test_none_grid_resolve_called_zero_times` · `test_none_grid_message_exact_prd_match` | ⏳ |
| **RED-A3** | UT-E01 ③ (2건) | `test_none_grid_failure_result_is_error_response_type` · `test_scope_excludes_ac_fr01_02_to_05_and_fr02_to_fr05` | ⏳ |
| **RED-A4** | U-IN ① | `test_u_in_04_minus_one_returns_e004` · `test_u_in_05_seventeen_returns_e004` · `test_u_in_06_duplicate_nonzero_returns_e005` | ⏳ |
| **RED-A5** | U-IN ② (2건) | `test_u_in_07_out_of_range_ninety_nine_returns_e004` · `test_u_in_08_non_list_grid_returns_e001` | ⏳ |
| **RED-A6** | U-FLOW ① | `test_u_flow_02_null_matrix_skips_execute` · `test_u_flow_02_invalid_size_skips_execute` · `test_u_flow_02_invalid_empty_count_skips_execute` | ⏳ |
| **RED-A7** | U-FLOW ② | `test_u_flow_02_invalid_range_skips_execute` · `test_u_flow_02_duplicate_skips_execute` · `test_u_flow_02_ragged_grid_skips_execute` | ⏳ |
| **RED-A8** | U-OUT | `test_u_out_01_success_payload_length_six` · `test_u_out_02_success_coordinates_one_indexed` · `test_u_out_03_success_fill_values_in_range` | ⏳ |

파일 접두: `tests/boundary/test_ac_fr_01_01_input_validation.py` (A0) · `test_validate_size.py` (A1~A3) · `test_u_in_04_08_input_validation.py` (A4~A5) · `test_u_flow_02_invalid_skips_execute.py` (A6~A7) · `test_u_out_01_03_output_contract.py` (A8)

- [ ] **RED-A1** — UT-E01 ① (3건)
- [ ] **RED-A2** — UT-E01 ② (3건)
- [ ] **RED-A3** — UT-E01 ③ (2건)
- [ ] **RED-A4** — U-IN ① (3건)
- [ ] **RED-A5** — U-IN ② (2건)
- [ ] **RED-A6** — U-FLOW ① (3건)
- [ ] **RED-A7** — U-FLOW ② (3건)
- [ ] **RED-A8** — U-OUT (3건)

#### GREEN — 1 node/커밋 (`green` 브랜치) · RED-A1 이후 순서

**UT-E01** (`test_validate_size.py`)

- [ ] **UT-E01-1** `::TestAcFr0101InvalidSize::test_none_grid_returns_invalid_size_failure`
- [ ] **UT-E01-2** `::test_empty_list_returns_invalid_size_failure`
- [ ] **UT-E01-3** `::test_ragged_four_rows_returns_invalid_size_failure`
- [ ] **UT-E01-4** `::test_three_by_four_grid_returns_invalid_size_failure`
- [ ] **UT-E01-5** `::test_none_grid_resolve_called_zero_times`
- [ ] **UT-E01-6** `::test_none_grid_message_exact_prd_match`
- [ ] **UT-E01-7** `::test_none_grid_failure_result_is_error_response_type`
- [ ] **UT-E01-8** `::test_scope_excludes_ac_fr01_02_to_05_and_fr02_to_fr05`

**U-IN-04~08** (`test_u_in_04_08_input_validation.py`)

- [ ] **U-IN-04** `::TestUIn04Through08InputValidation::test_u_in_04_minus_one_returns_e004`
- [ ] **U-IN-05** `::test_u_in_05_seventeen_returns_e004`
- [ ] **U-IN-06** `::test_u_in_06_duplicate_nonzero_returns_e005`
- [ ] **U-IN-07** `::test_u_in_07_out_of_range_ninety_nine_returns_e004`
- [ ] **U-IN-08** `::test_u_in_08_non_list_grid_returns_e001`

**U-FLOW-02** (`test_u_flow_02_invalid_skips_execute.py`)

- [ ] **U-FLOW-02a** `::test_u_flow_02_null_matrix_skips_execute`
- [ ] **U-FLOW-02b** `::test_u_flow_02_invalid_size_skips_execute`
- [ ] **U-FLOW-02c** `::test_u_flow_02_invalid_empty_count_skips_execute`
- [ ] **U-FLOW-02d** `::test_u_flow_02_invalid_range_skips_execute`
- [ ] **U-FLOW-02e** `::test_u_flow_02_duplicate_skips_execute`
- [ ] **U-FLOW-02f** `::test_u_flow_02_ragged_grid_skips_execute`

**U-OUT-01~03** (`test_u_out_01_03_output_contract.py`)

- [ ] **U-OUT-01** `::test_u_out_01_success_payload_length_six`
- [ ] **U-OUT-02** `::test_u_out_02_success_coordinates_one_indexed`
- [ ] **U-OUT-03** `::test_u_out_03_success_fill_values_in_range`

| Track A | RED 묶음 | GREEN 대기 |
|---------|----------|------------|
| AC-FR-01-01 | A0-1~3 ✅ | GREEN 완료 (9) |
| UT-E01 ~ U-OUT | A1~A8 ⏳ | **22** |

---

### Track B — Entity/Control (Mock 금지) · Report 02 §1.5.4

#### RED 묶음 — 3건/커밋 (`red` 브랜치)

| ID | 커밋 | 테스트 3건 | 상태 |
|----|------|------------|------|
| **RED-B1** | DT-E ① | DT-E01 · DT-E02 · DT-E03 (`test_magic_grid.py` 등 **미작성**) | ⏳ |
| **RED-B2** | DT-E ② | DT-E04 · DT-E05 · DT-E06 | ⏳ |
| **RED-B3** | D-VAL ① | `test_d_val_01_g0_complete_magic_true` · `test_d_val_02_row_sum_mismatch` · `test_d_val_03_col_sum_mismatch` | ⏳ |
| **RED-B4** | D-VAL ② | `test_d_val_04_diagonal_mismatch` · `test_d_val_05_duplicate_false` · `test_d_val_06_zero_in_filled_false` | ⏳ |
| **RED-B5** | D-LOC/MIS/SOL ① | `test_d_loc_01_g1_row_major_blanks` · `test_d_mis_01_g1_missing_sorted` · `test_d_sol_01_g1_step_a_success` | ⏳ |
| **RED-B6** | D-SOL ② | `test_d_sol_02_g2_step_b_reverse` · `test_d_sol_03_g3_unsolvable` · `test_d_sol_04_output_contract` | ⏳ |

- [ ] **RED-B1** — DT-E ① (3건)
- [ ] **RED-B2** — DT-E ② (3건)
- [ ] **RED-B3** — D-VAL ① (3건)
- [ ] **RED-B4** — D-VAL ② (3건)
- [ ] **RED-B5** — D-LOC/MIS/SOL ① (3건)
- [ ] **RED-B6** — D-SOL ② (3건)

#### GREEN — 1 node/커밋 (`green` 브랜치)

- [ ] **D-VAL-01** ~ **D-VAL-06** (`test_d_val_01_06_magic_validation.py`)
- [ ] **D-LOC-01** (`test_d_loc_01_blank_coords.py`)
- [ ] **D-MIS-01** (`test_d_mis_01_missing_numbers.py`)
- [ ] **D-SOL-01** ~ **D-SOL-04** (`test_d_sol_01_04_solution.py`)

| Track B | RED 묶음 | GREEN 대기 |
|---------|----------|------------|
| DT-E ~ D-SOL | B1~B6 ⏳ | **12+** |

> **제외:** `tests/entity/test_user.py` — 학습용 `User` (마방진 백로그 밖)

---

### 커버리지 목표 (REFACTOR / develop merge 시)

- [ ] Entity Logic: 95%+ branch
- [ ] Boundary: 85%+ branch
- [ ] 전체: 80%+ (Report 02 §4.4)
---

## 범위

- **포함**: 문제 정의, TDD 설계, Cursor 규칙, `User` entity, 테스트 인프라  
- **진행 중**: `MagicGrid` / `PuzzleSolver` (`DT-*` per Report 02)

---

## 문서 이력

| 날짜 | 변경 |
|------|------|
| 2026-05-28 | README · Report 01 · Prompting 01 |
| 2026-05-28 | Report 02 · Prompting 02 · `spec` 브랜치 |
| 2026-05-28 | Report 03 · Prompting 03 · `.cursorrules` · `User` entity |
| 2026-05-28 | Report 04 · Prompting 04 · `.cursor/rules/*.mdc` · README 01~04 동기화 |
| 2026-05-29 | TDD 브랜치 `red`/`green`/`refactoring` · RED 3건/커밋 · GREEN To-Do · AC-FR-01-01 반영 |
