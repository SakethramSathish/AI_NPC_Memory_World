import google.generativeai as genai
from typing import Optional
from config import (
    GEMINI_API_KEY,
    LLM_MODEL_NAME,
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS,
)

#Gemini Initialization

genai.configure(api_key=GEMINI_API_KEY)

class GeminiLLM:
    """
    Centralized Gemini wrapper for ALL agents.
    """

    def __init__(
        self,
        model_name: str = LLM_MODEL_NAME,
        temperature: float = LLM_TEMPERATURE,
        max_tokens: int = LLM_MAX_TOKENS,      
    ):
        self.model = genai.GenerativeModel(model_name)
        self.temperature = temperature
        self.max_tokens = max_tokens

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,  
    ) -> str:
        """
        Generate a response from Gemini using a structured prompt.
        """

        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"

        response = self.model.generate_content(
            full_prompt,
            generation_config={
                "temperature": self.temperature,
                "max_output_tokens": self.max_tokens,
            },
        )

        if not response or not response.text:
            raise RuntimeError("Gemini returned an empty response.")
        
        return response.text.strip()
    
#Singleton Accessor

_llm_instance: Optional[GeminiLLM] = None

def get_llm() -> GeminiLLM:
    """
    Returns a singleton instance of GeminiLLM.
    """
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = GeminiLLM()
    return _llm_instance