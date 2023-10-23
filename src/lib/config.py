import json
from typing import Any

from pydantic import BaseModel
from pydantic.v1.utils import deep_update


class Config(BaseModel):
    llama_model_path: str = "bundle/models/llama-2-7b-chat.Q4_K_M.gguf"
    llama_n_ctx: int = 4096
    llama_n_batch: int = 16
    llama_max_tokens: int = 5000
    llama_temperature: float = 0.0
    llama_top_p: float = 1.0
    document_embedder: str = "sentence-transformers/paraphrase-MiniLM-L12-v2" # all-MiniLM-L6-v2
    document_dir: str = "bundle/documents"
    document_cache: str = "./cache/"
    dump_dir_path: str = "logs/"
    retrieve_template: str = """<</SYS>>
    Вы консультант клиентов банка "Тиньков Банк".
Вашей задачей является ответы на вопросы клиента, используя предложенный фрагментов документов.
Всегда говори "Спасибо за Ваше обращение в наш банк!" в начале ответа.
Не придумывайте ответ, если его нет в предложенном фрагменте документов.
В своём ответе используй только русские слова.

<</SYS>>
------
Предложенных фрагменты документов:
-----
{context}
-----
История сообщений:
{chat_history}
-----
Вопрос клиента: {question}
Ответ на русском языке:"""


    @classmethod
    def load(cls, config_path: str):
        config: dict[str, Any] = {}

        with open(config_path) as config_file:
            config = deep_update(config, json.load(config_file))

        return cls.model_validate(config)
