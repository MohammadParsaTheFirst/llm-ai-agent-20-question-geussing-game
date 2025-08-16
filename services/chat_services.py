from typing import Tuple
import torch
from ..models.model_loader import ModelLoader
from ..services.exa_service import ExaService
from ..utils.helpers import manage_chat_history

class ChatService:
    def __init__(self, hf_token: str, exa_api_key: str):
        self.hf_token = hf_token
        self.exa_api_key = exa_api_key
        self.chat_history = []
        self.MAX_HISTORY = int(os.getenv("MAX_HISTORY", 3))  # Default to 3 if not set
        
        # Initialize services
        model_name = os.getenv("MODEL_NAME", "mistralai/Mistral-7B-Instruct-v0.3")
        self.model_loader = ModelLoader(model_name)
        self.tokenizer, self.model, self.stopping_criteria = self.model_loader.initialize()
        self.exa_service = ExaService(self.exa_api_key)
        # self.hf_token = hf_token
        # self.exa_api_key = exa_api_key
        # self.chat_history = []
        # self.MAX_HISTORY = 3
        
        # # Initialize services
        # self.model_loader = ModelLoader()
        # self.tokenizer, self.model, self.stopping_criteria = self.model_loader.initialize()
        # self.exa_service = ExaService(self.exa_api_key)
    
    def generate_initial_response(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda:0")
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=150,
            do_sample=False,
            pad_token_id=self.tokenizer.eos_token_id,
            stopping_criteria=self.stopping_criteria
        )
        return self.tokenizer.decode(outputs[0][len(inputs["input_ids"][0]):], skip_special_tokens=True).strip()
    
    def generate_response(self, prompt: str) -> Tuple[str, bool]:
        # Build context with proper formatting
        context = "\n".join(
            f"User: {conv['user']}\nAssistant: {conv['assistant']}" 
            for conv in self.chat_history
        )
        full_prompt = f"[INST]Context:\n{context}\n\nNew query: {prompt}\nProvide only the direct answer to the new query without adding any additional queries, examples, or continuations.\nAnswer:[/INST]"
        
        needs_search = self.exa_service.requires_search(prompt)
        search_result = self.exa_service.search(prompt) if needs_search else ""
        
        initial_response = self.generate_initial_response(full_prompt)
        
        final_response = initial_response
        if needs_search and search_result and not search_result.startswith("[Search error") and not search_result.startswith("[No relevant"):
            final_response += f"\n\n[Based on recent searches]:\n{search_result}"
        
        self.chat_history = manage_chat_history(
            self.chat_history,
            prompt,
            final_response,
            self.MAX_HISTORY
        )
        
        return final_response, needs_search
