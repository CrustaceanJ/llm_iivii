import requests
import time


if __name__ == "__main__":
    questions = [
        "Сколько мне надо платить за оповещения о переводах и оплатах с карты?",
        "Я хочу пополнить свой счет банковским переводом. Сколько стоит такая услуга?",
        "А если это будет банкомат другого банка?"
    ]

    base = {
        "user_id": "mda2"
    }

    for q in questions:
        start = time.time()
        r = requests.post("http://localhost:8994/message", json={"message": q, **base})
        timeout = time.time() - start
        a = r.json()["answer"]
        print(f"Question: {q}\nAnswer: {a}\nElapsed time: {timeout} sec")

