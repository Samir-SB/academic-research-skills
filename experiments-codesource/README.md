# Illinois Env - Experiment Automation

This repository trains and evaluates AP-selection models. The canonical workflow is now YAML-driven and run-oriented.

## Project Layout

```text
project/
│
├── configs/
│   ├── exp1.yaml
│   ├── exp2.yaml
│
├── runs/
├── logs/
│
├── train.py
├── run_experiments.sh
├── config.py
└── utils.py
```

- `configs/`: experiment configs (`exp1.yaml`, `exp2.yaml`, ...)
- `runs/`: per-run artifacts (`model/`, `plot/`)
- `logs/`: run logs and orchestration logs
- `train.py`: canonical training entrypoint
- `run_experiments.sh`: background sequential experiment runner
- `config.py`, `config_mgmt.py`, `utils.py`: config/load/runtime helpers
- `claude_a2c_online.py`: legacy wrapper (forwards to `train.py`)

## Environment

Use the project virtual environment:

```bash
cd /home/samir/project/illinois-env
source .venv/bin/activate
```

## Run One Experiment

```bash
python train.py --config configs/exp1.yaml
```

Optional fixed run id:

```bash
python train.py --config configs/exp1.yaml --run-id my_run_001
```

Outputs:

- `runs/<run_id>/model/` (best checkpoint + `resolved_config.yaml`)
- `runs/<run_id>/plot/` (training/eval plots)
- `logs/<run_id>.log`

## Run Multiple Experiments (Background)

```bash
./run_experiments.sh configs/exp1.yaml configs/exp2.yaml
```

Behavior:

- Runs configs sequentially in one detached process
- Stops on first failure
- Writes orchestration log to `logs/run_experiments_<timestamp>.log`

Monitor:

```bash
tail -f logs/run_experiments_<timestamp>.log
```

## Config Format (YAML only)

Only `.yaml` / `.yml` configs are accepted.

Minimal example:

```yaml
experiment_name: my_experiment
random_seed: 42
train: true
data_dir: data/selected
dataset:
  filename: df_shuffled_200.csv
env:
  final_nb_aps: 50
  train:
    num_aps: 20
    on_line: true
  eval:
    num_aps: 20
    on_line: true

network:
  hidden_layers: [512, 512, 512]
  dropout_prob: 0.5

training:
  learning_rate: 0.00005
  gamma: 0.9
  n_steps: 60
  invalid_action_penalty: -0.2
  reload_freq: 15
  episodes: 50
  target_accuracy: 95
  entropy_coef: 0.05
  max_grad_norm: 1.0
```

Environment/data keys:

- `dataset.filename`: CSV name under `data_dir`
- `env.final_nb_aps`: shared AP dimension for padding/permutation
- `env.train.*`: env settings used for training
- `env.eval.*`: env settings used for evaluation/inference

## DQN Entrypoints

All DQN scripts now accept YAML config via `--config`:

```bash
python dqn_baseline3.py --config configs/exp1.yaml
python inference_dqn.py --config configs/exp1.yaml
python dqn.py --config configs/exp1.yaml
```

## Legacy Entry

Running `claude_a2c_online.py` directly is deprecated and automatically forwards to `train.py`.

## Notes

- `configs/base.json` and `configs/override.json` are legacy files and are no longer used by the canonical flow.
- If data paths in a config do not exist, training fails with a file-not-found error.
