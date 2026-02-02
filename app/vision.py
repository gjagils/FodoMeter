import base64
import json

from openai import AsyncOpenAI

from app.config import OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """Je bent een voedingsexpert. Analyseer de foto van een maaltijd en geef een lijst
van ingrediënten terug in het Nederlands, geschikt om in te voeren in de Eetmeter
(Voedingscentrum).

Geef per ingrediënt:
- naam (Nederlands, zoals je het in de Eetmeter zou zoeken)
- geschat gewicht in grammen
- bereiding (rauw, gekookt, gebakken, gestoomd, etc.)

Antwoord ALLEEN met een JSON array, geen andere tekst. Voorbeeld:
[
  {"naam": "witte rijst", "gewicht_gram": 150, "bereiding": "gekookt"},
  {"naam": "kipfilet", "gewicht_gram": 120, "bereiding": "gebakken"},
  {"naam": "broccoli", "gewicht_gram": 80, "bereiding": "gestoomd"}
]"""


async def analyze_photo(image_bytes: bytes, content_type: str) -> list[dict]:
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    media_type = content_type if content_type else "image/jpeg"

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{media_type};base64,{base64_image}"
                        },
                    },
                    {
                        "type": "text",
                        "text": "Welke ingrediënten zie je in deze maaltijd? Geef een JSON lijst.",
                    },
                ],
            },
        ],
        max_tokens=1000,
        temperature=0.2,
    )

    text = response.choices[0].message.content.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        text = text.rsplit("```", 1)[0]
    return json.loads(text)
