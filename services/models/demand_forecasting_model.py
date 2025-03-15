# models/demand_forecasting_model.py

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization

def build_demand_forecasting_model(input_shape):
    model = Sequential()
    model.add(LSTM(64, activation='tanh', return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.3))
    model.add(BatchNormalization())
    model.add(LSTM(32, activation='tanh'))
    model.add(Dropout(0.3))
    model.add(BatchNormalization())
    model.add(Dense(16, activation='relu'))
    model.add(Dense(1, activation='linear'))  # Выходное значение – прогноз спроса
    model.compile(optimizer='adam', loss='mse')
    return model
