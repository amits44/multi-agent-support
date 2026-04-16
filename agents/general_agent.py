import json
import os
from typing import List, Optional, Dict
from util.llm_client import llm_client
from util.prompts import GENERAL_AGENT_SYSTEM_PROMPT, get_escalation_msg
from config import config
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings 

class GeneralAgent:

    def __init__(self):
        self.agent_type = "General"
        self.system_prompt = GENERAL_AGENT_SYSTEM_PROMPT
        self.knowledge_base = self._load_knowledge_base()
        self.conversation_history = []

    def _load_knowledge_base(self)-> List[Dict]:
        kb_path = os.path.join(
            config.KNOWLWDGE_BASE_DIR,
            "general",
            "faq.json"
        )
        try:
            with open(kb_path,'r') as f:
                kb = json.load(f)
                print(f"loaded {len(kb)} items from general knowledge base")
                return kb
        except FileNotFoundError:
            print(f"knowldge base not found {kb_path}")
            return []
        except json.JSONDecodeError as e:
            print(f"error parsing knowledge base {e}")
            return []
    
    def search_knowledge_base(self, query: str, top_k: int =3)-> List[Dict]:

        embed = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")
        vector_store = InMemoryVectorStore.from_documents(
            embdeeing = embed,
            documents = kb_path)
        similar_docs = vector_store.similarity_search("your query here")
        return similar_docs

