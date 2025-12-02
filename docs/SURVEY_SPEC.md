# Survey specification (summary)

This file summarizes the survey/questionnaire material present in the repo and points to the canonical locations.

Purpose
- Hold the long-form survey/spec content separately from the agent instructions.

Where the canonical code lives
- Entrance and dimension questions: `surveys/entrance_questions.py` and `surveys/dimension_*_*.py`
- Validator helpers: `surveys/validator.py`
- BibTeX sources: `surveys/bibtex_sources.bib`

Notes for contributors
- Keep all question text and scales inside `surveys/` files (not in docs) so code and tests can import them.
- When changing question IDs or scales update `analysis/calculate_5d_scores.py` and tests under `tests/`.

Example structure (already in `surveys/`):

- `entrance_questions.py`: demographic/entrance schema (Likert scales, coded options)
- `dimension_1_neurobiology.py` … `dimension_5_technology.py`: at least 10 items per dimension

Privacy / Ethics
- Follow `storage/anonymize.py` when storing or processing responses. No PII must be persisted.

If you want the full original, long survey spec (previously embedded in `.github/copilot-instructions.md`), tell me and I will extract it verbatim into this file.
