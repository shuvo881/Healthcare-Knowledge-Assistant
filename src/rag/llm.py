import os
from huggingface_hub import InferenceClient

class RAGLLM:
    def __init__(self, model="MiniMaxAI/MiniMax-M2"):

        self.client = InferenceClient(
            provider="novita",
            api_key=os.getenv("HF_TOKEN", "")
        )
        self.model = model
        

    def generate(self, query, context, language="en"):

        # Prepare the system and user prompts for the LLM
        system_prompt = (
            "You are a helpful assistant who answers questions by using relevant information from various sources. " + \
            "Please provide accurate and clear answers based on the information retrieved." + \
            f"Answer in {language}."
        )

        user_prompt = f"User query: {query}\n\nRelevant information: {context}\n\nAnswer:"

        
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},  # System message to guide the model's behavior
                {"role": "user", "content": user_prompt}     # User query with the retrieved information
            ]
        )
        return completion.choices[0].message.content.split("</think>")[1].strip()


