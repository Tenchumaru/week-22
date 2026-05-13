import logging
import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from schemas import PredictRequest, PredictResponse
from model import load_model, train_and_save_model
from sklearn import datasets

# Basic logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

# Train once if needed
MODEL_PATH = "iris_model.joblib"
train_and_save_model(MODEL_PATH)

# Load model at startup
model = load_model(MODEL_PATH)

# Iris class names
iris = datasets.load_iris()
CLASS_NAMES = iris.target_names

app = FastAPI(title="Iris Logistic Regression API")

# --- Monitoring State ---
REQUEST_COUNT = 0
ERROR_COUNT = 0


@app.middleware("http")
async def monitoring_middleware(request: Request, call_next):
    global REQUEST_COUNT, ERROR_COUNT

    REQUEST_COUNT += 1
    start = time.time()

    try:
        response = await call_next(request)
    except Exception as e:
        ERROR_COUNT += 1
        latency_ms = (time.time() - start) * 1000

        logging.error(f"ERROR | path={request.url.path} | latency_ms={latency_ms:.2f} | error={str(e)}")

        return JSONResponse(status_code=500, content={"detail": "Internal server error"})

    latency_ms = (time.time() - start) * 1000

    logging.info(
        f"REQUEST | path={request.url.path} | status={response.status_code} "
        f"| latency_ms={latency_ms:.2f} | total_requests={REQUEST_COUNT} "
        f"| total_errors={ERROR_COUNT}"
    )

    return response


@app.post("/v1/predict", response_model=PredictResponse)
def predict(payload: PredictRequest):
    if len(payload.features) != 4:
        raise HTTPException(status_code=400, detail="Expected 4 features")

    try:
        pred = model.predict([payload.features])[0]
        return PredictResponse(predicted_class=int(pred), class_name=CLASS_NAMES[pred])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
