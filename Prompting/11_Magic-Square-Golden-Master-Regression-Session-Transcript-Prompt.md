# Magic Square 4×4 — Prompt & Transcript (11 · Golden Master 회귀)

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_ |
| 짝 | [Report/11_Magic-Square-Golden-Master-Regression-Session-Report.md](../Report/11_Magic-Square-Golden-Master-Regression-Session-Report.md) |
| Export | 2026-05-29 (KST) |
| TDD phase | **GREEN 후 · REFACTOR 전** (Golden Master) |
| 형식 | **User** / **Cursor** 대화 Transcript + 프롬프트 요약 |
| Agent | Auto (Cursor) |
| 브랜치 | `stabilize/green` |
| 선행 | [10_Magic-Square-Dual-Track-MVP-and-Screen-GUI-Session-Report.md](../Report/10_Magic-Square-Dual-Track-MVP-and-Screen-GUI-Session-Report.md) |

---

## 목차

1. [대화 Transcript (이번 세션)](#대화-transcript-이번-세션)
2. [실행 프롬프트 요약](#실행-프롬프트-요약)
3. [산출물 목록](#산출물-목록)
4. [시도한 명령과 결과](#시도한-명령과-결과)

---

# 대화 Transcript (이번 세션)

## T1 — GM-1 기준 파일 생성

**User:**

- 🔲 GM-1 기준 파일 생성 — Magic Square
- 역할: 회귀 테스트(Approval/Golden Master) 설계 전문가
- Magic Square Solver **실제 출력** 기반 Golden Master 기준 파일 생성 · 버전 관리
- 시나리오: 정상 / reverse / invalid blank / duplicate / no valid solution
- stdout 또는 Result DTO serialize · approve 패턴 (없으면 생성 · 있으면 diff)
- baseline 형식: `[section]` + Input/Output 또는 Error
- 산출: `tests/golden_master_expected.txt` + 생성 스크립트 + approve 설계 문서

**Cursor (실행):**

1. `tests/golden_master/scenarios.py`, `approve.py` 작성
2. `scripts/generate_golden_master.py` — live `UIBoundary(execute=solution).solve`
3. `tests/golden_master_expected.txt` 생성 (5 sections)
4. `tests/test_gm_01_golden_master.py` (aggregate test)
5. `docs/golden_master_approve_design.md` 작성
6. `git add tests/golden_master_expected.txt` staging
7. `pytest tests/ -q` → **68 passed**

**초기 baseline 주의:** `normal_success` custom grid → 출력 `[3,3,6,4,4,1]` (Step B). 사용자 예시 `[3,3,1,4,4,6]`와 상이 — **실제 솔버 출력** 기준.

---

## T2 — GM-2 테스트 코드

**User:**

- 🔲 GM-2 테스트 코드 — Magic Square
- `@pytest.mark.golden_master` · `pytest -m golden_master -v`
- GM-TC-01~05 (정상 / reverse / INVALID_BLANK_COUNT / DUPLICATE / NO_VALID_MAGIC_SQUARE)
- 검증: int[6] · row-major · 1-index · small-first · reverse fallback · Error Contract
- 실패 시 `--- expected` / `+++ actual` unified diff
- 산출: `test_golden_master_magic_square.*` + baseline + 실행 예시

**Cursor (실행):**

1. `tests/golden_master/contracts.py` — contract assertion helpers
2. `tests/test_golden_master_magic_square.py` — 5 per-TC + 1 full baseline test
3. `approve_section()` — 섹션 단위 approve · separator 파싱 정정
4. **baseline 정정:** GM-TC-01 → PRD **RD-01** (`G1_RD01`), GM-TC-02 → **RD-02** (`G2`)
   - 이유: custom grid는 Step B 결과라 `assert_small_first_combination` FAIL
5. `pyproject.toml` · `tests/conftest.py` — `golden_master` marker 등록
6. `test_gm_01_golden_master.py` 삭제 → GM-2 모듈로 통합
7. `pytest -m golden_master -v` → **6 passed** · full **73 passed**

---

## T3 — GM-3 README 업데이트

**User:**

- `@docs/README.md`에 Golden Master 섹션 추가
- 위치: `"## RED 단계 To-Do 리스트"` 아래
- GM-01~10 체크리스트 (기준 파일 · 테스트 · 회귀 보호)

**Cursor (실행):**

1. `docs/README.md` **없음** — 루트 `README.md`의 `## TDD RED / GREEN To-Do (체크리스트)` 직후 삽입
2. Golden Master 회귀 안전장치 섹션 · GM-01~10 `[x]` · 명령 예시
3. pytest **67 → 73** · 문서 이력 GM 항목 추가

---

## T4 — pytest 파일명 실행 요청

**User:**

```text
pytest tests/test_gm_01_magic_square_golden_master.py -v
```

**Cursor (실행):**

- `tests/test_gm_01_magic_square_golden_master.py` → **file not found** (exit 4)
- 대체: `pytest tests/test_golden_master_magic_square.py -v` → **6 passed**
- 안내: GM-2에서 `test_golden_master_magic_square.py`로 통합됨

---

## T5 — Report · Prompting Export 요청

**User:**

> Report 폴더에 보고서 생성하고, Prompting 폴더에 Transcript도 Export 해줘

**Cursor (실행):**

- `Report/11_Magic-Square-Golden-Master-Regression-Session-Report.md` 생성
- `Prompting/11_Magic-Square-Golden-Master-Regression-Session-Transcript-Prompt.md` 생성 (본 문서)

---

# 실행 프롬프트 요약

```text
Phase: Post-GREEN · Pre-REFACTOR (Golden Master regression)

GM-1 — Baseline:
  Input scenarios: success (small-first), reverse, invalid blank, duplicate, no solution
  Capture: UIBoundary.solve → repr(list[int]) | ErrorResponse.code
  File: tests/golden_master_expected.txt
  Approve: missing → auto-create; present → string compare; mismatch → unified diff
  Script: scripts/generate_golden_master.py

GM-2 — Tests:
  Module: tests/test_golden_master_magic_square.py
  Marker: @pytest.mark.golden_master
  Run: pytest -m golden_master -v
  Cases: GM-TC-01~05 + full baseline aggregate
  Contracts: int[6], row-major, 1-index, small-first, reverse, Error

GM-3 — README:
  Section: Golden Master 회귀 안전장치 under TDD To-Do
  Checklist: GM-01~10

Grids (PRD §16.4):
  GM-TC-01: RD-01 G1_RD01 → [1,2,2,4,3,15]
  GM-TC-02: RD-02 G2       → [1,2,2,4,4,1]
  GM-TC-03: G0             → UI_INVALID_EMPTY_COUNT
  GM-TC-04: RD-05          → UI_DUPLICATE_VALUE
  GM-TC-05: G3             → DOMAIN_NO_SOLUTION
```

---

# 산출물 목록

| 유형 | 경로 |
|------|------|
| Report | `Report/11_Magic-Square-Golden-Master-Regression-Session-Report.md` |
| Transcript | `Prompting/11_Magic-Square-Golden-Master-Regression-Session-Transcript-Prompt.md` |
| Baseline | `tests/golden_master_expected.txt` |
| Script | `scripts/generate_golden_master.py` |
| Design | `docs/golden_master_approve_design.md` |
| Tests | `tests/test_golden_master_magic_square.py` |
| Helpers | `tests/golden_master/approve.py` |
| Helpers | `tests/golden_master/scenarios.py` |
| Helpers | `tests/golden_master/contracts.py` |
| Helpers | `tests/golden_master/__init__.py` |
| Config | `pyproject.toml` (marker), `tests/conftest.py` (marker) |
| Docs | `README.md` (Golden Master 섹션) |
| **삭제** | `tests/test_gm_01_golden_master.py` |
| **미생성** | `tests/test_gm_01_magic_square_golden_master.py` |
| **미생성** | `docs/README.md` |

---

# 시도한 명령과 결과

| 명령 | 결과 |
|------|------|
| `python scripts/generate_golden_master.py` | baseline written |
| `python -m pytest tests/test_gm_01_golden_master.py -v` | (GM-1) 1 passed → 이후 삭제 |
| `python -m pytest -m golden_master -v` | **6 passed** |
| `python -m pytest tests/test_golden_master_magic_square.py -v` | **6 passed** |
| `python -m pytest tests/ -q` | **73 passed** |
| `pytest tests/test_gm_01_magic_square_golden_master.py -v` | **ERROR** file not found |
| `git branch --show-current` | `stabilize/green` |

---

## Golden Master 검수 체크list

- [x] GM-01 baseline 파일 생성
- [x] GM-02 5 시나리오 + RD-01/RD-02 정정
- [x] GM-03 git add baseline (staging)
- [x] GM-04 `test_golden_master_magic_square.py`
- [x] GM-05 approve 패턴 (section + full file)
- [x] GM-06 `pytest -m golden_master` PASS
- [x] GM-07~10 contract helpers
- [x] README GM 섹션
- [x] Report 11 / Prompting 11 Export
- [ ] baseline git commit (사용자 요청 시)
- [ ] `test_gm_01_magic_square_golden_master.py` alias (선택)

---

*Export 완료 — Report 11 / Prompting 11*
