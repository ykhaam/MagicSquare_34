# Magic Square 4×4 — Prompt & Transcript (12 · REFACTOR Planning)

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_ |
| 짝 | [Report/12_Magic-Square-REFACTOR-Planning-Session-Report.md](../Report/12_Magic-Square-REFACTOR-Planning-Session-Report.md) |
| Export | 2026-05-29 (KST) |
| TDD phase | **REFACTOR (계획)** — 코드 미변경 |
| 형식 | **User** / **Cursor** 대화 Transcript + 프롬프트 요약 |
| Agent | Auto (Cursor) · code-reviewer |
| 브랜치 | `refactor/refactor` |
| 선행 | [11_Magic-Square-Golden-Master-Regression-Session-Transcript-Prompt.md](./11_Magic-Square-Golden-Master-Regression-Session-Transcript-Prompt.md) |

---

## 목차

1. [대화 Transcript (이번 세션)](#대화-transcript-이번-세션)
2. [실행 프롬프트 요약](#실행-프롬프트-요약)
3. [산출물 목록](#산출물-목록)
4. [시도한 명령과 결과](#시도한-명령과-결과)

---

# 대화 Transcript (이번 세션)

## T1 — 리팩토링 대상 테스트 갭 (REFACTOR phase)

**User:**

- 대상: `solve_partial_magic_square.py`, `ui_boundary.py`, `main_window.py` (ECB 매핑)
- 질문: (1) 대응 test_*.py 유무 (2) RED 스켈레톤 중 GREEN 선행 대상 (3) 테스트 없이 refactor 금지 이유 1줄
- 기준: REFACTOR phase `.cursorrules`

**Cursor (분석):**

- 실파일: `puzzle_solver.py`, `ui_boundary.py`, `window.py` — 목표명 파일 미존재
- `pytest.fail("RED:…")` 스켈레톤 **0건** — Report 08 → GREEN 완료, **73 passed**
- 테스트 매핑:
  - Control: `test_d_sol_01_04_solution.py`, IT, Golden Master
  - Boundary: `test_u_out_*`, `test_u_flow_*`, `test_validate_size.py` (UIBoundary 간접)
  - Screen: **테스트 없음** (0% cov)
- RED 선행: Screen UT-GUI, UT-F01/F02, `two_cell_solver` 추출 전 D-SOL
- 1줄: REFACTOR는 full pytest Green + 계약 불변 전제

---

## T2 — 코드 스멜 점검 (High 우선)

**User:**

- 동일 3파일 + `input_validator`, `two_cell_solver` (결합 참고만)
- 항목: 다중 역할 함수, 클래스 혼재, UI 비즈니스 판단
- 출력: 표, 위반만 `파일:줄번호`

**Cursor (산출):**

- `solution` / `_try_placement`: 오케스트레이션 + Domain 혼재
- `window`: Control import, `UI_INTERNAL` 249행, `_init_ui` 75줄+
- `ui_boundary`: 해당 없음 (re-export)
- UI 비즈니스: **249행만** (E00x 결정); payload 표시는 제외

---

## T3 — ECB 역할 · 이동 · Control vs Entity

**User:**

- `.cursorrules` ECB 기준: Boundary/Control/Entity/Screen 책임
- (1) 역할 현황 표 (2) 이동 대상 표 (3) Control vs Entity 혼재 (4) REFACTOR 1순위 1줄
- P0/P1 + Step1 테스트갭 · Step2 High 연계

**Cursor (산출):**

- `solve_partial` = **Control**; 알고리즘 → Entity `two_cell_solver`
- `ui_boundary` = Boundary **부분** (SSOT 분산)
- `main_window` = Screen **부분** (Control 직접 호출)
- P0: Boundary envelope + Screen UIBoundary + two_cell_solver 추출
- P1: validator SSOT, rename, layout extract

---

## T4 — SRP 위반 표 (함수·클래스·UI)

**User:**

- 동일 ECB 매핑, SRP 항목 3종 표
- `ui_boundary` / `solve_partial` / `main_window` 위반·해당 없음 명시

**Cursor:**

- §① 함수 다중 역할 6건 + ui_boundary 해당 없음
- §② 클래스 데이터+검증 혼재 해당 없음; `MagicSquareWindow` 복수 책임 별도 표기
- §③ UI 비즈니스: `window:249` only

---

## T5 — `/code-reviewer` 전체 리뷰

**User:**

- `@c:\dev\MagicSquare_\` code-reviewer 서브에이전트 리뷰

**Cursor (code-reviewer + 검증):**

- **73 passed**, cov **~67%**, Screen **0%**
- Critical 6건: Control SRP, Screen wiring, E006 gap, UT-F01/F02, DEF-003, UI_INTERNAL
- High: validator duplication, ui_boundary split, test_d_sol_01 doc drift
- P0/P1 refactor order, test gap 표
- 사용자에게 요약 전달 (패치 없음)

---

## T6 — 리팩토링 계획서

**User:**

- 앞선 분석 기반 계획서 (코드 수정 X)
- 형식: 대상 목록 표, 테스트 선행, 검증 방법

**Cursor (산출):**

- 순번 1~15 대상 표 (P0~P2)
- 테스트 선행: UT-F01/F02, UT-E07, UT-GUI-01~04, two_cell_solver, DEF-003
- 회귀: `pytest tests/`, `-m golden_master`, cov 80%
- 슬라이스 순서 P0-1 ~ P0-5

---

## T7 — Report · Transcript Export · commit

**User:**

- Report 폴더 보고서 생성
- Prompting Transcript Export
- commit

**Cursor (실행):**

- `Report/12_Magic-Square-REFACTOR-Planning-Session-Report.md`
- `Prompting/12_Magic-Square-REFACTOR-Planning-Session-Transcript-Prompt.md`
- git commit

---

# 실행 프롬프트 요약

| ID | 요약 | Phase |
|----|------|-------|
| T1 | REFACTOR 대상 3파일 테스트 갭·RED 스켈레톤 | 계획 |
| T2 | 코드 스멜 (High) | 계획 |
| T3 | ECB 역할·이동·P0/P1 | 계획 |
| T4 | SRP 위반 표 | 계획 |
| T5 | code-reviewer 전체 리뷰 | 계획 |
| T6 | 리팩토링 계획서 | 계획 |
| T7 | Report 12 · Prompting 12 · commit | 문서화 |

**공통 제약:** `src/`·`tests/` **코드 변경 없음** (T1~T6). Golden Master·73 Green 유지 전제.

---

# 산출물 목록

| 경로 | 설명 |
|------|------|
| `Report/12_Magic-Square-REFACTOR-Planning-Session-Report.md` | REFACTOR 계획 종합 보고서 |
| `Prompting/12_Magic-Square-REFACTOR-Planning-Session-Transcript-Prompt.md` | 본 Transcript |

**참고 (기존, 변경 없음):**

| 경로 | 역할 |
|------|------|
| `src/control/puzzle_solver.py` | Control (rename·extract 대상) |
| `src/boundary/ui_boundary.py` | Boundary re-export |
| `src/boundary/screen/window.py` | Screen (rename·UIBoundary 대상) |
| `tests/test_golden_master_magic_square.py` | 회귀 안전망 |

---

# 시도한 명령과 결과

| 명령 | 결과 |
|------|------|
| `python -m pytest tests/ -q` | **73 passed** |
| `git branch --show-current` | `refactor/refactor` |
| code-reviewer (Task) | Critical/High/P0/P1 표 산출 |
| `grep pytest.fail` | Golden Master approve 2건만 (RED 스켈레톤 0) |

---

## 문서 이력

| 버전 | 날짜 | 변경 |
|------|------|------|
| 1.0 | 2026-05-29 | REFACTOR Planning 세션 Transcript Export |

---

*본 문서는 User–Cursor 대화 요약이며, 구현 슬라이스는 Report 12 §9 순서를 따릅니다.*
