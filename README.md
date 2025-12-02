# localize_xcode

Localizable.xcstrings is Apple's modern, structured file format for managing localized strings in Xcode consolidating
all translatable content into a single, JSON-like catalog.

## Example (input) Localizable.xcstrings

```json
{
  "sourceLanguage": "en",
  "strings": {
    "HELLO_WORLD": {
      "extractionState": "manual",
      "localizations": {
        "en": {
          "stringUnit": {
            "state": "translated",
            "value": "Hello World"
          }
        }
      }
    }
  },
  "version": "1.0"
}
```

This python script will parse the Localizable.xcstrings looking for all string keys. In the example above there is only one string key in the reference language English "en" "HELLO_WORLD". The script will generate for each "en" key for all of the localizations in your .env file.

For example if your .env file has the variable LANGUAGES

```text
LANGUAGE_CODES="en,es,fr,pt,it,de"
```
[Reference language codes](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes)

* A Spanish, French, Portuguese, Italian and German translation would be added to Localizable.xcstrings when this script calls the Google Cloud Translation API.

* If a translation already exists for any key in the LANGUAGE_CODES list, it will be be preserved (skipped). This is to prevent any manual edits that you may have made to the translated string and to save any costs associated with invoking the Google Cloud API.

## Google Cloud Translation API

The Google Cloud Localization API, more formally known as the Cloud Translation API, provides a programmatic interface
for integrating Google's neural machine translation capabilities into applications and websites. It enables dynamic
translation of text between various supported languages.

### Google Cloud  setup

* Project Setup:

- Create a Google Cloud Project: All Google Cloud services, including localization APIs, require a project to manage
  resources, billing, and permissions. This is done through the Google Cloud Console.
- Enable the API: Navigate to the "APIs & Services" library within your project and enable the specific localization API
  you intend to use (e.g., Cloud Translation API, Cloud Natural Language API).

* Authentication:

- Service Accounts: For secure and programmatic access, create a Google Cloud service account. This account represents
  your application and can be granted specific roles and permissions to access the API, adhering to the principle of
  least privilege.

# Setup

## Python3 Virtual Environment

```bash
python3 -m venv .venv
source ./.venv/bin/activate
pip3 install --upgrade pip
pip3 install .
export PYTHONPATH="$PYTHONPATH:$PWD"
```

## Runtime Configuration

Example .env with values that contain secrets or values not likely to change

```bash
GOOGLE_APPLICATION_CREDENTIALS="Path to your Google Cloud json credentials file with permissions to call the Localization API"
GOOGLE_PROJECT_ID="Your Google Cloud project id .i.e. cs-host-??????????????????????"
LANGUAGES="en,es,fr,pt,it,de"
```
# run localize_xcode

## IMPORTANT make a backup of your Localizable.xcstrings

```bash
cp -p ./Localizable.xcstrings ./Localizable.xcstrings.ORIGINAL
python3 src/main.py --file ./Localizable.xcstrings
```
### Example (expected output) Localizable.xcstrings

```json
{
  "sourceLanguage": "en",
  "strings": {
    "HELLO_WORLD": {
      "extractionState": "manual",
      "localizations": {
        "en": {
          "stringUnit": {
            "state": "translated",
            "value": "Hello World"
          }
        },
        "es": {
          "stringUnit": {
            "state": "translated",
            "value": "Hola Mundo"
          }
        },
        "fr": {
          "stringUnit": {
            "state": "translated",
            "value": "Bonjour le monde"
          }
        },
        "pt": {
          "stringUnit": {
            "state": "translated",
            "value": "Olá, mundo!"
          }
        },
        "it": {
          "stringUnit": {
            "state": "translated",
            "value": "Ciao mondo"
          }
        },
        "de": {
          "stringUnit": {
            "state": "translated",
            "value": "Hallo Welt"
          }
        }
      }
    }
  },
  "version": "1.0"
}
```
