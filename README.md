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
main          ← 마일스톤 스냅샷 (안정)
develop       ← 통합 (merge 후 Green 목표)
spec          ← 수용 조건·설계 문서
  → red       ← 실패 테스트
    → green   ← 최소 구현
      → refactoring
        → develop
```

| 브랜치 | 용도 | 원격 |
|--------|------|------|
| `main` | 문서·동작 스냅샷 | `origin/main` |
| `develop` | TDD 통합 | `origin/develop` |
| `spec` | 설계·문서·규칙 | `origin/spec` |

TDD 사이클: `spec → red → green → refactoring → develop` (동시 3분기 금지)

---

## 저장소 구조

```
MagicSquare_/
├── README.md
├── .cursorrules              # 규칙 인덱스 · contract 요약
├── .cursor/rules/            # magicsquare-*.mdc (실행 규칙 SSOT)
├── pyproject.toml
├── src/entity/               # User (MagicGrid 등 예정)
├── tests/entity/
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
| `red` | Domain/UI 실패 테스트 (`DT-*`) | ⏳ |
| `green` | 최소 구현 | ⏳ |
| `refactoring` | 구조 정리 | ⏳ |
| `develop` / `main` merge | MVP 마일스톤 | ⏳ |

---

## 다음 단계

1. `red` 브랜치 생성 후 Report 02 §1.5.4 순서로 `DT-E01` RED  
2. Cursor Rules: Settings에서 5개 `.mdc` 로드 확인  
3. GREEN → REFACTOR → `develop` merge  
4. 계약 충돌 시 Report **02 우선** · AI 규칙은 **04 + `.mdc`**

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
