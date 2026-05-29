# Magic Square 4×4 — Dual-Track TDD RED Skeleton Session 보고서

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_ |
| 문서 버전 | 1.0 |
| 작성일 | 2026-05-29 (KST) |
| TDD phase | **RED (Skeleton)** — `tests/` 스켈레톤만; `src/` 미변경 |
| Agent | Auto (Cursor) |
| 브랜치 | `feature/dual-track-tdd` (로컬) |
| 선행 Report | [07_Magic-Square-Dual-Track-TDD-RED-Design-Report.md](./07_Magic-Square-Dual-Track-TDD-RED-Design-Report.md) |
| 짝 Transcript | [08_Magic-Square-Dual-Track-TDD-RED-Skeleton-Session-Transcript-Prompt.md](../Prompting/08_Magic-Square-Dual-Track-TDD-RED-Skeleton-Session-Transcript-Prompt.md) |
| SSOT | `docs/PRD_MagicSquare.md` v0.2, [02_Magic-Square-Dual-Track-TDD-Design.md](./02_Magic-Square-Dual-Track-TDD-Design.md), Report 07 §5–6, `.cursorrules` |
| 목적 | Report 07 설계표 중 **미착수 pytest** 항목에 대해 RED 스켈레톤 28건 작성·검증 |

---

## 1) 작업 목표

- **RED (Skeleton)** 규칙 준수: 테스트 구조·`pytest.fail()` 한 줄만; Then assert 금지
- Track A: `U-IN-04~08`, `U-OUT-01~03`, `U-FLOW-02`(6종 확장) 스켈레톤
- Track B: `D-LOC-01`, `D-MIS-01`, `D-VAL-01~06`, `D-SOL-01~04` 스켈레톤
- **제외:** `U-IN-01~03` (Report 06/08 AC-FR01-01 Full RED — `test_validate_size.py` 유지)
- G0~G3 fixture는 `conftest` **주석 placeholder**만
- `src/` 운영 코드·GREEN·REFACTOR **금지**

---

## 2) 수행한 작업

| 순서 | 작업 내용 | 결과 |
|------|-----------|------|
| 1 | Report 07 · PRD · `.cursorrules` RED Skeleton 규칙 대조 | 완료 |
| 2 | `tests/boundary/` Track A 스켈레톤 3파일 · 14테스트 | 완료 |
| 3 | `tests/entity/` Track B 스켈레톤 4파일 · 14테스트 | 완료 |
| 4 | `tests/conftest.py`, `tests/entity/conftest.py` G0~G3 placeholder | 완료 |
| 5 | `pytest` 실행 — ERROR/FAIL RED 확인 | 완료 |
| 6 | Report 08 · Prompting Transcript 08 Export | 완료 |

**본 세션에서 수행하지 않음 (금지 준수)**

- `src/` 추가·수정·stub
- GREEN / REFACTOR
- `test_validate_size.py` (Report 06 UT-E01) 수정
- skip / xfail / assert 완화

---

## 3) 생성·수정 파일

| 경로 | 변경 내용 |
|------|-----------|
| `tests/conftest.py` | G1-RD01 placeholder 주석 추가 |
| `tests/entity/conftest.py` | G0~G3 placeholder 주석 (신규) |
| `tests/boundary/test_u_in_04_08_input_validation.py` | U-IN-04~08 · 5 tests (신규) |
| `tests/boundary/test_u_out_01_03_output_contract.py` | U-OUT-01~03 · 3 tests (신규) |
| `tests/boundary/test_u_flow_02_invalid_skips_execute.py` | U-FLOW-02 a~f · 6 tests (신규) |
| `tests/entity/test_d_loc_01_blank_coords.py` | D-LOC-01 (신규) |
| `tests/entity/test_d_mis_01_missing_numbers.py` | D-MIS-01 (신규) |
| `tests/entity/test_d_val_01_06_magic_validation.py` | D-VAL-01~06 · 6 tests (신규) |
| `tests/entity/test_d_sol_01_04_solution.py` | D-SOL-01~04 · 4 tests (신규) |
| `Report/08_...` | 본 보고서 (신규) |
| `Prompting/08_...` | 세션 Transcript (신규) |

