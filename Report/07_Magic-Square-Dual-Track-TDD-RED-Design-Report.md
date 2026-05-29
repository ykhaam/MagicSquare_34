# Magic Square 4×4 — Dual-Track TDD RED 설계 보고서 (전체 FR-01~FR-05)

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_ |
| 문서 버전 | 1.0 |
| 작성일 | 2026-05-29 (KST) |
| TDD phase | **RED** (설계표만; 코드·pytest·파일 저장 없음) |
| Agent | Auto (Cursor) |
| 선행 Report | [06_Magic-Square-Dual-Track-TDD-RED-Session-Report.md](./06_Magic-Square-Dual-Track-TDD-RED-Session-Report.md) |
| 짝 Transcript | [07_Magic-Square-Dual-Track-TDD-RED-Design-Transcript-Prompt.md](../Prompting/07_Magic-Square-Dual-Track-TDD-RED-Design-Transcript-Prompt.md) |
| SSOT | `docs/PRD_MagicSquare.md` v0.2, [02_Magic-Square-Dual-Track-TDD-Design.md](./02_Magic-Square-Dual-Track-TDD-Design.md), `.cursorrules` |
| 목적 | FR-01~FR-05 범위 **Track A(Boundary)** + **Track B(Domain/Logic)** RED 테스트 설계표 확정 |

---

## 1) 작업 목표

- Dual-Track UI + Logic TDD **RED 단계**에서 구현·테스트 코드 없이 설계표만 작성
- Track A: 입력 검증(`U-IN-*`) · 출력 계약(`U-OUT-*`) · 흐름 격리(`U-FLOW-02`) 분리
- Track B: `find_blank_coords` / `find_not_exist_nums` / `is_magic_square` / `solution` 별칭 기준 슬라이스 분리
- SSOT Test-ID(`U-*`, `D-*`)와 Report 02(`UT-*`, `DT-*`) 추적성 매핑
- G0~G3 격자 fixture 정의(부록 placeholder 포함)

---

## 2) 수행한 작업

| 순서 | 작업 내용 | 결과 |
|------|-----------|------|
| 1 | PRD v0.2 · Report 02 · `.cursorrules` 계약·검증 순서 확인 | 완료 |
| 2 | Track A RED 설계표 14행 (U-IN 11 + U-OUT 2 + U-FLOW 1) | 완료 |
| 3 | Track B RED 설계표 14행 (D-LOC~D-SOL) | 완료 |
| 4 | G0~G3 fixture 표 · E-code ↔ UI code 매핑 | 완료 |
| 5 | RED 설계 자체 검수 체크리스트 6항 | 전부 통과 |
| 6 | Report 07 · Prompting Transcript 07 Export | 완료 |

**본 세션에서 수행하지 않음 (금지 준수)**

- `src/` · `tests/` 코드·스켈레톤 작성
- pytest 실행
- GREEN / REFACTOR 진입

---

## 3) 공개 계약 요약 (설계 전제)

| 항목 | 규칙 |
|------|------|
| 입력 | 4×4 `int[][]`; `0`=빈칸(정확히 2); 값 `0` 또는 `1..16`; non-zero 중복 금지 |
| 출력 | `int[6]` = `[r1,c1,n1,r2,c2,n2]`; 좌표 **1-index** |
| 마방진 상수 | M = **34** (`MagicConstant` SSOT) |
| Boundary 검증 순서 (short-circuit) | null → size → empty count → value range → duplicate |
| Boundary invalid | Failure envelope (Python 예외 아님) |
| invalid 시 Domain | `SolvePartialMagicSquare.execute` **0회** |
| Logic Track | **Domain Mock 금지** |

---

## 4) 격자 Fixture (G0~G3)

| ID | 용도 | 4×4 행렬 | 비고 |
|----|------|----------|------|
| **G0** | 완전 마방진 (`is_magic_square` true) | `[[16,3,2,13],[5,10,11,8],[9,6,7,12],[4,15,14,1]]` | D-VAL-01 |
| **G1** | Step A 성공; 빈칸 (2,2),(3,3); 누락 `{7,10}` | `[[16,3,2,13],[5,0,11,8],[9,6,0,12],[4,15,14,1]]` | 부록 placeholder; Then `[2,2,7,3,3,10]` |
| **G2** | Step A 실패 · Step B 성공 (PRD RD-02) | `[[16,0,3,13],[5,11,10,8],[9,7,6,12],[4,14,15,0]]` | D-SOL-02; 기대 `[1,2,2,4,4,1]` |
| **G3** | Step A·B 모두 실패 | `[[34,0,0,0],[0,0,0,34],[0,0,34,0],[0,34,0,0]]` | DT-X03 유형 placeholder |

