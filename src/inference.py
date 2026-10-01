import os
import pickle
import argparse
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from src.utils.versioning import get_version
from src.utils.logger import get_logger
from dotenv import load_dotenv

load_dotenv(override=True)
MODEL_PATH = os.getenv("MODEL_PATH")

logger = get_logger(__name__)
app = FastAPI(title="API de previsão de eficiência")


def load_model(model_path):
    if not model_path:
        raise ValueError("Defina MODEL_PATH no arquivo .env.")
    logger.info("Carregando o modelo...")
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    logger.info("Modelo carregado com sucesso.")
    return model


def predict_eff(model, x):
    x_array = np.array([x]).reshape(1, -1)
    result = float(model.predict(x_array)[0])
    logger.info(f"Dia {x} | eficiência: {result}")
    return result


def predict_data(model, y):
    a = model.coef_[0]
    b = model.intercept_
    x = (y - b) / a
    logger.info(f"Eficiência {y} | dia: {x}")
    return x


class EfficiencyRequest(BaseModel):
    efficiency: float


class DataRequest(BaseModel):
    data: float


@app.post("/predict/efficiency")
def api_predict_eff(req: EfficiencyRequest):
    model = load_model(os.getenv("MODEL_PATH"))
    res = predict_eff(model, req.efficiency)
    return {"result": res}


@app.post("/predict/data")
def api_predict_data(req: DataRequest):
    model = load_model(os.getenv("MODEL_PATH"))
    res = predict_data(model, req.data)
    return {"result": res}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script de inferência")
    parser.add_argument("--efficiency", type=float, help="Valor de entrada para eficiência")
    parser.add_argument("--data", type=float, help="Valor de entrada para o dia/dado")
    args = parser.parse_args()

    model_path = os.getenv("MODEL_PATH")
    if not model_path:
        raise ValueError("Defina MODEL_PATH no arquivo .env.")

    model = load_model(model_path)

    if args.efficiency is not None:
        predict_eff(model, args.efficiency)
    elif args.data is not None:
        predict_data(model, args.data)

