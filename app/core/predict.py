import io
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
    print(">>> Data to predict", _data)
    # prediction = model.predict([_data])
    # prediction = model.predict([_data])
    _data = np.array([[1, 1, 23.0, 7890.0, 1, 0, 0]])
    df = pd.DataFrame(_data, columns=["pclass",	"sex",	"age",	"fare",	"C",	"Q",	"S"])
    prediction = model.predict(df)
    print(">>> Result ",  prediction[0])
    return True if prediction[0] == 1 else False
