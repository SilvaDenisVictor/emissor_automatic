import requests
import json
import re
import tkinter as tk
import shutil
import os
from exp import ValorDiferente
from tkinter import filedialog, messagebox
from api_gpt import transform_json
from criando_nota import build_note, Emitente, Remetente

def selecionar_pdf():
    """Abre uma caixa de diálogo para selecionar um arquivo PDF"""
    caminho_pdf = filedialog.askopenfilename(
        title="Selecione um arquivo PDF",
        filetypes=(("PDF files", "*.pdf"), ("All files", "*.*"))
    )
    if caminho_pdf:
        entrada_pdf.delete(0, tk.END)
        entrada_pdf.insert(0, caminho_pdf)

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

def get_emitente_cnpj(cnpj_):
    #REQUISIÇÃO
    cnpj = re.sub('[^0-9]', '', cnpj_)
    response = requests.get(f"https://publica.cnpj.ws/cnpj/{cnpj}")

    #PEGANDO O JSON
    js = response.json()

    #DEF NULO POR VAZIO
    def substituir_nulo(valor):
        return "" if valor is None else valor
    
    sub = substituir_nulo
    
    #VALIDACAO
    nome = js["razao_social"] if js["razao_social"] else ""
    fantasia = js["estabelecimento"]["nome_fantasia"] if js["estabelecimento"]["nome_fantasia"] else ""
     

    #CRIANDO EMITENTE
    emitente_dict = {
        "nome": get_name_in(nome),
        "fantasia": get_name_in(fantasia),
        "inscricao_estadual": re.sub('[^0-9]', '', sub(js["estabelecimento"]["inscricoes_estaduais"][0]["inscricao_estadual"])),
        "cnpj": re.sub('[^0-9]', '', sub(js["estabelecimento"]["cnpj"])),
        "logradouro": sub(js["estabelecimento"]["tipo_logradouro"]) + " " + sub(js["estabelecimento"]["logradouro"]),
        "numero": sub(js["estabelecimento"]["numero"]),
        "complemento": sub(js["estabelecimento"]["complemento"]),
        "bairro": sub(js["estabelecimento"]["bairro"]),
        "municipio": sub(js["estabelecimento"]["cidade"]["nome"]),
        "uf": sub(js["estabelecimento"]["estado"]["sigla"]),
        "cep": re.sub('[^0-9]', '', sub(js["estabelecimento"]["cep"])),
        "telefone": re.sub('[^0-9]', '', sub(js["estabelecimento"]["ddd1"]) + sub(js["estabelecimento"]["telefone1"]))
    }

    return Emitente(*emitente_dict.values())

def get_remetente_cnpj(cnpj_):
    #REQUISIÇÃO
    cnpj = re.sub('[^0-9]', '', cnpj_)
    response = requests.get(f"https://publica.cnpj.ws/cnpj/{cnpj}")

    #PEGANDO O JSON
    js = response.json()

    #DEF NULO POR VAZIO
    def substituir_nulo(valor):
        return "" if valor is None else valor
    
    sub = substituir_nulo

    #VALIDANDO JS
    nome_fantasia = sub(js["estabelecimento"]["nome_fantasia"]) 
    nome_fantasia  = js["razao_social"] if nome_fantasia == "" else nome_fantasia

    #CRIANDO REMETENTE
    remetente_dict = {
        "nome_fantasia": get_name_in(nome_fantasia),
        "cnpj": re.sub('[^0-9]', '', sub(js["estabelecimento"]["cnpj"])),
        "logradouro": sub(js["estabelecimento"]["tipo_logradouro"]) + " " + js["estabelecimento"]["logradouro"],
        "numero": sub(js["estabelecimento"]["numero"]),
        "complemento": sub(js["estabelecimento"]["complemento"]),
        "bairro": sub(js["estabelecimento"]["bairro"]),
        "municipio": (js["estabelecimento"]["cidade"]["nome"]),
        "uf": sub(js["estabelecimento"]["estado"]["sigla"]),
        "cep": re.sub('[^0-9]', '', sub(js["estabelecimento"]["cep"])),
        "telefone": re.sub('[^0-9]', '', sub(js["estabelecimento"]["ddd1"]) + sub(js["estabelecimento"]["telefone1"]))
    }

    return Remetente(*remetente_dict.values())

def gerar_nota(numero_nota, cnpj_emitente, valor_total, informacoes_adicionais, tem_unidade):
    #TRANSFORMAR JSON EM NOTA.TXT
    emitente = get_emitente_cnpj(cnpj_emitente)

    #TRANSFORMAR NOTA EM JSON
    transform_json(numero_nota, cnpj_emitente, tem_unidade)

    with open(f"notas_json/{numero_nota}.json", "r", encoding='utf-8') as file:
        js = json.load(file)
        remetente = get_remetente_cnpj(js["cnpj_promotor"])#
    
    build_note(numero_nota, valor_total, emitente, remetente, informacoes_adicionais)

