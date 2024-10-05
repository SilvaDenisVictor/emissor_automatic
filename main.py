import requests
import json
import re
from api_gpt import transform_json
from criando_nota import build_note, Emitente, Remetente

def get_name_in(name):
    original_nome = name

    nome = original_nome.lower()
    index = 0

    if "escola" in nome:
        nome = nome.split(" ")
        index = nome.index("escola")

    nome_div =  original_nome.split(" ")[index:]
    nome = ""
    for div in nome_div:
        if len(nome + " " + div) > 60:
            break
        nome = nome + " " + div

    return nome

def get_emitente_cnpj(cnpj, inscricao_estadual = ''):
    #REQUISIÇÃO
    response = requests.get(f"https://receitaws.com.br/v1/cnpj/{cnpj}")

    #PEGANDO O JSON
    js = response.json()

    #CRIANDO EMITENTE
    emitente_dict = {
        "nome": get_name_in(js["nome"]),
        "fantasia": get_name_in(js["fantasia"]),
        "inscricao_estadual": re.sub('[^0-9]', '', inscricao_estadual),
        "cnpj": re.sub('[^0-9]', '', js["cnpj"]),
        "logradouro": js["logradouro"],
        "numero": js["numero"],
        "complemento": js["complemento"],
        "bairro": js["bairro"],
        "municipio": js["municipio"],
        "uf": js["uf"],
        "cep": re.sub('[^0-9]', '', js["cep"]),
        "telefone": re.sub('[^0-9]', '', js["telefone"].split('/')[0])
    }

    return Emitente(*emitente_dict.values())

def get_remetente_cnpj(cnpj):
    #REQUISIÇÃO
    response = requests.get(f"https://receitaws.com.br/v1/cnpj/{cnpj}")

    #PEGANDO O JSON
    js = response.json()

    #CRIANDO REMETENTE
    remetente_dict = {
        "nome": get_name_in(js["nome"]),
        "cnpj": re.sub('[^0-9]', '', js["cnpj"]),
        "logradouro": js["logradouro"],
        "numero": js["numero"],
        "complemento": js["complemento"],
        "bairro": js["bairro"],
        "municipio": js["municipio"],
        "uf": js["uf"],
        "cep": re.sub('[^0-9]', '', js["cep"]),
        "telefone": re.sub('[^0-9]', '', js["telefone"].split('/')[0])
    }

    return Remetente(*remetente_dict.values())

def main(numero_nota, cnpj_emitente, inscricao_estadual_emitente, valor_total):
    #TRANSFORMAR NOTA EM JSON
    transform_json(numero_nota)

    #TRANSFORMAR JSON EM NOTA.TXT
    emitente = get_emitente_cnpj(cnpj_emitente, inscricao_estadual_emitente)

    with open(f"notas_json/{numero_nota}.json", "r", encoding='utf-8') as file:
        js =  json.load(file)

        #REMOVENDO OS CARACTÉRES NÃO NUMÉRICOS
        cpnj = re.sub('[^0-9]', '', js["cnpj_promotor"])

        remetente = get_remetente_cnpj(cpnj)

    build_note(numero_nota, valor_total, emitente, remetente)

if __name__ == "__main__":
    #PEGAR NUMERO DA NOTA E CNPJ DO EMITENTE
    # numero_nota = input("DIGITE NUMERO DA NOTA: ")
    # cnpj_emitente = re.sub('[^0-9]', '', input("DIGITE DIGITE O CNPJ DO EMITENTE: "))
    # inscricao_estadual_emitente = input("DIGITE DIGITE A INSCRIÇÃO ESTADUAL DO EMITENTE: ")
    # valor_total = input("DIGITE O VALOR TOTAL: ")

    # main(numero_nota, cnpj_emitente, inscricao_estadual_emitente, valor_total)
    main(700, "46333345000168", "070633975",  2801.39)
    