**미변경 (의도적)**

| 경로 | 사유 |
|------|------|
| `tests/boundary/test_validate_size.py` | Report 06 AC-FR01-01 Full RED 8건 assert 유지 |
| `src/**` | red_phase: tests only |

---

## 4) RED Skeleton 규칙 적용

| 규칙 | 적용 |
|------|------|
| 본문 | 각 테스트 `pytest.fail("RED: <Test-ID> — …")` 단일 실패 |
| AAA | Given/When/Then **주석만** |
| production import | 허용 (`InputValidator`, `find_blank_coords`, `solution` 등) |
| Boundary Mock | U-OUT/U-FLOW: `Mock`/`execute` spy **주석 표시** |
| Logic Mock | **금지** (D-* 전부) |
| D-SOL-02 | `pytest.fail("RED: D-SOL-02 — G2 TBD")` |

---

## 5) Test-ID ↔ Report 07 매핑

### Track A — Boundary

| Test ID | pytest 함수 | 파일 | Report 07 | 비고 |
|---------|-------------|------|-----------|------|
| U-IN-04 | `test_u_in_04_minus_one_returns_e004` | `test_u_in_04_08_*` | U-IN-04a | E004 |
| U-IN-05 | `test_u_in_05_seventeen_returns_e004` | 동상 | U-IN-04b | RD-06 |
| U-IN-06 | `test_u_in_06_duplicate_nonzero_returns_e005` | 동상 | U-IN-05 | RD-05 |
| U-IN-07 | `test_u_in_07_out_of_range_ninety_nine_returns_e004` | 동상 | — | UT-E04 확장 |
| U-IN-08 | `test_u_in_08_non_list_grid_returns_e001` | 동상 | — | PRD EX-05 확장 |
| U-OUT-01 | `test_u_out_01_success_payload_length_six` | `test_u_out_01_03_*` | U-OUT-01 | Mock 주석 |
| U-OUT-02 | `test_u_out_02_success_coordinates_one_indexed` | 동상 | U-OUT-02 | |
| U-OUT-03 | `test_u_out_03_success_fill_values_in_range` | 동상 | — | TS-B01/B02 확장 |
| U-FLOW-02 | `test_u_flow_02_*` (6건) | `test_u_flow_02_*` | U-FLOW-02 | invalid 6종 |

### Track B — Entity / Control

| Test ID | pytest 함수 | 파일 | Report 07 | Report 02 |
|---------|-------------|------|-----------|-----------|
| D-LOC-01 | `test_d_loc_01_g1_row_major_blanks` | `test_d_loc_01_*` | D-LOC-01 | DT-N03 |
| D-MIS-01 | `test_d_mis_01_g1_missing_sorted` | `test_d_mis_01_*` | D-MIS-01 | DT-N04 |
| D-VAL-01~06 | `test_d_val_01` … `06` | `test_d_val_01_06_*` | D-VAL-01~06 | DT-N05 |
| D-SOL-01 | `test_d_sol_01_g1_step_a_success` | `test_d_sol_01_04_*` | D-SOL-01 | DT-N01 |
| D-SOL-02 | `test_d_sol_02_g2_step_b_reverse` | 동상 | D-SOL-02 | DT-N02 (G2 TBD) |
| D-SOL-03 | `test_d_sol_03_g3_unsolvable` | 동상 | D-SOL-03 | DT-E07 |
| D-SOL-04 | `test_d_sol_04_output_contract` | 동상 | D-SOL-04 | D-OUT-01 |

---

## 6) pytest 현황

