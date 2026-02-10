from __future__ import annotations

import builtins
import io

import table_stats


def test_compute_overall_accuracy_no_fs(monkeypatch):
    outputs_content = "\n".join(
        [
            '{"Category": "lab test", "Result": "Correct"}',
            '{"Category": "lab test", "Result": "Incorrect"}',
            '{"Category": "risk", "Result": "Correct"}',
        ]
    )

    def fake_open(path, mode="r", *args, **kwargs):
        if "outputs/" in path and "r" in mode:
            return io.StringIO(outputs_content)
        if "results/" in path and ("w" in mode or "a" in mode):
            return io.StringIO()
        return builtins.open(path, mode, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", fake_open)
    monkeypatch.setattr(table_stats.os.path, "exists", lambda path: True)
    monkeypatch.setattr(table_stats.os, "makedirs", lambda *args, **kwargs: None)

    stats = table_stats.compute_overall_accuracy("dummy.jsonl", "model/name", "prompt")
    assert stats["lab test"]["average"] == 50.0
    assert stats["risk"]["average"] == 100.0
    assert "overall" in stats
