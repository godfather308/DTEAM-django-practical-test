import logging

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

def ai_translate_cv(cv_id, language):

    cv_dict_translated = {
        'pk': cv_dict['id'],
        'first_name': cv_dict['first_name'],
        'last_name': cv_dict['last_name'],
        'bio': ai_translate_text(cv_dict['bio'], language),
        'skills': cv_dict['skills'],
        'projects': [
            {
                'project': project['project'],
                'description': ai_translate_text(project['description'], language)
            }
            for project in cv_dict['projects']
        ],
        'contacts': cv_dict['contacts'],
    }
    return cv_dict_translated
