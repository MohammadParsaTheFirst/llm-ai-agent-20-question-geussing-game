import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from accelerate import infer_auto_device_map, dispatch_model
from .stopping_criteria import StopOnTokens

class ModelLoader:
    def __init__(self, model_name: str = "mistralai/Mistral-7B-Instruct-v0.3"):
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.stopping_criteria = None
        
    def initialize(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
        device_map = infer_auto_device_map(
            AutoModelForCausalLM.from_pretrained(self.model_name, low_cpu_mem_usage=True, torch_dtype=torch.float16),
            max_memory={0: "16GB", 1: "16GB"}
        )
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True
        )
        self.model = dispatch_model(self.model, device_map=device_map)
        
        self.stopping_criteria = StoppingCriteriaList([StopOnTokens([self.tokenizer.eos_token_id])])
        
        return self.tokenizer, self.model, self.stopping_criteria
