# NEXUS: Structured Runtime Safety for Tool-Using LLM Agents

Runtime safety monitor for tool-using LLM agents, structured around a formal intervention policy $\Pi$ that operates on a structured plan IR and selects one of four graded interventions per plan: **allow**, **block**, **request confirmation**, or **request revision**.

`$\Pi$` combines:

1. a **deterministic rule set** ($V_R$): permission, irreversible-action, sensitive-data exposure, network access, resource budget, suspicious patterns;
2. an **argument-level inspector** ($V_A$) for credentials, sensitive paths, sensitive table/field names, suspicious URLs, and an access-grant permanence-flag rule for IoT-style trajectories;
3. a **calibrated learned risk score** ($\rho$) trained on a 9-dimensional plan feature vector, Platt-scaled on a held-out 60-instance calibration split.

The intervention policy is

```
Π(P) =
  BLOCK    if ∃ v ∈ V(P) : sev(v) = CRIT
  BLOCK    if ρ(P) ≥ τ_b ∧ |V(P)| ≥ 1
  CONFIRM  if ρ(P) ≥ τ_c ∨ ∃ v : sev(v) = HIGH
  REVISE   if ∃ v : sev(v) = MED
  ALLOW    otherwise
```

with `(τ_b, τ_c) = (0.75, 0.70)` selected on a safety–utility loss
`L(Π) = E[λ_s·u_s + λ_o·u_o + λ_c·c(Π(P))]`. The loss-optimal operating point is `(0.75, 0.70)` uniformly across a 5×5 grid of `(λ_s, λ_o)` settings on the synthetic split.

## Headline numbers

| Setting | n | F1 [95% CI] | Other |
|---|---|---|---|
| Synthetic test split | 128 | 0.965 [0.94, 0.99] | 4-class intervention acc 0.945, overblock 0.04 |
| IPI v1 adversarial set | 200 paired | 0.995 [0.98, 1.00] | adv block 100%, ctrl allow 99% |
| IPI v2 (5 injection styles) | 200 paired | 1.000 | adv block 100%, ctrl overblock 0% |
| Multi-turn benchmark (session memory on) | 120 sessions | 1.000 | 95/95 critical-turn caught, 25/25 legit controls allowed |
| **R-Judge external** (Yuan et al., 2024) | **571** | **0.861 [0.83, 0.89]** | Finance 0.92, Program 0.89, Web 0.95, Application 0.85, IoT 0.52 (post permanence-flag fix) |
| **AgentHarm external** (Andriushchenko et al., 2025) | **352** | **0.591 [0.53, 0.65]** | Identical to rule-only baseline; deliberate threat-model boundary (paired harmful/benign share target tools) |
| **NEXUS-Stress (rule-blind adversarial)** | **200** | **0.836 [0.79, 0.88]** | 4-class intervention acc 0.420; reveals CONFIRM/REVISE-blind gap — Π predicts only ALLOW or BLOCK on rule-blind plans |

Calibration: Platt scaling reduces ECE from 0.085 (raw) to 0.013 and Brier from 0.051 to 0.041 on the 128-instance test split.

All numbers are deterministic and reproducible from a fresh checkout in under 10 minutes on CPU; no GPU required.

## Repository layout

