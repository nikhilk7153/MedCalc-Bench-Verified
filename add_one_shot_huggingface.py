from __future__ import annotations

import json
from collections import defaultdict
from typing import Any

import requests
from datasets import Dataset, Features, Value, concatenate_datasets, load_dataset

# Hard-coded source JSON (raw GitHub URL)
SRC_URL = "https://raw.githubusercontent.com/nikhilk7153/MedCalc-Bench-Verified/main/evaluation/one_shot_finalized_explanation.json"

# Only exception: Calculator ID 24 (question collisions in HF dataset)
QUESTION_OVERRIDE_BY_CALC_ID: dict[int, str] = {
    24: "Based on the patient's dose of Hydrocortisone IV, what is the equivalent dosage in mg of Dexamethasone PO?",
}

def download_json(url: str) -> Any:
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    return r.json()


def make_features() -> Features:
    return Features(
        {
            "Row Number": Value("int64"),
            "Calculator ID": Value("int64"),
            "Calculator Name": Value("string"),
            "Category": Value("string"),
            "Output Type": Value("string"),
            "Note ID": Value("string"),
            "Note Type": Value("string"),
            "Patient Note": Value("string"),
            "Question": Value("string"),
            "Relevant Entities": Value("string"),
            "Ground Truth Answer": Value("string"),
            "Lower Limit": Value("string"),
            "Upper Limit": Value("string"),
            "Ground Truth Explanation": Value("string"),
        }
    )


def load_hf_mappings() -> tuple[
    dict[int, str],  # id_to_name
    dict[int, str],  # id_to_question (only for non-override IDs)
    dict[int, int],  # id_to_total_rows
    dict[int, int],  # id_to_num_unique_questions
]:
    """
    From nsk7153/MedCalc-Bench-Verified:
      - Calculator ID -> Calculator Name  (must be unique for every ID)
      - Calculator ID -> Question         (must be unique for every ID except overrides)
    """
    hf = load_dataset("nsk7153/MedCalc-Bench-Verified")
    base = concatenate_datasets([hf[s] for s in hf.keys()])

    id_to_names: dict[int, set[str]] = defaultdict(set)
    id_to_questions: dict[int, set[str]] = defaultdict(set)
    id_to_total_rows: dict[int, int] = defaultdict(int)

    for ex in base:
        cid = int(ex["Calculator ID"])
        id_to_total_rows[cid] += 1
        id_to_names[cid].add(ex["Calculator Name"])
        id_to_questions[cid].add(ex["Question"])

    # Validate / finalize name mapping
    id_to_name: dict[int, str] = {}
    for cid, names in id_to_names.items():
        if len(names) != 1:
            raise ValueError(f"Non-unique Calculator Name for ID={cid}: {sorted(names)}")
        id_to_name[cid] = next(iter(names))

    id_to_num_unique_questions = {cid: len(qs) for cid, qs in id_to_questions.items()}

    # Validate / finalize question mapping, allowing overrides
    id_to_question: dict[int, str] = {}
    for cid, qs in id_to_questions.items():
        if cid in QUESTION_OVERRIDE_BY_CALC_ID:
            # We'll always use the override for this ID.
            continue
        if len(qs) != 1:
            raise ValueError(
                f"Expected 1 unique question for Calculator ID={cid}, got {len(qs)}.\n"
                "If this is a known exception, add it to QUESTION_OVERRIDE_BY_CALC_ID."
            )
        id_to_question[cid] = next(iter(qs))

    return (
        id_to_name,
        id_to_question,
        dict(id_to_total_rows),
        dict(id_to_num_unique_questions),
    )


