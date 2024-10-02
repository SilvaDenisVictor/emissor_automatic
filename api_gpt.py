from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from PyPDF2 import PdfFileReader
import os

def get_pdf_txt(path):
    full_pdf_txt = ""

    # Abrindo um arquivo PDF existente
    with open(path, "rb") as input_pdf:
        # Criando um objeto PdfFileReader
        pdf_reader = PdfFileReader(input_pdf)

        # Obtendo o número de páginas do arquivo PDF
        num_pages = pdf_reader.numPages

        # Lendo o texto de cada página
        for page_number in range(num_pages):
            page = pdf_reader.getPage(page_number)
            text = page.extractText()
            #print("Texto da página", page_number + 1, ":", text)
            full_pdf_txt = full_pdf_txt + "\n" + text

    return full_pdf_txt

def get_completion(content, prompt_path="prompt.txt"):
    #LOAD THE .ENV FILE

    client = OpenAI(
        api_key = os.environ.get("OPENAI_API_KEY")
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": open(prompt_path, 'r').read()},
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

    with open("nota_1.txt", "w") as file:
        file.write(completion.choices[0].message.content)
    