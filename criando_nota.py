import pandas as pd
import random
import json
import datetime
from copy import deepcopy
from exp import ValorDiferente

class Emitente:
    def __init__(self, nome, nome_fantasia, inscricao_estadual, cnpj, logradouro, numero, complemento, bairro, municipio, uf, cep, fone):
        self.nome = nome
        self.nome_fantasia = nome_fantasia
        self.inscricao_estadual = inscricao_estadual
        self.cnpj = cnpj
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.municipio = municipio
        self.uf = uf
        self.cep = cep
        self.fone = fone

    def to_dict(self):
        return {
            "emitente_nome": self.nome,
            "emitente_nome_fantasia": self.nome_fantasia,
            "emitente_inscricao_estadual": self.inscricao_estadual,
            "emitente_cnpj": self.cnpj,
            "emitente_logradouro": self.logradouro,
            "emitente_numero": self.numero,
            "emitente_complemento": self.complemento,
            "emitente_bairro": self.bairro,
            "emitente_municipio": self.municipio,
            "emitente_uf": self.uf,
            "emitente_cep": self.cep,
            "emitente_fone": self.fone
        }

class Remetente:
    def __init__(self, nome, cnpj, logradouro, numero, complemento, bairro, municipio, uf, cep, fone):
        self.nome = nome
        self.cnpj = cnpj
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.municipio = municipio
        self.uf = uf
        self.cep = cep
        self.fone = fone

    def to_dict(self):
        return {
            "remetente_nome": self.nome,
            "remetente_cnpj": self.cnpj,
            "remetente_logradouro": self.logradouro,
            "remetente_numero": self.numero,
            "remetente_complemento": self.complemento,
            "remetente_bairro": self.bairro,
            "remetente_municipio": self.municipio,
            "remetente_uf": self.uf,
            "remetente_cep": self.cep,
            "remetente_fone": self.fone
        }

class Produto:
    def __init__(self, index, codigo, descricao, unidade, quantidade, preco_unitario, total, ncm):
        self.index = index
        self.codigo = codigo
        self.descricao = descricao
        self.unidade = unidade
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.total = round(float(self.quantidade) * float(self.preco_unitario), 2)
        self.ncm = ncm

    def to_dict(self):
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
        return f"Produto {self.index} - Código: {self.codigo}, Descrição: {self.descricao}, " \
               f"Unidade: {self.unidade}, Quantidade: {self.quantidade}, Valor Unitário: {self.preco_unitario}, " \
               f"Total: {self.total}, NCM: {self.ncm}"

