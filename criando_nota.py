import pandas as pd
import unicodedata
import random
import json
import datetime
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

class Produto:
    def __init__(self, index, codigo, descricao, unidade, quantidade, preco_unitario, total, ncm):
        """
        Inicializa um objeto Produto com os detalhes fornecidos.
        
        Args:
            index (int): Índice do produto.
            codigo (str): Código do produto.
            descricao (str): Descrição do produto.
            unidade (str): Unidade de medida.
            quantidade (float): Quantidade disponível.
            preco_unitario (float): Valor unitário do produto.
            total (float): Valor total do produto (quantidade * valor unitário).
            ncm (str): Código NCM do produto.
        """
        self.index = index
        self.codigo = codigo
        self.descricao = descricao
        self.unidade = unidade
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.total = round(float(self.quantidade) * float(self.preco_unitario), 2)
        self.ncm = ncm

    def to_dict(self):
        """
        Retorna os detalhes do produto como um dicionário.
        
        Returns:
            dict: Dicionário contendo os atributos do produto.
        """
        return {
            "index": self.index,
            "codigo": self.codigo,
            "descricao": self.descricao,
            "unidade": self.unidade,
            "quantidade": self.quantidade,
            "preco_unitario": self.preco_unitario,
            "total": self.total,
            "ncm": self.ncm
        }

    def __str__(self):
        """
        Retorna uma string legível para representar o produto.
        
        Returns:
            str: Representação legível do produto.
        """
        return f"Produto {self.index} - Código: {self.codigo}, Descrição: {self.descricao}, " \
               f"Unidade: {self.unidade}, Quantidade: {self.quantidade}, Valor Unitário: {self.preco_unitario}, " \
               f"Total: {self.total}, NCM: {self.ncm}"

class Nota:
    def __init__(self, numero_nota, valor_total, data = ''):
        self.numero_nota = str(numero_nota)
        self.data = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z-03:00")
        self.valor_total = valor_total
        self.valor_total_calculado = 0
            
        print(self.data)

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

    def adicionar_produto(self, index, codigo, descricao, unidade, quantidade, preco_unitario, total, ncm):
        produto = Produto(index, codigo, descricao, unidade, quantidade, preco_unitario, total, ncm)

        self.produtos.append(produto)
    
    def adicionar_produtos(self, lista):
        for index, produto in enumerate(lista):
            self.adicionar_produto(index + 1, random.randint(0, 500000000), produto["descricao"], produto["unidade"], produto["quantidade"], produto["preco_unitario"], produto["total"], produto["ncm"].replace('.', ''))

        self.calcular_valor_nota()

    def adicionar_informacoes_adicionais(self, informacoes_adicionais):
        self.informacoes_adicionais = informacoes_adicionais

    def calcular_valor_nota(self):
        self.valor_total_calculado = 0

        for produto in self.produtos:
            self.valor_total_calculado += produto.total
        
        self.valor_total_calculado = str(self.valor_total_calculado)

        #ADICIONANDO UM 0 CASO O A SEGUNDA CASA DECIMAL SEJA == 0
        ultimo = '*'
        penultimo = '*'

        depois_ponto = False

        for c in self.valor_total_calculado:
            if depois_ponto and ultimo != '*':
                penultimo = c

            if depois_ponto and ultimo == '*':
                ultimo = c

            if c == '.':
                depois_ponto = True
        
        if penultimo == '*':
            self.valor_total_calculado += "0"
        
        self.valor_total = str(self.valor_total_calculado)
    
    def criar_arquivo_nota(self):
        with open("padrao_nota.txt", "r") as padrao_nota, open("padrao_produto.txt", "r") as padrao_produto, open(f"notas_feitas/{self.numero_nota}.txt", "w", encoding="utf-8") as nova_nota:
            keys = list(map(lambda a: "{" + a + "}", list(self.__dict__.keys())))

            nota_final = padrao_nota.read()  

            for key in keys:
                key_only = key.replace("{", "").replace("}", "")

                value = ""

                if "produtos" in key:
                    produtos_txt_final = ""
                    padrao_produto_txt = padrao_produto.read()

                    for produto in [produto.to_dict() for produto in self.produtos]:
                        keys_prod = list(map(lambda a: "{" + a + "}", list(produto.keys())))
                        produtos_txt = deepcopy(padrao_produto_txt)

                        for key_prod in keys_prod:
                            key_only_prod = key_prod.replace("{", "").replace("}", "")

                            value = str(produto[key_only_prod])

                            if key_only_prod in ("unidade", "quantidade", "preco_unitario", "total"):
                                value =  value.replace(",", ".")

                            #ADICIONANDO UM 0 CASO O A SEGUNDA CASA DECIMAL SEJA == 0
                            if key_only_prod == "total":
                                ultimo = '*'
                                penultimo = '*'

                                depois_ponto = False

                                for c in value:
                                    if depois_ponto and ultimo != '*':
                                        penultimo = c

                                    if depois_ponto and ultimo == '*':
                                        ultimo = c

                                    if c == '.':
                                        depois_ponto = True
                                
                                if penultimo == '*':
                                    value += "0"

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

def get_json(path):
    with open(path, "r", encoding='utf-8') as file:
        js = json.load(file)

    return js
    
def main():
    #RECEBENDO CAMINHO
    numero = str(input('Digite o nome do arquivo em nota: '))
    
    #TRANSFORMANDO ARQUIVO EM DATAFRAME
    js = get_json(f"notas_json/{numero}.json")
    df = pd.DataFrame(data=js['data'], columns=js['columns'])

    #CRIANDO E PREENCHENDO NOTA
    nota = Nota(numero, 50)
    nota.adicionar_emitente(*emitente.values())
    nota.adicionar_remetente(*remetente.values())
    nota.adicionar_informacoes_adicionais("BANCO DO BRASIL | AGÊNCIA 2906-8 | CONTA CORRENTE 29896-4|")
    nota.adicionar_produtos(df.to_dict(orient='records'))
    nota.criar_arquivo_nota()


if __name__ == "__main__":
    main()
