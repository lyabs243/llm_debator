# Complete debate interface
import gradio as gr
from model_conversation import Model
from model_debator import MessageTone

def start_debate(topic, initial_message, turns, show_logs, first_model, first_position, first_tone, second_model, second_position, second_tone):
    return f"Debate started on: {topic}\nInitial message: {initial_message}\nTurns: {turns}"

def chat_debate(message, history):
    history = history or []
    response = f"Debater response: {message}"
    history.append((message, response))
    return history, ""

with gr.Blocks(title="LLM Debator - Full Interface") as debate_demo:
    gr.Markdown("<h1 style='text-align: center;'>🤖 LLM Debator</h1>")
    gr.Markdown("<h3 style='text-align: center; color: #666;'>Complete AI Debate Interface</h3>")
    
    # Topic and Initial message in horizontal layout
    with gr.Row():
        topic = gr.Textbox(label="Topic", placeholder="Enter the debate topic", scale=1)
        initial_message = gr.Textbox(label="Initial message", placeholder="Opening message", scale=1)
    
    with gr.Row():
        # Left panel - Configuration
        with gr.Column(scale=1):
            gr.Markdown("## ⚙️ Debate Configuration")
            
            with gr.Row():
                turns = gr.Number(label="Turns", value=5, minimum=1, maximum=20, scale=2)
                with gr.Column(scale=1, min_width=120):
                    gr.HTML("<div style='height: 20px;'></div>")  # Spacer pour aligner verticalement
                    show_logs = gr.Checkbox(label="Show Logs", value=False)
            
            gr.Markdown("### First Debater")
            first_model = gr.Dropdown(
                choices=[model.model_name for model in Model],
                label="Model",
                value=Model.GPT_4_1.model_name
            )
            first_position = gr.Textbox(label="Position", placeholder="First debater's position")
            first_tone = gr.Dropdown(
                choices=[tone.title for tone in MessageTone],
                label="Tone",
                value=MessageTone.FORMAL.title
            )
            
            gr.Markdown("### Second Debater")
            second_model = gr.Dropdown(
                choices=[model.model_name for model in Model],
                label="Model",
                value=Model.GEMINI_2_5_FLASH.model_name
            )
            second_position = gr.Textbox(label="Position", placeholder="Second debater's position")
            second_tone = gr.Dropdown(
                choices=[tone.title for tone in MessageTone],
                label="Tone",
                value=MessageTone.FORMAL.title
            )
        
        # Right panel - Chat
        with gr.Column(scale=2):
            gr.Markdown("## 💬 Chat")
            debate_chatbot = gr.Chatbot(height=650)
            
            with gr.Row():
                start_btn = gr.Button("🚀 Start Debate", variant="primary", scale=2)
                debate_clear = gr.ClearButton([debate_chatbot], value="Reset", scale=1)
    
    # Events
    start_btn.click(
        start_debate,
        inputs=[topic, initial_message, turns, show_logs, first_model, first_position, first_tone, second_model, second_position, second_tone],
        outputs=debate_chatbot
    )

if __name__ == "__main__":
    debate_demo.launch(inbrowser=True)