# MagicSquare_

4×4 **마방진(Magic Square)** 을 다루는 프로그램을 목표로 하는 저장소입니다.  
현재는 **문제 정의** 단계만 진행했으며, 구현은 아직 시작하지 않았습니다.

---

## 프로젝트 목적

격자에 값을 배치할 때 **여러 규칙(합·중복·범위)이 동시에 성립하는지**를 다루는 과제를, 구현 전에 **관찰 → Why → 명확한 문제 정의** 순으로 정리하는 것이 1차 목표입니다.

**현재로서의 문제 정의 (요약)**

> 학습자가 제시한 4×4 격자 상태가 마방진 규칙을 **모두 만족하는지 일관되게 판정**하고, **명확한 피드백**을 제공하는 연습 환경을 정의·보장한다.

(가정: 학습·퍼즐형 · 값 1~16 · 행·열·대각선 합 동일 — 상세는 Report 참고)

---

## 저장소 구조

```
MagicSquare_/
├── README.md                 ← 이 파일 (프로젝트 개요)
├── Report/                   ← 문제 정의 보고서
│   └── 01_Magic-Square-Problem-Definition-Report.md
└── Prompting/                ← 문제 정의 워크숍 대화·프롬프트 기록
    └── 01_Magic-Square-Problem-Definition-Prompt.md
```

---

## 문서 바로가기

| 문서 | 설명 |
|------|------|
| [Report/01_Magic-Square-Problem-Definition-Report.md](./Report/01_Magic-Square-Problem-Definition-Report.md) | STEP 1~5 통합 보고서 (요약·Invariant·열린 질문 포함) |
| [Prompting/01_Magic-Square-Problem-Definition-Prompt.md](./Prompting/01_Magic-Square-Problem-Definition-Prompt.md) | 워크숍 프롬프트·대화 export |

---

## 진행 현황

| 단계 | 내용 | 상태 |
|------|------|------|
| STEP 1 | Observation (관찰) | ✅ |
| STEP 2~4 | Why #1 ~ #3 (TDD 맥락) | ✅ |
| STEP 5 | 진짜 문제 정의 · Invariant | ✅ |
| STEP 6+ | 수용 조건, 구현 | ⏳ 미정 |

---

## 핵심 Invariant (계약)

| ID | 요약 |
|----|------|
| I1 | 완성 시 1~16이 각각 정확히 한 번 |
| I2 | 완성 시 행·열·대각선 합이 모두 동일 |
| I3 | “완성” ⇔ I1·I2 동시 만족 |
| I4 | 같은 격자 → 같은 판정 |
| I5 | I1·I2 위반 시 완성 아님 |

---

## 범위와 제외

- **포함**: 문제 정의, 가정, 불변, Why, 학습·TDD 관점의 사고 훈련 목표  
- **제외**: 구현 설계, 코드, 알고리즘 (의도적으로 보류)

---

## 다음 단계

1. 열린 질문 확정 (사용자, 입출력, 피드백 수준) — [Report §9](./Report/01_Magic-Square-Problem-Definition-Report.md#9-열린-질문--다음-단계-후보)  
2. Acceptance Criteria 작성  
3. TDD용 입·출력 예시 정리 후 구현 착수  

---

## 문서 이력

| 날짜 | 변경 |
|------|------|
| 2026-05-28 | 프로젝트 README 추가 |
| 2026-05-28 | Report/README.md 제거, 루트 README만 유지 |
