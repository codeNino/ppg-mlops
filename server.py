from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import pandas as pd
import io
from util import validate_gender
from pipeline import get_features_for_prediction, reload_model
from signal_analyzer import extract_ppg_features
app = FastAPI()


PREDICTOR = reload_model("./xgb_model.json")


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.post("/upload/")
async def upload_csv_and_fields(
    signal: UploadFile = File(...),
    age: int = Form(...),
    gender: str = Form(...),
    height: float = Form(...),
    weight: float = Form(...)
):
    # Read the CSV content into a pandas DataFrame
    signal_contents = await signal.read()
    try:
        sex = validate_gender(gender)
        signal_df = pd.read_csv(io.StringIO(signal_contents.decode("utf-8")))
        ppg_signal = signal_df.iloc[:, 0].values
        feature_dict = extract_ppg_features(ppg_signal)
        feature_dict["age"] = age
        feature_dict["gender"] = sex.value
        feature_dict["height"] = height
        feature_dict["weight"] = weight
        feature_df = pd.DataFrame([feature_dict])
        feature_matrix = get_features_for_prediction(feature_df)
        prediction = PREDICTOR.predict(feature_matrix)
        return JSONResponse(float(prediction[0]), 200)
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content=str(e)
        )


# if __name__ == "__main__":
#     uvicorn.run(
#         "server:app",
#         host="0.0.0.0",
#         port=8002,
#         log_level="debug",
#         reload=True
#     )