def print_question_counts_per_id(
    id_to_total_rows: dict[int, int],
    id_to_num_unique_questions: dict[int, int],
) -> None:
    """Counts-only table (no example lines)."""
    print("\n=== Question counts per Calculator ID (from HF dataset) ===")
    print("Calculator ID | #rows | #unique_questions | collision")
    print("-" * 60)

    for cid in sorted(id_to_total_rows.keys()):
        total = id_to_total_rows[cid]
        n_uq = id_to_num_unique_questions.get(cid, 0)
        collision = "YES" if n_uq > 1 else ""
        print(f"{cid:12d} | {total:5d} | {n_uq:17d} | {collision}")

    n_collisions = sum(1 for n in id_to_num_unique_questions.values() if n > 1)
    print(f"\nIDs with >1 unique question: {n_collisions}\n")
    print(f"Mapping overrides: {QUESTION_OVERRIDE_BY_CALC_ID}\n")


def build_dataset(id_to_name: dict[int, str], id_to_question: dict[int, str]) -> Dataset:
    outer = download_json(SRC_URL)
    if not isinstance(outer, dict):
        raise TypeError(f"Expected top-level JSON object (dict), got {type(outer)}")

    def key_sort(k: str) -> int:
        try:
            return int(k)
        except ValueError:
            return 10**18

    rows: list[dict[str, Any]] = []
    for row_num, calc_id_str in enumerate(sorted(outer.keys(), key=key_sort), start=1):
        try:
            calc_id = int(calc_id_str)
        except ValueError:
            continue

        inner = outer.get(calc_id_str) or {}
        resp = inner.get("Response") or {}

        patient_note = inner.get("Patient Note") or inner.get("patient_note")
        gt_answer = resp.get("answer")
        gt_expl = resp.get("step_by_step_thinking")
        input_params = inner.get("input_parameters")

        relevant_entities = (
            None if input_params is None else json.dumps(input_params, ensure_ascii=False)
        )

        if calc_id not in id_to_name:
            raise KeyError(f"Calculator ID {calc_id} not found in HF dataset")
        calc_name = id_to_name[calc_id]

        # Question: use override for 24, otherwise 1:1 mapping by calc_id
        question = QUESTION_OVERRIDE_BY_CALC_ID.get(calc_id)
        if question is None:
            if calc_id not in id_to_question:
                raise KeyError(
                    f"Calculator ID {calc_id} has no unique Question mapping. "
                    "If this is an exception like 24, add an override."
                )
            question = id_to_question[calc_id]

        rows.append(
            {
                "Row Number": row_num,
                "Calculator ID": calc_id,
                "Calculator Name": calc_name,
                "Category": None,
                "Output Type": None,
                "Note ID": None,
                "Note Type": None,
                "Patient Note": patient_note,
                "Question": question,
                "Relevant Entities": relevant_entities,
                "Ground Truth Answer": None if gt_answer is None else str(gt_answer),
                "Lower Limit": None,
                "Upper Limit": None,
                "Ground Truth Explanation": gt_expl,
            }
        )

    return Dataset.from_list(rows, features=make_features())


def main():
    id_to_name, id_to_question, id_to_total_rows, id_to_num_unique_questions = (
        load_hf_mappings()
    )
    print_question_counts_per_id(id_to_total_rows, id_to_num_unique_questions)

    ds = build_dataset(id_to_name=id_to_name, id_to_question=id_to_question)

    out_path = "one-shot.json"
    with open(out_path, "w", encoding="utf-8") as f:
        rows = ds.to_list()
        for row in rows:
            v = row.get("Relevant Entities")
            if isinstance(v, str) and v:
                try:
                    # Aesthetics only: in the HF Dataset schema this column is a JSON-encoded string,
                    # but for the exported one-shot.json we decode it so it appears as a nested object.
                    # This preserves the exact same information; it just avoids lots of escaped quotes.
                    row["Relevant Entities"] = json.loads(v)
                except json.JSONDecodeError:
                    pass

        json.dump(rows, f, ensure_ascii=False, indent=2)
    print(f"\nWrote {len(ds)} rows to {out_path}\n")
    


if __name__ == "__main__":
    main()