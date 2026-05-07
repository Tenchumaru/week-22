from fastapi import FastAPI, HTTPException
from schemas import PredictRequest, PredictResponse
from model import load_model, train_and_save_model
from sklearn import datasets

# Train once if needed
MODEL_PATH = "iris_model.joblib"
train_and_save_model(MODEL_PATH)

# Load model at startup
model = load_model(MODEL_PATH)

# Iris class names
iris = datasets.load_iris()
CLASS_NAMES = iris.target_names

app = FastAPI(title="Iris Logistic Regression API")

@app.post("/v1/predict", response_model=PredictResponse)
def predict(payload: PredictRequest):
    if len(payload.features) != 4:
        raise HTTPException(status_code=400, detail="Expected 4 features")

    try:
        pred = model.predict([payload.features])[0]
        return PredictResponse(
            predicted_class=int(pred),
            class_name=CLASS_NAMES[pred]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
