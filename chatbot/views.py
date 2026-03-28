from django.shortcuts import render
from django.http import JsonResponse
import json
from openai import OpenAI
import os
from dotenv import load_dotenv

#Correct .env loading (absolute path)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(BASE_DIR, '.env')


load_dotenv(env_path)


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print("KEY:", os.getenv("OPENAI_API_KEY"))
def home(request):
    return render(request, 'chatbot/index.html')


def chat(request):
    

    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message")

        prompt = f"""
Act as a professional customer support chatbot for an online course platform.

Your job is to help users with course and enrollment questions.

Course Data:
- Python Course: 3 months, ₹5000, weekend batch
- Django Course: 2 months, ₹4000, weekday batch

Scope:
Answer only about:
- Course details
- Fees
- Duration
- Enrollment

Rules:
- Be polite and friendly
- Use simple Indian English
- Keep answers short (2–3 lines)
- Do not use any information outside given data
- Do not guess anything
- If question is unclear, ask 1 simple question
- If question is unrelated, say:
  "I can help only with course and enrollment questions."

Response Style:
- Clear and direct

User: {user_message}
"""

        try:
            response = client.responses.create(
                model="gpt-4.1-mini",
                input=prompt
            )
            reply = response.output[0].content[0].text

        except Exception as e:
            print("FULL ERROR:", e)
            reply = str(e)

        return JsonResponse({"reply": reply})

    return JsonResponse({"reply": "Invalid request"})