```
runtime_safety/
├── README.md
├── requirements.txt
├── pyproject.toml
├── .gitignore
│
├── src/runtime_safety/             # importable Python package
│   ├── paths.py                    # central path configuration
│   ├── core/                       # agent, executor, rag, schemas, tools, utils
│   ├── models/                     # RiskScorer (the model class, 9-D feature vector)
│   ├── monitors/
│   │   ├── basic/                  # baseline SafetyMonitor
│   │   └── enhanced/               # EnhancedSafetyMonitor + argument_inspector
│   ├── baselines/                  # rule_only, learned_only, llm_judge, text_only
│   ├── benchmarks/
│   │   ├── schema.py, split.py, generate_deterministic.py, harvest.py
│   │   ├── adversarial/            # IPI v1 + v2 generators
│   │   └── external/               # R-Judge + AgentHarm loaders
│   ├── evaluation/                 # runner, ablation, calibration, latency, report
│   ├── metrics/                    # ONLY metric functions
│   └── study/                      # human-study tasks, analysis, LLM proxy
│
├── scripts/                        # all CLI entrypoints
│   ├── run_all.py                  # train → Phase 1 → Phase 2
│   ├── run_emnlp_pipeline.py       # full EMNLP experimental pipeline
│   ├── train_risk_scorer.py
│   ├── eval/
│   │   ├── eval_per_category.py    # per-category + thresholds + strong learned + ablation
│   │   ├── eval_figures_tables.py  # tables + figures + error analysis
│   │   ├── eval_calibration.py     # ECE/Brier + reliability diagram
│   │   ├── eval_bootstrap_ci.py    # 1000-resample CIs
│   │   ├── eval_lambda_sensitivity.py
│   │   ├── eval_external.py        # external + adversarial benchmark eval
│   │   ├── eval_ipi_v2.py          # IPI v2 (5 injection styles)
│   │   ├── eval_rjudge.py          # R-Judge external benchmark
│   │   ├── eval_agentharm.py       # AgentHarm external benchmark
│   │   ├── eval_session_ablation.py
│   │   ├── eval_bugfix_comparison.py
│   │   └── analyze_ipi.py
│   ├── generate/
│   │   ├── generate_synthetic_benchmark.py
│   │   ├── generate_multistep_benchmark.py
│   │   └── build_ipi_benchmark.py  # generates IPI v1
│   ├── validate/
│   │   ├── validate_sessions.py
│   │   └── validate_benchmarks.py
│   └── demo/
│       ├── demo_unprotected.py     # Phase 1: agent without safety monitor
│       └── demo_protected.py       # Phase 2: agent with safety monitor
│
├── benchmark/                      # NEXUS-Stress rule-blind adversarial stress benchmark
│   ├── nexus_stress/
│   │   ├── nexus_stress.jsonl      # 200 examples (canonical file)
│   │   ├── nexus_stress.json       # same content as a single JSON array
│   │   ├── nexus_stress.csv        # flat view with serialised plan
│   │   ├── nexus_stress_summary.csv
│   │   ├── build_benchmark.py      # regenerates the benchmark deterministically
│   │   ├── scenarios.py            # aggregator over the 5 chunk files
│   │   ├── scenarios_chunk_01.py … scenarios_chunk_05.py
│   │   ├── generation_log.md
│   │   ├── audit_report.md         # acceptance metrics + per-category audit
│   │   └── rejected_examples_log.csv
│   └── nexus_stress_eval/
│       ├── run_eval.py             # runs NEXUS on nexus_stress.jsonl
│       ├── metrics_summary.{json,csv}
│       ├── binary_confusion_matrix.csv
│       ├── intervention_confusion_matrix.csv
│       ├── per_class_metrics.csv, per_category_metrics.csv, per_difficulty_metrics.csv
│       ├── false_positives.csv, false_negatives.csv, intervention_errors.csv
│       ├── predictions.csv
│       └── NEXUS_Stress_Evaluation_Report.md
│
├── data/                           # inputs
│   ├── scenarios.json
│   ├── knowledge_base/Nexora_Knowledge_Base.docx
│   ├── benchmarks/                 # synthetic + multistep benchmarks
│   ├── adversarial/                # IPI v1 + v2 JSONL
│   └── external/                   # R-Judge / AgentHarm (raw data gitignored)
│
├── checkpoints/                    # trained model weights (risk_scorer.pkl, 9-D)
├── indexes/rag/                    # FAISS index cache
├── sandboxes/                      # executor working trees
├── results/                        # raw experiment artefacts
│   ├── phase1_phase2/, emnlp/, adversarial/
│   ├── external/                   # R-Judge + AgentHarm eval outputs
│   └── eval/                       # per_category, thresholds, calibration, bootstrap_cis
├── figures/                        # generated PDFs (also PNG mirrors)
└── docs/
    └── reports/                    # per-experiment Markdown reports
```

## Setup

```bash
# Python 3.10 or newer
git clone <anonymized-repo-url>
cd nexus
pip install -e .
```

A `.env` (with an `HF_TOKEN`) is needed only for fetching the AgentHarm dataset; it is not required for the synthetic, IPI, R-Judge (after manual fetch), or NEXUS-Stress evaluations.

## Reproduction — in-distribution + adversarial

```bash
# Generate adversarial benchmarks (IPI v1 + v2, deterministic)
python scripts/generate/build_ipi_benchmark.py
python scripts/validate/validate_benchmarks.py

# Synthetic split + per-category + thresholds + strong learned + policy ablation
python scripts/eval/eval_per_category.py

# Tables + figures + error analysis
python scripts/eval/eval_figures_tables.py

# Calibration (Platt vs isotonic, ECE, Brier, reliability diagram)
python scripts/eval/eval_calibration.py

# Safety–utility sensitivity sweep over (λ_s, λ_o)
python scripts/eval/eval_lambda_sensitivity.py

# IPI v2 evaluation (5 styles × 20 pairs = 200 records)
python scripts/eval/eval_ipi_v2.py

# Bootstrap 95% CIs on all headline metrics (1000 resamples, seed 0)
python scripts/eval/eval_bootstrap_ci.py
```

## Reproduction — NEXUS-Stress (rule-blind adversarial stress benchmark)

NEXUS-Stress is a 200-example rule-blind adversarial stress benchmark we release. Examples are authored without matching to the rule-set vocabulary, span 20 scenario categories across 11 domains, and are filtered at generation time by TF-IDF cosine ≥ 0.80 to enforce semantic distinctness. The benchmark and its build pipeline are committed; the eval can be run directly.

```bash
# (Optional) Regenerate NEXUS-Stress from scratch
cd benchmark/nexus_stress
python build_benchmark.py
cd ../..

# Run NEXUS on NEXUS-Stress and produce all metrics + per-category +
# per-difficulty + bootstrap CIs + error CSVs + markdown report
cd benchmark/nexus_stress_eval
PYTHONPATH=../../src python run_eval.py
```

