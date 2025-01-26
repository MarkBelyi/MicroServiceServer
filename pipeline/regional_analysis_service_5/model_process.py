from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd
import joblib

class RegionalAnalysisService:
    def __init__(self, model_path='regional_analysis_model.pkl'):
        self.model_path = model_path
        try:
            self.model = joblib.load(model_path)
        except FileNotFoundError:
            self.model = DecisionTreeClassifier(random_state=42)

    def train(self, data: pd.DataFrame):
        X = data[['Region', 'Season', 'Quantity_Sold']]
        y = data['Regional_Impact']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_test)
        report = classification_report(y_test, predictions)

        joblib.dump(self.model, self.model_path)
        return {'classification_report': report, 'message': 'Regional analysis model trained and saved.'}

    def predict(self, input_data):
        return self.model.predict([input_data])
