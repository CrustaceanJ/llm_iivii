### 1. Put your model file to bundle/models -> bundle/models/llama-2-7b-chat.Q4_K_M.gguf

### 2. Build and run docker:
```#bash
docker build --network=host --tag llm_crustacean:v1 .

docker run -p 8994:8994 --network host llm_crustacean:v1
```

### 3. To run tests:
```
python src/tests/test.py
```

```
Question: Сколько мне надо платить за оповещения о переводах и оплатах с карты?
Answer:  Спасибо за Ваше обращение в наш банк! Для оповещений о переводах и оплатах с карты вы должны платить 99 руб. в месяц, в соответствии с условиями сервиса "Оповещение об операциях". Если у вас есть дополнительная карта, то вы также должны платить 59 руб. в месяц, в соответствии с условиями сервиса "Плата за услугу «Оповещение об operaциях»". Если у вас нет тарифа на процентную ставку, то вы не начисляется платы. Если у вас есть вопросы, пожалуйста, обращайтесь к нам.
Elapsed time: 39.83311748504639 sec
Question: Я хочу пополнить свой счет банковским переводом. Сколько стоит такая услуга?
Answer:  Спасибо за Ваше обращение в наш банк! Пожалуйста, уточните, какой сервис вы хотите пополнить счетом. Наши тарифы для переводов из других банков можно найти в документах, приложенных к этому сообщению. Сколько стоит такая услуга? - Бесплатно!
Elapsed time: 31.339133262634277 sec
Question: А если это будет банкомат другого банка?
Answer:  Спасибо за Ваше обращение в наш банк! Для пополнения счета через банкомат другого банка необходимо предоставить дополнительную информацию, такую как IBAN и SWIFT-код. Это позволит нам проверить, есть ли у вас достаточно средств на счете для пополнения, а также обеспечить безопасность транзакции. Если у вас нет этой информации, пожалуйста, обратитесь к вашему банку для получения необходимых данных.
Elapsed time: 37.71772503852844 sec
```
