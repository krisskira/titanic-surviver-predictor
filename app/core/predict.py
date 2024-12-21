import os
from app.model.survivor import Survivor
import joblib
import pandas as pd
import numpy as np

model_path = os.path.dirname(os.path.abspath(
    __file__)) + "/../../modelo_entrenado.pkl"

model = joblib.load(model_path) # Carga del modelo.

async def predict(data: Survivor) -> bool:
    _data = data.getData()
    _data = np.array([_data])
    df = pd.DataFrame(_data, columns=["pclass",	"sex",	"age",	"fare",	"C",	"Q",	"S"])
    prediction = model.predict(df)
    return True if prediction[0] == 1 else False
