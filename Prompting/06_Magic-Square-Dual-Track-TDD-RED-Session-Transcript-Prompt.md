# Magic Square 4×4 — Prompt & Transcript (06 · Dual-Track TDD RED Session)

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_ |
| 짝 | [Report/06_Magic-Square-Dual-Track-TDD-RED-Session-Report.md](../Report/06_Magic-Square-Dual-Track-TDD-RED-Session-Report.md) |
| Export | 2026-05-29 (KST) |
| 브랜치 | `feature/dual-track-tdd` |
| 형식 | **User** / **Cursor** 대화 Transcript + 프롬프트 요약 |
| Agent | backup-documentation-agent |
| 선행 | [05_Magic-Square-Level1-5-Alignment-Transcript-Prompt.md](./05_Magic-Square-Level1-5-Alignment-Transcript-Prompt.md) |

---

## 목차

1. [대화 Transcript (이번 세션)](#대화-transcript-이번-세션)
2. [실행 프롬프트 요약](#실행-프롬프트-요약)
3. [산출물 목록](#산출물-목록)
4. [시도한 명령과 결과](#시도한-명령과-결과)

---

# 대화 Transcript (이번 세션)

## T1 — Git 브랜치 전략 요청

**User:**  
`MagicSquare _1004` 프로젝트 Dual-Track TDD Git 브랜치 전략. 순서: Dual-Track UI+Logic TDD → GREEN → Dual-Track Refactoring.

**Cursor (요약):**

- 장수 브랜치: `main`, `develop`, `spec`
- TDD 단계: `red → green → refactoring → develop` (동시 3분기 금지)
- Dual-Track = 별도 브랜치가 아닌 **슬라이스 내 Track A/B 교차** (DT-E01 → UT-E01 …)
- Mermaid 다이어그램, 슬라이스별 워크플로, 브랜치별 허용/금지 표 제공
- 현재 저장소: `develop` 기준, `red/green/refactoring` 미분리

---

## T2 — feature 브랜치 생성

**User:**  
`feature/dual-track-tdd` 브랜치 생성.

**Cursor (실행):**

```text
git checkout -b feature/dual-track-tdd   # develop 기준, working tree clean
```

---

## T3 — 테스트 플랜 샘플 AC 선정

**User:**  
PRD 기준 FR-01 선행 AC 샘플 1개 선택. `grid=None` → `INVALID_SIZE`. 코드 작성 금지.

**Cursor (요약):**

- **AC-FR01-01** (+ AC-FR01-05 Domain 미호출)
- FR-01 §10, BR-01, §12.1, §13
- 기대: `{ code: "UI_INVALID_SIZE", message: "Grid must be 4x4." }` (PRD SSOT)
- 선택 이유: 4×4 확인 최선행; Boundary+Domain 격리 동시 검증 가능

---

## T4 — test_plan.md 작성

**User:**  
QA 리드 프롬프트 — AC-FR-01-01 범위 test_plan.md (pytest, 경계값, mock/spy, cov).

**Cursor (실행):**

- `docs/test_plan.md` 생성
- Track A UT-E01 / Track B DT-E01, BV-01~06, EX-01~08, pytest-cov 명령 포함

---

## T5 — README RED To-Do 추가

**User:**  
README에 **RED 단계 To-Do 리스트** 섹션 삽입 (Track A/B, 커버리지, 결함 연결).

**Cursor (실행):**

- `README.md` 「다음 단계」와 「범위」 사이에 체크리스트 추가

---

## T6 — Boundary RED 테스트 작성

**User:**  
AC-FR-01-01 범위 pytest 8건. Given-When-Then, `# AC-FR-01-01`, RED(실패) 상태.

**Cursor (실행):**

- `tests/boundary/test_validate_size.py` — 8 tests
- import: `MagicSquareBoundary`, `ErrorResponse` (미구현 → collect ERROR)
- `pyproject.toml`: pydantic, pytest-cov dev 의존성 추가

---

## T7 — pytest 실패 원인 문의

**User:**  
`python -m pytest --cov=src --cov-report=term-missing` 왜 실패?

**Cursor (요약):**

- 원인: `ModuleNotFoundError: boundary.magic_square_boundary`
- RED 의도 — GREEN `src/boundary/` 미구현
- entity만: `pytest tests/entity/ --cov=src` → 8 passed, 100%

---

## T8 — venv + entity 커버리지

**User:**  
`source .venv/Scripts/activate` + entity pytest cov html.

**Cursor (실행):**

- `.venv` 없음 → `python -m venv .venv` 생성 후 activate
- `pip install -e ".[dev]"`
- 8 passed, htmlcov 100% (entity 4파일)

---

## T9 — 진행 상태 확인

**User:**  
잘 진행되고 있는거지?

**Cursor (요약):**

- TDD RED 관점 정상 진행
- Track A RED 완료, Track B·GREEN 미착수
- User entity Green 유지

---

## T10 — htmlcov 79% vs 100% 문의

**User:**  
스크린샷(79%, `exceptions/` 서브패키지)처럼 왜 안 뜨지?

**Cursor (요약):**

- 스크린샷 = 다른 날짜/구조 (2026-05-24, 38 stmts)
- 현재 = entity 단일 파일 구조, tests/entity만 실행 → 100%
- 전체 pytest는 boundary import ERROR로 htmlcov 미갱신

---

## T11 — QA 결함 분석

**User:**  
pytest 실패 로그 기반 — 기대/실제, 버그 위치, 심각도, GREEN 최소 수정 diff.

**Cursor (요약):**

- 실패 = collect 단계 import (AttributeError 아님)
- 위치: `test_validate_size.py:10`, `src/boundary/` 부재
- Critical: DEF-001
- 제안 diff: `schemas.py`, `magic_square_boundary.py` 최소 GREEN

---

## T12 — defect_list.md

**User:**  
결함을 `defect_list.md`에 정리, README 결함 체크박스 업데이트.

**Cursor (실행):**

- `defect_list.md` — DEF-001~005
- README: `defect_list.md 생성` → `[x]`, 회귀 확인 → `[ ]`

---

## T13 — 백업 문서 Export (본 Transcript)

**User:**  
`backup-documentation-agent` — Report + Prompting Transcript Export.

**Cursor (실행):**

- `Report/06_Magic-Square-Dual-Track-TDD-RED-Session-Report.md`
- `Prompting/06_Magic-Square-Dual-Track-TDD-RED-Session-Transcript-Prompt.md`

---

# 실행 프롬프트 요약

| Turn | 역할 태그 | 핵심 지시 |
|------|-----------|-----------|
| T1 | — | Dual-Track TDD Git 브랜치 전략 |
| T2 | — | `feature/dual-track-tdd` 생성 |
| T3 | — | PRD FR-01 샘플 AC 선정 (코드 금지) |
| T4 | [P] QA | test_plan.md (AC-FR-01-01) |
| T5 | — | README RED To-Do |
| T6 | [P] QA | Boundary RED pytest 8건 |
| T7~T10 | — | pytest/cov/진행/ htmlcov 질의 |
| T11 | [P] QA | 결함 분석 + GREEN diff 제안 |
| T12 | [P] QA | defect_list.md |
| T13 | backup-documentation-agent | Report 06 + Transcript 06 |

---

# 산출물 목록

| 유형 | 경로 |
|------|------|
| Report | `Report/06_Magic-Square-Dual-Track-TDD-RED-Session-Report.md` |
| Transcript | `Prompting/06_Magic-Square-Dual-Track-TDD-RED-Session-Transcript-Prompt.md` |
| Test Plan | `docs/test_plan.md` |
| RED Tests | `tests/boundary/test_validate_size.py` |
| Defects | `defect_list.md` |
| README | RED To-Do + defect 체크 |

---

# 시도한 명령과 결과

| 명령 | 결과 |
|------|------|
| `git checkout -b feature/dual-track-tdd` | 성공 |
| `python -m pytest tests/boundary/` | ERROR — ModuleNotFoundError |
| `python -m pytest --cov=src` | exit 2 — collect ERROR |
| `python -m venv .venv` + `pytest tests/entity/ --cov=src --cov-report=html` | 8 passed, entity 100% |
| `python -m pytest tests/boundary/ tests/entity/` | 8 collected + 1 error |

---

## 민감 정보

- 본 세션 대화에 API Key, PAT, 비밀번호 노출 **없음** — 마스킹 대상 없음.

---

## 후속 권장 (Git)

- 사용자 명시 요청 시: `feature/dual-track-tdd` 변경사항 commit
- GREEN 구현 후: boundary 8건 Green → `develop` merge 검토
