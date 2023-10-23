import os

from fastapi import FastAPI
from langchain.chains import ConversationalRetrievalChain, RetrievalQA, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.document_loaders import UnstructuredPDFLoader, CSVLoader
from langchain.embeddings import CacheBackedEmbeddings, SentenceTransformerEmbeddings
from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.storage import LocalFileStore
from langchain.vectorstores.faiss import FAISS


from src.lib.config import Config
from src.lib.api import api


def create_app(config: Config):
    app = FastAPI()

    @app.on_event("startup")
    def on_startup():
        docs_pdf = [
            UnstructuredPDFLoader(os.path.join(config.document_dir, x))
            for x in os.listdir(config.document_dir) if x.endswith(".pdf")
        ]

        docs_csv = [
            CSVLoader(
                file_path=os.path.join(config.document_dir, x),
                csv_args={
                    "delimiter": ",",
                    "quotechar": '"',
                    "fieldnames": ["Сервис", "Условие", "Тариф"]
                },
            ) for x in os.listdir(config.document_dir) if x.endswith(".csv")
        ]

        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=0,
            length_function=len,
        )

        docs = []
        for doc in [*docs_pdf, *docs_csv]:
            doc = doc.load()
            splitted = text_splitter.transform_documents(doc)
            docs.extend(splitted)


        doc_cache = LocalFileStore(config.document_cache)
        embedder = SentenceTransformerEmbeddings(
            model_name=config.document_embedder
        )
        cached_embedder = CacheBackedEmbeddings.from_bytes_store(
            embedder, doc_cache, namespace="mem"
        )
        app.db = FAISS.from_documents(docs, cached_embedder)

        app.llm = LlamaCpp(
            model_path=config.llama_model_path,
            n_ctx=config.llama_n_ctx,
            temperature=config.llama_temperature,
            max_tokens=config.llama_max_tokens,
            top_p=config.llama_top_p,
            n_batch=config.llama_n_batch,
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        )

        app.retrieval_prompt = PromptTemplate(
            template=config.retrieve_template, 
            input_variables=["context",  "chat_history", "question"]
        )
        app.memory = dict()

    app.include_router(api)

    return app