def verificar_criar_diretorio():
    diretorios = ["notas_json", "notas_feitas", "notas"]

    for diretorio in diretorios:
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
   
def main():
    """Processa o arquivo PDF e os outros três valores inseridos"""
    caminho_pdf = entrada_pdf.get()
    cnpj_emitente = entrada_cnpj_emitente.get()
    valor_total = entrada_valor_total.get()
    informacoes_adicionais = entrada_informacoes_adicionais.get()
    numero_nota =  entrada_numero_nota.get()
    tem_unidade =  entrada_tem_unidade.get()

    #VALIDATION
    if not caminho_pdf or not cnpj_emitente or not valor_total or not informacoes_adicionais or not numero_nota:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return
    
    #----VALIDANDO CNPJ
    if not re.findall(r"^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$", cnpj_emitente):
        messagebox.showerror("INVALID CNPJ", "CNPJ inválido.")
        return

    #----VALIDANDO VALOR TOTAL
    try:
        num = float(valor_total)
    except Exception as e:
        messagebox.showerror("INVALID NUMBER", str(e))
        return
   
    #---VALIDANDO INFORMAÇÕES ADICIONAIS
    if "|" in informacoes_adicionais:
        messagebox.showerror("INVALID ADDITIONAL INFORMATION", "AS INFORMAÇÕES ADICIONAIS NÃO PODEM CONTER O CARACTERE '|'")
        return
    
    #---VALIDANDO NUMERO NOTA
    try:
        num = int(numero_nota)
    except Exception as e:
        messagebox.showerror("INVALID NUMBER", str(e))
        return

    #---VALIDANDO TEM UNIDADE
    if tem_unidade.lower() != "sim" and tem_unidade.lower() != "nao":
        messagebox.showerror("INVALID HAD UNIT", "A CAMPO TEM UNIDADE DEVE CONTER APENAS SIM OU NAO")
        return
    else:
        tem_unidade =  True if tem_unidade.lower() == "sim" else False

    # Copia do arquivo pdf
    shutil.copy(caminho_pdf, f"./notas/{numero_nota}.pdf")

    # INICIANDO NOTA
    try:
        gerar_nota(numero_nota, cnpj_emitente, valor_total, informacoes_adicionais, tem_unidade)
    except ValorDiferente as e:
        messagebox.showerror("Erro", e)
    except Exception as e:
        messagebox.showerror("Erro", e)
    else:
        messagebox.showinfo("Sucesso", "A nota foi feita com sucesso!")

if __name__ == "__main__":
    # Criando diretórios
    verificar_criar_diretorio()

    # Configuração da janela principal
    janela = tk.Tk()
    janela.title("EMISSOR AUTOMATICO")
    janela.geometry("600x500")

    # Labels e campos de entrada
    label_pdf = tk.Label(janela, text="PDF:")
    label_pdf.pack(pady=5)

    entrada_pdf = tk.Entry(janela, width=50)
    entrada_pdf.pack(pady=5)

    botao_pdf = tk.Button(janela, text="PDF NOTA", command=selecionar_pdf)
    botao_pdf.pack(pady=5)

    label_cnpj_remetente = tk.Label(janela, text="CNPJ REMETENTE")
    label_cnpj_remetente.pack(pady=5)

    entrada_cnpj_emitente = tk.Entry(janela) 
    entrada_cnpj_emitente.pack(pady=5)

    label_valor_total = tk.Label(janela, text="TOTAL NOTA")
    label_valor_total.pack(pady=5)

    entrada_valor_total = tk.Entry(janela)
    entrada_valor_total.pack(pady=5)

    label_informacoes_adicionais = tk.Label(janela, text="INFORMAÇÕES ADICIONAIS")
    label_informacoes_adicionais.pack(pady=5)

    entrada_informacoes_adicionais = tk.Entry(janela)
    entrada_informacoes_adicionais.pack(pady=5)

    label_numero_nota = tk.Label(janela, text="NUMERO NOTA")
    label_numero_nota.pack(pady=5)

    entrada_numero_nota = tk.Entry(janela)
    entrada_numero_nota.pack(pady=5)

    label_tem_unidade = tk.Label(janela, text="O ARQUIVO TEM COLUNA UNIDADE?(SIM OU NAO)")
    label_tem_unidade.pack(pady=5)

    entrada_tem_unidade = tk.Entry(janela)
    entrada_tem_unidade.pack(pady=5)

    

    # Botão para processar os dados
    botao_processar = tk.Button(janela, text="Processar", command=main)
    botao_processar.pack(pady=20)

    # Inicia o loop da interface
    janela.mainloop()
