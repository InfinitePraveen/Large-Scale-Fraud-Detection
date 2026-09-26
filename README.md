# Large-Scale Fraud Detection

A lightweight, notebook-first fraud detection project that demonstrates how a
real-time transaction scoring system can combine **machine learning, streaming,
online features, a feature store, and MLOps-style monitoring**.

The project is deliberately designed for a normal Windows laptop without a GPU.
The training workflow uses scikit-learn, and the streaming layer can run in a
local simulation without starting a Kafka cluster.

## Project Highlights

- Fraud classification on an open-source transaction dataset
- Time and transaction-behaviour feature engineering
- Class-imbalance aware evaluation using precision, recall, F1 and PR-AUC
- Online feature store implemented with lightweight SQLite
- Kafka-ready transaction streaming example
- Local fallback stream simulator for machines without Kafka
- Flask web app for live transaction scoring
- Simple model/version metadata and prediction logging
- No `src/` directory and no separate preprocessing modules
- Notebook-first implementation for interview walkthroughs

## Architecture

```text
Open Dataset
     |
     v
01_eda_training.ipynb
     |
     +----> fraud_model.joblib
     |
     v
02_streaming_feature_store.ipynb
     |
     +----> SQLite Online Feature Store
     |
     +----> Kafka topic / local simulator
     |
     v
Flask Web App
     |
     +----> Feature lookup
     +----> Model scoring
     +----> Fraud / review decision
```

## Repository Structure

```text
Large-Scale-Fraud-Detection/
├── data/
│   └── README.md
├── models/
│   ├── fraud_model.joblib
│   └── feature_store.db
├── notebooks/
│   ├── 01_eda_training.ipynb
│   └── 02_streaming_feature_store.ipynb
├── static/
│   └── style.css
├── templates/
│   └── index.html
├── app.py
├── requirements.txt
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTE.md
└── README.md
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Run the notebooks:

```bash
jupyter notebook
```

Run the web demo:

```bash
python app.py
```

Open `http://127.0.0.1:5000`.

## Kafka

Kafka is included as an integration skill rather than a mandatory local
dependency for the demo. Notebook 02 shows the producer/consumer pattern using
`kafka-python`. If Kafka is unavailable, it demonstrates the same event flow
with an in-process simulator.

A typical production design would use:

- Kafka for transaction events
- Redis/Feast/a managed feature store for low-latency online features
- A model registry for model versions
- Prometheus/Grafana or a cloud monitoring stack
- A stream processor such as Kafka Streams, Flink or Spark Structured Streaming

This repository intentionally keeps those infrastructure components out of
the laptop demo.

## Interview Demo Flow

1. Explain why fraud detection needs low-latency decisions.
2. Show the notebook's feature engineering and imbalanced classification.
3. Explain the difference between offline training features and online features.
4. Open the Flask app and submit several transactions.
5. Show how user features are read from the local feature store.
6. Explain how Kafka would carry the transaction event in production.
7. Discuss model monitoring, drift, false positives and threshold tuning.

## Dataset

The public dataset is documented in `data/README.md`. The raw CSV is not
bundled with this repository to keep the project small.

## Profiles

GitHub: https://github.com/InfinitePraveen

LinkedIn: https://www.linkedin.com/in/infinitepraveen/

## License

The code in this repository is provided for educational and portfolio use.
Check the original dataset repository for its data terms.
