from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import joblib

class ReturnAnalysisService:
    def __init__(self, model_path='return_analysis_model.pkl'):
        self.model_path = model_path
        try:
            self.model = joblib.load(model_path)
        except FileNotFoundError:
            self.model = LogisticRegression(random_state=42)

    def train(self, data: pd.DataFrame):
        X = data[['Discount', 'Region', 'Quantity_Sold']]
        y = data['Returns']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)

        joblib.dump(self.model, self.model_path)
        return {'accuracy': accuracy, 'message': 'Return analysis model trained and saved.'}

    def predict(self, input_data):
        return self.model.predict([input_data])
