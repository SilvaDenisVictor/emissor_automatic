# Automação de Criação de Notas Fiscais a partir de PDFs de Ordens

Este projeto tem como objetivo **automatizar a criação de notas fiscais** a partir de PDFs de ordens, reduzindo significativamente o tempo necessário para gerar as notas manualmente. Utiliza tecnologias avançadas de **Modelos de Linguagem de Grande Escala (LLM)**, como **LLama**, **ChatGPT**, **LangChain** e **PyDantic** para garantir um retorno de dados estruturado. A interface do usuário foi desenvolvida com **Tkinter** para proporcionar uma experiência desktop intuitiva.

## Tecnologias Utilizadas

- **LLama**, **ChatGPT**: Utilizados para entender o conteúdo do PDF da ordem e gerar a nota fiscal com base nos dados extraídos.
- **LangChain**: Integrado para facilitar o fluxo de dados entre diferentes modelos e APIs, proporcionando automação e integração eficiente.
- **PyDantic**: Utilizado para a tipagem dos dados, garantindo que o retorno dos dados esteja bem estruturado e validado.
- **Tkinter**: Utilizado para a criação da interface desktop, permitindo que o usuário interaja facilmente com o sistema.

## Funcionalidades

- **Leitura de PDFs**: O sistema lê PDFs de ordens e extrai dados relevantes para a criação de uma nota fiscal.
- **Automatização da Criação de Notas**: Através da interpretação dos dados extraídos, o sistema automatiza a geração da nota fiscal, economizando horas de trabalho manual.
- **Geração de Arquivo TXT**: O sistema gera um arquivo de texto (.txt) seguindo o **padrão TXT-NFe 4.0**, utilizado para a troca de informações fiscais eletrônicas no Brasil.
- **Integração com APIs**: O sistema faz uso extensivo de APIs para buscar informações adicionais necessárias para completar a nota fiscal.
- **Interface Desktop**: Interface gráfica simples e intuitiva desenvolvida com Tkinter, que permite o carregamento de arquivos PDF e visualização das notas geradas.
- **Retorno Estruturado**: Os dados extraídos e a nota fiscal gerada são retornados de forma estruturada, utilizando PyDantic para validação.
