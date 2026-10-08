"""Read-only review probes. No GPU, network, or external service calls."""
import contextlib
import importlib.util
import io
import json
import math
from pathlib import Path
import statistics
import sys
import tempfile
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
TUNE = ROOT / "repositories/Apex-Tune-results"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


results = {}
sld = load("sld_review", TUNE / "sldbench/evaluate.py")
with patch.object(sld.subprocess, "run", return_value=SimpleNamespace(
    returncode=1, stdout="Combined Score: 0.99\n", stderr="late failure"
)):
    result = sld.run_subtask("parallel", sld.SUBTASKS["parallel"])
    assert result["returncode"] == 1 and result["score"] == 0.99
    results["sld_nonzero_exit_still_has_score"] = {k: result[k] for k in ("returncode", "score")}


def fake_subtask(name, spec):
    return {"task": name, "returncode": 0 if name == "parallel" else 1,
            "score": 0.999989 if name == "parallel" else None,
            "stderr": "" if name == "parallel" else "mock evaluator failure"}


with tempfile.TemporaryDirectory() as tmp:
    out = Path(tmp) / "scores.json"
    with patch.object(sld, "run_subtask", side_effect=fake_subtask), patch.object(
        sys, "argv", ["evaluate.py", "--output", str(out)]
    ), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        sld.main()
    report = json.loads(out.read_text())
    assert report["suite_mean"] == 0.999989
    results["sld_three_failed_tasks"] = {"suite_mean": report["suite_mean"], "failed_tasks": 3,
                                          "main_returned_normally": True}

bench = load("bench_review", TUNE / "mls-bench_fused_attention/bench.py")
with patch.object(bench, "run_one", return_value={"returncode": 1, "crash": True, "wall_s": 0.1}):
    try:
        bench.bench(TUNE / "mls-bench_fused_attention/submission.py", 64, runs=1)
    except KeyError as exc:
        assert str(exc) == "'max_diff'"
        results["mls_crash_reporting"] = {"exception": "KeyError: max_diff"}
    else:
        raise AssertionError("Expected missing max_diff to break summary")

summary = json.loads((TUNE / "nanochat_autoresearch/results/summary.json").read_text())
values = list(summary["seeds"].values())
results["nanochat_recalculated"] = {"n": len(values), "mean": statistics.mean(values),
                                      "sample_std": statistics.stdev(values)}
assert abs(statistics.mean(values) - summary["statistics_10_seed"]["mean_val_bpb"]) < 1e-7
results["nan_comparison_guard"] = {"nan_gt_threshold": float("nan") > 1e-2,
                                     "finite_guard_needed": True}
# Analytic FP16 overflow witness for the unshifted exp -> FP16 path.
# q=k=2, head dimension 64 -> scaled dot product 32. This is not a GPU reproduction.
results["attention_numeric_witness"] = {"scaled_logit": 32, "exp_logit": math.exp(32),
                                         "fp16_max": 65504, "gpu_executed": False}
print(json.dumps(results, indent=2))
