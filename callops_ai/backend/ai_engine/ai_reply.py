from groq import Groq
from django.conf import settings

BUSINESS_KEYWORDS = [
    "tarif",
    "narx",
    "price",
    "integratsiya",
    "integration",
    "shartnoma",
    "bog‘lanish",
    "aloqa",
    "xizmat",
    "buyurtma"
]



def is_business_question(text: str) -> bool:
    text = text.lower()
    return any(keyword in text for keyword in BUSINESS_KEYWORDS)


client = Groq(api_key=settings.GROQ_API_KEY)

SYSTEM_PROMPT = """
Siz 'Namuna:Jahongir' kompaniyasining rasmiy AI assistentsiz.

SIZ FAQAT quyidagi mavzularga javob berasiz:
- CallOps xizmatlari
- tariflar va narxlar
- buyurtma va ulanish
- integratsiya
- shartnoma va aloqa

Agar savol BU doiraga kirmasa:
FAKT: hech qanday tushuntirishsiz faqat:
NOT_IN_SCOPE
deb javob bering.

Agar savol doiraga kirsa, lekin murakkab bo‘lsa:
OPERATOR_NEEDED deb yozing.

Hech qachon umumiy savollarga javob bermang.
"""

def is_business_question(text: str) -> bool:
    text = text.lower()
    return any(word in text for word in BUSINESS_KEYWORDS)



def ai_answer(user_text: str) -> str:
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            temperature=0.0,
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print("❌ AI ERROR:", e)
        return "OPERATOR_NEEDED"