| 명령 | 결과 |
|------|------|
| `pytest tests/boundary/test_u_out_01_03_output_contract.py tests/boundary/test_u_flow_02_invalid_skips_execute.py -v` | **9 failed**, 0 passed — `pytest.fail` RED |
| `pytest tests/boundary/test_u_in_04_08_input_validation.py` | **ERROR (collect)** — `boundary.input_validator` 없음 |
| `pytest tests/entity/test_d_*.py` | **ERROR (collect)** — `entity.services`, `control` 없음 |
| `pytest tests/boundary/ tests/entity/ -v` | **6 errors** (collect) + `test_user.py` **8 passed** (슬라이스 외 Green) |
| `pytest tests/boundary/test_validate_size.py` | **ERROR (collect)** — `boundary.magic_square_boundary` 없음 (기존과 동일) |

**RED 판정:** MagicSquare 신규 28건은 전부 **FAIL** 또는 **collection ERROR** — GREEN 미진입 상태 유지.

---

## 7) 주요 결정사항

| ID | 결정 | 근거 |
|----|------|------|
| D-08-01 | 설계 SSOT = **Report 07** (사용자 프롬프트의 Report/09 미존재) | 저장소 내 최신 U-*/D-* 설계표 |
| D-08-02 | U-IN-04~08 = Report 07 `04a/04b/05` + PRD 확장 2건 | 사용자 범위 5건 충족 |
| D-08-03 | U-OUT-03 · U-FLOW-02 6분기 스켈레톤 추가 | 출력 계약·invalid 격리 확장 |
| D-08-04 | `ModuleNotFoundError` = RED 정상 (Report 06 D-05 동일) | production import 허용·미구현 |
| D-08-05 | `test_validate_size.py` **미수정** | Report 06 Full RED assert 보존 |

---

## 8) RED Skeleton 자체 검수

- [x] `src/` 변경 없음
- [x] Then assert 없음 (`pytest.fail`만)
- [x] skip / xfail / assert 완화 없음
- [x] U-IN-01~03 중복 스켈레톤 없음
- [x] Logic Track Domain Mock 없음
- [x] U-OUT/U-FLOW Mock은 주석만
- [x] D-SOL-02 G2 TBD 명시

---

## 9) 미완료 · 다음 단계

### 9.1 설계 확정 필요

- [ ] G1/G3/G0-ROW 등 variant fixture 부록 확정 (Report 07 §9.1)
- [ ] `ERROR_MESSAGES["E003"]` 문구 SSOT
- [ ] U-IN-07/08, U-OUT-03 Report 07 formal Test-ID 반영 여부

### 9.2 RED → GREEN 권장 순서 (Report 02 §1.5.4)

1. Report 06 `test_validate_size.py` GREEN — `src/boundary/` 최소
2. `U-IN-04~08` Full RED (assert) → GREEN — `InputValidator`
3. `D-VAL-01` → `D-LOC`/`D-MIS` → `D-SOL-*` Logic Track
4. `U-OUT`/`U-FLOW` Boundary (Domain Mock)
5. 슬라이스당 REFACTOR → `develop`

### 9.3 문서

- [ ] Report 09 (선택): Report 07 + 본 스켈레톤 통합 TestPlan Design (사용자 프롬프트 SSOT 명칭 정렬)

---

## 10) 참고 문서

- [docs/PRD_MagicSquare.md](../docs/PRD_MagicSquare.md)
- [Report/02_Magic-Square-Dual-Track-TDD-Design.md](./02_Magic-Square-Dual-Track-TDD-Design.md)
- [Report/06_Magic-Square-Dual-Track-TDD-RED-Session-Report.md](./06_Magic-Square-Dual-Track-TDD-RED-Session-Report.md)
- [Report/07_Magic-Square-Dual-Track-TDD-RED-Design-Report.md](./07_Magic-Square-Dual-Track-TDD-RED-Design-Report.md)
- [defect_list.md](../defect_list.md)

---

## 문서 이력

| 버전 | 날짜 | 변경 |
|------|------|------|
| 1.0 | 2026-05-29 | RED Skeleton Session Report 최초 작성 |

---

*본 문서는 TDD RED(Skeleton) 세션 산출물이며, GREEN 구현 명세가 아닙니다.*