**G1-RD01** (Boundary U-OUT Mock용): PRD §16.4 RD-01  
`[[16,0,3,13],[5,11,10,8],[9,7,6,12],[4,14,0,1]]`

---

## 5) Track A — Boundary / UI Contract RED

### 5.1 UI RED Tests

| Test ID | Layer | 테스트 이름 | Given | When | Then | Expected RED Failure | 실패 이유 | Boundary 계약 | Invariant/AC |
|---|---|---|---|---|---|---|---|---|---|
| U-IN-01 | Boundary | `test_u_in_01_null_matrix_returns_e003` | `matrix = null` | `InputValidator.validate(matrix)` | Failure; `code=="E003"`; message exact; 예외 없음 | `ModuleNotFoundError` / assertion fail | null short-circuit 미구현 | Failure envelope | AC-FR01-05; ①null |
| U-IN-02a | Boundary | `test_u_in_02a_empty_list_returns_e001` | `matrix = []` | `InputValidator.validate(matrix)` | `code=="E001"`; `Grid must be 4x4.` | 동상 | size≠4×4 | AC-FR01-01 | BR-01; ②size |
| U-IN-02b | Boundary | `test_u_in_02b_ragged_4_rows_zero_cols` | `matrix = [[]]*4` | `InputValidator.validate(matrix)` | `code=="E001"`; message exact | 동상 | ragged 거부 없음 | AC-FR01-01 | BR-01 |
| U-IN-02c | Boundary | `test_u_in_02c_3x4_returns_e001` | 3×4 행렬 | `InputValidator.validate(matrix)` | `code=="E001"` | 동상 | 행≠4 | AC-FR01-01; TS-E01 | BR-01 |
| U-IN-02d | Boundary | `test_u_in_02d_4x3_returns_e001` | 4×3 행렬 | `InputValidator.validate(matrix)` | `code=="E001"` | 동상 | 열≠4 | AC-FR01-01 | BR-01 |
| U-IN-02e | Boundary | `test_u_in_02e_5x5_returns_e001` | 5×5 행렬 | `InputValidator.validate(matrix)` | `code=="E001"` | 동상 | 5×5 허용 | AC-FR01-01 | BR-01 |
| U-IN-03a | Boundary | `test_u_in_03a_zero_blanks_returns_e002` | RD-04 (빈칸 1개) | `InputValidator.validate(matrix)` | `code=="E002"`; empty message exact | assertion fail | 빈칸≠2 | AC-FR01-02 | BR-02; ③empty |
| U-IN-03b | Boundary | `test_u_in_03b_three_blanks_returns_e002` | `0` 3개 격자 | `InputValidator.validate(matrix)` | `code=="E002"` | 동상 | 3빈칸 허용 | AC-FR01-02 | BR-02 |
| U-IN-04a | Boundary | `test_u_in_04a_minus_one_returns_e004` | 셀 `-1` | `InputValidator.validate(matrix)` | `code=="E004"`; range message exact | 동상 | 범위 미검출 | AC-FR01-03 | BR-03; ④range |
| U-IN-04b | Boundary | `test_u_in_04b_seventeen_returns_e004` | RD-06 (`17`) | `InputValidator.validate(matrix)` | `code=="E004"` | 동상 | 17 허용 | AC-FR01-03 | BR-03 |
| U-IN-05 | Boundary | `test_u_in_05_duplicate_nonzero_returns_e005` | RD-05 (16 중복) | `InputValidator.validate(matrix)` | `code=="E005"`; duplicate message exact | 동상 | 중복 미검출 | AC-FR01-04 | BR-04; ⑤dup |
| U-OUT-01 | Boundary | `test_u_out_01_success_payload_length_six` | G1-RD01; Mock `int[6]` | `UIBoundary.solve(matrix)` | success; `len==6` | assertion fail | 길이 계약 | AC-FR05-04; RG-01 | D-OUT-01 |
| U-OUT-02 | Boundary | `test_u_out_02_success_coordinates_one_indexed` | G1-RD01; Mock | `UIBoundary.solve(matrix)` | r,c ∈ [1,4] | assertion fail | 1-index | AC-FR05-04; TS-B04 | D-OUT-01 |
| U-FLOW-02 | Boundary | `test_u_flow_02_invalid_skips_execute` | invalid 6종 | `UIBoundary.solve`; execute spy | Failure; `call_count==0` | execute called | Domain 0회 | AC-FR01-05 | U-FLOW-02 |

