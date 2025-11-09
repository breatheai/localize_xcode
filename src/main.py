import json
import os
import re
from typing import Dict
from dotenv import load_dotenv
import argparse
# Cloud Translation v3 client instance
from google.cloud import translate_v3
from google.api_core import client_options

# Load environment variables from .env file
load_dotenv()

class Localize:
    def __init__(self, input_file_path):
        # Create a client
        self.gcp_project_id = os.getenv("GOOGLE_PROJECT_ID")
        self.parent = f"projects/{self.gcp_project_id}"
        self.parent_resource=f"projects/{self.gcp_project_id}/locations/global"
        self.input_file_path = input_file_path
        self.v3_client = translate_v3.TranslationServiceClient(client_options=client_options.ClientOptions(quota_project_id=self.gcp_project_id))


    # https://www.kaggle.com/code/kornelregius/google-cloud-translation-tutorial
    def translate(self, text_to_translate, target_language_code):
        request={
            "parent": self.parent_resource,
            "contents": [text_to_translate],
            "mime_type": "text/plain",  # mime types can be: text/plain, text/html
            "target_language_code": target_language_code,
        }
        response = self.v3_client.translate_text(request=request)
        for translation in response.translations:
            # print(f"Translated text: {translation.translated_text}")
            return translation.translated_text
        return None


    def parse_localizations(self, localizations: Dict):
        # reset language code cache each time, remove all blanks and use comma as delimiters
        language_codes = re.sub(r'\s+', '',os.getenv("LANGUAGE_CODES")).split(",")
        english_translation_exists = False
        for key, value in localizations.items():
            if key is None:
                english_translation_exists = False
                continue
            if key == "en":
                english_translation_exists = True
            language_codes.remove(key)
        if english_translation_exists:
            en_text = localizations["en"]["stringUnit"]["value"]
            for language_code in language_codes:
                translated_text = en_text if (len(en_text) <= 1) else self.translate(en_text, language_code)
                if translated_text is None:
                    translated_text = ""
                localizations[language_code] = {
                    "stringUnit": {
                        "state": "translated",
                        "value": translated_text
                    }
                }


    def edit_xcstrings(self):
        """
        Edits a specific translation for a given key and language in an .xcstrings file.

        Args:
            file_path (str): The path to the Localizable.xcstrings file.
        """

        try:
            with open(self.input_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for key, value in data['strings'].items():
                if 'localizations' in value:
                    self.parse_localizations(value['localizations'])

            with open(self.input_file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        except FileNotFoundError:
            print(f"Error: File not found at '{self.input_file_path}'")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in '{self.input_file_path}'")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


# Example usage:
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='''Xcode Localizable.xcstrings file''')
    parser.add_argument('--file', '-f', type=str, help='path to Xcode strings file, i.e. Localizable.xcstrings',
                    required=True)
    args = parser.parse_args()
    localize = Localize(args.file)
    localize.edit_xcstrings() # "../Localizable.xcstrings"

