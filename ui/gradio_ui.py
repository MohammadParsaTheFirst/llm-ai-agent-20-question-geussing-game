import gradio as gr
import torch
from ..services.chat_service import ChatService

class GradioUI:
    def __init__(self, chat_service: ChatService):
        self.chat_service = chat_service
    
    def create_interface(self):
        with gr.Blocks() as demo:
            gr.Markdown("## � Main Menu")
            
            # Configs
            with gr.Row():
                with gr.Column(scale=8):
                    gr.Markdown("")  
                with gr.Column(scale=2):
                    with gr.Accordion("⚙️ Configurations", open=False):
                        config_name = gr.Textbox(label="Config Name", placeholder="My setup")
                        exa_api_box = gr.Textbox(label="Exa API Key", type="password")
                        hf_token_box = gr.Textbox(label="HuggingFace Token", type="password")
                        config_selector = gr.Radio(["Default", "Custom1", "Custom2"], label="Active Config")
            
            # Menu Options
            with gr.Row():
                btn_game = gr.Button("🎮 20 Questions Game")
                btn_news = gr.Button("📰 News Check")
                btn_chat = gr.Button("💬 Chatbot")
                btn_pdf = gr.Button("📄 PDF/Text Reading")
            
            # Pages
            chatbot_page = gr.Group(visible=False)
            with chatbot_page:
                gr.Markdown("## 💬 Dual-GPU Mistral Chat")
                chatbot = gr.Chatbot()
                txt = gr.Textbox(placeholder="Type your message here...")
                
                def respond(message, history):
                    bot_response, _ = self.chat_service.generate_response(message)
                    history = history + [[message, bot_response]]
                    return history, history, ""
                
                txt.submit(respond, [txt, chatbot], [chatbot, chatbot, txt])
            
            game_page = gr.Group(visible=False)
            with game_page:
                gr.Markdown("### 🎮 20 Questions Game (Coming soon...)")
            
            news_page = gr.Group(visible=False)
            with news_page:
                gr.Markdown("### 📰 News Check (Coming soon...)")
            
            pdf_page = gr.Group(visible=False)
            with pdf_page:
                gr.Markdown("### 📄 PDF/Text Reading (Coming soon...)")
            
            # Navigation
            def show_page(choice):
                return {
                    chatbot_page: gr.update(visible=(choice=="chat")),
                    game_page: gr.update(visible=(choice=="game")),
                    news_page: gr.update(visible=(choice=="news")),
                    pdf_page: gr.update(visible=(choice=="pdf")),
                }
            
            btn_chat.click(lambda: show_page("chat"), None, [chatbot_page, game_page, news_page, pdf_page])
            btn_game.click(lambda: show_page("game"), None, [chatbot_page, game_page, news_page, pdf_page])
            btn_news.click(lambda: show_page("news"), None, [chatbot_page, game_page, news_page, pdf_page])
            btn_pdf.click(lambda: show_page("pdf"), None, [chatbot_page, game_page, news_page, pdf_page])
        
        return demo
