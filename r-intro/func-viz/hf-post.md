Hi,

  I wasn't able to reproduce the normalized scores for `Llama-2-7b-hf` published
  on [Open LLM LeaderBoard][1]. The latest scores published are as follows:

| Model | AVG | ⬆️IFEval | BBH | MATH Lvl 5 | GPQA | MUSR | MMLU-PRO |
| ------------------------- | ----- | ----- | ----- | ---- | ---- | ---- | ----- |
| meta-llama/Llama-2-7b-hf | 8.72 | 25.19 | 10.35 | 1.21 | 2.24 | 3.76 | 9.57 |
| meta-llama/Llama-2-7b-hf(mine) | - | 18.48 | 10.35 | 1.33 | 1.84 | 3.76 | 18.61 |

I attempted to reproduce the published scores on HF by following the calculation
rules described on the [Open LLM Leaderboard score normalization page][2], I can
only reproduce the BBH and MUSR. According to the [Open LLM Leaderboard score
normalization page][2], the IFEval's lower bound is 0, the higher bound is 1.0
which means the normalized IFEval score is simply 100 times the number in the
results.json. However, the published IFEval score 25.19 doesn't match any
numbers in the [corresponding results.json from huggingface][3], which are

    "prompt_level_strict_acc,none": 0.18484288354898337,
    "inst_level_strict_acc,none": 0.31894484412470026,

Is there any undocumented rules to normalize the IFEval and other scores? Or do
we have an out-of-box library to normalize these scores?(I can't identify such
code on any of HF official github repositories)

BTW, I'm conducting a research on a new LLM quantization method on the Llama
family models and attempt to use the new leaderboard benchmark to compare the
my approach to SOTA baselines. Attached is the code to calculate normalized
scores for your reference:

 ````python
import json
import os


def _cal_leaderboard_mathlevel5(results):
    subtask_names = results["group_subtasks"]["leaderboard_math_hard"]
    scores = []
    for metric in subtask_names:
        value = results["results"][metric]["exact_match,none"]
        scores.append(_cal_normalized_score(value, 0, 1.0))
    return sum(scores) / len(scores)


def _cal_leaderboard_bbh(results):
    subtask_names = results["group_subtasks"]["leaderboard_bbh"]
    metrics = {}
    for name in subtask_names:
        metrics[name] = len(results["configs"][name]["doc_to_choice"])
    scores = []
    for metric, choices in metrics.items():
        value = results["results"][metric]["acc_norm,none"]
        scores.append(_cal_normalized_score(value, 1 / choices, 1.0))
    return sum(scores) / len(scores)


def _cal_leaderboard_gpqa(results):
    subtask_names = results["group_subtasks"]["leaderboard_gpqa"]
    metrics = {}
    for name in subtask_names:
        metrics[name] = len(results["configs"][name]["doc_to_choice"])
    scores = []
    for metric, choices in metrics.items():
        value = results["results"][metric]["acc_norm,none"]
        scores.append(_cal_normalized_score(value, 1 / choices, 1.0))
    return sum(scores) / len(scores)


# refer to: https://huggingface.co/docs/leaderboards/open_llm_leaderboard/normalization#example-normalizing-musr-scores
def _cal_leaderboard_musr(results):
    metrics = {
        "leaderboard_musr_murder_mysteries": 2,
        "leaderboard_musr_object_placements": 5,
        "leaderboard_musr_team_allocation": 3,
    }
    scores = []
    for metric, choices in metrics.items():
        value = results["results"][metric]["acc_norm,none"]
        scores.append(_cal_normalized_score(value, 1 / choices, 1.0))
    return sum(scores) / len(scores)


def _cal_leaderboard_mmlu_pro(results):
    value = results["results"]["leaderboard_mmlu_pro"]["acc,none"]
    return _cal_normalized_score(value, 0, 1.0)


def _cal_leaderboard_ifeval_score(results):
    # value = results["results"]["leaderboard_ifeval"]["inst_level_strict_acc,none"]
    value = results["results"]["leaderboard_ifeval"]["prompt_level_strict_acc,none"]
    return _cal_normalized_score(value, 0, 1.0)


def _cal_normalized_score(value, lower_bound, higher_bound=1.0):
    if value < lower_bound:
        return 0
    return 100 * (value - lower_bound) / (higher_bound - lower_bound)


def _prepare_tokenizer_files(model_id, quant_dir):
    files = [
        "tokenizer.model",
        "tokenizer.json",
        "special_tokens_map.json",
        "tokenizer_config.json",
    ]

    model_id_x = model_id.replace("/", "--")
    hf_model_dir = os.path.join(HUGGINGFACE_HUB_CACHE, f"models--{model_id_x}")

    ref_main_fp = os.path.join(hf_model_dir, "refs", "main")
    with open(ref_main_fp) as fh:
        commit_sha = fh.read().strip()

    base_dir = os.path.join(hf_model_dir, "snapshots", commit_sha)

    for f in files:
        src_fp = os.path.join(base_dir, f)
        dst_fp = os.path.join(quant_dir, f)
        shutil.copyfile(src_fp, dst_fp, follow_symlinks=True)


if __name__ == "__main__":
    # result3.json is a copy of https://huggingface.co/datasets/open-llm-leaderboard/meta-llama__Llama-2-7b-hf-details/raw/main/meta-llama__Llama-2-7b-hf/results_2024-06-16T18-52-55.970021.json
    with open("result3.json") as fh:
        results = json.load(fh)
        t = _cal_leaderboard_score(results)
        ifeval, bbh, mathlevel5, gpqa, musr, mmlupro = _cal_leaderboard_score(results)
        print(f"ifeval={ifeval}")
        print(f"bbh={bbh}")
        print(f"mathlevel5={mathlevel5}")
        print(f"gpqa={gpqa}")
        print(f"musr={musr}")
        print(f"mmlupro={mmlupro}")

 ````


[1]: https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard
[2]: https://huggingface.co/docs/leaderboards/open_llm_leaderboard/normalization
[3]: https://huggingface.co/datasets/open-llm-leaderboard/meta-llama__Llama-2-7b-hf-details/raw/main/meta-llama__Llama-2-7b-hf/results_2024-06-16T18-52-55.970021.json