### 5.2 E-code ↔ Report 02 매핑

| E-code | Report 02 `code` | 고정 message (Report 02 §2.4) |
|--------|------------------|------------------------------|
| E003 | *(SSOT 신규)* | `ERROR_MESSAGES["E003"]` 확정 필요 |
| E001 | `UI_INVALID_SIZE` | `Grid must be 4x4.` |
| E002 | `UI_INVALID_EMPTY_COUNT` | `Grid must contain exactly 2 empty cells (0).` |
| E004 | `UI_INVALID_VALUE_RANGE` | `Cell values must be 0 or between 1 and 16.` |
| E005 | `UI_DUPLICATE_VALUE` | `Non-zero values must not duplicate.` |

---

## 6) Track B — Domain / Logic RED

### 6.1 Logic RED Tests

| Test ID | Layer | 테스트 이름 | Given | When | Then | Expected RED Failure | Logic Invariant | 필요성 |
|---|---|---|---|---|---|---|---|---|
| D-LOC-01 | Entity | `test_d_loc_01_g1_row_major_blanks` | G1 | `find_blank_coords(G1)` | (2,2),(3,3) 1-index; Mock 없음 | NotImplemented / assert fail | I6; D-ORDER-01 | row-major 빈칸 고정 |
| D-MIS-01 | Entity | `test_d_mis_01_g1_missing_sorted` | G1 | `find_not_exist_nums(G1)` | `{7,10}` 오름차순; Mock 없음 | 동상 | I7,I11; D-SOLVE-01 | 누락 수·정렬 |
| D-VAL-01 | Entity | `test_d_val_01_g0_complete_magic_true` | G0 | `is_magic_square(G0)` | `true`; Mock 없음 | `False` | I1~I5; D-MAGIC-01 | 완성 판정 기준 |
| D-VAL-02 | Entity | `test_d_val_02_row_sum_mismatch` | G0-ROW | `is_magic_square` | `false` | `True` | I1 | 행 합 분리 |
| D-VAL-03 | Entity | `test_d_val_03_col_sum_mismatch` | G0-COL | `is_magic_square` | `false` | `True` | I2 | 열 합 분리 |
| D-VAL-04 | Entity | `test_d_val_04_diagonal_mismatch` | G0-DIAG | `is_magic_square` | `false` | `True` | I3 | 대각 분리 |
| D-VAL-05 | Entity | `test_d_val_05_duplicate_false` | G0-DUP | `is_magic_square` | `false` | `True` | I4 | 유일성 |
| D-VAL-06 | Entity | `test_d_val_06_zero_in_filled_false` | G0-ZERO | `is_magic_square` | `false` | `True` | I4,I5 | 완성에 0 금지 |
| D-SOL-01 | Control | `test_d_sol_01_g1_step_a_success` | G1 | `solution(G1)` | `[2,2,7,3,3,10]`; Mock 없음 | wrong vector | I8; D-SOLVE-02 | Step A 성공 |
| D-SOL-02 | Control | `test_d_sol_02_g2_step_b_reverse` | G2 | `solution(G2)` | `[1,2,2,4,4,1]`; Mock 없음 | wrong order | I9; D-SOLVE-03 | Step B 성공 |
| D-SOL-03 | Control | `test_d_sol_03_g3_unsolvable` | G3 | `solution(G3)` | `UnsolvableDomainError`; Mock 없음 | returns list | I10; D-SOLVE-04 | 해 없음 |
| D-SOL-04 | Control | `test_d_sol_04_output_contract` | G1 | `solution(G1)` | len 6; coords 1-index; Mock 없음 | 0-index | I8,I9; D-OUT-01 | 출력 계약 |

### 6.2 I6~I11 별칭 (설계용)

