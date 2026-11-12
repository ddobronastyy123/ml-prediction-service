from flask import Flask, request, jsonify
import psycopg2
import json
import os
import pickle

app = Flask(__name__)

MODEL_PATH = os.getenv("MODEL_PATH", "/model/model.pkl")


def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "10.0.2.4"),
        dbname=os.getenv("DB_NAME", "ml_predictions"),
        user=os.getenv("DB_USER", "ml_app"),
        password=os.getenv("DB_PASSWORD", "StrongPassword"),
        sslmode=os.getenv("DB_SSLMODE", "require"),
    )


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Expected JSON object"}), 400

    features = data.get("features")

    if not isinstance(features, list) or len(features) != 30:
        return jsonify({
            "error": "Expected exactly 30 numeric features"
        }), 400

    try:
        features = [float(value) for value in features]
    except (TypeError, ValueError):
        return jsonify({"error": "Features must be numeric"}), 400

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    pred = int(model.predict([features])[0])
    proba = float(max(model.predict_proba([features])[0]))

    result = {
        "class": pred,
        "class_name": "malignant" if pred == 0 else "benign",
        "probability": proba,
    }

    conn = get_db()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO predictions
                    (input_data, prediction, model_version)
                VALUES (%s, %s, %s)
                """,
                (
                    json.dumps({"features": features}),
                    json.dumps(result),
                    "breast-cancer-v1.0",
                ),
            )
        conn.commit()
    finally:
        conn.close()

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
