# MagicSquare_

4×4 **마방진(Magic Square)** TDD 연습 프로젝트입니다.  
**Phase 01(문제 정의)** 와 **Phase 02(Dual-Track TDD 설계)** 까지 문서화했으며, **구현(Red/Green/Refactor)** 은 `spec` 브랜치 이후 진행 예정입니다.

저장소: [ykhaam/MagicSquare_xx](https://github.com/ykhaam/MagicSquare_xx)

---

## Phase 요약

| Phase | 내용 | Report | Prompting | 상태 |
|-------|------|--------|-----------|------|
| **01** | 관찰 · Why · 문제 정의 · Invariant I1~I5 | [01](./Report/01_Magic-Square-Problem-Definition-Report.md) | [01](./Prompting/01_Magic-Square-Problem-Definition-Prompt.md) | ✅ |
| **02** | Dual-Track(UI+Logic) TDD · Clean Architecture 설계 | [02](./Report/02_Magic-Square-Dual-Track-TDD-Design.md) | [02](./Prompting/02_Magic-Square-Prompt.md) | ✅ |
| **03** | TDD 구현 (spec → red → green → refactoring) | — | — | ⏳ 예정 |

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

## Git 브랜치 전략

```
main          ← 마일스톤 스냅샷 (안정)
develop       ← 통합 (merge 후 Green 목표)
spec          ← 수용 조건·설계 문서 (현재 작업)
  → red       ← 실패 테스트
    → green   ← 최소 구현
      → refactoring
        → develop
```

| 브랜치 | 용도 | 원격 |
|--------|------|------|
| `main` | 문서·동작 스냅샷 | `origin/main` |
| `develop` | TDD 통합 | `origin/develop` |
| `spec` | **Phase 02 설계·문서** (현재) | `origin/spec` |

TDD 사이클: `spec → red → green → refactoring → develop` (동시 3분기 금지)

---

## 저장소 구조

```
MagicSquare_/
├── README.md
├── Report/
│   ├── 01_Magic-Square-Problem-Definition-Report.md
│   └── 02_Magic-Square-Dual-Track-TDD-Design.md
└── Prompting/
    ├── README.md
    ├── 01_Magic-Square-Problem-Definition-Prompt.md
    └── 02_Magic-Square-Prompt.md
```

---

## 문서 바로가기

| 문서 | 설명 |
|------|------|
| [Report/01](./Report/01_Magic-Square-Problem-Definition-Report.md) | STEP 1~5 · I1~I5 · 열린 질문 |
| [Report/02](./Report/02_Magic-Square-Dual-Track-TDD-Design.md) | Logic / UI / Data / Integration · Traceability |
| [Prompting/01](./Prompting/01_Magic-Square-Problem-Definition-Prompt.md) | 문제 정의 워크숍 대화 |
| [Prompting/02](./Prompting/02_Magic-Square-Prompt.md) | Turn 03~18 + 실행 프롬프트 |

---

## 진행 현황

| 단계 | 내용 | 상태 |
|------|------|------|
| STEP 1~5 | 문제 정의 (Report 01) | ✅ |
| Dual-Track 설계 | Report 02 · Prompting 02 | ✅ |
| `spec` 브랜치 | 설계 문서 반영 | ✅ |
| `red` | Domain/UI 실패 테스트 | ⏳ |
| `green` | 최소 구현 | ⏳ |
| `refactoring` | 구조 정리 | ⏳ |
| `develop` / `main` merge | MVP 마일스톤 | ⏳ |

---

## 다음 단계

1. `spec`에서 Report 02·Prompting 02 확정 후 `red` 브랜치 생성  
2. RED: `DT-*`(Domain) · `UT-*`(UI Boundary) 테스트부터  
3. GREEN → REFACTOR → `develop` merge  
4. [Report 01 §9](./Report/01_Magic-Square-Problem-Definition-Report.md#9-열린-질문--다음-단계-후보) 열린 질문은 Phase 02 계약과 충돌 시 **02 우선**

---

## 범위

- **포함**: 문제 정의, TDD 설계, 계약, 테스트 명세, 브랜치 전략  
- **미포함**: 소스 코드 구현 (Phase 03부터)

---

## 문서 이력

| 날짜 | 변경 |
|------|------|
| 2026-05-28 | README · Report 01 · Prompting 01 |
| 2026-05-28 | Report 02 · Prompting 02 통합 · `spec` 브랜치 |
