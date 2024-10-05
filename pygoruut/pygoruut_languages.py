class PygoruutLanguages:
    def __init__(self):
        # ISO 639 language codes and their corresponding languages
        self.languagesISO639 = {
		"ar": "Arabic",
		"bn": "Bengali",
		"zh": "ChineseMandarin",
		"cs": "Czech",
		"nl": "Dutch",
		"en": "English",
		"eo": "Esperanto",
		"fa": "Farsi",
		"fi": "Finnish",
		"fr": "French",
		"de": "German",
		"el": "Greek",
		"gu": "Gujarati",
		"hi": "Hindi",
		"hu": "Hungarian",
		"is": "Icelandic",
		"tts": "Isan",
		"it": "Italian",
		"jam": "Jamaican",
		"ja": "Japanese",
		"lb": "Luxembourgish",
		"ms": "MalayLatin",
		"mr": "Marathi",
		"no": "Norwegian",
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
		"tr": "Turkish",
		"uk": "Ukrainian",
		"ur": "Urdu",
		"vi": "VietnameseNorthern"
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
