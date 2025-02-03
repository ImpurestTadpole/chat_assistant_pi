import tkinter as tk
from tkinter import ttk
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch

class ChatAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Chat Assistant")
        
        # Initialize AI model
        self.tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/Janus-Pro-1B")
        
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        
        self.model = AutoModelForCausalLM.from_pretrained(
            "deepseek-ai/Janus-Pro-1B",
            device_map="auto",
            quantization_config=quantization_config,
            trust_remote_code=True
        )
        
        self.create_widgets()
    
    def create_widgets(self):
        # Input Frame
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=10, padx=10, fill=tk.X)
        
        self.input_entry = ttk.Entry(input_frame, width=50)
        self.input_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.input_entry.bind("<Return>", self.process_input)
        
        submit_btn = ttk.Button(input_frame, text="Send", command=self.process_input)
        submit_btn.pack(side=tk.RIGHT, padx=5)
        
        # Chat History
        self.chat_history = tk.Text(self.root, wrap=tk.WORD, height=20, width=70)
        self.chat_history.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)
        self.chat_history.config(state=tk.DISABLED)
    
    def process_input(self, event=None):
        user_input = self.input_entry.get()
        self.input_entry.delete(0, tk.END)
        
        if user_input.strip():
            self.update_chat(f"You: {user_input}\n")
            
            # Generate response
            response = self.generate_response(user_input)
            self.update_chat(f"Assistant: {response}\n\n")
    
    def generate_response(self, prompt):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.7,
            top_p=0.9
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    def update_chat(self, text):
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, text)
        self.chat_history.see(tk.END)
        self.chat_history.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatAssistant(root)
    root.mainloop()