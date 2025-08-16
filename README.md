# llm-ai-agent-20-question-geussing-game
```bash
llm-ai-agent-20-question-geussing-game
├── main.py                  # Main entry point that launches the app
├── run.sh                   # Script to run the application
├── setup.sh                 # Script to install dependencies
├── .env                     # Configuration file for API keys (create from .env.example)
├── .env.example             # Example config file template
├── requirements.txt         # Python dependencies
├── utils/                   # Utility functions
│   ├── setup.py             # Handles package installation
│   └── helpers.py           # Helper functions
├── models/                  # AI model related code
│   ├── model_loader.py      # Loads the Mistral model
│   └── stopping_criteria.py # Custom model stopping logic
├── services/                # Core functionality
│   ├── chat_service.py      # Main chat logic
│   └── exa_service.py       # Web search functionality
└── ui/
    └── gradio_ui.py         # Web interface setup
```


## Key Files Explained

### 1. Configuration
- `.env` – Contains all API keys and settings  
- `requirements.txt` – Lists all Python dependencies  

### 2. Core Components
- `chat_service.py` – Brain of the chatbot (handles conversations)  
- `exa_service.py` – Handles web searches when needed  
- `model_loader.py` – Loads the AI model onto GPUs  

### 3. Interface
- `gradio_ui.py` – Creates the web interface  
- `main.py` – Starts everything up  

## How to Run

### First-Time Setup

```bash
chmod +x setup.sh run.sh  # Make scripts executable
./setup.sh                # Install dependencies
cp .env.example .env      # Create config file
```


Then edit the `.env` file:

```ini
HF_TOKEN="your_huggingface_token"
EXA_API_KEY="your_exa_api_key"
```


Run the Application
```bash
./run.sh
```

Access the web interface at:
```bash
http://localhost:7860
```
