import pandas as pd
import unicodedata
import random
import json
from copy import deepcopy

informacoes_nota = {
    "numero_nota": "5",
    "data": "2024-07-31T16:00:00-03:00", #
}

emitente = {
    "emitente_nome": "J F MENDES COMERCIO E SERVICOS",
    "emitente_nome_fantasia": "DIGITAL PAPELARIA E INFORMATICA",
    "emitente_inscricao_estadual": "066794145", 
    "emitente_cnpj": "46333345000168",
    "emitente_logradouro": "R COLOMBO",
    "emitente_numero": "310",
    "emitente_bairro": "PARQUE SANTA ROSA",
    "emitente_municipio": "Fortaleza",
    "emitente_uf": "CE",
    "emitente_cep": "60060520",
    "emitente_numero_contato": "8533333333",
}

remetente = {
    "remetente_nome": "Instituto Cultural Iracema",
    "remetente_cnpj": "13637888000110",
    "remetente_logradouro": "Rua dos Pacajus",
    "remetente_numero": "33",
    "remetente_bairro": "Praia de Iracema",
    "remetente_municipio": "Fortaleza",
    "remetente_uf": "CE",
    "remetente_numero_contato": "996193827"
}

produto = {
    "numero_prod": None,
    "codigo_prod": None,
    "descricao_prod": None,
    "ncm_prod": None,
    "und_prod": None,
    "qtde_prod": None,
    "valor_und_prod": None,
    "total_prod": None
}

class Nota:
    def __init__(self, numero_nota, data, valor_total):
        self.numero_nota = numero_nota
        self.data = data
        self.valor_total = valor_total

        # Detalhes do Emitente
        self.emitente_nome = None
        self.emitente_nome_fantasia = None
        self.emitente_inscricao_estadual = None
        self.emitente_cnpj = None
        self.emitente_logradouro = None
        self.emitente_numero = None
        self.emitente_bairro = None
        self.emitente_municipio = None
        self.emitente_uf = None
        self.emitente_cep = None
        self.emitente_numero_contato = None

        # Detalhes do Remetente
        self.remetente_nome = None
        self.remetente_cnpj = None
        self.remetente_logradouro = None
        self.remetente_numero = None
        self.remetente_bairro = None
        self.remetente_municipio = None
        self.remetente_uf = None
        self.remetente_numero_contato = None

        # Detalhes dos Produtos
        self.produtos = []

        # Detalhes Adicionais
        self.informacoes_adicionais = None

    def adicionar_emitente(self, nome, nome_fantasia, inscricao_estadual, cnpj, logradouro, numero, bairro, municipio, uf, cep, numero_contato):
        self.emitente_nome = nome
        self.emitente_nome_fantasia = nome_fantasia
        self.emitente_inscricao_estadual = inscricao_estadual
        self.emitente_cnpj = cnpj
        self.emitente_logradouro = logradouro
        self.emitente_numero = numero
        self.emitente_bairro = bairro
        self.emitente_municipio = municipio
        self.emitente_uf = uf
        self.emitente_cep = cep
        self.emitente_numero_contato = numero_contato

    def adicionar_remetente(self, nome, cnpj, logradouro, numero, bairro, municipio, uf, numero_contato):
        self.remetente_nome = nome
        self.remetente_cnpj = cnpj
        self.remetente_logradouro = logradouro
        self.remetente_numero = numero
        self.remetente_bairro = bairro
        self.remetente_municipio = municipio
        self.remetente_uf = uf
        self.remetente_numero_contato = numero_contato

    def adicionar_produto(self, numero_prod, codigo_prod, descricao_prod, ncm_prod, und_prod, qtde_prod, valor_und_prod, total_prod):
        produto = {
            "numero_prod": numero_prod,
            "codigo_prod": codigo_prod,
            "descricao_prod": descricao_prod,
            "ncm_prod": ncm_prod,
            "und_prod": und_prod,
            "qtde_prod": qtde_prod,
            "valor_und_prod": valor_und_prod,
            "total_prod": total_prod
        }

        self.produtos.append(produto)
    
    def adicionar_produtos(self, lista):
        for index, produto in enumerate(lista):
            # print(produto)
            # print()
            self.adicionar_produto(index, random.randint(0, 5000000), produto["descricao_prod"], produto["ncm_prod"], produto["und_prod"], produto["qtde_prod"], produto["valor_und_prod"], produto["total_prod"])

    def adicionar_informacoes_adicionais(self, informacoes_adicionais):
        self.informacoes_adicionais = informacoes_adicionais

    def criar_arquivo_nota(self):
        with open("pater_nota.txt", "r") as pater_nota, open("pater_prod.txt", "r") as pater_prod, open("notas_feitas/NOTAFISCAL.txt", "w", encoding="utf-8") as nova_nota:
            keys = list(map(lambda a: "{" + a + "}", list(self.__dict__.keys())))

            nota_final = pater_nota.read()  

            for key in keys:
                key_only = key.replace("{", "").replace("}", "")

                value = ""

                if "produtos" in key:
                    produtos_txt_final = ""
                    pater_prod_txt = pater_prod.read()

                    for produto in self.produtos:
                        keys_prod = list(map(lambda a: "{" + a + "}", list(produto.keys())))
                        produtos_txt = deepcopy(pater_prod_txt)

                        for key_prod in keys_prod:
                            key_only_prod = key_prod.replace("{", "").replace("}", "")

                            value = str(produto[key_only_prod])

                            if key_only_prod in ("und_prod", "qtde_prod", "valor_und_prod", "total_prod"):
                                value =  value.replace(",", ".")

                            produtos_txt = produtos_txt.replace(key_prod, value)
                    
                        produtos_txt_final = produtos_txt_final + "\n\n" + produtos_txt

                    value = produtos_txt_final
                else:
                    if "valor_total" == key_only:
                        value = str(self.__dict__[key_only]).replace(",", ".")
                    else:
                        value = self.__dict__[key_only] 
                
                nota_final = nota_final.replace(key, value)

            nota_final = unicodedata.normalize('NFKD', nota_final).encode('ASCII', 'ignore').decode('ASCII')
            nova_nota.write(nota_final)

def main():
    path = str(input('Digite o nome do arquivo em nota: '))
    df = pd.read_csv(f"notas/{path}.csv", sep = ";", names=["descricao_prod", "und_prod", "qtde_prod", "valor_und_prod", "total_prod", "ncm_prod"], header=None)

    nota = Nota("ok", "ok", 50)
    #nota.adicionar_produtos(df.to_dict(orient='records'))

    nota.adicionar_emitente(*emitente.values())
    nota.adicionar_remetente(*remetente.values())
    nota.adicionar_informacoes_adicionais("BANCO DO BRASIL | AGÊNCIA 2906-8 | CONTA CORRENTE 29896-4|")
    #nota.criar_arquivo_nota()
    nota.adicionar_produtos(df.to_dict(orient='records'))
    nota.criar_arquivo_nota()

def get_json(path):
    # Carregar o JSON a partir de um arquivo
    with open(path, "r", encoding='utf-8') as file:
        js = json.load(file)

        print(type(js))
        #df = pd.read_json(file)

    #df.head(10)

if __name__ == "__main__":
    get_json("nota_1.json")

