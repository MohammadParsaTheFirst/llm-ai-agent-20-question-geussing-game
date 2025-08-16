# main.py
import os
from dotenv import load_dotenv
from huggingface_hub import login
from utils.setup import check_and_install_packages
from services.chat_service import ChatService
from ui.gradio_ui import GradioUI
import torch

def main():
    # Load environment variables
    load_dotenv()
    HF_TOKEN = os.getenv("HF_TOKEN")
    EXA_API_KEY = os.getenv("EXA_API_KEY")
    
    if not HF_TOKEN or not EXA_API_KEY:
        raise ValueError("Please set HF_TOKEN and EXA_API_KEY in .env file")
    
    # Check and install required packages
    check_and_install_packages()
    
    # Login to HuggingFace
    login(token=HF_TOKEN)
    
    # Initialize services
    chat_service = ChatService(
        hf_token=HF_TOKEN,
        exa_api_key=EXA_API_KEY
    )
    
    # Create and launch UI
    ui = GradioUI(chat_service)
    demo = ui.create_interface()
    
    # Print GPU memory info
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        print(f"GPU 0 Memory: {torch.cuda.memory_allocated(0)/1024**2:.2f}MB used")
        if torch.cuda.device_count() > 1:
            print(f"GPU 1 Memory: {torch.cuda.memory_allocated(1)/1024**2:.2f}MB used")
    
    demo.launch()

if __name__ == "__main__":
    main()
