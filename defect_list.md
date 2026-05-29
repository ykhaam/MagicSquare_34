# Defect List — MagicSquare_ (Dual-Track TDD)

| 항목 | 내용 |
|------|------|
| **문서 버전** | 1.0 |
| **기준 브랜치** | `feature/dual-track-tdd` |
| **관련 AC** | AC-FR01-01 (Boundary invalid size) |
| **관련 테스트** | `tests/boundary/test_validate_size.py` |
| **최종 갱신** | 2026-05-29 |

> 본 목록은 RED 단계에서 확인된 pytest 실패·차단 이슈를 기록합니다.  
> TDD RED 의도(import 실패)와 GREEN 미착수로 인한 **구현 결함**을 구분해 표기합니다.

---

## 결함 요약

| 상태 | 건수 |
|------|------|
| Open | 4 |
| Fixed | 0 |
| Won't Fix (RED 의도) | 0 |

---

## 결함 상세

| ID | Severity | AC ID | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 |
|----|----------|-------|-----------|--------|--------|-----------|-----------|
| DEF-001 | Critical | AC-FR01-01 | `python -m pytest tests/boundary/test_validate_size.py -v` 실행 | `MagicSquareBoundary`, `ErrorResponse` import 성공 후 테스트 수집·실행 | `ModuleNotFoundError: No module named 'boundary.magic_square_boundary'` (`test_validate_size.py:10`) | `src/boundary/` 패키지 미구현 (GREEN 미착수) | `src/boundary/__init__.py`, `schemas.py`, `magic_square_boundary.py` 최소 구현 추가 |
| DEF-002 | Critical | AC-FR01-01 | `python -m pytest --cov=src --cov-report=html` 실행 | 전체 테스트 수집 후 entity 8건 Green + boundary 실행/커버리지 리포트 생성 | 수집 단계 ERROR (exit 2), `htmlcov` 미갱신 | DEF-001 파생 — boundary import 실패로 suite 중단 | DEF-001 해소 후 전체 pytest 재실행 |
| DEF-003 | Major | AC-FR01-01 | RED 테스트 `EXPECTED_CODE` vs PRD §13 Error Policy 대조 | PRD SSOT: `code="UI_INVALID_SIZE"` | 테스트·README: `code="INVALID_SIZE"` | PRD(§10, §13)와 RED 테스트 계약 문자열 불일치 | GREEN 통과 후 별도 Red 슬라이스에서 코드명 정렬 또는 테스트/PRD 중 SSOT 확정 |
| DEF-004 | Info | AC-FR01-01 | `tests/boundary/` 8건 대비 `src/boundary/` 파일 존재 여부 확인 | Boundary size 검증 분기 구현 | `src/boundary/` 디렉터리 없음 (0 files) | Track A RED만 작성, Track A GREEN 미시작 | DEF-001과 동일 — Boundary 최소 GREEN 착수 |
| DEF-005 | Info | — (Track B) | README RED To-Do TC-B-01~04 및 Report 02 DT-E01 대조 | `tests/entity/test_magic_grid.py` RED 존재 | Domain Track B RED 테스트 파일 없음 | Dual-Track RED 슬라이스 Track A만 진행 | Track B RED (`DT-E01`) 별도 커밋으로 추가 (AC-FR01-01 범위 유지) |

---

## pytest 로그 스냅샷 (DEF-001 / DEF-002)

```
ERROR collecting tests/boundary/test_validate_size.py
tests\boundary\test_validate_size.py:10: in <module>
    from boundary.magic_square_boundary import MagicSquareBoundary
E   ModuleNotFoundError: No module named 'boundary.magic_square_boundary'

!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
exit code: 2
```

---

## AC-FR01-01 슬라이스 — 테스트별 실행 상태

| Test-ID (파일 내) | 상태 | 차단 결함 |
|-------------------|------|-----------|
| `test_none_grid_returns_invalid_size_failure` | Blocked | DEF-001 |
| `test_empty_list_returns_invalid_size_failure` | Blocked | DEF-001 |
| `test_ragged_four_rows_returns_invalid_size_failure` | Blocked | DEF-001 |
| `test_three_by_four_grid_returns_invalid_size_failure` | Blocked | DEF-001 |
| `test_none_grid_resolve_called_zero_times` | Blocked | DEF-001 |
| `test_none_grid_message_exact_prd_match` | Blocked | DEF-001 |
| `test_none_grid_failure_result_is_error_response_type` | Blocked | DEF-001 |
| `test_scope_excludes_ac_fr01_02_to_05_and_fr02_to_fr05` | Blocked | DEF-001 |

> Assertion 실패(`AttributeError`, code/message 불일치)는 **아직 관측되지 않음** — import 단계에서 수집 중단.

---

## 수정 우선순위

1. **DEF-001** — Boundary 최소 GREEN (`grid is None` / size 분기만, `resolve()` 미호출)
2. **DEF-002** — DEF-001 해소 후 전체 pytest + `--cov=src` 재검증
3. **DEF-003** — GREEN Green 후 계약 코드명 SSOT 정렬 (범위 외 AC 선제 구현 금지)
4. **DEF-005** — Track B RED 추가 (선택, Track A Green 이후)

---

## 회귀 확인 체크리스트 (수정 후)

- [ ] `python -m pytest tests/boundary/test_validate_size.py -v` → 8 passed
- [ ] `python -m pytest tests/entity/ -v` → 8 passed (기존 User Green 유지)
- [ ] `python -m pytest --cov=src --cov-report=html` → exit 0, `htmlcov/index.html` 갱신
- [ ] DEF-003 계약 코드명 SSOT 확정 및 문서 동기화

---

## 참고

- `docs/test_plan.md` — UT-E01 / AC-FR01-01 테스트 계획
- `docs/PRD_MagicSquare.md` — FR-01, §13 Error Policy
- `README.md` — RED 단계 To-Do 리스트
