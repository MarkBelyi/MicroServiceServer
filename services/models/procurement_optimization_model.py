# models/procurement_optimization_model.py

# Здесь можно использовать подход Deep Q-Network или PPO.
# Приведён упрощённый пример полносвязной сети для оценки действий.

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization

def build_procurement_optimization_model(input_dim, output_dim):
    model = Sequential()
    model.add(Dense(128, activation='relu', input_dim=input_dim))
    model.add(Dropout(0.3))
    model.add(BatchNormalization())
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.3))
    model.add(BatchNormalization())
    model.add(Dense(output_dim, activation='linear'))  # Выход – рекомендованное количество закупки
    model.compile(optimizer='adam', loss='mse')
    return model
