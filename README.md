# Learned Page Replacement

## CSE-307 Operating Systems

This project implements classical and learned page replacement policies and evaluates their behavior under a workload shift.

## Implemented Policies

- FIFO
- LRU
- Optimal (Belady's)
- Learned Page Replacement

MRU is not part of this project.

## Learned Policy

The learned policy uses a lightweight Decision Tree classifier.

Features used:

- Recency
- Recent access frequency
- Page age

The model is trained using Optimal-policy information to create training labels. Future references are used only during training to identify suitable eviction candidates. During final simulation, the learned policy uses current and past information.

## Workload

The test workload contains 2,000 page references:

- First 1,000 references: locality-heavy workload
- Second 1,000 references: random/bursty workload

Configuration:

- Pages: 20
- Frames: 8
- Test seed: 42
- Training seed: 100
- Decision tree maximum depth: 4

## Evaluation Metrics

The project measures:

- Hit ratio
- Page-fault count
- Performance before workload shift
- Performance after workload shift

## Bonus Analysis

The project also provides:

- Learned decision explanations
- Decision confidence
- Comparison with an Optimal oracle

The confidence value is a decision-confidence indicator based on the model's score margin. It is not treated as a calibrated probability of correctness.

## How to Run

From the project root:

```text
py src/main.py
py src/plot_results.py
py src/plot_shift.py
py src/bonus_analysis.py
py src/interactive_results.py