class Nota:
    def __init__(self, numero_nota, valor_total, data = ''):
        self.numero_nota = str(numero_nota)
        self.data = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z-03:00")
        self.valor_total = valor_total
        self.valor_total_calculado = 0

        # Detalhes do Emitente
        self.emitente_nome = ""
        self.emitente_nome_fantasia = ""
        self.emitente_inscricao_estadual = ""
        self.emitente_cnpj = ""
        self.emitente_logradouro = ""
        self.emitente_numero = ""
        self.emitente_complemento = ""
        self.emitente_bairro = ""
        self.emitente_municipio = ""
        self.emitente_uf = ""
        self.emitente_cep = ""
        self.emitente_fone = ""

        # Detalhes do Remetente
        self.remetente_nome = ""
        self.remetente_cnpj = ""
        self.remetente_logradouro = ""
        self.remetente_numero = ""
        self.remetente_complemento = ""
        self.remetente_bairro = ""
        self.remetente_municipio = ""
        self.remetente_uf = ""
        self.remetente_cep = ""
        self.remetente_fone = ""

        # Detalhes dos Produtos
        self.produtos = []

        # Detalhes Adicionais
        self.informacoes_adicionais = ""

    def adicionar_emitente(self, nome, nome_fantasia, inscricao_estadual, cnpj, logradouro, numero, complemento, bairro, municipio, uf, cep, fone):
        self.emitente_nome = nome
        self.emitente_nome_fantasia = nome_fantasia
        self.emitente_inscricao_estadual = inscricao_estadual
        self.emitente_cnpj = cnpj
        self.emitente_logradouro = logradouro
        self.emitente_numero = numero
        self.emitente_complemento = complemento
        self.emitente_bairro = bairro
        self.emitente_municipio = municipio
        self.emitente_uf = uf
        self.emitente_cep = cep
        self.emitente_fone = fone

    def adicionar_remetente(self, nome, cnpj, logradouro, numero, complemento, bairro, municipio, uf, cep, fone):
        self.remetente_nome = nome
        self.remetente_cnpj = cnpj
        self.remetente_logradouro = logradouro
        self.remetente_numero = numero
        self.remetente_complemento = complemento
        self.remetente_bairro = bairro
        self.remetente_municipio = municipio
        self.remetente_uf = uf
        self.remetente_cep = cep
        self.remetente_fone = fone

    def adicionar_produto(self, index, codigo, descricao, unidade, quantidade, preco_unitario, total, ncm):
        produto = Produto(index, codigo, descricao, unidade, quantidade, preco_unitario, total, ncm)

        self.produtos.append(produto)
    
    def adicionar_produtos(self, lista):
        for index, produto in enumerate(lista):
            self.adicionar_produto(index + 1, random.randint(0, 500000000), produto["descricao"], produto["unidade"], produto["quantidade"], produto["preco_unitario"], produto["total"], produto["ncm"].replace('.', ''))

        self.calcular_valor_nota()

    def adicionar_informacoes_adicionais(self, informacoes_adicionais):
        self.informacoes_adicionais = informacoes_adicionais.replace("|", "-")

    def calcular_valor_nota(self):
        self.valor_total_calculado = 0

        for produto in self.produtos:
            self.valor_total_calculado += produto.total
        
        self.valor_total_calculado = str(round(self.valor_total_calculado, 2))

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

        if float(self.valor_total_calculado) != float(self.valor_total):
            # print(float(self.valor_total_calculado), "    ", float(self.valor_total))
            self.diferent_values()
        else:
            print("TUDO OK")
        
        self.valor_total = str(self.valor_total_calculado)
    
    def criar_arquivo_nota(self):
        with open("utils/padrao_nota.txt", "r", encoding="utf-8") as padrao_nota, open("utils/padrao_produto.txt", "r", encoding="utf-8") as padrao_produto, open(f"notas_feitas/{self.numero_nota}.txt", "w", encoding="utf-8") as nova_nota:
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
                        value = str(self.__dict__[key_only] )
                    
                    if value.lower() == "none":
                        value = ""
                    
                    value = value.strip()
                
                nota_final = nota_final.replace(key, value)

            #nota_final = unicodedata.normalize('NFKD', nota_final).encode('ASCII', 'ignore').decode('ASCII')
            nova_nota.write(nota_final)

    def diferent_values(self):
        raise ValorDiferente(f"Valores diferentes!\nValor Calculado:{float(self.valor_total_calculado)}\nValor Informado: {float(self.valor_total)}")

def get_json(path):
    with open(path, "r", encoding='utf-8') as file:
        js = json.load(file)

    return js
    
def build_note(numero, valor_total, emitente, remetente, informacoes_adicionais, hora = ''):
    #TRANSFORMANDO ARQUIVO EM DATAFRAME
    js = get_json(f"notas_json/{numero}.json")
    df = pd.DataFrame(data=js['data'], columns=js['columns'])

    #CRIANDO E PREENCHENDO NOTA
    nota = Nota(numero, valor_total, data=hora)
    nota.adicionar_emitente(*emitente.to_dict().values())
    nota.adicionar_remetente(*remetente.to_dict().values())
    nota.adicionar_informacoes_adicionais(informacoes_adicionais)
    
    nota.adicionar_produtos(df.to_dict(orient='records'))
    nota.criar_arquivo_nota()
