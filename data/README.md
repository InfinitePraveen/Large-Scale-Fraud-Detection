# Dataset

This project uses the open-source **Fraud_Data.csv** dataset from the public
`rashida048/Datasets` GitHub repository.

Source:
https://github.com/rashida048/Datasets/blob/master/fraud_data.csv

The dataset contains simulated e-commerce transactions with fields such as
purchase time, purchase value, user/device identifiers, browser, source,
demographics and a fraud class.

The raw CSV is intentionally **not included** in this repository so the project
stays lightweight. The first notebook downloads it with `requests` and
`pathlib` when network access is available.

If the source becomes unavailable, place a compatible `fraud_data.csv` in this
directory before running the training notebook.
