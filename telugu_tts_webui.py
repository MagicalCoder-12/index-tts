#!/usr/bin/env python3
"""
Telugu Text-to-Speech WebUI using Gradio and Meta MMS-TTS
"""

import gradio as gr
import torch
import scipy.io.wavfile
from transformers import VitsModel, AutoTokenizer
import os
from pathlib import Path


class TeluguTTSWebUI:
    def __init__(self):
        """Initialize the Telugu TTS model."""
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
    
    def load_model(self):
        """Load the Meta MMS-TTS Telugu model."""
        if self.model is None:
            print("Loading Meta MMS-TTS Telugu model...")
            self.model = VitsModel.from_pretrained("facebook/mms-tts-tel")
            self.tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-tel")
            self.model.to(self.device)
            print("✓ Model loaded successfully!")
        return self.model, self.tokenizer
    
    def generate_speech(self, text):
        """Generate Telugu speech from text."""
        if not text.strip():
            return None, "Error: Please enter Telugu text"
        
        try:
            # Load model if not already loaded
            model, tokenizer = self.load_model()
            
            print(f"Generating speech for: {text[:50]}...")
            
            # Tokenize
            inputs = tokenizer(text=text, return_tensors="pt").to(self.device)
            
            # Generate speech
            with torch.no_grad():
                outputs = model(**inputs)
            
            # Get waveform and sampling rate
            waveform = outputs.waveform[0].cpu().numpy()
            sampling_rate = model.config.sampling_rate
            
            return (sampling_rate, waveform), f"✓ Generated {len(waveform) / sampling_rate:.2f} seconds of Telugu speech"
        
        except Exception as e:
            return None, f"Error: {str(e)}"
    
    def generate_with_examples(self, text):
        """Generate speech with example texts."""
        if not text.strip():
            # Use default examples
            examples = [
                "నమస్కారం, నేను తెలుగు మాట్లాడతాను",
                "తెలుగు భాష చాలా అందంగా ఉంది",
                "కృత్రిమ మేధస్సు భవిష్యత్తు సాంకేతికత",
            ]
            
            results = []
            for example in examples:
                audio, msg = self.generate_speech(example)
                if audio:
                    results.append((audio, example))
            
            if results:
                return results[0][0], f"Generated {len(results)} examples. Showing first one."
            else:
                return None, "Error generating examples"
        else:
            # Generate with provided text
            return self.generate_speech(text)
    
    def create_interface(self):
        """Create the Gradio interface."""
        with gr.Blocks(title="Telugu Text-to-Speech", theme=gr.themes.Soft()) as demo:
            gr.Markdown("# 🎤 Telugu Text-to-Speech (Meta MMS-TTS)")
            gr.Markdown(
                "Generate high-quality Telugu speech from text. "
                "Powered by Meta's Massively Multilingual Speech (MMS-TTS) model."
            )
            
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 📝 Input")
                    
                    text_input = gr.Textbox(
                        label="Telugu Text",
                        placeholder="Enter your Telugu text here...",
                        lines=4,
                        value="నమస్కారం, ఇది తెలుగు వాయిస్ సింథసిస్"
                    )
                    
                    gr.Markdown("**Example Telugu Sentences:**")
                    gr.Examples(
                        examples=[
                            "నమస్కారం, నేను తెలుగు మాట్లాడతాను",
                            "తెలుగు భాష చాలా అందంగా ఉంది",
                            "కృత్రిమ మేధస్సు భవిష్యత్తు సాంకేతికత",
                            "ఈ రోజు మంచి రోజు",
                            "మన సంస్కృతి చాలా గొప్పది",
                        ],
                        inputs=text_input,
                        label="Quick Examples"
                    )
                
                with gr.Column(scale=1):
                    gr.Markdown("### 🔊 Output")
                    
                    audio_output = gr.Audio(
                        label="Generated Speech",
                        type="numpy",
                        interactive=False
                    )
                    
                    status_output = gr.Textbox(
                        label="Status",
                        interactive=False,
                        value="Ready to generate..."
                    )
            
            with gr.Row():
                generate_btn = gr.Button(
                    "🎵 Generate Speech",
                    variant="primary",
                    size="lg"
                )
                clear_btn = gr.Button(
                    "🗑️ Clear",
                    size="lg"
                )
            
            gr.Markdown("---")
            gr.Markdown(
                "**About:** This interface uses Meta's MMS-TTS model trained on Telugu speech data. "
                "It generates high-quality, natural-sounding Telugu audio from text input. "
                "First generation may take longer as the model is downloaded (~145MB)."
            )
            
            # Button actions
            generate_btn.click(
                fn=self.generate_speech,
                inputs=text_input,
                outputs=[audio_output, status_output]
            )
            
            clear_btn.click(
                fn=lambda: (None, "", "Ready to generate..."),
                outputs=[audio_output, text_input, status_output]
            )
            
            # Auto-generate on Enter
            text_input.submit(
                fn=self.generate_speech,
                inputs=text_input,
                outputs=[audio_output, status_output]
            )
        
        return demo


def main():
    """Launch the WebUI."""
    webui = TeluguTTSWebUI()
    demo = webui.create_interface()
    
    print("\n" + "="*60)
    print("Telugu TTS WebUI Started!")
    print("="*60)
    print("\n🌐 Open your browser to the URL shown below:")
    print("\n   http://127.0.0.1:7860\n")
    print("="*60 + "\n")
    
    demo.launch(
        share=False,
        server_name="127.0.0.1",
        server_port=7860,
        show_error=True
    )


if __name__ == "__main__":
    main()
