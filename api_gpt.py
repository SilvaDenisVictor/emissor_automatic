#from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from llama_parse import LlamaParse
from struture_order import Ordem
from langchain_openai import ChatOpenAI
from pydantic import ValidationError
import re
import json
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

def get_completion(content, cnpj_promotor, prompt_path="utils/prompt.txt"):
    #definindo llm
    llm = ChatOpenAI(model="gpt-4o-mini")

    structured_llm = llm.with_structured_output(Ordem)

    #definindo prompt
    with open(prompt_path, "r", encoding='utf-8') as file:
        system = file.read()

    #DEFININDO CONTEXTO
    context = f""""
    {system}
    
    [EXTRAIA A NOTA ABAIXO]

    {content}
    """

    #PEGANDO OBJETO
    max_tentativas = 3
    outro_erro = False

    while(max_tentativas > 0 and not outro_erro):
        try:
            response = structured_llm.invoke(context)
            
            if re.sub('[^0-9]', '', cnpj_promotor) == re.sub('[^0-9]', '', response.cnpj_promotor):
                print("CNPJ PROMOTOR: ", response.cnpj_promotor)
                print("CNPJ REMETENTE: ", cnpj_promotor)
                raise Exception("CNPJ_PROMOTOR INCORRETO")
        except ValidationError as e:
            print(f"Erro de validação do Pydantic ({3 - max_tentativas + 1}ª tentativa): ", e)
            max_tentativas -= 1
        else:
            print("ESTRUTURA RETORNADA CORRETAMENTE.")
            break

    return response

def get_json(path, cnpj_promotor):
    completion = get_completion(get_mark_down(path), cnpj_promotor)
    
    return completion

def transform_json(numero, cnpj_promotor, tem_unidade):
    _ = load_dotenv(find_dotenv())

    with open(f"notas_json/{numero}.json", "w", encoding='utf-8') as file:
        obj = get_json(numero, cnpj_promotor)
        obj.coluna_unidade_bool = tem_unidade

        #AJUSTANDO ORDEM
        obj.validar_descricao()
        obj.validar_ncm()
        obj.validar_und()
        
        json.dump(obj.model_dump(), file, indent=2, default=str, ensure_ascii=False)
