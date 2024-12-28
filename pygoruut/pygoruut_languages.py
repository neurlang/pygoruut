class PygoruutLanguages:
    def __init__(self):
        # ISO 639 language codes and their corresponding languages
        self.languagesISO639 = {
		"af": "Afrikaans",
		"am": "Amharic",
		"ar": "Arabic",
		"az": "Azerbaijani",
		"be": "Belarusian",
		"bn": "Bengali",
		"my": "Burmese",
		"ceb": "Cebuano",
		"ce": "Chechen",
		"zh": "ChineseMandarin",
		"cs": "Czech",
		"da": "Danish",
		"nl": "Dutch",
		"dz": "Dzongkha",
		"en": "English",
		"eo": "Esperanto",
		"fa": "Farsi",
		"fi": "Finnish",
		"fr": "French",
		"de": "German",
		"el": "Greek",
		"gu": "Gujarati",
		"ha": "Hausa",
		"he": "Hebrew",
		"hi": "Hindi",
		"hu": "Hungarian",
		"is": "Icelandic",
		"id": "Indonesian",
		"tts": "Isan",
		"it": "Italian",
		"jam": "Jamaican",
		"ja": "Japanese",
		"jv": "Javanese",
		"kk": "Kazakh",
		"ko": "Korean",
		"lb": "Luxembourgish",
		"mk": "Macedonian",
		"ml": "Malayalam",
		"ms": "MalayLatin",
		"mt": "Maltese",
		"mr": "Marathi",
		"mn": "Mongolian",
		"ne": "Nepali",
		"no": "Norwegian",
		"ps": "Pashto",
		"pl": "Polish",
		"pt": "Portuguese",
		"pa": "Punjabi",
		"ro": "Romanian",
		"ru": "Russian",
		"sk": "Slovak",
		"es": "Spanish",
		"sw": "Swahili",
		"sv": "Swedish",
		"ta": "Tamil",
		"te": "Telugu",
		"th": "Thai",
		"bo": "Tibetan",
		"tr": "Turkish",
		"uk": "Ukrainian",
		"ur": "Urdu",
		"ug": "Uyghur",
		"vi": "VietnameseNorthern",
		"zu": "Zulu",
		"hy": "Armenian",
		"eu": "Basque",
		"bg": "Bulgarian",
		"ca": "Catalan",
		"ny": "Chichewa",
		"hr": "Croatian",
		"et": "Estonian",
		"gl": "Galician",
		"ka": "Georgian",
		"km": "KhmerCentral",
		"lo": "Lao",
		"lv": "Latvian",
		"lt": "Lithuanian",
		"sr": "Serbian",
		"tl": "Tagalog",
		"yo": "Yoruba"
        }

        # Non-ISO 639 language or dialect names
        self.languagesNonISO639 = [
		"BengaliDhaka",
		"BengaliRahr",
		"MalayArab",
		"VietnameseCentral",
		"VietnameseSouthern"
        ]

    def get_supported_languages(self):
        # Concatenate the keys of languagesISO639 with the values of languagesNonISO639
        return list(self.languagesISO639.keys()) + self.languagesNonISO639

    def get_all_supported_languages(self):
        # Concatenate the keys and values of languagesISO639 with the values of languagesNonISO639
        return list(self.languagesISO639.keys()) + list(self.languagesISO639.values()) + self.languagesNonISO639

    def __getitem__(self, value):
        if len(value) == 2 or len(value) == 3:
            value = self.languagesISO639[value] or value
        return value

# Example usage:
if __name__ == '__main__':
    pygoruut = PygoruutLanguages()
    print(pygoruut.get_supported_languages())
    print(pygoruut["vi"])
