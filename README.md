# Vocabulary Study Tool

This project extracts English vocabulary from a JSON file, generates:

- IPA pronunciation
- Chinese translations
- POS (part of speech)
- Word variants (e.g., synonyms or inflections)

and exports everything to an Excel file for vocabulary learning and review.

---

## 🔧 Requirements

- Python **3.9**
- Internet access (for translation and Datamuse synonyms)
- Input JSON file with the following structure:

```json
{
  "vocabulary_words": [
    "example",
    "another",
    "word"
  ]
}
```

---

## 📦 Installation

Create and activate a virtual environment (optional but recommended):

```bash
python3.9 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### Command Format:

```bash
python main.py [input_json] [output_excel]
```

### Example:

```bash
python main.py cleaned_vocabulary_words.json vocabulary_study_list.xlsx
```

This will:

1. Read vocabulary from `cleaned_vocabulary_words.json`
2. Translate each word to Chinese using Google Translate
3. Get IPA pronunciation using `eng_to_ipa`
4. Use `nltk` or `spaCy` to get part of speech
5. Use WordNet or Datamuse API to fetch similar or related words
6. Export the result to `vocabulary_study_list.xlsx`

---

## ✅ Output Example

| English  | IPA       | Chinese | POS   | Variants               |
|----------|-----------|---------|-------|------------------------|
| example  | ɪɡˈzæmpəl | 例子    | noun  | instance, illustration |
| run      | rʌn       | 跑      | verb  | sprint, jog, flee      |
| happy    | ˈhæpi     | 开心的  | adj.  | joyful, glad, content  |

---



## 💡 Notes

- Tested on **Python 3.9**
- Requires internet connection to use Google Translate and Datamuse API
- You can easily change the translation language by modifying the `dest="zh-cn"` parameter
- If `googletrans` fails, consider switching to an official API like Google Cloud Translate or DeepL

---

Enjoy learning your vocabulary efficiently 📘🎧✍️
