import groq
from typing import List, Optional, Dict
import time
from config import config

class LLMClient:

    def __init__(self):
        self.client = groq.Groq(api_key= config.GROQ_API_KEY)
        self.model = config.MODEL_NAME
        self.max_tokens = config.MAX_TOKENS
        self.temperature = config.TEMPERATURE
    
    def generate_response(
            self,
            system_prompt: str,
            user_message: str,
            conversation_history: Optional[List[Dict[str, str]]] = None,
            temperature: Optional[float]= None,
            max_tokens: Optional[int]= None
    )-> str:
        messages=[]
        if conversation_history:
            messages.extend(conversation_history)
        
        messages.append({"role":"user", "content": user_message})

        for attempt in range(config.MAX_RETRIES):
            try:
                response = self.client.message.create(
                    model = self.model,
                    max_tokens = self.max_tokens,
                    temperature = self.temperature,
                    system = system_prompt,
                    messages= messages
                )
                return response.content[0].text
            except groq.APIError as error:
                print(f"API error(attempt {attempt+1}/{config.MAX_RETRIES}):{error}")
                if attempt < config.MAX_RETRIES-1:
                    time.sleep(2 ** attempt)
                else:
                    return"facing issues connecting at this moment, please try again"
            except Exception as e:
                print(f"Unexpected error{e}")
                return"an unexpected error occured. please try again"
    
    def generate_with_tools(
            self,
            system_prompt:str,
            user_message:str,
            tools: List[Dict],
            conversation_history: Optional[List[Dict[str,str]]]= None
    )-> Dict:
        messages=[]
        if conversation_history:
            messages.extend(conversation_history)
        messages.append({"role":"user", "content":user_message})

        try:
            response = self.client.messages.create(
                model = self.model,
                max_tokens= self.max_tokens,
                system = system_prompt,
                messages = messages,
                tools = tools
            )
            return{
                "content": response.content,
                "stop_reason": response.stop_reason
            }
        except Exception as e:
            print("error in tool calling")
            return{
                "content":[{"typr":"text", "text":"error processing request"}],
                "stop_reason": "error"
            }

    def classify_query(
            self,
            query:str,
            categories: List[str]
    )-> str:
        
        category_list= ", ".join(categories)
        prompt = f"""Classify this customer support query into exactly ONE of these categories: {category_list} Query: "{query}"
                Respond with ONLY the category name, nothing else."""
        
        system = "You are a query classification system. Always respond with exactly one category name."

        response= self.generate_response(
            system_prompt = system,
            user_message= prompt,
            temperature = 0.3
        ) 
        category = response.strip().lower()
        if category not in category_list:
            print(f"warning unexpected query{category} defaulting to general")
            return "general"
        
llm_client = LLMClient()