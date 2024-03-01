import pickle
import os
from django.conf import settings
import pandas as pd

with open(os.path.join(settings.BASE_DIR, 'core', 'ml_models', 'model.pkl'), 'rb') as f:
    model = pickle.load(f)

def prepare_data(data):
    column_order = ['vehicle length',
                    'vehicle weight',
                    'axles number',
                    'vehicle speed',
                    'road condition',
                    'Air temperature',
                    'precipitation type',
                    'precipitation intensity',
                    'relative humidity',
                    'wind direction',
                    'wind speed',
                    'Lighting condition']
    data = pd.DataFrame(data, index=[0], columns=column_order)
    return data