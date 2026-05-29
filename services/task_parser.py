import re

from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsNERTagger,
    Doc
)

import pymorphy2


segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
ner_tagger = NewsNERTagger(emb)
morph = pymorphy2.MorphAnalyzer()

def normalize_name(name):
    parsed = morph.parse(name)[0]
    return parsed.normal_form


def extract_tasks(text):
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_ner(ner_tagger)
    tasks = []
    sentences = re.split(r'[.!?]', text)

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue
        local_doc = Doc(sentence)
        local_doc.segment(segmenter)
        local_doc.tag_ner(ner_tagger)
        person_name = None

        for span in local_doc.spans:

            if span.type == "PER":
                span.normalize(morph_vocab)
                person_name = normalize_name(
                    span.text
                )
                break

        if not person_name:
            continue

        task_text = sentence
        task_text = re.sub(
            person_name,
            "",
            task_text,
            flags=re.IGNORECASE
        )

        task_text = re.sub(
            r'^\s*,?',
            '',
            task_text
        ).strip()

        replacements = {
            "сделай": "сделать",
            "доработай": "доработать",
            "заполни": "заполнить",
            "напиши": "написать",
            "создай": "создать"
        }

        words = task_text.split()

        if words:

            first_word = words[0].lower()

            if first_word in replacements:
                words[0] = replacements[first_word]

        task_text = " ".join(words)

        tasks.append({
            "name": person_name,
            "task": task_text
        })

    return tasks