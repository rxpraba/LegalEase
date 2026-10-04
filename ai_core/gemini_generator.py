"""Gemini integration: builds the prompt and calls the model."""
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL


class GeminiDocumentGenerator:
    def __init__(self, model_name: str = GEMINI_MODEL):
        if not GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY is missing. Add it to your .env file.")
        genai.configure(api_key=GEMINI_API_KEY)
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)

    def generate_document(self, document_type, parties, terms, dates) -> str:
        term_lines = "\n".join(
            f"- {t.strip()}" for t in terms.split(";") if t.strip()
        )
        prompt = (
            f"Generate a comprehensive legal document titled '{document_type}'.\n"
            f"Involved parties: {parties}\n"
            f"Effective Date: {dates}\n"
            f"Terms and conditions:\n{term_lines}\n\n"
            "Requirements:\n"
            "- Use formal legal structure with numbered sections (e.g. '1. Services:') "
            "and standard legal clauses (governing law, severability, entire agreement, "
            "termination, confidentiality where relevant).\n"
            "- Incorporate every listed term faithfully.\n"
            "- Use [square-bracket placeholders] for any missing details.\n"
            "- End with an IN WITNESS WHEREOF signature block.\n"
            "- Output plain text only: no markdown, no code fences, no commentary."
        )
        # Try configured model first, then fallback to other active models if unavailable or rate-limited
        fallback_models = list(dict.fromkeys([self.model_name, "gemini-3.5-flash", "gemini-3.5-flash-lite", "gemini-3.7-flash"]))
        last_error = None
        for m_name in fallback_models:
            try:
                model = genai.GenerativeModel(m_name)
                response = model.generate_content(prompt)
                if response and response.text:
                    return response.text
            except Exception as e:
                last_error = e
                continue
        if last_error:
            raise last_error
        raise RuntimeError("Failed to generate document with available Gemini models.")

