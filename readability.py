from cs50 import get_string
import re

text=get_string("Text: ")

def count_text_elements(text):
    # Count letters
    letters = re.findall(r'[a-zA-Z]', text)
    num_letters = len(letters)

    # Count words
    words = re.findall(r'\b\w+\b', text)
    num_words = len(words)

    # Count sentences
    sentences = re.findall(r'[.!?]', text)
    num_sentences = len(sentences)

    return num_letters, num_words, num_sentences

a=count_text_elements(text)

index=0.0588*(float(a[0]/a[1])*100.00)-0.296*(float(a[2]/a[1])*100.00)-15.8
index=round(index)

if index<1:
    print("Before Grade 1")
elif index>=16:
    print("Grade 16+")
else:
    print(f"Grade {index}")
