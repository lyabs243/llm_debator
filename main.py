# Complete debate interface
import gradio as gr
from dotenv import load_dotenv
from model_conversation import Model
from model_debator import MessageTone, ModelDebator
from model_debate import ModelDebate

load_dotenv(override=True)

# Store debate state
current_debate = None
debate_config = {}

async def start_debate(topic, initial_message, turns, show_logs, first_model, first_position, first_tone, second_model, second_position, second_tone, history):
    global current_debate, debate_config
    
    try:
        # Ensure history is not None
        if history is None:
            history = []
            
        # Check if we're starting a new debate or continuing
        new_config = {
            'topic': topic,
            'first_model': first_model,
            'first_position': first_position,
            'first_tone': first_tone,
            'second_model': second_model,
            'second_position': second_position,
            'second_tone': second_tone
        }
        
        # If config changed or no debate exists, start new
        if current_debate is None or debate_config != new_config:
            debate_config = new_config
            
            # Get enums from strings
            first_model_enum = next(model for model in Model if model.model_name == first_model)
            first_tone_enum = next(tone for tone in MessageTone if tone.title == first_tone)
            second_model_enum = next(model for model in Model if model.model_name == second_model)
            second_tone_enum = next(tone for tone in MessageTone if tone.title == second_tone)
            
            # Create debators
            first_debator = ModelDebator(model=first_model_enum, debate_for=first_position, tone=first_tone_enum)
            second_debator = ModelDebator(model=second_model_enum, debate_for=second_position, tone=second_tone_enum)
            
            # Create debate
            current_debate = ModelDebate(
                debator_a=first_debator,
                debator_b=second_debator,
                topic=topic,
                turns=turns,
                initial_message=initial_message,
                log=show_logs
            )
            
            # Run debate and get history
            history = await current_debate.debate()
        else:
            # Continue the debate for additional turns
            current_debate.turns = turns
            # Check if history is empty or incomplete after reset
            if not history or len(history) == 0:
                # Restart the debate if history is empty
                history = await current_debate.debate()
            else:
                # Get the last message from history to continue
                last_message = history[-1][1] if len(history) > 0 and history[-1][1] is not None else current_debate.initial_message
                
                # Get new messages
                for _ in range(turns):
                    response_a = await current_debate.debator_a.send_message(message=last_message)
                    history.append((f"**{current_debate.debator_a.model.model_name}**: {response_a}", None))
                    
                    response_b = await current_debate.debator_b.send_message(message=response_a)
                    history[-1] = (history[-1][0], f"**{current_debate.debator_b.model.model_name}**: {response_b}")
                    
                    # Update last_message for the next iteration
                    last_message = response_b
        
        # Print logs to console if enabled
        if show_logs and current_debate:
            for log in current_debate.history:
                print(log)
        
        return history
    except Exception as e:
        print(f"Error: {str(e)}")
        return [("Error", f"An error occurred: {str(e)}.")]

def reset_debate():
    global current_debate, debate_config
    current_debate = None
    debate_config = {}
    return []

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
                start_btn = gr.Button("➕ Continue Debate", variant="primary", scale=2)
                debate_clear = gr.Button("Reset", scale=1)
    
    # Events
    start_btn.click(
        start_debate,
        inputs=[topic, initial_message, turns, show_logs, first_model, first_position, first_tone, second_model, second_position, second_tone, debate_chatbot],
        outputs=debate_chatbot
    )
    
    debate_clear.click(
        reset_debate,
        outputs=debate_chatbot
    )

if __name__ == "__main__":
    debate_demo.launch(inbrowser=True)