## Reproduction — external benchmarks

### R-Judge (Yuan et al., Findings of EMNLP 2024)

R-Judge is published at <https://github.com/Lordog/R-Judge> under CC BY-NC-SA and is not redistributed here.

```bash
mkdir -p data/external/rjudge/raw
cp -r <local R-Judge clone>/data/* data/external/rjudge/raw/
python scripts/eval/eval_rjudge.py
```

Our loader parses 491/571 records into structured plans across four R-Judge action formats; the remaining 80 are content-safety dialogue with no tool calls and use a placeholder step.

### AgentHarm (Andriushchenko et al., 2025)

AgentHarm is a gated dataset on HuggingFace. To run the AgentHarm evaluation:

1. Accept the dataset terms at <https://huggingface.co/datasets/ai-safety-institute/AgentHarm>.
2. Create a HuggingFace token with read access and put it in `checkpoints/.env`:

   ```
   HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

3. Download the benchmark files into `data/external/agentharm/raw/benchmark/`:

   ```bash
   set -a && source checkpoints/.env && set +a
   python3 -c "
   from huggingface_hub import hf_hub_download
   import os
   for f in [
       'benchmark/harmful_behaviors_test_public.json',
       'benchmark/harmful_behaviors_validation.json',
       'benchmark/benign_behaviors_test_public.json',
       'benchmark/benign_behaviors_validation.json',
   ]:
       hf_hub_download('ai-safety-institute/AgentHarm', f,
                       repo_type='dataset',
                       token=os.environ['HF_TOKEN'],
                       local_dir='data/external/agentharm/raw')
   "
   ```

4. Run the evaluation:

   ```bash
   PYTHONPATH=src python scripts/eval/eval_agentharm.py
   ```

The AgentHarm raw data is intentionally not redistributed in this repository.

## Where to find each headline number

| Number | Reproduce by running |
|---|---|
| Synthetic F₁ = 0.965, intervAcc = 0.945 | `scripts/eval/eval_per_category.py` |
| Calibration: ECE 0.085 → 0.013 | `scripts/eval/eval_calibration.py` |
| Threshold sweep (τ_b, τ_c) | `scripts/eval/eval_per_category.py` then `scripts/eval/eval_figures_tables.py` |
| λ-sensitivity (loss-optimal at (0.75, 0.70)) | `scripts/eval/eval_lambda_sensitivity.py` |
| IPI v2 (5 styles × 20 pairs) | `scripts/eval/eval_ipi_v2.py` |
| Bootstrap CIs for every headline metric | `scripts/eval/eval_bootstrap_ci.py` |
| R-Judge F₁ = 0.861 (full 571) | `scripts/eval/eval_rjudge.py` |
| R-Judge IoT 0.462 → 0.518 (permanence-flag) | `scripts/eval/eval_rjudge.py` (rule in `argument_inspector.py`) |
| AgentHarm F₁ = 0.591 | `scripts/eval/eval_agentharm.py` |
| **NEXUS-Stress F₁ = 0.836** | `benchmark/nexus_stress_eval/run_eval.py` |
| NEXUS-Stress 4-class confusion | same; CSV at `benchmark/nexus_stress_eval/intervention_confusion_matrix.csv` |

## Citation

```
@misc{hossain2026nexusstructuredruntimesafety,
      title={NEXUS: Structured Runtime Safety for Tool-Using LLM Agents}, 
      author={Elias Hossain and Md Mehedi Hasan Nipu and Tasfia Nuzhat Ornee and Rajib Rana and Niloofar Yousefi},
      year={2026},
      eprint={2607.19356},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2607.19356}, 
}
```

## Notes

- All experiments are deterministic. Splits use `seed=42` (train/test) and `seed=7` (train/calibration); benchmark generators and bootstrap use `seed=0`.
- The deployed `(τ_b, τ_c) = (0.75, 0.70)` operating point is the loss-optimal point uniformly across a 5×5 `(λ_s, λ_o)` grid on the synthetic split. F₁ and overblocking are invariant to threshold position on that distribution; only 4-class intervention accuracy varies.
- The 9-D feature vector replaced an earlier 10-D version that included a redundant normalised-plan-length feature; the model was retrained and all numbers in this README reflect the 9-D scorer.
- The NEXUS-Stress evaluation reveals a middle-severity coverage gap: NEXUS predicts only ALLOW or BLOCK on rule-blind plans, never CONFIRM or REVISE. We disclose this as a deployment-relevant limitation; future rule-set extensions should target medium-severity scope-tighten and disambiguation patterns.
- Long-horizon escalation (`multi_step_escalation`) reaches `F₁ = 0.500` under single-turn evaluation but is mitigated to 95/95 critical-turn-caught on the authored 120-session benchmark when session memory is enabled.

## License

Code: Apache-2.0.
Benchmark JSONs (in `data/benchmarks/`, `data/adversarial/`, and `benchmark/nexus_stress/`) and generated figures: CC BY-4.0.
