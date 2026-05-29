# Magic Square 4×4 — Prompt & Transcript (05 · Level 1~5 Alignment)

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_ |
| 짝 | [Report/05_Magic-Square-Level1-5-Alignment-Verification-Report.md](../Report/05_Magic-Square-Level1-5-Alignment-Verification-Report.md) |
| Export | 2026-05-28 17:21 (KST) |
| 형식 | **User** / **Cursor** 대화 Transcript + 프롬프트 요약 |
| 선행 | [04_Magic-Square-Cursor-Rules-Migration-Prompt.md](./04_Magic-Square-Cursor-Rules-Migration-Prompt.md) |

---

## 목차

1. [대화 Transcript (이번 세션)](#대화-transcript-이번-세션)
2. [실행 프롬프트 요약](#실행-프롬프트-요약)
3. [산출물 목록](#산출물-목록)

---

# 대화 Transcript (이번 세션)

## T1 — Level 1 Epic 작성 요청

**User:**  
Epic → User Story → Task 구조에서, 우선 Level 1(Epic)만 작성.  
코드/테스트/파일 생성 없이 비즈니스 목표와 학습 목표 중심으로 정리.

**Cursor (요약):**

- Epic Title, Business Goal, Learning Goal, Scope/Non-Scope, Success Criteria 제시
- 불변식, 추적성 규칙, Level 2 후보 User Story 테마 정리
- Contract-first, Dual-Track TDD, 리팩토링 후 계약 불변 원칙 명시

---

## T2 — Level 2 User Journey 작성 요청

**User:**  
5개 Stage(Problem Recognition, Contract Definition, Domain Separation, Dual-Track TDD Progress, Regression Protection)로 Journey 작성 요청.

**Cursor (요약):**

- Persona, Journey Goal, Overview 테이블 작성
- 각 Stage별 Action/Thinking/Emotion/Pain Point/Opportunity 정리
- Stage별 Invariant/Contract 연결 및 학습 성과 정의
- 이후 User Story/Task로 분해 가능하도록 구조화

---

## T3 — Level 3 User Stories 작성 요청

**User:**  
Story 1~5를 기준으로 User Story + Acceptance Criteria 작성.  
Boundary/Domain 분리, AC는 테스트 가능한 문장으로 제한.

**Cursor (요약):**

- Story 1(입력 검증) Boundary, Story 2~5 Domain 중심으로 분리
- 각 Story별 AC, 보호 Contract/Invariant, 향후 RED 방향 정의
- Epic/Journey/Story 간 Traceability Matrix 제공

---

## T4 — Level 4 Technical Scenarios 작성 요청

**User:**  
`SC-DOM-SOL-001`, `SC-BND-VAL-001~003` 시나리오를 기술적 형태로 정리 요청.

**Cursor (요약):**

- Background 공통 전제(4x4, 0=blank, 2 blanks, range, duplicate rule, output contract) 정리
- Solver reverse 성공 시나리오 1개
- Boundary 검증 실패(빈칸 수/중복/범위) 시나리오 3개
- 각 Scenario에 관련 Story, Layer, 보호 Invariant/Contract, RED ID, Task Candidate 연결

---

## T5 — Level 5 Verification 작성 요청

**User:**  
Level 1~4 연결 검증, AC 누락 확인, Edge Coverage, 책임 분리, 분해 가능성, 추적성 요약 요청.

**Cursor (요약):**

- 적합성 점수 7.6/10, 상태 일부 수정 필요 판단
- 강점: 상위 정렬/책임 분리/Dual-Track 준비도
- 약점: Story 2~4 대응 Technical Scenario 누락
- 보강 권장: size 오류, missing number, validator 독립, small-first 성공 분기

---

## T6 — 백업 문서 생성 요청

**User:**  
`/backup-documentation-agent`로 Report 생성 + Prompting Transcript export 요청.

**Cursor (실행 결과 요약):**

- backup-documentation-agent 위임 수행
- 서브에이전트가 읽기 전용 제약으로 파일 직접 생성 실패 보고
- 이후 본 에이전트가 직접 문서 생성으로 보완 수행

---

# 실행 프롬프트 요약

## A. 레벨별 산출물 생성 프롬프트 (요약)

1. Level 1: Epic만 작성 (코드/테스트/파일 생성 금지)  
2. Level 2: 5단계 User Journey 작성  
3. Level 3: Story+AC 작성, Boundary/Domain 분리  
4. Level 4: Technical Scenario 구조화 (Given/When/Then)  
5. Level 5: 정합성 검증 및 누락/보강 포인트 도출

## B. 백업 프롬프트 (요약)

- Report 폴더 보고서 생성
- Prompting 폴더 Transcript export
- 산출물 경로와 검증 결과 보고

---

# 산출물 목록

| 구분 | 파일 | 설명 |
|------|------|------|
| Report | `Report/05_Magic-Square-Level1-5-Alignment-Verification-Report.md` | Level 1~5 정합성 검증 및 보강 포인트 |
| Prompting | `Prompting/05_Magic-Square-Level1-5-Alignment-Transcript-Prompt.md` | 이번 세션 대화/프롬프트 transcript export |

---

## 메모

- 본 문서는 코드/테스트 구현이 아닌 **기획·검증·추적성 문서 백업** 목적이다.
- Level 6 실행 전, Report 05의 누락 항목 보강이 권장된다.

