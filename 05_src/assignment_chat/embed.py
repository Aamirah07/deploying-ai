import dotenv
import os

# Load environment variables from .secrets
dotenv.load_dotenv("../.secrets")   # adjust path if needed

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your .secrets file.")

from chromadb import PersistentClient
from langchain_text_splitters import RecursiveCharacterTextSplitter
#from langchain.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore = Chroma(
    persist_directory="embeddings/chroma_db",
    embedding_function=embeddings
)

# 1. Load your dataset
with open("data/chesterton.txt", "r", encoding="utf-8") as f:
    text = f.read()

# 2. Split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_text(text)

# 3. Create persistent ChromaDB
client = PersistentClient(path="embeddings/chroma_db")
collection = client.get_or_create_collection("my_docs")

# 4. Embed and store
#embeddings = OpenAIEmbeddings()
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


for i, chunk in enumerate(chunks):
    vector = embeddings.embed_query(chunk)
    collection.add(
        ids=[f"chunk_{i}"],
        documents=[chunk],
        embeddings=[vector]
    )

print("Embedding complete.")