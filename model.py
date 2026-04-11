import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle

data = {
    "people_count": [10, 50, 100, 200, 300],
    "noise_level": [20, 40, 60, 80, 90],
    "engagement": [0, 0, 1, 1, 1]
}

df = pd.DataFrame(data)

X = df[["people_count", "noise_level"]]
y = df["engagement"]

model = LogisticRegression()
model.fit(X, y)

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained successfully!")