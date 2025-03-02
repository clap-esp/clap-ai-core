# Dictionnaire : code langdetect -> code M2M100
# - this dictionary associates the ISO codes of the python langdetect lib with the m2m100 codes

langdetect_to_m2m100 = {
    'af': 'af',      # Afrikaans
    'ar': 'ar',      # Arabic
    'bg': 'bg',      # Bulgarian
    'bn': 'bn',      # Bengali
    'ca': 'ca',      # Catalan
    'cs': 'cs',      # Czech
    'cy': 'cy',      # Welsh
    'da': 'da',      # Danish
    'de': 'de',      # German
    'el': 'el',      # Greeek
    'en': 'en',      # English
    'es': 'es',      # Spanish
    'et': 'et',      # Estonian
    'fa': 'fa',      # Persian
    'fi': 'fi',      # Finnish
    'fr': 'fr',      # French
    'gu': 'gu',      # Gujarati
    'he': 'he',      # Hebrew
    'hi': 'hi',      # Hindi
    'hr': 'hr',      # Croatian
    'hu': 'hu',      # Hungarian
    'id': 'id',      # Indonesian
    'it': 'it',      # Italian
    'ja': 'ja',      # Japanese
    'kn': 'kn',      # Kannada
    'ko': 'ko',      # Korean
    'lt': 'lt',      # Lithuanian
    'lv': 'lv',      # Latvian
    'mk': 'mk',      # Macedonian
    'ml': 'ml',      # Malayalam
    'mr': 'mr',      # Marathi
    'ne': 'ne',      # Nepali
    'nl': 'nl',      # Dutch
    'no': 'no',      # Norwegian
    'pa': 'pa',      # Panjabi
    'pl': 'pl',      # Polish
    'pt': 'pt',      # Portuguese
    'ro': 'ro',      # Romanian
    'ru': 'ru',      # Russian
    'sk': 'sk',      # Slovak
    'sl': 'sl',      # Slovenian
    'so': 'so',      # Somali
    'sq': 'sq',      # Albanian
    'sv': 'sv',      # Swedish
    'sw': 'sw',      # Swahili
    'ta': 'ta',      # Tamil
    'te': 'te',      # Telugu
    'th': 'th',      # Thai
    'tl': 'tl',      # Tagalog
    'tr': 'tr',      # Turkish
    'uk': 'uk',      # Ukrainian
    'ur': 'ur',      # Urdu
    'vi': 'vi',      # Vietnamese`
    'zh-cn': 'zh',   # Chinese
}


def get_m2m100_code(langdetect_code: str) -> str:
    """
    Return the M2M100 code corresponding to the 'langdetect_code'
    """
    return langdetect_to_m2m100.get(langdetect_code.lower())


# Note: Languages that could not be mapped are as follows:
# - Langdetect : 
#   bg - Bulgarian, ca - Catalan, cy - Welsh, da - Danish, et - Estonian, hr - Croatian, lt - Lithuanian, lv - Latvian, sl - Slovenian, so - Somali, sq - Albanian, sv - Swedish, sw - Swahili, vi - Vietnamese
# - m2m100 : 
#   ast - Asturian, az - Azerbaijani, ba - Bashkir, be - Belarusian, br - Breton, bs - Bosnian, ceb - Cebuano, ff - Fulah, fy - Western Frisian, ga - Irish, gd - Gaelic; Scottish Gaelic, gl - Galician, ha - Hausa, ht - Haitian; Haitian Creole, hy - Armenian, ig - Igbo, ilo - Iloko, is - Icelandic, jv - Javanese, ka - Georgian, kk - Kazakh, km - Central Khmer, lb - Luxembourgish; Letzeburgesch, lg - Ganda, ln - Lingala, lo - Lao, mg - Malagasy, mn - Mongolian, ms - Malay, my - Burmese, ns - Northern Sotho, oc - Occitan (post 1500), or - Oriya, ps - Pushto; Pashto, sd - Sindhi, si - Sinhala; Sinhalese, ss - Swati, su - Sundanese, tn - Tswana, uz - Uzbek, wo - Wolof, xh - Xhosa, yi - Yiddish, yo - Yoruba, zu - Zulu