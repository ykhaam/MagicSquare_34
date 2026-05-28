# Magic Square 4×4 — Cursor Rules · Phase 03 Kickoff 보고서

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_ |
| 문서 버전 | 1.0 |
| 작성일 | 2026-05-28 |
| 상위 문서 | [01](./01_Magic-Square-Problem-Definition-Report.md) · [02](./02_Magic-Square-Dual-Track-TDD-Design.md) |
| 짝 프롬프트 | [03_Magic-Square-Phase03-Cursorrules-Prompt.md](../Prompting/03_Magic-Square-Phase03-Cursorrules-Prompt.md) |
| 목적 | `.cursorrules` 정립 · ECB 첫 구현(`User`) · Phase 03 착수 기록 |
| 후속 | 규칙 `.mdc` 이전 → [04](./04_Magic-Square-Cursor-Rules-Migration-Report.md) |

---

## 1) 요약

Phase 03(구현)에 앞서 **Cursor AI 행동 규칙**을 `.cursorrules`(YAML)로 고정했고, ECB **entity** 레이어에 **`User` 도메인 엔티티**와 **pytest 8건**을 추가했다. 마방진 핵심(`MagicGrid`, `PuzzleSolver`)은 Report 02 설계대로 **다음 RED 슬라이스**로 남긴다.

| 산출물 | 경로 | 상태 |
|--------|------|------|
| 프로젝트 규칙 | `.cursorrules` | ✅ 8개 섹션 완성 |
| Entity — User | `src/entity/user.py` 등 | ✅ Green (8 tests) |
| 테스트 인프라 | `pyproject.toml`, `tests/conftest.py` | ✅ |
| 마방진 Domain | `MagicGrid`, `DT-*` | ⏳ 미착수 |

---

## 2) `.cursorrules` 설계·완성

### 2.1 파일 형식 선택

| 방식 | 판단 |
|------|------|
| `.cursor/rules/*.mdc` | Dual-Track·레이어별 `globs` 분리에 유리 (장기 권장) |
| **`.cursorrules` (YAML)** | **현재 채택** — 단일 SSOT, 8개 최상위 키로 팀 합의·리뷰 용이 |

조건(PEP 8, type hints, ECB, Dual-Track TDD, `print()` 금지, RED 없이 구현 금지 등)을 **섹션별로 매핑**했다.

### 2.2 섹션 구성

| 키 | 역할 |
|----|------|
| `project` | 이름, Report 01/02 링크, `int[4][4]`/`int[6]` 계약, 브랜치·Dual-Track |
| `code_style` | Python 3.10+, PEP 8, type hints, Google docstring, Black 88 |
| `architecture` | ECB 3레이어, `boundary → control → entity` 의존 방향 |
| `tdd_rules` | `red_phase` / `green_phase` / `refactor_phase` (description, rules, must_not) |
| `testing` | pytest, AAA, coverage 80%+, fixture_scope, `test_` 접두사 |
| `forbidden` | print, 하드코딩, bare except, RED 없이 src/, 테스트 약화, ECB 역전 등 |
| `file_structure` | `src/{boundary,control,entity}`, `tests/` 트리 |
| `ai_behavior` | 코딩 전·중·후 체크, `[TDD WARNING]`, `.cursor` 내 README 금지 |

### 2.3 검토(리뷰) 시 확인된 이슈

| # | 항목 | 내용 | 조치 |
|---|------|------|------|
| 1 | YAML 문법 | PyYAML 파싱 성공 | — |
| 2 | `refactor_phase.forbidden` vs `forbidden` | 중복·모순 **위험** | 최상위 `forbidden`에 통합 완료 |
| 3 | `red_phase.branch` | “테스트만” vs “스텁·인터페이스 예외” 모호 | Phase 03에서 red 브랜치 실무 시 재확인 |
| 4 | AI 강제 한계 | 브랜치·pytest·커버리지는 **에이전트가 도구 실행 시**만 검증 가능 | `ai_behavior.after_coding`에 pytest 보고 명시 |

---

## 3) Phase 03 첫 구현 — `User` Entity

