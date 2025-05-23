import logging
from copy import deepcopy

from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

LANGUAGES = [
    'Bislama',
    'Breton',
    'Chuvash',
    'Cornish',
    'Kashubian',
    'Manx',
    'Upper Sorbian',
    'Inuktitut',
    'Kalaallisut',
    'Ladino',
    'Livonian',
    'Occitan',
    'Romani',
    'Northern Sami',
    'Saramaccan',
    'Tsakonian',
    'Zazaki',
]

MESSAGE_TEMPLATE = 'You are a pro English/{language} translator with 20 years of experience. Translate the text below'

def ai_translate_text(text, language, model="gpt-3.5-turbo"):
    system_message = {
        "role": "system",
        "content": MESSAGE_TEMPLATE.format(language=language)
    }
    user_message = {"role": "user", "content": text}

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[system_message, user_message]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(e)
        return text

def ai_translate_cv(cv_dict, language):
    translated_cv = deepcopy(cv_dict)

    translated_cv['bio'] = ai_translate_text(cv_dict['bio'], language)

    for pi, project in enumerate(translated_cv['projects']['all']):
        translated_cv['projects']['all'][pi]['description'] = ai_translate_text(project['description'], language)

    for ci, contact in enumerate(translated_cv['contacts']['all']):
        translated_cv['contacts']['all'][ci]['option'] = ai_translate_text(contact['option'], language)

    return translated_cv
