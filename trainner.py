
import joblib 
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier

import ssl
import urllib.request

# Deshabilitar la verificación de SSL a nivel global
ssl._create_default_https_context = ssl._create_unverified_context


# datos = pd.read_csv("sample_data/train_titanic.csv")
datos = sns.load_dataset('titanic')

# Seleccionar características
features = ['pclass', 'sex', 'age', 'fare', 'embarked', 'survived']
data_to_process = datos[features]

# Preprocesar el dataset
datana = data_to_process.dropna(subset=['embarked']).copy()

datana['age'] = datana['age'].fillna(datana["age"].mean())
datana['sex'] = datana['sex'].map({'male': 0, 'female': 1})
datana['embarked'] = datana['embarked'].dropna()
embarked = pd.get_dummies(datana["embarked"], drop_first=False)
datana = datana.drop(['embarked'], axis=1)
datana = pd.concat([datana, embarked], axis=1)

# Seleccionar características y objetivo
X = datana.drop(['survived'],axis=1)
y = datana['survived']

# Dividir en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf = RandomForestClassifier(
    random_state=42,
    n_estimators=200,
    max_depth=12,
    max_features=0.99
  )
rf.fit(X_train, y_train)
print('>>> Score train: ', rf.score(X_train, y_train))
print('>>> Score test:', rf.score(X_test, y_test))
y_pred = rf.predict(X_test)

test_accuracy_rf =accuracy_score(y_test, y_pred)

print('El accuracy es:', test_accuracy_rf)
print("Classification Report:\n", classification_report(y_test, y_pred))

joblib.dump(rf, 'modelo_entrenado.pkl') # Guardo el modelo.
