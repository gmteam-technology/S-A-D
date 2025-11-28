import numpy as np
from sklearn.linear_model import LinearRegression


def predict_productivity(features: list[dict[str, float]]) -> list[float]:
    if not features:
        return []
    X = np.array(
        [
            [row.get("rainfall", 0), row.get("ndvi", 0), row.get("cost", 0), row.get("temperature", 0)]
            for row in features
        ]
    )
    y = np.array([row.get("yield", 55) for row in features])
    model = LinearRegression().fit(X, y)
    return model.predict(X).round(2).tolist()
