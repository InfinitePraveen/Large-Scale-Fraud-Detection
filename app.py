from datetime import datetime
from pathlib import Path
import sqlite3
import joblib
from flask import Flask, render_template, request

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "fraud_model.joblib"
FEATURE_DB = BASE_DIR / "models" / "feature_store.db"

app = Flask(__name__)
bundle = joblib.load(MODEL_PATH)
model = bundle["model"]
FEATURES = bundle["features"]


def get_online_features(user_id):
    conn = sqlite3.connect(FEATURE_DB)
    row = conn.execute(
        """SELECT user_tx_count_24h, amount_avg_24h, last_purchase_value,
                  device_seen_count
           FROM online_features WHERE user_id = ?""",
        (user_id,),
    ).fetchone()
    conn.close()

    if row is None:
        return {
            "user_tx_count_24h": 0,
            "amount_avg_24h": 0.0,
            "last_purchase_value": 0.0,
            "device_seen_count": 0,
        }

    return {
        "user_tx_count_24h": row[0],
        "amount_avg_24h": row[1],
        "last_purchase_value": row[2],
        "device_seen_count": row[3],
    }


def update_online_features(user_id, amount, device_seen_count):
    old = get_online_features(user_id)
    count = old["user_tx_count_24h"] + 1
    if old["user_tx_count_24h"] == 0:
        average = amount
    else:
        average = (
            old["amount_avg_24h"] * old["user_tx_count_24h"] + amount
        ) / count

    conn = sqlite3.connect(FEATURE_DB)
    conn.execute(
        """INSERT OR REPLACE INTO online_features
           (user_id, user_tx_count_24h, amount_avg_24h,
            last_purchase_value, device_seen_count, updated_at)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (
            user_id, count, average, amount, device_seen_count,
            datetime.utcnow().isoformat(timespec="seconds"),
        ),
    )
    conn.commit()
    conn.close()


def build_model_row(form_data, online):
    amount = float(form_data.get("purchase_value", 50))
    device_seen_count = int(form_data.get("device_seen_count", online.get("device_seen_count", 0)))
    hour = int(form_data.get("hour", datetime.now().hour))
    dayofweek = int(form_data.get("dayofweek", datetime.now().weekday()))
    new_device = int(form_data.get("new_device", 0))
    high_risk_source = int(form_data.get("high_risk_source", 0))
    user_tx_count_24h = online.get("user_tx_count_24h", 0)
    amount_avg_24h = online.get("amount_avg_24h", 0.0)
    velocity_score = min(1.0, user_tx_count_24h / 10.0)

    row = {
        "purchase_value": amount,
        "age": int(form_data.get("age", 35)),
        "hour": hour,
        "dayofweek": dayofweek,
        "user_tx_count_24h": user_tx_count_24h,
        "device_seen_count": device_seen_count,
        "amount_avg_24h": amount_avg_24h,
        "velocity_score": velocity_score,
        "new_device": new_device,
        "high_risk_source": high_risk_source,
    }

    for feature in FEATURES:
        row.setdefault(feature, 0.0)
    row["Amount"] = amount

    return row


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        user_id = request.form.get("user_id", "demo_user_001").strip()
        amount = float(request.form.get("purchase_value", 50))
        age = int(request.form.get("age", 35))
        hour = int(request.form.get("hour", datetime.now().hour))
        dayofweek = int(request.form.get("dayofweek", datetime.now().weekday()))
        new_device = int(request.form.get("new_device", 0))
        high_risk_source = int(request.form.get("high_risk_source", 0))
        device_seen_count = int(request.form.get("device_seen_count", 0))

        online = get_online_features(user_id)
        velocity_score = min(1.0, online["user_tx_count_24h"] / 10.0)

        row = {
            "purchase_value": amount,
            "age": age,
            "hour": hour,
            "dayofweek": dayofweek,
            "user_tx_count_24h": online["user_tx_count_24h"],
            "device_seen_count": device_seen_count,
            "amount_avg_24h": online["amount_avg_24h"],
            "velocity_score": velocity_score,
            "new_device": new_device,
            "high_risk_source": high_risk_source,
        }

        model_row = build_model_row(request.form, online)
        X = [[model_row[name] for name in FEATURES]]
        probability = float(model.predict_proba(X)[0, 1])
        threshold = 0.50
        decision = "FRAUD REVIEW" if probability >= threshold else "APPROVE"

        update_online_features(user_id, amount, device_seen_count)

        result = {
            "probability": probability,
            "decision": decision,
            "user_id": user_id,
            "features": row,
        }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
