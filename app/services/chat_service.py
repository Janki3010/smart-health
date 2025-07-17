from transformers import pipeline
from app.schemas.ChatRequest import ChatRequest

class ChatService:
    def __init__(self):
        self.pipe = pipeline("text2text-generation", model="google/flan-t5-base")

    def get_ai_response(self, chat: ChatRequest):
        prompt = f"Answer the following medical question:\n{chat.question}"
        result = self.pipe(prompt, max_new_tokens=150)[0]["generated_text"]

        return {
            "question": chat.question,
            "answer": result.strip()
        }