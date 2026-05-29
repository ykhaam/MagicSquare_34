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
| **03** | `.cursorrules` YAML · ECB `User` · TDD 구현 | [03](./Report/03_Magic-Square-Cursorrules-and-Phase03-Kickoff-Report.md) | [03](./Prompting/03_Magic-Square-Phase03-Cursorrules-Prompt.md) | ✅ |
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
  → stabilize/red       ← RED 단계 시 생성 (tests/ only)
    → stabilize/green   ← GREEN 단계 (**현재 로컬에 존재**)
      → stabilize/refactoring  ← REFACTOR 단계 시 생성
        → develop
```

| 브랜치 | 용도 | 변경 허용 | 로컬 |
|--------|------|-----------|------|
| `main` | 문서·동작 스냅샷 | 문서·릴리스 | ✅ |
| `develop` | TDD 통합 | merge from `stabilize/refactoring` | ✅ |
| `spec` | 설계·PRD·규칙 | `Report/`, `docs/`, `.cursor/` | ✅ |
| `feature/dual-track-tdd` | Dual-Track RED 묶음 (레거시) | — | ✅ |
| **`stabilize/green`** | **GREEN 슬라이스** | **`src/`만** | ✅ **작업 중** |
| `stabilize/red` | RED 슬라이스 | `tests/`만 | ⏳ **필요 시 생성** (`git checkout -b stabilize/red develop`) |
| `stabilize/refactoring` | REFACTOR 슬라이스 | 구조·이름 (계약 동일) | ⏳ **필요 시 생성** |

TDD 사이클: `spec → stabilize/red → stabilize/green → stabilize/refactoring → develop` (**동시 3분기 금지**)

| 단계 | 커밋 단위 | 브랜치 | 이번 작업 |
|------|-----------|--------|-----------|
| **RED** | 테스트 **3건** = 1 커밋 | `stabilize/red` (생성 후) | `tests/`만 |
| **GREEN** | **RED 1묶음** = 1 커밋 | **`stabilize/green`** | `src/`만 · 해당 묶음 전건 PASS |
| **REFACTOR** | 슬라이스별 | `stabilize/refactoring` (생성 후) | **이번 커밋 범위 밖** |

```bash
# RED 시작할 때만 (아직 브랜치 없으면)
git checkout develop
git checkout -b stabilize/red

# GREEN (현재 작업 브랜치)
git checkout stabilize/green
python -m pytest <node1> <node2> <node3> -v   # FAIL → src/ 최소 수정 → PASS
git add src/ && git commit -m "feat(boundary): GREEN-A1 …"
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
│   ├── boundary/             # InputValidator, UIBoundary, screen (Track A)
│   ├── control/              # puzzle_solver.solution
│   ├── data/                 # InMemoryMatrixRepository
│   └── entity/               # MagicGrid, services (Track B)
├── tests/
│   ├── boundary/             # UT-* · AC-FR-* (Mock 허용)
│   ├── entity/               # DT-* · D-* (Mock 금지)
│   ├── data/                 # DATA-T*
│   └── integration/          # IT-*
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
| **AC-FR-01-01 ~ U-OUT** | Boundary Track A 전 슬라이스 | ✅ GREEN (`stabilize/green`) |
| **DT-E01 ~ D-SOL** | Entity/Control Track B 전 슬라이스 | ✅ GREEN |
| **DATA-T01 ~ T05** | InMemory 저장소 | ✅ |
| **IT-N01 ~ IT-E04** | 통합 (Boundary→Control→Entity) | ✅ |
| **PyQt6 GUI** | `python -m boundary.screen` · `magicsquare-gui` | ✅ (optional `[gui]`) |
| **`stabilize/refactoring`** | 구조 정리 · 커버리지 80%+ | ⏳ 선택 |
| `develop` / `main` merge | MVP 마일스톤 | ⏳ |

상세 세션: [Report 09](./Report/09_Magic-Square-AC-FR-01-01-Boundary-GREEN-Session-Report.md) (AC-FR-01-01) · [Report 10](./Report/10_Magic-Square-Dual-Track-MVP-and-Screen-GUI-Session-Report.md) (MVP · GUI)

---

## 다음 단계

1. **`stabilize/refactoring`:** 중복 제거·커버리지 80%+ 측정 후 `develop` merge
2. **File JSON `MatrixRepository`** (Report 02 옵션 B) — `IT-E03` / `DATA-T03`
3. 계약 충돌 시 Report **02 우선** · AI 규칙은 **04 + `.mdc`**

### GUI 실행 (PyQt6)

```bash
python -m venv .venv
.\.venv\Scripts\pip install -e ".[gui]"
.\.venv\Scripts\python -m boundary.screen
# 또는: magicsquare-gui
```

