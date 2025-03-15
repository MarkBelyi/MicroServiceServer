# models/return_analysis_model.py

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization

def build_return_analysis_model(input_shape):
    model = Sequential()
    model.add(LSTM(32, activation='relu', input_shape=input_shape))
    model.add(Dropout(0.3))
    model.add(BatchNormalization())
    model.add(Dense(16, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))  # Выход – вероятность возврата
    model.compile(optimizer='adam', loss='binary_crossentropy')
    return model
