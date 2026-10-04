# LegalEase - AI Legal Document Generator
FastAPI backend + Streamlit frontend + Gemini. Exports .txt, .docx, .pdf.

## Setup
    python -m venv venv && source venv/bin/activate   # Windows: venv\scripts\activate
    pip install -r requirements.txt
    cp .env.example .env    # then add GEMINI_API_KEY

## Run
    uvicorn legalEaseAPI.main:app --reload     # terminal 1 (port 8000)
    streamlit run frontend/app.py              # terminal 2 (port 8501)
or `./run.sh` for both.

## Notes
- Model defaults to gemini-1.5-pro (per spec). If Google reports it as
  unavailable, set GEMINI_MODEL in .env to a current Gemini model.
- Replace Image/Logo.png (light bg) and Image/inverseLogo.png (dark UI) with your own branding.
- Deploy: backend via Procfile/Dockerfile (Render, Railway, Fly.io); frontend on
  Streamlit Community Cloud with BACKEND_URL pointing to the deployed API.
- AI-generated documents are drafts; have a lawyer review before use.
