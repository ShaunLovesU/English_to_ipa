import json
import eng_to_ipa as ipa
import asyncio
from googletrans import Translator
import nltk
from nltk.corpus import wordnet
from nltk.tag import PerceptronTagger
import pandas as pd
import os
import sys


# '''
# For install NLTK package
# Only run for the first time running
# '''
# nltk.download('wordnet')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')


if len(sys.argv) != 3:
    print("wrong usage, the format should be : python main.py [input JSON dir] [output Excel dir]")
    sys.exit(1)

input_path = sys.argv[1]
output_path = sys.argv[2]

if not os.path.exists(input_path):
    print(f"input file does not exists: {input_path}")
    sys.exit(1)

with open(input_path, "r", encoding="utf-8") as file:
    data = json.load(file)
    word_list = data["vocabulary_words"]


tagger = PerceptronTagger()
translator = Translator()


def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return 'adj.'
    elif tag.startswith('V'):
        return 'v.'
    elif tag.startswith('N'):
        return 'n.'
    elif tag.startswith('R'):
        return 'adv.'
    else:
        return ''


def get_variants(word):
    forms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            name = lemma.name().replace("_", " ")
            if name.lower() != word.lower():
                forms.add(name)
    return ', '.join(sorted(forms))


async def main():
    tagged_words = tagger.tag(word_list)
    records = []

    for word, tag in tagged_words:
        try:
            pronunciation = ipa.convert(word)
        except:
            pronunciation = ''
        try:
            result = await translator.translate(word, src="en", dest="zh-cn")
            translation = result.text
        except:
            translation = ''
        pos = get_wordnet_pos(tag)
        variants = get_variants(word)
        records.append([word, pronunciation, translation, pos, variants])

    df = pd.DataFrame(records, columns=["English", "IPA", "Chinese", "POS", "Variants"])
    df.to_excel(output_path, index=False)
    print(f"saved to：{output_path}")

if __name__ == "__main__":
    asyncio.run(main())