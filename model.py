from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib


def train_and_save_model(path: str = "iris_model.joblib"):
    iris = datasets.load_iris()
    X, y = iris.data, iris.target

    model = LogisticRegression(max_iter=200)
    model.fit(X, y)

    joblib.dump(model, path)
    return path


def load_model(path: str = "iris_model.joblib"):
    return joblib.load(path)
