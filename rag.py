import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import PGVector
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAI
from datascraper import get_wikipedia_articles, topics_to_fetch

qa = None


def initialize_rag_chain():
    global qa
    if qa is None:
        try:
            knowledge_base_path = "/home/meriton/codingprojects/fastapi_rag_project/knowledge_base.txt"
            if not os.path.exists(knowledge_base_path):
                print("Knowledge base not found, scraping Wikipedia articles...")
                get_wikipedia_articles(topics_to_fetch, knowledge_base_path)
                print("Finished scraping Wikipedia articles.")

            # 1. Load Documents
            loader = TextLoader(knowledge_base_path)
            documents = loader.load()

            # 2. Split Documents
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            docs = text_splitter.split_documents(documents)

            # 3. Create Embeddings
            embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=os.environ.get("GEMINI_API_KEY"),
            )

            # 4. Store in PGVector
            connection_string = os.environ.get("DATABASE_URL")
            collection_name = "my_rag_collection"

            db = PGVector.from_documents(
                embedding=embeddings,
                documents=docs,
                collection_name=collection_name,
                connection_string=connection_string,
            )

            # 5. Create Retrieval Chain
            retriever = db.as_retriever()
            llm = GoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=os.environ.get("GEMINI_API_KEY"),
            )
            qa = RetrievalQA.from_chain_type(
                llm=llm, chain_type="stuff", retriever=retriever
            )
            print("RAG chain initialized successfully.")
        except Exception as e:
            print(f"Error initializing RAG chain: {e}")
            raise


def get_answer(question: str) -> str:
    if qa is None:
        initialize_rag_chain()

    if qa is None:
        return "RAG chain is not initialized. Please check the logs for errors."

    return qa.run(question)
