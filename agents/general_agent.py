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
    
    def _create_vector_store(self):
        if not self.knowledge_base:
            print("no knowledg base found")
            return None
        try:
            documents =[]
            for item in self.knowledge_base:
                text = f"Question: {item['question']}\n Answers: {item['answer']}"
                doc = documents(
                    page_content = text,
                    metadata={
                        'id': item.get('id','')
                        'category': item.get('category','')
                        'question': item.get('question','')
                        'answer': item.get('answer','')
                    }
                )
                documents.append(doc)
            vector_store = InMemoryVectorStore(
                documents= documents,
                embedding= self.embeddings
            )
            print(f"vector store created containing {len(documents)} documents")
            return vector_store
        
        except Exception as e:
            print("failed to create vector store{e}")
            return None

    def search_knowledge_base(self, query: str, top_k: int =3)-> List[Dict]:

        if self.vector_store:
            try:
                similar_docs = self.vector_store.similarity_search(
                    query = query,
                    k = top_k
                )
                results=[]
                for docs in similar_docs:
                    results.append({
                        'id' : docs.metadata.get('id',''),
                        'category': docs.metadata.get('category',''),
                        'question': docs.metadata.get('question',''),
                        'answer': docs.metadata.get('answer','')
                    })
                print(f"found {len(results)} through vector search")
                return results
            
            except Exception as e:
                print(f"vector search failed {e}")
        return self._keyword_search(query, top_k)
    
    def _keyword_search(self, query:str, top_k: int =3):
        if not self.knowledge_base:
            return None
        

