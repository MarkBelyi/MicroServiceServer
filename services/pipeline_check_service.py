from flask import Blueprint, jsonify

pipeline_blueprint = Blueprint('pipeline', __name__)

# Глобальная переменная-счётчик, изначально равная 0
counter = 0

def stage_0(results):
    global counter
    counter += 1
    results.append(f"Этап 0 выполнен. counter = {counter}")

def stage_1(results):
    global counter
    counter += 1
    results.append(f"Этап 1 выполнен. counter = {counter}")

def stage_2(results):
    global counter
    counter += 1
    results.append(f"Этап 2 выполнен. counter = {counter}")

def stage_3(results):
    global counter
    counter += 1
    results.append(f"Этап 3 выполнен. counter = {counter}")

def stage_4(results):
    global counter
    counter += 1
    results.append(f"Этап 4 выполнен. counter = {counter}")

def stage_5(results):
    global counter
    counter += 1
    results.append(f"Этап 5 выполнен. counter = {counter}")

def stage_6(results):
    global counter
    counter += 1
    results.append(f"Этап 6 выполнен. counter = {counter}")

def stage_7(results):
    global counter
    counter += 1
    results.append(f"Этап 7 выполнен. counter = {counter}")

def run_pipeline_logic():
    results = []
    stage_0(results)
    stage_1(results)
    stage_2(results)
    stage_3(results)
    stage_4(results)
    stage_5(results)
    stage_6(results)
    stage_7(results)
    return results
