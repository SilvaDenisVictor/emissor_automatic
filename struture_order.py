from pydantic import BaseModel, Field, field_validator
from decimal import Decimal
from typing import List
import requests

#Completar o ncm : 1542.1 -> 1542.10.00
def completar_ncm(ncm):
  final_ncm = ncm

  while len(final_ncm) < 10:
    final_ncm += '_'

  for index, c in enumerate(final_ncm):
    if c == "_":
      if index == 4 or index == 7:
        final_ncm = final_ncm.replace("_", ".", 1)
      else:
        final_ncm = final_ncm.replace("_", "0", 1)

  return final_ncm

#Calcular distancia entre dois ncms
def calcular_distancia(ncm_1, ncm_2):
  ncm_sep_1 = completar_ncm(ncm_1).split('.')
  ncm_sep_2 = completar_ncm(ncm_2).split('.')

  distancia = 0
  for i in range(len(ncm_sep_1)):
    distancia += abs(int(ncm_sep_1[i]) - int(ncm_sep_2[i]))

  return distancia

# Definindo o modelo de cada item
class Item(BaseModel):
    descricao: str = Field(..., description="Descrição completa do item.")
    quantidade: Decimal = Field(..., gt=0, decimal_places=2, description="Quantidade do item. Deve ser um valor decimal positivo.")
    preco_unitario: Decimal = Field(..., gt=0, decimal_places=2, description="Preço unitário do item. Deve ser um valor decimal positivo.")
    total: Decimal = Field(..., gt=0, decimal_places=2, description="Total referente ao item. Deve ser um valor decimal positivo.")
    unidade: str = Field(..., max_length=10, description="Unidade de medida do item, com no máximo 6 caracteres.")
    ncm: str = Field(..., pattern=r"^\d{4}\.\d{2}\.\d{2}$", description="Código NCM no formato NNNN.NN.NN")

# Definindo o modelo geral que receberá os dados
class Ordem(BaseModel):
    columns: List[str] = Field(..., description= "'descricao', 'quantidade', 'preco_unitario', 'total', 'unidade', 'ncm'")
    data: List[Item]  = Field(..., description="Lista de itens")
    total_ordem: Decimal = Field(..., gt=0, decimal_places=2, description="Valor total da nota.")
    cnpj_promotor: str = Field(..., pattern=r"^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$", description="O CPF deve ser diferente desse 46.333.345/0001-68.")
    coluna_unidade_bool: bool = Field(..., description="Deve retornar True caso a coluna unidade tem sido passada na tabela do pdf, False caso não")

    @field_validator('coluna_unidade_bool')
    def verificar_unidade_ativa(cls, v):
        if v not in [True, False]:
            raise ValueError('O valor deve ser um booleano (True ou False).')
        return v

    def validar_ncm(self):
      #Pegando lista de ncm
      response = requests.get("https://val.portalunico.siscomex.gov.br/classif/api/publico/nomenclatura/download/json")

      js = response.json()

      Nomenclaturas = []

      for nom in js["Nomenclaturas"]:
        if len(nom["Codigo"]) == 10:
          Nomenclaturas.append(nom)

      #ATUALIZANDO NCM
      distancia = [2**20]*len(self.data)
      id_distancia = [0]*len(self.data)

      nova_distancia = [-1]*len(self.data)

      for id_nom, nomeclatura in enumerate(Nomenclaturas):
          for id_dado, dado in enumerate(self.data):
              nova_distancia[id_dado] = calcular_distancia(nomeclatura["Codigo"], dado.ncm)

              if nova_distancia[id_dado] < distancia[id_dado]:
                distancia[id_dado] = nova_distancia[id_dado]
                id_distancia[id_dado] = id_nom

      for count in range(len(self.data)):
          self.data[count].ncm =  completar_ncm(Nomenclaturas[id_distancia[count]]["Codigo"])
          
    def ajustar_descricao(self, descricao_):
      descricao = descricao_.replace("\n", "")
    
      if len(descricao) <= 120:
          return descricao
      
      part_descricao = descricao.split(",")
      
      first = 0
      last = len(part_descricao) - 1
      next = 1
      descricao_ajustada_inicio = []
      descricao_ajustada_fim = []
      descricao_ajustada = []
      
      while len(", ".join(descricao_ajustada + [part_descricao[first if next else last]])) <= 120:
          if next:
              descricao_ajustada_inicio.append(part_descricao[first])
              first += 1
              next = 0
          else:
              descricao_ajustada_fim.insert(0, part_descricao[last])
              last -= 1
              next = 1
          
          descricao_ajustada = descricao_ajustada_inicio + descricao_ajustada_fim
      
      return ", ".join(descricao_ajustada)
  
    def validar_descricao(self):
       for dado in self.data:
          dado.descricao =  self.ajustar_descricao(dado.descricao)
    
    def validar_und(self):
      for dado in self.data:
        if self.coluna_unidade_bool:
          if dado.unidade.lower() == "pacote":
            dado.unidade = "PCT"
          
          elif dado.unidade.lower() == "unidade":
            dado.unidade = "UND"
          
          elif dado.unidade.lower() == "caixa":
            dado.unidade = "CX"

          elif dado.unidade.lower() == "conjunto":
            dado.unidade = "CONJ"

          else:
            dado.unidade = dado.unidade[0:6]
        else:
          if "resma" in dado.descricao.lower():
            dado.unidade =  "RESMA"
          elif "caixa" in dado.descricao.lower():
            dado.unidade =  "CX"
          elif "pacote" in dado.descricao.lower():
            dado.unidade = "PCT"
          elif "kg" in dado.descricao.lower():
            dado.unidade =  "KG"
          elif "unidade" in dado.descricao.lower() or "und" in dado.descricao.lower() or "unid" in dado.descricao.lower():
            dado.unidade =  "UND"