---

## TDD RED / GREEN To-Do (체크리스트)

> **RED:** `stabilize/red` · **`tests/`만** · **3 test = 1 커밋**  
> **GREEN:** `stabilize/green` · **`src/`만** · **RED 1묶음 = 1 커밋** (묶음 내 node id **전부 PASS**)  
> **REFACTOR:** `stabilize/refactoring` · **이번 커밋/슬라이스에서 하지 않음**  
> **Track A/B 동시 RED·GREEN 금지**  
> SSOT: [Report 02 §1.5.4](./Report/02_Magic-Square-Dual-Track-TDD-Design.md#154-red-작성-순서-권장) · [docs/test_plan.md](./docs/test_plan.md)

### Golden Master 회귀 안전장치

> **Refactoring 시작 전 구축** · **GREEN 완료 후 즉시 적용**  
> 설계: [docs/golden_master_approve_design.md](./docs/golden_master_approve_design.md)

**기준 파일 생성**

- [x] **GM-01:** `tests/golden_master_expected.txt` 생성 (`scripts/generate_golden_master.py`)
- [x] **GM-02:** 정상 / 역순 / 오류 시나리오 추가 (GM-TC-01~05)
- [x] **GM-03:** `git add tests/golden_master_expected.txt` (버전 관리)

**테스트 코드**

- [x] **GM-04:** `tests/test_golden_master_magic_square.py` 작성
- [x] **GM-05:** approve 패턴 적용 (`tests/golden_master/approve.py`)
- [x] **GM-06:** Golden Master 테스트 PASS 확인 (`pytest -m golden_master -v`)

**회귀 보호**

- [x] **GM-07:** row-major 규칙 보호 (`assert_row_major_blank_order`)
- [x] **GM-08:** 1-index 출력 보호 (`assert_one_index_coordinates`)
- [x] **GM-09:** reverse 조합 fallback 보호 (`assert_reverse_fallback_combination`)
- [x] **GM-10:** Error Contract 보호 (`assert_error_contract`)

```bash
python scripts/generate_golden_master.py
python -m pytest -m golden_master -v
```

---

### 매 슬라이스 (1 RED 묶음 → 1 GREEN 커밋)

| # | RED (`stabilize/red`) | GREEN (`stabilize/green`) |
|---|----------------------|---------------------------|
| 1 | 묶음 내 3건 `pytest` → **전부 FAIL** · `tests/` 커밋 1건 | `git checkout stabilize/green` |
| 2 | — | 동일 3건 `pytest` → **전부 FAIL** 확인 (이미 PASS면 `src/` 수정 금지) |
| 3 | — | `src/` 최소 수정 · Boundary는 `FailureResponse`/`ErrorResponse` (throw 금지) |
| 4 | — | 동일 3건 **전부 PASS** · `src/` 커밋 1건 · **REFACTOR·설계 개선 금지** |

---

### Track A — Boundary (Mock 허용)

**RED / GREEN 동일 ID** — 한 행 = RED 1커밋 + GREEN 1커밋

| ID | RED (`stabilize/red` · 3건) | GREEN (`stabilize/green` · 묶음 전건 PASS) | 상태 |
|----|-------------------|----------------------------------|------|
| **A0-1** | `test_none_grid_returns_failure_with_invalid_size_code` · `[empty_list]` · `[four_empty_rows]` | `test_ac_fr_01_01_input_validation.py` 위 3 node | ✅ |
| **A0-2** | `[size_3x4]` · `test_none_grid_message_matches_prd_section_8_1_exactly` · `test_none_grid_returns_exact_invalid_size_code_string` | 동일 파일 위 3 node | ✅ |
| **A0-3** | `test_none_grid_returns_pydantic_failure_response_type` · scope 2건 | 동일 파일 위 3 node | ✅ |
| **A1** | `test_validate_size.py` — none · empty · ragged | **GREEN-A1** — 위 3 node 동시 PASS | ✅ |
| **A2** | 3×4 · resolve 0회 · message exact | **GREEN-A2** | ✅ |
| **A3** | ErrorResponse type · scope (2건) | **GREEN-A3** | ✅ |
| **A4** | U-IN-04 · 05 · 06 | **GREEN-A4** | ✅ |
| **A5** | U-IN-07 · 08 (2건) | **GREEN-A5** | ✅ |
| **A6** | U-FLOW null · size · empty count | **GREEN-A6** | ✅ |
| **A7** | U-FLOW range · duplicate · ragged | **GREEN-A7** | ✅ |
| **A8** | U-OUT-01 · 02 · 03 | **GREEN-A8** | ✅ |

**pytest 예 (GREEN-A1):**

```bash
python -m pytest \
  tests/boundary/test_validate_size.py::TestAcFr0101InvalidSize::test_none_grid_returns_invalid_size_failure \
  tests/boundary/test_validate_size.py::TestAcFr0101InvalidSize::test_empty_list_returns_invalid_size_failure \
  tests/boundary/test_validate_size.py::TestAcFr0101InvalidSize::test_ragged_four_rows_returns_invalid_size_failure \
  -v
```

**체크리스트**

- [x] **RED-A0-1** + **GREEN-A0-1**
- [x] **RED-A0-2** + **GREEN-A0-2**
- [x] **RED-A0-3** + **GREEN-A0-3**
- [x] **RED-A1** + **GREEN-A1**
- [x] **RED-A2** + **GREEN-A2**
- [x] **RED-A3** + **GREEN-A3**
- [x] **RED-A4** + **GREEN-A4**
- [x] **RED-A5** + **GREEN-A5**
- [x] **RED-A6** + **GREEN-A6**
- [x] **RED-A7** + **GREEN-A7**
- [x] **RED-A8** + **GREEN-A8**

| Track A | RED+GREEN 묶음 | 남은 GREEN 커밋 |
|---------|----------------|-----------------|
| AC-FR-01-01 ~ U-OUT | A0-1~A8 ✅ | — |

---

### Track B — Entity/Control (Mock 금지) · Report 02 §1.5.4

**RED / GREEN 동일 ID** — 한 행 = RED 1커밋 + GREEN 1커밋

| ID | RED (`stabilize/red`) | GREEN (`stabilize/green` · 묶음 전건 PASS) | 상태 |
|----|-------------|----------------------------------|------|
| **B1** | DT-E01 · E02 · E03 (`test_magic_grid.py`) | **GREEN-B1** | ✅ |
| **B2** | DT-E04 · E05 · E06 | **GREEN-B2** | ✅ |
| **B3** | D-VAL-01 · 02 · 03 | **GREEN-B3** | ✅ |
| **B4** | D-VAL-04 · 05 · 06 | **GREEN-B4** | ✅ |
| **B5** | D-LOC-01 · D-MIS-01 · D-SOL-01 | **GREEN-B5** | ✅ |
| **B6** | D-SOL-02 · 03 · 04 | **GREEN-B6** | ✅ |

- [x] **RED-B1** + **GREEN-B1**
- [x] **RED-B2** + **GREEN-B2**
- [x] **RED-B3** + **GREEN-B3**
- [x] **RED-B4** + **GREEN-B4**
- [x] **RED-B5** + **GREEN-B5**
- [x] **RED-B6** + **GREEN-B6**

| Track B | RED+GREEN 묶음 | 남은 GREEN 커밋 |
|---------|----------------|-----------------|
| DT-E ~ D-SOL | B1~B6 ✅ | — |

> **제외:** `tests/entity/test_user.py` — 학습용 `User` (마방진 백로그 밖)

---

### 커버리지 목표 (REFACTOR / develop merge 시)

- [ ] Entity Logic: 95%+ branch (`pytest --cov=src/entity`)
- [ ] Boundary: 85%+ branch (`pytest --cov=src/boundary`)
- [ ] 전체: 80%+ (Report 02 §4.4)

현재: `python -m pytest tests/ -q` → **73 passed**
---

## 범위

- **포함**: 문제 정의, TDD 설계, Cursor 규칙, Dual-Track 구현, Data/InMemory, Integration, PyQt6 GUI  
- **선택**: File JSON Repository (`IT-E03`), REFACTOR 커버리지, `develop` merge

---

## 문서 이력

| 날짜 | 변경 |
|------|------|
| 2026-05-28 | README · Report 01 · Prompting 01 |
| 2026-05-28 | Report 02 · Prompting 02 · `spec` 브랜치 |
| 2026-05-28 | Report 03 · Prompting 03 · `.cursorrules` · `User` entity |
| 2026-05-28 | Report 04 · Prompting 04 · `.cursor/rules/*.mdc` · README 01~04 동기화 |
| 2026-05-29 | Track A/B GREEN 완료 · Data/IT · PyQt6 GUI · [Report 10](./Report/10_Magic-Square-Dual-Track-MVP-and-Screen-GUI-Session-Report.md) |
| 2026-05-29 | GM-1~2 Golden Master baseline · approve 패턴 · README GM-03 체크리스트 |
| 2026-05-29 | [Report 11](./Report/11_Magic-Square-Golden-Master-Regression-Session-Report.md) · [Prompting 11](./Prompting/11_Magic-Square-Golden-Master-Regression-Session-Transcript-Prompt.md) |
