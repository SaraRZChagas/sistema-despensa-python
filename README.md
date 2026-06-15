# Sistema de Gestão de Despensa

> **Projeto Final — Módulo: Criar Aplicações em Linguagem de Programação Python**

***

## Descrição

O Sistema de Gestão de Despensa é uma aplicação de terminal desenvolvida em Python para gerir o inventário doméstico. O utilizador pode cadastrar produtos com quantidades esperadas e mínimas, acompanhar o stock atual, gerar listas de compras automaticamente e registar as compras efetuadas — com atualização do inventário em tempo real.

Os dados são guardados automaticamente em ficheiros `.txt` após cada alteração, garantindo persistência entre sessões.

O projeto aplica os principais conceitos abordados no módulo: variáveis, condições, ciclos, funções, listas, dicionários, tratamento de erros e manipulação de ficheiros.

***

## Funcionalidades

### Gestão da Despensa
- Cadastrar produtos com nome, unidade, quantidade ideal e quantidade mínima — a quantidade atual começa a 0 e é registada separadamente
- Editar qualquer campo de um produto já cadastrado (nome, unidade, ideal, mínimo)
- Atualizar a quantidade atual de um produto na despensa
- Listar todos os produtos com indicador visual de estado (🔴 Crítico / 🟡 Baixo / 🟢 OK / ✅ Cheio), distinguindo produtos cadastrados de produtos com stock
- Remover produtos

### Lista de Compras
- Geração automática com base nos produtos abaixo da quantidade ideal
- Itens urgentes (abaixo do mínimo) destacados no topo
- Adição manual de itens à lista
- Edição e remoção de itens da lista
- Mesclagem de itens manuais com os gerados automaticamente — sem duplicados
- Marcação de compras efetuadas com atualização automática da despensa

### Persistência de Dados
- Gravação automática em `despensa.txt` e `lista_compras.txt` após cada operação
- Carregamento automático dos dados ao iniciar o programa
- Utiliza `open()` nos modos `"w"` e `"r"` com `with open()` como Context Manager

### Relatórios e Histórico
- Relatório com contagem por estado e percentagem de saúde da despensa
- Histórico das últimas ações com data e hora

***

## Estrutura do Projeto

```
sistema-despensa-python/
├── despensa.py        # Código principal da aplicação
├── despensa.txt       # Dados da despensa (criado automaticamente)
├── lista_compras.txt  # Lista de compras (criado automaticamente)
└── README.md          # Documentação do projeto
```

***

## Como Executar

**Pré-requisitos:** Python 3.x instalado ([python.org](https://www.python.org/downloads/))

```bash
git clone https://github.com/SaraRZChagas/sistema-despensa-python
cd sistema-despensa-python
python despensa.py
```

Não são necessárias bibliotecas externas. O programa utiliza apenas `os` e `datetime` da biblioteca padrão do Python.

***

## Conceitos Python Aplicados

| Conceito | Onde é utilizado |
|---|---|
| **Variáveis e tipos** | `str`, `float`, `int`, `bool` em cada produto |
| **Listas** | `despensa`, `lista_compras`, `historico` |
| **Dicionários** | Cada produto é um dicionário com 5 chaves |
| **Condições `if/elif/else`** | Estado do item, validações, menus |
| **Ciclos `while`** | Menus em loop até o utilizador sair |
| **Ciclos `for`** | Percorrer e listar produtos |
| **Funções** | +20 funções organizadas por responsabilidade |
| **`try/except ValueError`** | Validação de inputs numéricos em `input_numero()` e `input_inteiro()` |
| **`try/except FileNotFoundError`** | Carregar ficheiros em `carregar_dados()` e `carregar_lista()` |
| **`f-strings`** | Formatação de todos os outputs |
| **`datetime`** | Timestamp no histórico de ações |
| **`open()` modo `"w"`** | Guardar dados nos ficheiros |
| **`open()` modo `"r"`** | Carregar dados dos ficheiros |
| **`readlines()`** | Ler todas as linhas do ficheiro |
| **`with open()`** | Context Manager para fechar ficheiro automaticamente |

***

## Como Funciona o Armazenamento

Cada produto é guardado como uma linha em `despensa.txt`, com campos separados por vírgula:

```
Arroz,kg,0.5,5.0,1.0
Açúcar,kg,2.0,2.0,0.5
Café,g,50.0,500.0,100.0
```

Ao iniciar, o ficheiro é lido com `readlines()`, cada linha é separada com `.split(",")` e convertida num dicionário na lista `despensa`. A lista de compras segue o mesmo princípio, com 6 campos (incluindo o campo `manual`, que distingue itens adicionados manualmente dos gerados automaticamente).

***

## Arquitetura do Código

O código está organizado em 5 camadas de funções:

1. **Utilitários** — `limpar_ecra()`, `linha()`, `cabecalho()`, `pausar()`, `registar_acao()`, `input_numero()`, `input_inteiro()`
2. **Ficheiros** — `guardar_dados()`, `carregar_dados()`, `guardar_lista()`, `carregar_lista()`
3. **Despensa** — `adicionar_item()`, `editar_produto()`, `atualizar_quantidade()`, `listar_despensa()`, `remover_item()`
4. **Compras** — `gerar_lista_compras()`, `adicionar_item_lista()`, `editar_item_lista()`, `ver_lista_compras()`, `remover_item_lista()`, `ver_e_marcar_compras()`
5. **Menus** — `menu_principal()`, `menu_despensa()`, `menu_compras()`

***

## Melhorias Futuras

- [ ] Exportação da lista de compras para ficheiro `.txt`
- [ ] Pesquisa de produtos por nome
- [ ] Categorias de produtos (frescos, congelados, limpeza, etc.)
- [ ] Interface gráfica com `tkinter`
- [ ] Armazenamento em base de dados com SQLite

***

## Autora

Desenvolvido como projeto final do Módulo de Criar Aplicações em Linguagem de Programação Python.

***

## Licença

Projeto de uso académico.