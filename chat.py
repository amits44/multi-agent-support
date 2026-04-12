from langchain_groq import ChatGroq
from dotenv import load_dotenv


load_dotenv()
llm = ChatGroq(model ="llama-3.3-70b-versatile")

query = llm.invoke("what is the capital of india")

print(query)