

import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
from langchain_core.documents.base import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableSerializable
from langchain_core.load.serializable import Serializable
from langchain_chroma import Chroma
from chromadb.api import ClientAPI
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import requests
import re
from uuid import uuid4
from typing import List
import logging
import os

# Hint: Use these variables in your tasks
OLLAMA_HOST_NAME = os.environ.get("OLLAMA_HOST_NAME", "localhost")
CHROMA_HOST_NAME = os.environ.get("CHROMA_HOST_NAME", "localhost")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "bge-m3")
MODEL_NAME = os.environ.get("MODEL_NAME", "llama3.2:1B")
PDF_DOC_PATH = os.environ.get("PDF_DOC_PATH", "src/AI_Book.pdf")

logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more details
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Console logs
    ],
)

logger = logging.getLogger(__name__)

class CustomChatBot:
    """
    A class representing a chatbot that uses a ChromaDB client for document retrieval
    and the ChatOllama model for generating answers.

    This chatbot uses a retrieval-augmented generation (RAG) pipeline where it retrieves
    relevant information from a custom document database (ChromaDB) and then generates
    concise answers using a language model (ChatOllama).
    """

    def __init__(self, index_data: bool, pull_embedding_model: bool) -> None:
        """
        Initialize the CustomChatBot class by setting up the ChromaDB client for document retrieval
        and the ChatOllama language model for answer generation.
        """

        # Initialize the embedding function for document retrieval
        if pull_embedding_model:
            logger.info(f"Pulling embedding model{EMBEDDING_MODEL} now.")
            self._pull_embedding_model()

        # Task: initialize the embedding model
        self.embedding_function = OllamaEmbeddings(
            model=EMBEDDING_MODEL,
            base_url=f"http://{OLLAMA_HOST_NAME}:11434",
        )

        # Initialize the ChromaDB client
        self.client = self._initialize_chroma_client()
        
        # Get or create the document collection in ChromaDB
        self.vector_db = self._initialize_vector_db()

        # Process pdf, embedd data and index to ChromaDB
        if index_data:
            logger.info(f"Index data to chroma db now.")
            self._index_data_to_vector_db()

        # Task: Initialize the document retriever
        self.retriever = self.vector_db.as_retriever(search_kwargs={"k": 4})

        # Task: Initialize the large language model (LLM) from Ollama
        self.llm = ChatOllama(model=MODEL_NAME,base_url=f"http://{OLLAMA_HOST_NAME}:11434")

        # Set up the retrieval-augmented generation (RAG) pipeline
        self.qa_rag_chain = self._initialize_qa_rag_chain()

    def _pull_embedding_model(self):
        logger.info(f"Pull embedding model {EMBEDDING_MODEL}")
        try:

            response = requests.post(f"http://{OLLAMA_HOST_NAME}:11434/api/pull", json = {"name": EMBEDDING_MODEL,  "stream": False})
            response.raise_for_status()
            logger.info(response.json())
        except:
            raise

    def _initialize_chroma_client(self) -> ClientAPI:
        """
        Initialize and return a ChromaDB HTTP client for document retrieval.

        Returns:
            chromadb.HttpClient: A client used to communicate with ChromaDB.
        """ 
        logger.info("Initialize chroma db client.")

        # Task: Initilaize chromadb http client
        return chromadb.HttpClient(
            host=CHROMA_HOST_NAME,
            port=8000
        )

    def _initialize_vector_db(self) -> Chroma:
        """
        Initialize and return a Chroma vector database using the HTTP client.

        Returns:
            Chroma: A vector database instance connected to the document collection in ChromaDB.
        """
        logger.info("Initialize chroma vector db.")

        # Task initialize langchain chromadb object with chromadb http client and embedding function
        return Chroma(
            client=self.client,
            collection_name="documents",
            embedding_function=self.embedding_function
        )

    def _index_data_to_vector_db(self):

        pdf_doc = PDF_DOC_PATH

        # Create pdf data loaders
        loader = PyPDFLoader(pdf_doc)

        # Load and split documents in chunks
        pages_chunked = loader.load_and_split(text_splitter=RecursiveCharacterTextSplitter())

        # Function to clean text by removing invalid unicode characters, including surrogate pairs
        def clean_text(text):
            # Remove surrogate pairs
            text = re.sub(r'[\ud800-\udfff]', '', text)
            # Optionally remove non-ASCII characters (depends on your use case)
            text = re.sub(r'[^\x00-\x7F]+', '', text)
            return text

        pages_chunked_cleaned = [
            Document(page_content=clean_text(doc.page_content), metadata=doc.metadata)
            for doc in pages_chunked
        ]

        uuids = [str(uuid4()) for _ in range(len(pages_chunked_cleaned[0:100]))]

        self.vector_db.add_documents(documents=pages_chunked_cleaned[0:100], ids=uuids)

    def _initialize_qa_rag_chain(self) -> RunnableSerializable[Serializable, str]:
        """
        Set up the retrieval-augmented generation (RAG) pipeline for answering questions.
        
        The pipeline consists of:
        - Retrieving relevant documents from ChromaDB.
        - Formatting the retrieved documents for input into the language model (LLM).
        - Using the LLM to generate concise answers.
        
        Returns:
            dict: The RAG pipeline configuration.
        """
        logger.info("Initialize rag chain.")

        # Task: Define prompt
        prompt_template = """Answer the question based on the following context:

        {context}

Question: {question}"""

        # Task: Initialize prompt langchain prompt template
        rag_prompt = ChatPromptTemplate.from_template(prompt_template)

        # Task: Build the RAG pipeline using the retriever and LLM
        return ({"context": self.retriever | self._format_docs, "question": RunnablePassthrough()}
            | rag_prompt
            | self.llm
            | StrOutputParser()
        )

    def _format_docs(self, docs: List[Document]) -> str:
        """
        Helper function to format the retrieved documents into a single string.
        
        Args:
            docs (List[Document]): A list of documents retrieved by ChromaDB.

        Returns:
            str: A string containing the concatenated content of all retrieved documents.
        """
        return "\n\n".join(doc.page_content for doc in docs)
        
    async def astream(self, question: str):
        """
        Handle a user query asynchronously by running the question through the RAG pipeline and stream the answer.

        Args:
            question (str): The user's question as a string.

        Yields:
            str: The generated answer from the model, streamed chunk by chunk.
        """
        logger.info("Streaming RAG chain response.")
        try:
            async for event in self.qa_rag_chain.astream_events(question, version="v2"):
                    # Task: Filter stream events to get chunk which can be returned to the streamlit interface
                    if isinstance(event, dict) and event.get("event") == "on_chain_stream":
                        data = event.get("data", {})
                        chunk = data.get("chunk")
                        if chunk is None:
                            continue
                        text = getattr(chunk, "content", None) or str(chunk)
                        if text:
                            yield text
        except Exception as e:
            logger.error(f"Error in stream_answer: {e}", exc_info=True)
            raise