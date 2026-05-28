# Magic Square 4×4 — Prompt & Transcript (04 · Cursor Rules Migration)

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_ |
| 짝 | [Report/04_Magic-Square-Cursor-Rules-Migration-Report.md](../Report/04_Magic-Square-Cursor-Rules-Migration-Report.md) |
| Export | 2026-05-28 |
| 형식 | **User** / **Cursor** 대화 + 실행 프롬프트 요약 |
| 선행 | [03](./03_Magic-Square-Phase03-Cursorrules-Prompt.md) (Turn 19~27) |

**선행 Turn:** 01~18 → Prompting 01·02 · 19~27 → Prompting 03 · **28~32 → 본 파일**

---

## 목차

1. [대화 Transcript (Turn 28~32)](#대화-transcript-turn-2832)
2. [실행 프롬프트 요약](#실행-프롬프트-요약)

---

# 대화 Transcript (Turn 28~32)

| Turn | 주제 | 산출물 |
|------|------|--------|
| 28 | `.mdc` 확장 **전략** (코드 없음) | 5파일 매핑, alwaysApply/globs, 마이그레이션 Phase A~D |
| 29 | 전략 실행 승인 | “이렇게 진행해보자” |
| 30 | `.cursor/rules` 5파일 + 슬림 `.cursorrules` | `magicsquare-*.mdc`, 인덱스 ~40줄 |
| 31 | Report 03 export (이전 요청) | `Report/03`, `Prompting/03` |
| 32 | Report 04 · Prompting 04 · README 01~04 | 본 파일, `Report/04`, README 갱신 |

---

## Turn 28 — `.mdc` 확장 전략

**User:** 아래 구조로 Cursor 규칙 확장하고 싶다. 코드 작성 말고 전략만.

```text
MagicSquare_/
├── .cursorrules
└── .cursor/rules/
    ├── magicsquare-ecb-architecture.mdc
    ├── magicsquare-forbidden.mdc
    ├── magicsquare-project.mdc
    ├── magicsquare-python-code-style.mdc
    └── magicsquare-tdd-testing.mdc
```

**Cursor (요약):**

- **이중 레이어:** `.mdc` = 실행 SSOT, `.cursorrules` = 인덱스·계약 요약.
- **5파일 매핑:** project+ai_behavior, forbidden, tdd+testing, code_style (`**/*.py`), architecture+file_structure (`src/**`, `tests/**`).
- **alwaysApply:** project, forbidden, tdd-testing (3개).
- **금지:** 176줄 YAML과 `.mdc` **동시 풀텍스트** 유지.
- **마이그레이션:** Phase A 골격 → B 섹션 이전 → C 검증 → D 문서 정리.
- **Phase 2:** 필요 시 `magicsquare-entity.mdc`, `magicsquare-boundary.mdc` 분리.

---

## Turn 29 — 실행 승인

**User:** 이렇게 진행해보자.

**Cursor:** (Turn 30에서 구현 예정)

---

## Turn 30 — 마이그레이션 구현

**User:** (Turn 29 승인에 따른 구현)

**Cursor:**

| 생성/변경 | 내용 |
|-----------|------|
| `.cursor/rules/magicsquare-project.mdc` | alwaysApply — 프로젝트, 계약, AI workflow |
| `.cursor/rules/magicsquare-forbidden.mdc` | alwaysApply — 7개 금지 패턴 |
| `.cursor/rules/magicsquare-tdd-testing.mdc` | alwaysApply — red/green/refactor, pytest AAA |
| `.cursor/rules/magicsquare-python-code-style.mdc` | globs `**/*.py` |
| `.cursor/rules/magicsquare-ecb-architecture.mdc` | globs `src/**`, `tests/**` |
| `.cursorrules` | 176줄 → ~40줄 `rules_index` |
| `README.md` | `.cursor/rules/` 구조 반영 |

- pytest `tests/entity/test_user.py`: **8 passed**.

---

## Turn 31 — (참고) Phase 03 export

**User:** Report 생성 + Prompting transcript (Turn 27).

**Cursor:** `Report/03`, `Prompting/03` — Turn 19~27 범위.

---

## Turn 32 — Report 04 · Export · README

**User:**

1. Report 폴더에 보고서 생성  
2. 프롬프트 전체 대화형 Export (Prompting)  
3. README Report 01~04 미반영분 업데이트  

**Cursor:** `Report/04`, 본 파일, README Phase 04·문서 링크·진행 현황 갱신.

---

# 실행 프롬프트 요약

## A. `.mdc` 확장 전략 (Turn 28)

```
MagicSquare: .cursorrules 유지 + .cursor/rules/ 아래 5개 mdc.
코드 작성 없이 전략만: 매핑, alwaysApply vs globs, SSOT, 마이그레이션 단계,
.cursorrules 슬림화, Phase 2 entity/boundary 분리 시점.
```

## B. 마이그레이션 실행 (Turn 29~30)

```
전략대로 5개 magicsquare-*.mdc 생성.
.cursorrules는 project+contract+rules_index만.
YAML 본문 섹션 삭제(중복 방지). README 구조 반영.
```

## C. Export (Turn 32)

```
Report/04 마이그레이션 보고서.
Prompting/04 Turn 28~32 transcript.
README Phase 01~04 테이블·링크·이력 동기화.
```

---

*End of 04.*