| ID | 대응 불변/규칙 |
|----|----------------|
| I6 | D-ORDER-01 (row-major 빈칸) |
| I7, I11 | D-SOLVE-01 (누락 2수·정렬) |
| I8 | D-SOLVE-02 (Step A) |
| I9 | D-SOLVE-03 (Step B) |
| I10 | D-SOLVE-04 (해 없음) |

### 6.3 Report 02 Test-ID 매핑

| 설계 ID | Report 02 |
|---------|-----------|
| U-IN-* | UT-E01~E05 |
| U-OUT-* | UT-F01, UT-F02 |
| U-FLOW-02 | AC-FR01-05 / UT-E01-g |
| D-LOC-01 | DT-N03 |
| D-MIS-01 | DT-N04 |
| D-VAL-01 | DT-N05 |
| D-SOL-01/02 | DT-N01, DT-N02 |
| D-SOL-03 | DT-E07 |

---

## 7) 주요 결정사항

| ID | 결정 | 근거 |
|----|------|------|
| D-07-01 | RED 산출물 = **설계표 텍스트만** | 사용자 금지: 코드·pytest·GREEN |
| D-07-02 | Boundary Test-ID = `U-IN` / `U-OUT` / `U-FLOW` | 슬라이스별 U-* vs UT-* 병행 추적 |
| D-07-03 | Logic Test-ID = `D-LOC` / `D-MIS` / `D-VAL` / `D-SOL` | 함수 별칭 단위 분리 RED |
| D-07-04 | `E003` null은 size와 **별도 코드** | short-circuit 1순위; message는 ERROR_MESSAGES SSOT |
| D-07-05 | G1/G3 일부 **placeholder** | Report 02 부록 G0~G3 미기재; Then-clause로 fixture 고정 |
| D-07-06 | Report 06(UT-E01 구현 RED)와 **범위 분리** | 본 문서는 FR-01~05 전체 설계; 구현 슬라이스는 순차 착수 |

---

## 8) RED 설계 자체 검수

- [x] Boundary는 E00x Failure schema (generic Exception 아님)
- [x] invalid → execute 0회 (`U-FLOW-02`)
- [x] U-IN vs U-OUT 분리
- [x] Logic Track Domain Mock 없음
- [x] I1~I11 · AC-FR* 추적 가능
- [x] 코드/스켈레톤/구현 미작성

---

## 9) 미완료 · 다음 단계

### 9.1 설계 확정 필요

- [ ] `ERROR_MESSAGES["E003"]` 문구 SSOT 확정
- [ ] G1/G3 행렬 부록 확정 (현재 placeholder)
- [ ] `E00x` vs `UI_*` 코드명 GREEN 전 정렬 (Report 06 DEF-003 연계)

### 9.2 RED 구현 순서 (권장)

1. Report 02 §1.5.4: `DT-E01~E06` → `DT-N05` → `DT-N03,N04` → `DT-N01,N02` → `DT-E07`
2. Boundary: `U-IN-01`~`05` → `U-FLOW-02` → `U-OUT-01,02` (Domain Mock)
3. 슬라이스당: RED(tests/) → GREEN(src/) → REFACTOR → develop

### 9.3 Report 06 연계

- [ ] `tests/boundary/test_validate_size.py` (UT-E01) ↔ `U-IN-02*` 매핑 검토
- [ ] `src/boundary/` GREEN (DEF-001) 후 U-IN 전체 RED 착수

---

## 10) 참고 문서

- [docs/PRD_MagicSquare.md](../docs/PRD_MagicSquare.md) — FR-01~05, §12~13, §16.4 RD-01~06
- [Report/02_Magic-Square-Dual-Track-TDD-Design.md](./02_Magic-Square-Dual-Track-TDD-Design.md)
- [Report/06_Magic-Square-Dual-Track-TDD-RED-Session-Report.md](./06_Magic-Square-Dual-Track-TDD-RED-Session-Report.md)
- [docs/test_plan.md](../docs/test_plan.md)
- [defect_list.md](../defect_list.md)

---

## 문서 이력

| 버전 | 날짜 | 변경 |
|------|------|------|
| 1.0 | 2026-05-29 | FR-01~05 Dual-Track RED 설계표 Report 최초 작성 |

---

*본 문서는 TDD RED 설계 산출물이며, 구현 명세서·테스트 코드가 아닙니다.*
