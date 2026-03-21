from fastapi import APIRouter, HTTPException
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Carga la llave desde el archivo .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configuración de Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

router = APIRouter(prefix="/ai", tags=["IA Financiera"])

@router.get("/consultar")
async def consultar_ia(pregunta: str):
    try:
        # Aquí le damos la "personalidad" de Finara
        prompt_config = f"Eres Finara, un asistente de educación financiera. Responde de forma clara y motivadora: {pregunta}"
        
        response = model.generate_content(prompt_config)
        return {"respuesta": response.text}
    except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la IA: {str(e)}") from e