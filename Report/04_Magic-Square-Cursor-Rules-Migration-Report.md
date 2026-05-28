# Magic Square 4×4 — Cursor Rules Migration 보고서

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_ |
| 문서 버전 | 1.0 |
| 작성일 | 2026-05-28 |
| 상위 문서 | [03](./03_Magic-Square-Cursorrules-and-Phase03-Kickoff-Report.md) |
| 짝 프롬프트 | [04_Magic-Square-Cursor-Rules-Migration-Prompt.md](../Prompting/04_Magic-Square-Cursor-Rules-Migration-Prompt.md) |
| 목적 | `.cursorrules` 단일 YAML → `.cursor/rules/*.mdc` 이중 레이어 전환 |

---

## 1) 요약

Phase 03에서 완성한 **176줄 `.cursorrules` YAML**을 **실행 규칙 SSOT**인 5개 `.mdc`로 분리하고, 루트 `.cursorrules`는 **인덱스·계약 요약(~40줄)** 만 남겼다. 중복 제거로 토큰·충돌 위험을 줄이고, Cursor 공식 권장 패턴(`alwaysApply` / `globs`)에 맞췄다.

| Before | After |
|--------|-------|
| 8개 YAML 섹션 단일 파일 | 5개 `.mdc` + 슬림 `.cursorrules` |
| 전 대화마다 전체 규칙 로드 | 파일·작업에 따라 규칙 선택적 적용 |
| `refactor_phase.forbidden` vs `forbidden` 중복 위험 | `magicsquare-forbidden.mdc` 단일 목록 |

---

## 2) 목표 구조

```text
MagicSquare_/
├── .cursorrules                 # 인덱스, contract, rules_index
└── .cursor/rules/
    ├── magicsquare-project.mdc           alwaysApply
    ├── magicsquare-forbidden.mdc         alwaysApply
    ├── magicsquare-tdd-testing.mdc       alwaysApply
    ├── magicsquare-python-code-style.mdc globs **/*.py
    └── magicsquare-ecb-architecture.mdc  globs src/**, tests/**
```

**원칙:** Report 01/02 = 도메인 SSOT · `.mdc` = AI 행동 SSOT · `.cursorrules` = 진입점.

---

## 3) 파일별 역할

| 파일 | alwaysApply | globs | 이전 `.cursorrules` 섹션 |
|------|-------------|-------|-------------------------|
| `magicsquare-project.mdc` | true | — | `project`, `ai_behavior` |
| `magicsquare-forbidden.mdc` | true | — | `forbidden` |
| `magicsquare-tdd-testing.mdc` | true | — | `tdd_rules`, `testing` |
| `magicsquare-python-code-style.mdc` | false | `**/*.py` | `code_style` |
| `magicsquare-ecb-architecture.mdc` | false | `src/**`, `tests/**` | `architecture`, `file_structure` |

### alwaysApply 3개를 쓰는 이유

- `src/`만 열고 `tests/`를 열지 않아도 **RED 없이 구현 금지·테스트 약화 금지**가 적용되어야 함.
- TDD phase·forbidden은 코드 편집과 무관하게 항상 유효.

### globs 2개를 쓰는 이유

- `Report/*.md` 편집 시 ECB·PEP8 노이즈 감소.
- Python·레이어 코드 작업 시에만 상세 스타일·구조 규칙 활성화.

---

## 4) `.cursorrules` 슬림화

**유지:** `project` 메타, `contract` 3항, `branch_flow`, `rules_location`, `rules_index` 표.

**제거:** `code_style`, `architecture`, `tdd_rules`, `testing`, `forbidden`, `file_structure`, `ai_behavior` 본문 (`.mdc`로 이전).

**효과:** 약 176줄 → 약 40줄; 이중 적용 방지.

---

## 5) SSOT·중복 정책

| 주제 | 단일 출처 |
|------|-----------|
| 금지 패턴 (print, bare except, test skip) | `magicsquare-forbidden.mdc` |
| Red/Green/Refactor phase | `magicsquare-tdd-testing.mdc` |
| 입출력 계약 요약 | `.cursorrules` + 상세는 Report 02 |
| ECB 의존 방향 | `magicsquare-ecb-architecture.mdc` |
| `[TDD WARNING]` 동작 | `magicsquare-project.mdc` |

Phase별 `must_not`은 **짧은 bullet**만 두고, 상세 금지는 forbidden 파일을 참조한다.

---

## 6) Phase 2 확장 (미적용 · 권장 시점)

Report 02 본격 구현 시 파일이 50줄을 넘기면 분리:

| 추가 파일 | globs | 시점 |
|-----------|-------|------|
| `magicsquare-entity.mdc` | `src/entity/**`, `tests/entity/**` | `DT-*` 슬라이스 본격화 |
| `magicsquare-boundary.mdc` | `src/boundary/**`, `tests/boundary/**` | `UT-*` + 고정 Error 문구 |

현재 5파일 구성으로 `User` entity + pytest 8건 검증 완료.

---

## 7) 검증

| 항목 | 결과 |
|------|------|
| `.cursorrules` YAML 파싱 | OK |
| `pytest tests/entity/test_user.py` | 8 passed |
| `.cursor/rules/` README | 없음 (정책 준수) |
| Report 01~03 내용 변경 | 없음 (04가 규칙 구조만 다룸) |

### Cursor IDE 수동 확인 (권장)

1. Settings → Rules에서 5개 규칙 표시 여부  
2. `src/entity/user.py` 열고 ECB·Python 규칙 반영 질의  
3. “MagicGrid 구현” 요청 시 테스트 선행 제안 여부  

---

## 8) Report 01~04 관계

| Report | 역할 |
|--------|------|
| 01 | 문제 정의 · I1~I5 |
| 02 | Dual-Track 설계 · DT/UT 계약 |
| 03 | `.cursorrules` YAML 완성 · `User` entity kickoff |
| **04** | **규칙 이중 레이어 (`.mdc` migration)** |

도메인·테스트 명세 변경은 **02 우선**; AI 코딩 규칙 변경은 **04 + `.mdc`**.

---

## 9) 다음 단계

1. `red` 브랜치에서 `DT-E01` RED 테스트 추가  
2. Cursor에서 규칙 적용 동작 샘플 1회 기록 (선택)  
3. 필요 시 `magicsquare-entity.mdc` 분리 (Phase 2)  
4. CI에 pytest + coverage gate 연동 (Report 02 RG-05)

---

## 10) 문서 이력

| 버전 | 날짜 | 변경 |
|------|------|------|
| 1.0 | 2026-05-28 | `.cursor/rules` 5파일 생성 · `.cursorrules` 슬림화 |

---

*본 문서는 Cursor 규칙 구조 변경 산출물이며, Report 02 도메인 계약을 수정하지 않는다.*
