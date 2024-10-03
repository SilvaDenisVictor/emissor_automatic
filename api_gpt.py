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

    documents =  parser.load_data(f"notas/{path}.pdf")

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

def get_json(path):
    completion = get_completion(get_pdf_txt(path))

    return completion

if __name__ == "__main__":
    _ = load_dotenv(find_dotenv())

    nome = input("Nome da nota:")

    with open(f"notas_json/{nome}.json", "w", encoding='utf-8') as file:
        completion = get_json(nome)
        txt = completion.choices[0].message.content

        inicio = -1
        fim = -1

        for index, char in enumerate(txt):
            if inicio == -1 and char == "{":
                inicio = index
            
            if char == '}':
                fim = index
        
        json_txt = txt[inicio: fim + 1]

        file.write(json_txt)
    