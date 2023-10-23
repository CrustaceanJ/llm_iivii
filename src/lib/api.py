from fastapi import APIRouter, Request
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain

from src.lib.models import InputMessage, ResponseMessage


api = APIRouter()


@api.post("/message")
def generate(request: Request, msg: InputMessage) -> ResponseMessage:
    user_id = msg.user_id
    message = msg.message

    memory = request.app.memory.get(
        msg.user_id, 
        ConversationBufferMemory(
            human_prefix="Клиент",
            ai_prefix="Консультант",
            memory_key="chat_history",
            return_messages=True,
        )
    )

    qa_chain = LLMChain(
        llm=request.app.llm,
        prompt=request.app.retrieval_prompt
    )

    docs = request.app.db.similarity_search(message)
    context = "\n".join([d.page_content for d in docs])

    answer = qa_chain({
        "question": message,
        "chat_history": memory,
        "context": context,
    })["text"]

    memory.chat_memory.add_user_message(message)
    memory.chat_memory.add_ai_message(message)
    request.app.memory[user_id] = memory

    return {"answer": answer}
