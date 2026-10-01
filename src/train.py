import os
import pickle
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sqlalchemy import create_engine
from src.utils.versioning import get_version
from src.utils.logger import get_logger
from dotenv import load_dotenv

logger = get_logger(__name__)

load_dotenv(override=True)
DB_PATH = os.getenv('DB_PATH')

def read_dataset(path):
    logger.info('Carregando o dataset...')
    engine = create_engine(f'sqlite:///{path}')
    df = pd.read_sql_query(
        'SELECT timestamp, heat_efficiency FROM heat_exchanger ORDER BY timestamp',
        engine,
    )
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['day_index'] = (df['timestamp'] - df['timestamp'].min()).dt.days
    return df

def train(x: np.ndarray, y: np.ndarray) -> LinearRegression:
    logger.info('Treinando o modelo...')
    model = LinearRegression()
    model.fit(x, y)
    return model

def save_model(model: LinearRegression, path: str, r2: float, description: str = 'Modelo de regressão linear para eficiência térmica'):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = {'model': model, 'metrics': r2, 'description': description}
    with open(path, 'wb') as f:
        pickle.dump(data, f)

def evaluate(model: LinearRegression, y: np.ndarray, x: np.ndarray):
    pred = model.predict(x)
    r2 = r2_score(y, pred)
    logger.info(f'R² Score: {r2:.4f}')
    return r2

if __name__ == '__main__':
    df = read_dataset(path=DB_PATH)
    x = df['day_index'].values.reshape(-1, 1)
    y = df['heat_efficiency'].values
    model = train(x, y)
    r2 = evaluate(model, y, x)
    model_path = get_version()
    save_model(model, path=model_path, r2=r2)
    logger.info(f'Modelo treinado e salvo com sucesso em {model_path}!')

