from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from llama_parse import LlamaParse
import os

def get_mark_down(path):
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
    completion = get_completion(get_mark_down(path))

    return completion

def transform_json(numero):
    _ = load_dotenv(find_dotenv())

    with open(f"notas_json/{numero}.json", "w", encoding='utf-8') as file:
        completion = get_json(numero)
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

# if __name__ == "__main__":
#    pass
    
    