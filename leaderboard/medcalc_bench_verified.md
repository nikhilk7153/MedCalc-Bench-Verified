# MedCalc-Bench Verified — SOTA Evidence

Last updated: 2026-02-10

Scope note:
- The MedCalc-Bench Verified dataset card documents dataset composition (train/test sizes and fields) but does not report benchmark scores as of 2026-01-30.
- Evidence below mixes MedCalc-Bench (original) and cleaned/restructured variants. Scores are not directly comparable across dataset versions or evaluation protocols.
- Added in-repo runs from branch `original` (GLM-4.6v/GLM-4.7 and Oracle replay). Subsample and replay rows are diagnostic and not head-to-head with full-test results.
- Table sorted by score (descending). Rows with ranges are sorted by the first value in the range.

## Evidence Table (sorted by score)

| Approach category | Date (pub) | Source | Dataset variant | Model/System | Setting | Metric | Score | Evidence/Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| In-repo Oracle replay (extrapolated full-test) | 2026-02-05 | This repository (`original` branch artifacts) | MedCalc-Bench Verified (extrapolated to test n=1,100) | GPT-5.2-Thinking xhigh (Oracle) | Assume all GLM-4.6v-correct rows remain correct, plus Oracle fixes on the 198-row incorrect subset | Accuracy | 94.73%* | Derived as (902 + 140) / 1100 using `results_glm-4.6v_encounter_cot_full_v2.csv` and `results_oracle_52thinking_v2_incorrect198.csv`. |
| In-repo prompted evaluation | 2026-02-03 | This repository (`original` branch artifacts) | MedCalc-Bench Verified (stratified 25% subset; n=275) | GLM-4.7 | `calc_spec` prompt | Accuracy | 85.45% | `evaluation/results/results_glm-4.7_calc_spec_full.csv` and `evaluation/results/results_glm-4.7_calc_spec_full.json` (235/275 correct). |
| In-repo prompted evaluation | 2026-02-03 | This repository (`original` branch artifacts) | MedCalc-Bench Verified (stratified 25% subset; n=275) | GLM-4.7 | `encounter_cot_full_v2` prompt | Accuracy | 84.00% | `evaluation/results/results_glm-4.7_encounter_cot_full_v2.csv` and `evaluation/results/results_glm-4.7_encounter_cot_full_v2.json` (231/275 correct). |
| In-repo prompted evaluation | 2026-02-03 | This repository (`original` branch artifacts) | MedCalc-Bench Verified (test n=1,100) | GLM-4.6v | `encounter_cot_full_v2` prompt | Accuracy | 82.00% | `evaluation/results/results_glm-4.6v_encounter_cot_full_v2.csv` and `evaluation/results/results_glm-4.6v_encounter_cot_full_v2.json` (902/1100 correct). |
| In-repo prompted evaluation | 2026-02-03 | This repository (`original` branch artifacts) | MedCalc-Bench Verified (test n=1,100) | GLM-4.6v | `calc_spec` prompt | Accuracy | 81.45% | `evaluation/results/results_glm-4.6v_calc_spec_full.csv` and `evaluation/results/results_glm-4.6v_calc_spec_full.json` (896/1100 correct). |
| RL with verifiable rewards | 2025-09-19 | MedCalc-R1 (OpenReview; ICLR 2026 submission, withdrawn) | MedCalc-Bench (train/test 9,765/1,048) | DeepSeek-R1 | SFT + GRPO with formula-verification rewards | Avg accuracy | 73.95 | https://openreview.net/pdf?id=kKvEleeIsa |
| RL fine-tuning on recomputed labels | 2026-01-21 | Scalably Enhancing the Clinical Validity of a Task Benchmark with Physician Oversight (arXiv v2) | MedCalc-Bench (recomputed labels; test n=1,047) | Qwen3-8B | GRPO RL trained on recomputed labels | Test accuracy | 71.4% | https://arxiv.org/pdf/2512.19691 |
| In-repo Oracle replay (diagnostic subset) | 2026-02-05 | This repository (`original` branch artifacts) | MedCalc-Bench Verified (198-row subset where GLM-4.6v `encounter_cot_full_v2` was incorrect) | Oracle 5.2 Thinking | Replay with `encounter_cot_full_v2` prompt | Accuracy | 70.71% | `evaluation/results/results_oracle_52thinking_v2_incorrect198.csv` and `evaluation/results/results_oracle_52thinking_v2_incorrect198_summary.json` (140/198 correct). |
| RL with verifiable rewards | 2025-09-19 | MedCalc-R1 (OpenReview; ICLR 2026 submission, withdrawn) | MedCalc-Bench (train/test 9,765/1,048) | o1-mini | SFT + GRPO with formula-verification rewards | Avg accuracy | 67.84 | https://openreview.net/pdf?id=kKvEleeIsa |
| Tool/agent framework | 2025-03-05 | RiskAgent (arXiv v1) | MedCalc-Bench (external evaluation) | RiskAgent-GPT-4o | Zero-shot CoT; tool-driven calculator execution | Overall accuracy | 67.71 | https://arxiv.org/pdf/2503.03802 |
| Extended thinking + tool use | 2026-01-11 | Anthropic healthcare & life sciences announcement | MedCalc Bench (company eval) | Claude Opus 4.5 | Extended thinking (64k tokens) + native tool use; Python code execution | Accuracy | 61.3% | https://www.anthropic.com/news/healthcare-life-sciences?p=2 (figure); https://www-cdn.anthropic.com/images/4zrzovbb/website/9de13efd2402bda97dfb174739633ef598c3b59a-1920x1080.png |
| Step-wise eval diagnostic | 2025-11 | From Scores to Steps (EMNLP 2025) | Cleaned & restructured MedCalc-Bench | GPT-4o | Step-wise evaluation vs final-answer | Accuracy (drops) | 62.7% → 43.6% | https://aclanthology.org/2025.emnlp-main.548.pdf |
| Agentic pipeline + step-wise eval | 2025-11 | From Scores to Steps (EMNLP 2025) | Cleaned & restructured MedCalc-Bench | MedRaC | Retrieval + Python; no fine-tuning | Accuracy under step-wise eval | up to 53.19% | https://aclanthology.org/2025.emnlp-main.548.pdf |
| RL with verifiable rewards | 2025-09-19 | MedCalc-R1 (OpenReview; ICLR 2026 submission, withdrawn) | MedCalc-Bench (train/test 9,765/1,048) | MedCalc-R1 (3B) | SFT + GRPO with formula-verification rewards | Avg accuracy | 51.34 | https://openreview.net/pdf?id=kKvEleeIsa |
| Prompting baseline | 2024-06-17 | MedCalc-Bench paper (arXiv v4) | MedCalc-Bench (orig; test 1,047) | GPT-4 | One-shot CoT | Avg accuracy (exact for rule-based; ±5% for equation-based) | 50.9% | https://arxiv.org/abs/2406.12036 |
| Supervised fine-tuning | 2024 | MedCalc-Bench NeurIPS 2024 supplemental | MedCalc-Bench (orig; train split) | Mistral-7B | SFT on MedCalc-Bench train | Accuracy | 49.19% | Baseline 10.79% in same source: https://papers.nips.cc/paper_files/paper/2024/file/99e81750f3fdfcaf9613db2dbf4bd623-Supplemental-Datasets_and_Benchmarks_Track.pdf |
| Code-exec prompting | 2024 | MedCalc-Bench NeurIPS 2024 supplemental | MedCalc-Bench (orig) | GPT-4 | Zero-shot CoT + code interpreter prompt | Accuracy | 48.51% | https://papers.nips.cc/paper_files/paper/2024/file/99e81750f3fdfcaf9613db2dbf4bd623-Supplemental-Datasets_and_Benchmarks_Track.pdf |
| Supervised fine-tuning | 2024 | MedCalc-Bench NeurIPS 2024 supplemental | MedCalc-Bench (orig; train split) | Llama-2-7B | SFT on MedCalc-Bench train | Accuracy | 45.75% | Baseline 1.53% in same source: https://papers.nips.cc/paper_files/paper/2024/file/99e81750f3fdfcaf9613db2dbf4bd623-Supplemental-Datasets_and_Benchmarks_Track.pdf |
| Code-exec prompting | 2024 | MedCalc-Bench NeurIPS 2024 supplemental | MedCalc-Bench (orig) | GPT-3.5 | Zero-shot CoT + code interpreter prompt | Accuracy | 30.29% | https://papers.nips.cc/paper_files/paper/2024/file/99e81750f3fdfcaf9613db2dbf4bd623-Supplemental-Datasets_and_Benchmarks_Track.pdf |

## Notes
- Dataset card (MedCalc-Bench Verified): https://huggingface.co/datasets/nsk7153/MedCalc-Bench-Verified
- `*` marks a hypothetical extrapolation, not a direct measured full-test run.
