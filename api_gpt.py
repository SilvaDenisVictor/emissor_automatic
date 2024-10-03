from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from llama_parse import LlamaParse
import os

def get_pdf_txt(path):
    full_pdf_txt = ""

    parser = LlamaParse(
        result_type='markdown',
        verbose=True,
        language='pt',
    )

    documents =  parser.load_data(path)

    for document in documents:
        full_pdf_txt += document.text
    
    return full_pdf_txt

def get_completion(content, prompt_path="prompt.txt"):
    client = OpenAI(
        api_key = os.environ.get("OPENAI_API_KEY")
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": open(prompt_path, 'r', encoding='utf-8').read()},
            {"role": "user", "content": content}
        ]
    )

    return completion

def get_csv(path):
    completion = get_completion(get_pdf_txt(path))

    return completion

if __name__ == "__main__":
    _ = load_dotenv(find_dotenv())

    path = "nota_2.pdf"
    completion =  get_csv(path)

    with open("nota_1.json", "w", encoding='utf-8') as file:
        txt = completion.choices[0].message.content
        #file.write(completion.choices[0].message.content)

        inicio = -1
        fim = -1

        for index, char in enumerate(txt):
            if inicio == -1 and char == "{":
                inicio = index
            
            if char == '}':
                fim = index
        
        json_txt = txt[inicio: fim + 1]

        file.write(json_txt)
    