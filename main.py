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

def get_emitente_cnpj(cnpj):
    #REQUISIÇÃO
    response = requests.get(f"https://publica.cnpj.ws/cnpj/{cnpj}")

    #PEGANDO O JSON
    js = response.json()

    #CRIANDO EMITENTE
    emitente_dict = {
        "nome": get_name_in(js["razao_social"]),
        "fantasia": get_name_in(js["estabelecimento"]["nome_fantasia"]),
        "inscricao_estadual": re.sub('[^0-9]', '', js["estabelecimento"]["inscricoes_estaduais"][0]["inscricao_estadual"]),
        "cnpj": re.sub('[^0-9]', '', js["estabelecimento"]["cnpj"]),
        "logradouro": js["estabelecimento"]["tipo_logradouro"] + " " + js["estabelecimento"]["logradouro"],
        "numero": js["estabelecimento"]["numero"],
        "complemento": js["estabelecimento"]["complemento"],
        "bairro": js["estabelecimento"]["bairro"],
        "municipio": js["estabelecimento"]["cidade"]["nome"],
        "uf": js["estabelecimento"]["estado"]["sigla"],
        "cep": re.sub('[^0-9]', '', js["estabelecimento"]["cep"]),
        "telefone": re.sub('[^0-9]', '', js["estabelecimento"]["ddd1"] + js["estabelecimento"]["telefone1"])
    }

    return Emitente(*emitente_dict.values())

def get_remetente_cnpj(cnpj):
    #REQUISIÇÃO
    response = requests.get(f"https://publica.cnpj.ws/cnpj/{cnpj}")

    #PEGANDO O JSON
    js = response.json()

    #CRIANDO REMETENTE
    remetente_dict = {
        "nome_fantasia": get_name_in(js["estabelecimento"]["nome_fantasia"]),
        "cnpj": re.sub('[^0-9]', '', js["estabelecimento"]["cnpj"]),
        "logradouro": js["estabelecimento"]["tipo_logradouro"] + " " + js["estabelecimento"]["logradouro"],
        "numero": js["estabelecimento"]["numero"],
        "complemento": js["estabelecimento"]["complemento"],
        "bairro": js["estabelecimento"]["bairro"],
        "municipio": js["estabelecimento"]["cidade"]["nome"],
        "uf": js["estabelecimento"]["estado"]["sigla"],
        "cep": re.sub('[^0-9]', '', js["estabelecimento"]["cep"]),
        "telefone": re.sub('[^0-9]', '', js["estabelecimento"]["ddd1"] + js["estabelecimento"]["telefone1"])
    }

    return Remetente(*remetente_dict.values())

def main(numero_nota, cnpj_emitente, valor_total, informacoes_adicionais):
    #TRANSFORMAR NOTA EM JSON
    transform_json(numero_nota)

    #TRANSFORMAR JSON EM NOTA.TXT
    emitente = get_emitente_cnpj(cnpj_emitente)

    with open(f"notas_json/{numero_nota}.json", "r", encoding='utf-8') as file:
        js =  json.load(file)

        #REMOVENDO OS CARACTÉRES NÃO NUMÉRICOS
        cpnj = re.sub('[^0-9]', '', js["cnpj_promotor"])

        remetente = get_remetente_cnpj(cpnj)

    
    build_note(numero_nota, valor_total, emitente, remetente, informacoes_adicionais)

if __name__ == "__main__":
    #PEGAR NUMERO DA NOTA E CNPJ DO EMITENTE
    numero_nota = input("DIGITE NUMERO DA NOTA: ")
    cnpj_emitente = re.sub('[^0-9]', '', input("DIGITE DIGITE O CNPJ DO EMITENTE: "))
    valor_total = input("DIGITE O VALOR TOTAL: ")
    informacoes_adicionais = input("Digite: 1 - JFMENDES, 2 - OUROVERDE \n")

    if informacoes_adicionais == "1":
        informacoes_adicionais = "BANCO DO BRASIL | AGÊNCIA 2906-8 | CONTA CORRENTE 29896-4"
    elif informacoes_adicionais == "2":
        informacoes_adicionais = "Bradesco: Agência  0649 - C/C 86123-5"

    main(numero_nota, cnpj_emitente, valor_total, informacoes_adicionais)
    #main(700, "46333345000168", "070633975",  2801.39)
    