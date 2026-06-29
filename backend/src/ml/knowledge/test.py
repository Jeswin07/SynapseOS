from groq import Groq
from src.core.config import settings

client = Groq(api_key=settings.groq_api_key)

for model in client.models.list().data:
    print(model.id)