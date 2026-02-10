# Run Manifest (GLM + Oracle)

This file pins the exact runner/job/prompt combinations for the runs used in the reported ballpark metrics.

## Runners

- GLM runs: `evaluation/eval-46v-queue.py`
- GLM postprocess: `evaluation/postprocess_46v_run.py`
- Oracle run IDs listed for traceability only (no Oracle runner code included in this package).

## GLM-4.6v (full test set: 1100 rows)

- 81.45% (`896/1100`) :
  - prompt: `calc_spec`
  - run_id: `20260202T212511Z_glm-4.6v_calc_spec_calc_spec`
  - run metadata: `evaluation/results/selected_run_metadata.json`
  - summary: `evaluation/results/results_glm-4.6v_calc_spec_full.json`

- 51.91% (`571/1100`) :
  - prompt: `mistral_zero_shot`
  - run_id: `20260203T212022Z_glm-4.6v_mistral_zero_shot_mistral_zero_shot`
  - run metadata: `evaluation/results/selected_run_metadata.json`
  - summary: `evaluation/results/results_glm-4.6v_mistral_zero_shot.json`

- Third set (same model, alternate prompt):
  - 82.00% (`902/1100`)
  - prompt: `encounter_cot_full_v2`
  - run_id: `20260203T202955Z_glm-4.6v_encounter_cot_full_v2_encounter_cot_full_v2`
  - run metadata: `evaluation/results/selected_run_metadata.json`
  - summary: `evaluation/results/results_glm-4.6v_encounter_cot_full_v2.json`

## GLM-4.7 (subsampled set: 275 rows; strict sequential)

- 85.45% (`235/275`) :
  - prompt: `calc_spec`
  - run_id: `20260203T220328Z_glm-4.7_calc_spec_calc_spec_sub25`
  - run metadata: `evaluation/results/selected_run_metadata.json`
  - summary: `evaluation/results/results_glm-4.7_calc_spec_full.json`

- 36.00% (`99/275`) :
  - prompt: `mistral_zero_shot`
  - run_id: `20260204T084309Z_glm-4.7_mistral_zero_shot_mistral_zero_shot_sub25`
  - run metadata: `evaluation/results/selected_run_metadata.json`
  - summary: `evaluation/results/results_glm-4.7_mistral_zero_shot.json`

- Third set (same model, alternate prompt):
  - 84.00% (`231/275`)
  - prompt: `encounter_cot_full_v2`
  - run_id: `20260204T162646Z_glm-4.7_encounter_cot_full_v2_encounter_cot_full_v2_sub25`
  - run metadata: `evaluation/results/selected_run_metadata.json`
  - summary: `evaluation/results/results_glm-4.7_encounter_cot_full_v2.json`

## Oracle run IDs (results-only package in PR C)

- primary completed run: `20260204_oracle_52thinking_v2_incorrect198`
- earlier partial run: `20260203_oracle_52thinking_v2_incorrect198`
- consolidated summary (completed run): `evaluation/results/results_oracle_52thinking_v2_incorrect198_summary.json`

## Job manifests used

- GLM-4.6v two-job pack (mistral + v2): `evaluation/jobs/queue_mistral_and_new.json`
- GLM-4.7 sub25 sequential pack: `evaluation/jobs/queue_glm47_sub25.json`

## 4.7 sequential guardrail

`queue_glm47_sub25.json` enforces:

- `workers=1`
- `max_inflight=1`

which keeps GLM-4.7 requests fully sequential.
