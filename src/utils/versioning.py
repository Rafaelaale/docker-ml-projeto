from datetime import datetime

def get_date():
    return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

def get_version():
    return f'artifacts/heat_efficiency_model_{get_date()}.pkl'
