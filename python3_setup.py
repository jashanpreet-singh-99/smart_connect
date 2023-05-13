print("Performing a Check For All the required Libraries")

import os

os.system('pip3 install -U nltk')
os.system('pip3 install -U numpy')
os.system('pip3 install -U pandas')
os.system('pip3 install -U tkinter')

print("Library Check Complete")

import nltk

print("Checking For Corpus.")

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

print("All Corpus Ready To Use")