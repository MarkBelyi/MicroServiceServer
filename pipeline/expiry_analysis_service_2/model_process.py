from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import joblib

class ExpiryAnalysisService:
    def __init__(self, model_path='expiry_analysis_model.pkl'):
        self.model_path = model_path
        try:
            self.model = joblib.load(model_path)
        except FileNotFoundError:
            self.model = GradientBoostingClassifier(random_state=42)

    def train(self, data: pd.DataFrame):
        X = data[['Stock_Left', 'Days_to_Expiry', 'Season']]
        y = data['Will_Sell_Before_Expiry']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)

        joblib.dump(self.model, self.model_path)
        return {'accuracy': accuracy, 'message': 'Expiry analysis model trained and saved.'}

    def predict(self, input_data):
        return self.model.predict([input_data])
