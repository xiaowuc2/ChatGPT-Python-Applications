# Importing required libraries
import argparse
import requests
from bs4 import BeautifulSoup
import openai
import yaml

# Reading private yml file
with open("pass.yml") as f:
    content = f.read()

# from pass.yml importing api key
my_credentials = yaml.load(content, Loader=yaml.FullLoader)    
# from pass.yml importing api key
openai.api_key = my_credentials["api"]

# Creating the parser
parser = argparse.ArgumentParser(description='web scrapping summarizer')

# Adding arguments
parser.add_argument('--web', type=str, help='website link (default : https://github.com/xiaowuc2/ChatGPT-Python-Applications)', default="https://github.com/xiaowuc2/ChatGPT-Python-Applications")
parser.add_argument('--limit', type=int, help='summarized text limit (default : 100)', default=100)

# Parsing arguments
args = parser.parse_args()

response = requests.get(args.web)
soup = BeautifulSoup(response.content, 'html.parser')

# Extracting the text 
text = ''
for p in soup.find_all('p'):
    text += p.text


#trimming the text. Openai can only take 4097 tokens. 

mine = (int(len(text)/4.2))
#print(f"my text has chars : {len(text)} tokens : {mine}")

allowed = 16132
#print(f"numebr of chars allowed is : {allowed}")

h = len(text) - allowed
#print(f"we've to save this much texts : {h}")

# `ntext` is trimeed 'text'
ntext = text[:len(text)-h]
#print(f"new text has chars : {len(ntext)} . tokens : {len(ntext)/4}")


def summarize_text(text):
    model_engine = "text-davinci-002" # Replace with your preferred GPT-3 model engine
    prompt = (f"Please summarize the following text:\n{text}\n\nSummary:")

    response = openai.Completion.create(
      engine=model_engine,
      prompt=prompt,
      max_tokens=args.limit,
      n=1,
      stop=None,
      temperature=0.5,
    )

    summary = response.choices[0].text.strip()
    return summary

print(f"Summary : {summarize_text(ntext)}")
