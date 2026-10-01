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
MODEL_PATH = os.getenv('MODEL_PATH')

logger = get_logger(__name__)
app = FastAPI(title='API de previsão de eficiência')


def load_model(model_path):
    if not model_path:
        raise ValueError('Defina MODEL_PATH no arquivo .env.')
    logger.info('Carregando o modelo...')
    with open(model_path, 'rb') as f:
        data = pickle.load(f)
    logger.info(f"R² Score do modelo carregado: {data['metrics']:.4f}")
    logger.info(f"Descrição do modelo: {data['description']}")
    return data['model']


def predict_eff(model, x):
    x_array = np.array([x]).reshape(1, -1)
    result = float(model.predict(x_array)[0])
    logger.info(f'Dia {x} | eficiência: {result}')
    return result


def predict_data(model, y):
    coef = float(np.asarray(model.coef_).reshape(-1)[0])
    intercept = float(np.asarray(model.intercept_).reshape(-1)[0])
    if coef == 0:
        raise ValueError('Coeficiente zero: não é possível calcular o dia.')
    dia = (y - intercept) / coef
    logger.info(f'Eficiência {y} | dia: {dia}')
    return dia


class Entrada(BaseModel):
    dia: float


@app.get('/')
def inicio():
    return {'mensagem': 'API de previsão de eficiência'}


@app.post('/predict')
def prever(entrada: Entrada):
    model = load_model(MODEL_PATH)
    return {
        'dia': entrada.dia,
        'eficiencia': predict_eff(model, entrada.dia),
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--efficiency', type=int)
    group.add_argument('--data', type=float)
    parser.add_argument('--version', type=str)
    args = parser.parse_args()
    model_path = f'artifacts/{args.version}.pkl' if args.version else MODEL_PATH
    model = load_model(model_path)

    if args.efficiency is not None:
        predict_eff(model, args.efficiency)
    else:
        predict_data(model, args.data)

