# Magic Square 4×4 — Prompt & Transcript (07 · Dual-Track TDD RED Design)

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_ |
| 짝 | [Report/07_Magic-Square-Dual-Track-TDD-RED-Design-Report.md](../Report/07_Magic-Square-Dual-Track-TDD-RED-Design-Report.md) |
| Export | 2026-05-29 (KST) |
| TDD phase | **RED** (설계만) |
| 형식 | **User** / **Cursor** 대화 Transcript + 프롬프트 요약 |
| Agent | Auto (Cursor) |
| 선행 | [06_Magic-Square-Dual-Track-TDD-RED-Session-Transcript-Prompt.md](./06_Magic-Square-Dual-Track-TDD-RED-Session-Transcript-Prompt.md) |

---

## 목차

1. [대화 Transcript (이번 세션)](#대화-transcript-이번-세션)
2. [실행 프롬프트 요약](#실행-프롬프트-요약)
3. [산출물 목록](#산출물-목록)
4. [RED 설계 산출 요약](#red-설계-산출-요약)

---

# 대화 Transcript (이번 세션)

## T1 — 전체 FR-01~FR-05 Dual-Track RED 설계표 요청

**User:**

- 역할: Dual-Track UI + Logic TDD 전문가
- **TDD phase: RED** — 오직 RED 테스트 설계표만 작성
- **금지 (엄격):** 구현/테스트/스켈레톤 코드, 클래스·파일 구조 확정, GREEN/REFACTOR, pytest 실행, 파일 저장 (설계표 텍스트 출력만)
- **SSOT:** `docs/PRD_MagicSquare.md` v0.2, `Report/02_Magic-Square-Dual-Track-TDD-Design.md`, `.cursorrules`
- **범위:** FR-01~FR-05 Dual-Track RED 설계표

**Track A — Boundary / UI Contract RED**

1. `matrix=null` → E003
2. size ≠ 4×4 → E001 (3×4, 4×3, 5×5, `[]`)
3. 빈칸 ≠ 2 → E002 (0개·3개)
4. 값 범위 위반 → E004 (-1, 17)
5. non-zero 중복 → E005
6. 성공 반환 길이 6 (U-OUT-01)
7. 좌표 1-index (U-OUT-02)
8. invalid 시 `execute` call_count == 0 (U-FLOW-02)

각 항목: Test ID, Layer, 테스트 이름, Given, When, Then, Expected RED Failure, 실패 이유, Boundary 계약, Invariant/AC

**Track B — Domain / Logic RED**

- 별칭: `find_blank_coords`, `find_not_exist_nums`, `is_magic_square`, `solution`
- Given: Report/02 부록 G0~G3 (없으면 placeholder)
- D-LOC-01 ~ D-SOL-04 슬라이스 분리
- Domain Mock 금지 명시

**출력 형식:** `# UI RED Tests` / `# Logic RED Tests` 표 + RED 설계 자체 검수 체크리스트

**Cursor (요약):**

- SSOT 문서(Report 02, PRD, test_plan) 참조 후 설계표 작성
- Track A 14행: U-IN-01, U-IN-02a~e, U-IN-03a/b, U-IN-04a/b, U-IN-05, U-OUT-01/02, U-FLOW-02
- Track B 14행: D-LOC-01, D-MIS-01, D-VAL-01~06, D-SOL-01~04
- G0~G3 fixture 표 · E-code ↔ UI code 매핑 · Report 02 UT/DT 매핑
- 검수 체크리스트 6항 전부 통과
- G1/G3 일부 Report 02 부록 미기재 → placeholder 명시

---

## T2 — Report · Prompting Export 요청

**User:**

> Report 폴더에 보고서 생성하고, Prompting 폴더에 Transcript도 Export 해줘

**Cursor (실행):**

- `Report/07_Magic-Square-Dual-Track-TDD-RED-Design-Report.md` 생성
- `Prompting/07_Magic-Square-Dual-Track-TDD-RED-Design-Transcript-Prompt.md` 생성 (본 문서)

---

# 실행 프롬프트 요약

| Turn | 역할 | 핵심 지시 |
|------|------|-----------|
| T1 | Dual-Track TDD RED 전문가 | FR-01~05 전체 RED 설계표; 코드·pytest·저장 금지 |
| T2 | — | Report 07 + Prompting Transcript 07 Export |

### T1 프롬프트 구조 (재현용)

```text
TDD phase: RED
금지: 구현/테스트/스켈레톤, GREEN/REFACTOR, pytest, 파일 저장
SSOT: PRD v0.2, Report/02, .cursorrules

Track A: U-IN-* (E003,E001,E002,E004,E005), U-OUT-*, U-FLOW-02
Track B: D-LOC, D-MIS, D-VAL-01~06, D-SOL-01~04
격자: G0~G3
표 컬럼: Test ID, Layer, 이름, Given, When, Then, Expected RED Failure, ...
출력: UI RED Tests 표 + Logic RED Tests 표 + 체크리스트
```

---

# 산출물 목록

| 유형 | 경로 |
|------|------|
| Report | `Report/07_Magic-Square-Dual-Track-TDD-RED-Design-Report.md` |
| Transcript | `Prompting/07_Magic-Square-Dual-Track-TDD-RED-Design-Transcript-Prompt.md` |
| (채팅 산출) | T1 RED 설계표 — UI 14행 + Logic 14행 (코드 파일 미생성) |

**연계 (선행 세션 06)**

| 유형 | 경로 |
|------|------|
| Report | `Report/06_Magic-Square-Dual-Track-TDD-RED-Session-Report.md` |
| RED Tests (코드) | `tests/boundary/test_validate_size.py` |
| Test Plan | `docs/test_plan.md` |

---

# RED 설계 산출 요약

## Track A (Boundary) — 14 Test-ID

| 구분 | Test-ID | 건수 |
|------|---------|------|
| 입력 검증 | U-IN-01, U-IN-02a~e, U-IN-03a/b, U-IN-04a/b, U-IN-05 | 11 |
| 출력 계약 | U-OUT-01, U-OUT-02 | 2 |
| 흐름 격리 | U-FLOW-02 | 1 |

## Track B (Logic) — 14 Test-ID

| 구분 | Test-ID | 건수 |
|------|---------|------|
| 빈칸 | D-LOC-01 | 1 |
| 누락 수 | D-MIS-01 | 1 |
| 마방진 판정 | D-VAL-01 ~ D-VAL-06 | 6 |
| 솔버 | D-SOL-01 ~ D-SOL-04 | 4 |

## 검수 체크리스트 (T1 결과)

- [x] Boundary E00x Failure envelope
- [x] invalid → execute 0회
- [x] U-IN / U-OUT 분리
- [x] Logic Domain Mock 없음
- [x] I1~I11 · AC-FR* 추적
- [x] 코드 미작성

---

## 민감 정보

- 본 세션 대화에 API Key, PAT, 비밀번호 노출 **없음**.

---

## 후속 권장

1. `ERROR_MESSAGES["E003"]` SSOT 확정 후 U-IN-01 RED 테스트 작성
2. Report 06 UT-E01 Green 완료 후 U-IN-02~05 슬라이스 순차 RED
3. G1/G3 fixture 부록 확정 → D-LOC/D-SOL RED 테스트 Given 고정
4. 사용자 Git commit 요청 시: Report 07 + Prompting 07 포함 커밋
