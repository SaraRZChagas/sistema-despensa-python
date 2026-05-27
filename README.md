# 🏠 Sistema de Gestão de Despensa

> **Projeto Final — Módulo: Criar Aplicações em Linguagem de Programação Python**  

***

## 📋 Descrição

O **Sistema de Gestão de Despensa** é uma aplicação de terminal desenvolvida em Python que permite gerir o inventário doméstico de forma prática e intuitiva. O utilizador pode cadastrar produtos com quantidades ideais e mínimas, gerar listas de compras automaticamente e registar as compras efetuadas — atualizando o inventário em tempo real.

Os dados são guardados automaticamente num ficheiro `.txt` após cada alteração, garantindo que a informação persiste entre sessões do programa.

O projeto foi desenvolvido como trabalho final do módulo de Python, aplicando os conceitos fundamentais da linguagem: variáveis, condições, ciclos, funções, listas, dicionários, tratamento de erros e manipulação de ficheiros.

***

## ✨ Funcionalidades

### 📦 Gestão da Despensa
- Adicionar produtos com nome, unidade, quantidade atual, quantidade ideal e quantidade mínima
- Listar todos os produtos com indicador visual de estado (🔴 Crítico / 🟡 Baixo / 🟢 OK / ✅ Cheio)
- Atualizar a quantidade de qualquer produto
- Remover produtos da despensa

### 🛒 Lista de Compras
- Geração **automática** da lista com base nos produtos abaixo da quantidade ideal
- Produtos urgentes (abaixo do mínimo) aparecem em destaque no topo
- Marcação de itens como comprados com atualização automática da despensa

### 💾 Persistência de Dados
- Dados guardados automaticamente no ficheiro `despensa.txt` após cada alteração
- Na próxima execução, o programa carrega os dados guardados automaticamente
- Usa `open()` com modos `"w"` e `"r"` e `with open()` como Context Manager

### 📊 Relatórios e Histórico
- Relatório resumo com percentagem de "saúde" da despensa
- Histórico completo de ações com data e hora

***

## 🗂️ Estrutura do Projeto

```
sistema-despensa-python/
├── despensa.py      # Código principal da aplicação
├── despensa.txt     # Ficheiro de dados (criado automaticamente)
└── README.md        # Documentação do projeto
```

***

## 🚀 Como Executar

### Pré-requisitos
- Python 3.x instalado ([python.org](https://www.python.org/downloads/))

### Passos
1. Clona o repositório:
   ```bash
   git clone https://github.com/SaraRZChagas/sistema-despensa-python
   cd sistema-despensa-python
   ```

2. Executa o programa:
   ```bash
   python despensa.py
   ```

> Não são necessárias bibliotecas externas. O programa usa apenas módulos da biblioteca padrão do Python (`os`, `datetime`).

***

## 🧩 Conceitos Python Aplicados

| Conceito | Onde é utilizado |
|---|---|
| **Variáveis e tipos** | `str`, `float`, `int`, `bool` em cada produto |
| **Listas** | `despensa`, `lista_compras`, `historico` |
| **Dicionários** | Cada produto é um dicionário com 5 chaves |
| **Condições `if/elif/else`** | Estado do item, validações, confirmações |
| **Ciclos `while`** | Menus interativos em loop até o utilizador sair |
| **Ciclos `for`** | Percorrer e listar produtos |
| **Funções** | +15 funções organizadas por responsabilidade |
| **`try/except`** | Validação de todos os inputs numéricos |
| **`f-strings`** | Formatação de todos os outputs |
| **`datetime`** | Timestamp no histórico de ações |
| **`open()` modo `"w"`** | Guardar dados no ficheiro (Aula 12) |
| **`open()` modo `"r"`** | Carregar dados do ficheiro (Aula 12) |
| **`readlines()`** | Ler todas as linhas do ficheiro (Aula 12) |
| **`with open()`** | Context Manager — fechar ficheiro automaticamente (Aula 12) |

***

## 💾 Como Funciona o Armazenamento

Cada produto é guardado como uma linha no ficheiro `despensa.txt`, com os campos separados por vírgula:

```
Arroz,kg,0.5,5.0,1.0
Açúcar,kg,2.0,2.0,0.5
Café,g,50.0,500.0,100.0
```

Ao iniciar o programa, o ficheiro é lido com `readlines()`, cada linha é separada com `.split(",")` e convertida num dicionário na lista `despensa`.

***

## 🖥️ Demonstração

```
╔══════════════════════════════════════════════════════╗
║         🏠  SISTEMA DE GESTÃO DE DESPENSA            ║
╚══════════════════════════════════════════════════════╝
  📦 5 produto(s) na despensa  |  🔴 2 em nível crítico

  1. 📦  Gestão da Despensa
  2. 🛒  Lista de Compras
  3. 📊  Relatório
  4. 📜  Histórico

  0. 🚪  Sair
```

***

## 🏗️ Arquitetura do Código

O código está organizado em 5 camadas de funções:

1. **Utilitários** — `limpar_ecra()`, `input_numero()`, `input_inteiro()`, `registar_acao()`
2. **Ficheiros** — `guardar_dados()`, `carregar_dados()`
3. **Despensa** — `adicionar_item()`, `listar_despensa()`, `atualizar_quantidade()`, `remover_item()`
4. **Compras** — `gerar_lista_compras()`, `ver_e_marcar_compras()`
5. **Menus** — `menu_principal()`, `menu_despensa()`, `menu_compras()`

***

## 💡 Melhorias Futuras

- [ ] Exportação da lista de compras para ficheiro `.txt`
- [ ] Pesquisa de produtos por nome
- [ ] Categorias de produtos (frescos, congelados, limpeza, etc.)
- [ ] Interface gráfica com `tkinter`
- [ ] Armazenamento em base de dados com SQLite

***

## 👩‍💻 Autora

Desenvolvido como projeto final do Módulo de Criar aplicações em linguagem de programação Python  


***

## 📄 Licença

Este projeto é de uso académico.