### 3.1 범위

Report 02에 `User` 명세는 없다. **학습자(퍼즐 사용자) 식별**용 보조 엔티티로, `.cursorrules`의 entity 규칙(순수 도메인, 상수 분리, `UserValidationError` + code)을 검증하는 **ECB 샘플**로 추가했다.

### 3.2 파일

| 파일 | 설명 |
|------|------|
| `src/entity/user.py` | `@dataclass(frozen=True)` — `create`, `rename_display_name`, `is_same_identity_as` |
| `src/entity/user_constants.py` | 길이·`USER_*` 에러 코드 상수 |
| `src/entity/exceptions.py` | `UserValidationError(code, message)` |
| `tests/entity/test_user.py` | AAA, `test_user_n01` / `test_user_e01` … (8 tests) |

### 3.3 도메인 불변 (User)

| ID | 규칙 |
|----|------|
| U-ID-01 | `user_id` 비공백, 최대 64자 |
| U-NAME-01 | `display_name` 길이 1~50 (trim 후) |
| U-EMAIL-01 | 이메일 형식·최대 254자 |
| U-IMMUT-01 | 변경은 새 인스턴스 (`rename_display_name`) |
| U-IDENT-01 | 동일성은 `user_id`만으로 판단 |

### 3.4 테스트 결과

```text
pytest tests/entity/test_user.py — 8 passed
```

### 3.5 기술 메모

- `tests/entity/__init__.py`는 `src/entity` 패키지와 **이름 충돌** → **제거** (`test_*.py`만 유지).
- `tests/conftest.py`에서 `src/`를 `sys.path`에 등록.

---

## 4) Report 02와의 정렬

| Report 02 | Phase 03 현재 |
|-----------|----------------|
| Domain `MagicGrid`, `DT-*` | ⏳ 다음 RED: `DT-E01~E06` |
| UI Boundary `UT-*` | ⏳ entity 안정 후 |
| ECB 폴더 | `src/entity`만 일부 구현; `boundary/`, `control/` 빈 상태 |
| 브랜치 `spec → red → green → refactoring` | 로컬 구현 시작; **red 브랜치 분리는 미실시** |

**우선순위:** Report 02 §1.5.4 RED 순서 — 구조 테스트(`DT-E01~E06`) → `MagicSquareJudge` → `PuzzleSolver`.

---

## 5) 저장소 구조 (현재)

```text
MagicSquare_/
├── .cursorrules
├── pyproject.toml
├── src/
│   └── entity/
│       ├── user.py
│       ├── user_constants.py
│       └── exceptions.py
├── tests/
│   ├── conftest.py
│   └── entity/
│       └── test_user.py
├── Report/
│   ├── 01_...
│   ├── 02_...
│   └── 03_... (본 문서)
└── Prompting/
    ├── 01_...
    ├── 02_...
    └── 03_...
```

---

## 6) 열린 질문 · 다음 단계

1. **`red` 브랜치** 생성 후 `DT-E01`부터 테스트만 커밋할지, 현재 `spec`/작업 트리에서 이어갈지.
2. `.mdc` 분할(`.cursor/rules/`)을 **언제** 도입할지 — `.cursorrules`와 이중 유지 방지.
3. `User`를 Boundary/Control에서 쓸 **유스케이스** 정의 여부 (세션·저장 연동).
4. CI(pytest + coverage gate) 추가 시점.

### 권장 다음 작업

1. `git checkout -b red` (또는 팀 정책에 맞는 브랜치)
2. `tests/entity/test_magic_grid.py` — `DT-E01` (3×3 거부) RED 작성
3. `MagicGrid.from_raw` 최소 Green
4. Report 02 Traceability에 `User`는 **부록**으로만 유지 (핵심 계약 아님)

---

## 7) 문서 이력

| 버전 | 날짜 | 변경 |
|------|------|------|
| 1.0 | 2026-05-28 | Phase 03 kickoff — `.cursorrules`, `User` entity, pytest |

---

*본 문서는 Phase 03 착수 산출물이며, Report 02 구현 명세를 대체하지 않는다.*
