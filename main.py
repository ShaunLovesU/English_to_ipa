import json
import eng_to_ipa as ipa
import asyncio
from googletrans import Translator
import nltk
from nltk.corpus import wordnet
from nltk.tag import PerceptronTagger
import pandas as pd

# 加载词汇 JSON
with open("cleaned_vocabulary_words.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    word_list = data["vocabulary_words"]

# 初始化词性标注器和翻译器
tagger = PerceptronTagger()
translator = Translator()

# 词性映射
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

# 获取变种形式
def get_variants(word):
    forms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            name = lemma.name().replace("_", " ")
            if name.lower() != word.lower():
                forms.add(name)
    return ', '.join(sorted(forms))

# 异步主函数
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

    # 导出 Excel
    df = pd.DataFrame(records, columns=["English", "IPA", "Chinese", "POS", "Variants"])
    df.to_excel("vocabulary_study_list.xlsx", index=False)
    print("✅ Saved to vocabulary_study_list.xlsx")

# 运行异步任务
asyncio.run(main())
