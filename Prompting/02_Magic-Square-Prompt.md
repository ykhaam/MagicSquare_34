# Magic Square 4×4 — Prompt & Transcript (02)

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_ |
| 짝 | [Report/02_Magic-Square-Dual-Track-TDD-Design.md](../Report/02_Magic-Square-Dual-Track-TDD-Design.md) |
| Export | 2026-05-28 |
| 형식 | **User** / **Cursor** 대화 + 실행 프롬프트 전문 |
| 보안 | PAT → `[REDACTED_PAT]` |

**01과의 관계:** Turn 01~02(문제 정의) 상세는 [01_Magic-Square-Problem-Definition-Prompt.md](./01_Magic-Square-Problem-Definition-Prompt.md) 에만 둡니다.

---

## 목차

1. [대화 Transcript (Turn 03~18)](#대화-transcript-turn-0318)
2. [실행 프롬프트 — TDD 설계 문서 (Turn 16)](#실행-프롬프트--tdd-설계-문서-turn-16)
3. [실행 프롬프트 — Dual-Track 설계 (Turn 17)](#실행-프롬프트--dual-track-설계-turn-17)

---

# 대화 Transcript (Turn 03~18)

| Turn | 주제 | 산출물 |
|------|------|--------|
| 03 | Report export | `Report/01_...` |
| 04~05 | README | 루트 README |
| 06~12 | GitHub push | `origin/main`, `develop` |
| 13~14 | TDD · 브랜치 전략 | — |
| 15 | spec 브랜치 | `origin/spec` |
| 16 | TDD 설계 실행 프롬프트 | [§2](#실행-프롬프트--tdd-설계-문서-turn-16) |
| 17 | Dual-Track 설계 | [§3](#실행-프롬프트--dual-track-설계-turn-17) → `Report/02_...` |
| 18 | transcript export | 본 파일 |

---

## Turn 03 — Report export

**User:** 지금까지 작업한 내용을 Report 폴더에 보고서로보내줘.

**Cursor:** `Report/01_Magic-Square-Problem-Definition-Report.md` 작성.

---

## Turn 04 — README 업데이트

**User:** 앞서서 작업한 내용을 기초로 README.md 파일을 업데이트해줘.

**Cursor:** 루트 `README.md`·`Report/README.md` 갱신 (Report README는 Turn 05에서 삭제).

---

## Turn 05 — Report README 삭제

**User:** report폴더 안의 readme는 지워줘도 돼.

**Cursor:** `Report/README.md` 삭제, 루트 README 링크 정리.

---

## Turn 06~12 — GitHub push

**User:** MagicSquare_xx 업로드 / push / 토큰 / 브랜치 push 등

**Cursor:** `git init`, 커밋 `fd08d3b`, 403 후 PAT로 push 성공, `main`·`develop` 반영, `push-to-github.ps1` 생성·삭제.

---

## Turn 13 — TDD 브랜치 전략

**User:** RED, Green, Refactoring — 적당한 브랜치 전략?

**Cursor:** Red/Green/Refactor = feature 안 커밋 순서. `main` ← `develop` ← `feature/*`(Invariant 단위).

---

## Turn 14 — TDD 쉬운 설명

**User:** TDD 설명 + 전략 매칭, 쉽게.

**Cursor:** 테스트 먼저 → Red → Green → Refactor. `feature`에서 한 바퀴 → `develop` merge.

---

## Turn 15 — spec 브랜치

**User:** develop에서 red/green/refactoring 전략. spec 브랜치 먼저.

**Cursor:** 순차 `spec → red → green → refactoring → develop`. `spec` 생성·push.

---

## Turn 16 — TDD 설계 실행 프롬프트

**User:** Cursor용 실행 프롬프트만 작성 (설계 문서 X).

**Cursor:** → [§2 전문](#실행-프롬프트--tdd-설계-문서-turn-16)

---

## Turn 17 — Dual-Track 설계

**User:** Dual-Track UI + Logic TDD 설계 (구현 코드 금지).

**Cursor:** `Report/02_Magic-Square-Dual-Track-TDD-Design.md` 작성. → [§3 User 프롬프트](#실행-프롬프트--dual-track-설계-turn-17)

---

## Turn 18 — transcript export

**User:** 프롬프트 전체를 Prompting에 export.

**Cursor:** 본 파일 `02_Magic-Square-Prompt.md` 로 통합.

---

# 실행 프롬프트 — TDD 설계 문서 (Turn 16)

```markdown
# 실행용 프롬프트: Magic Square 4×4 TDD 설계 문서 작성

## 역할
당신은 TDD·도메인 설계 문서를 작성하는 시니어 설계자다.
구현·코드·알고리즘·프레임워크 선택은 하지 않는다.
목표 산출물: MagicSquare_ 프로젝트용 「4×4 Magic Square TDD 설계 문서」(Markdown 1개).

## 반드시 먼저 읽을 컨텍스트
1. README.md
2. Report/01_Magic-Square-Problem-Definition-Report.md
3. (선택) Prompting/01_Magic-Square-Problem-Definition-Prompt.md

고정 전제: 4×4, 1~16 각 한 번, 행·열·대각선 합 동일, 학습·퍼즐형, 판정+피드백.

## 브랜치·TDD 워크플로
develop | spec | red | green | refactoring
순차 merge: spec → red → green → refactoring → develop

## 작성 금지
소스 코드, 의사코드, 알고리즘, UI 목업, 보고서 단순 복붙

## 산출물
Report/02_Magic-Square-TDD-Design.md (또는 Spec/ — 저장소 관례에 맞게)
한국어, 각 섹션 끝 「설계 결정」/「열린 질문」

## 필수 목차
0. 문서 메타 · 1. 설계 목표 · 2. 시스템 경계 · 3. 도메인 계약(I1~I5)
4. 입출력 명세 · 5. 수용 조건 ≥12 · 6. 테스트 전략
7. 테스트 데이터 카탈로그 · 8. 브랜치 매핑 · 9. 리스크·열린 질문 · 10. 용어집

## 품질 체크리스트
I1~I5 연결, 완성↔I3, 빈칸 정책 단일, 코드 없음, spec→red 실패≥1, develop Green 명확

## 출력 지시
설계 문서 전문 + 파일 저장 + 3줄 요약. 구현·테스트 코드·브랜치 생성 금지.
```

---

# 실행 프롬프트 — Dual-Track 설계 (Turn 17)

**User (전문)**

```
당신은 Dual-Track UI + Logic TDD 및 Clean Architecture 설계 전문가입니다.
프로젝트: Magic Square (4x4) — TDD 연습용
목적: 알고리즘 난이도보다 “레이어 분리 + 계약 기반 테스트 + 리팩토링” 훈련
제약:
- 구현 코드는 작성하지 마십시오. (설계/계약/테스트/통합 계획만)
- UI는 실제 화면이 아니라 “입력/출력 경계(Boundary)”로 정의
- Data Layer는 DB가 아니라 “저장/로드 인터페이스(메모리/파일 교체 가능)” 수준만
- 입력/출력은 명확히 고정
입력 계약:
- 4x4 int[][] (0은 빈칸)
- 빈칸은 정확히 2개
- 값 범위: 0 또는 1~16
- 0 제외 중복 금지
출력 계약:
- int[6]
- 좌표는 1-index
- 반환 형식: [r1,c1,n1,r2,c2,n2]
- n1,n2는 두 누락 숫자이며, (작은수→첫빈칸, 큰수→둘째빈칸) 조합이 마방진이면 그 순서로, 아니면 반대로

------------------------------------------------------------
출력 형식 (반드시 이 구조로)
------------------------------------------------------------
# 1) Logic Layer (Domain Layer) 설계
## 1.1 도메인 개념
## 1.2 도메인 불변조건(Invariants)
## 1.3 핵심 유스케이스(도메인 관점)
## 1.4 Domain API(내부 계약)
## 1.5 Domain 단위 테스트 설계(RED 우선)

# 2) Screen Layer (UI Layer) 설계 (Boundary Layer)
## 2.1 사용자/호출자 관점 시나리오
## 2.2 UI 계약(외부 계약)
## 2.3 UI 레벨 테스트(Contract-first, RED 우선)
## 2.4 UX/출력 규칙

# 3) Data Layer 설계
## 3.1 목적 정의
## 3.2 인터페이스 계약
## 3.3 구현 옵션 비교(메모리/파일)
## 3.4 Data 레이어 테스트

# 4) Integration & Verification
## 4.1 통합 경로 정의
## 4.2 통합 테스트 시나리오
## 4.3 회귀 보호 규칙
## 4.4 커버리지 목표
## 4.5 Traceability Matrix (필수)

------------------------------------------------------------
추가 조건
------------------------------------------------------------
- 모호한 표현 금지(“적절히/충분히” 금지)
- 모든 규칙은 검증 가능해야 함(테스트로 확인 가능)
- 구현 코드 작성 금지
- 표/체크리스트를 적극 사용
```

**Cursor (요약)**

- `Report/02_Magic-Square-Dual-Track-TDD-Design.md` 생성.
- 입력 `int[4][4]`(빈칸 2) → 출력 `int[6]`(1-index), Magic Constant 34.
- Logic / UI Boundary / Data / Integration + Traceability Matrix.
- `01` 보고서(판정·피드백)와 계약 상이 — **02 계약 우선**.

---

*End of 02. PAT 미기록.*
