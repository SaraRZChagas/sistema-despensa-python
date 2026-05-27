# ================================================================================
#   SISTEMA DE GESTÃO DE DESPENSA
#   Projeto Final - Módulo Criar aplicações em linguagem de programação Python 
#   Aplicação de terminal para gerir inventário doméstico
# ================================================================================

import os
from datetime import datetime

# ── Dados em memória ─────────────────────────────────────────
despensa = []        # Lista de produtos cadastrados
lista_compras = []   # Lista gerada automaticamente
historico = []       # Registo de ações com data/hora

FICHEIRO_DESPENSA = "despensa.txt"

# ──────────────────────────────────────────────────────────────
# FUNÇÕES UTILITÁRIAS
# ──────────────────────────────────────────────────────────────

def limpar_ecra():
    os.system("cls" if os.name == "nt" else "clear")

def linha(char="─", largura=56):
    return char * largura

def cabecalho(titulo):
    print()
    print("╔" + "═" * 54 + "╗")
    print("║" + titulo.center(54) + "║")
    print("╚" + "═" * 54 + "╝")

def pausar():
    input("\n  Pressiona ENTER para continuar...")

def registar_acao(acao):
    timestamp = datetime.now().strftime("%d/%m %H:%M")
    historico.append(f"[{timestamp}] {acao}")

def input_numero(mensagem, minimo=0, maximo=None, permitir_zero=True):
    while True:
        try:
            valor = float(input(mensagem))
            if not permitir_zero and valor == 0:
                print("  ⚠  O valor não pode ser zero.")
                continue
            if valor < minimo:
                print(f"  ⚠  O valor mínimo é {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"  ⚠  O valor máximo é {maximo}.")
                continue
            return valor
        except ValueError:
            print("  ⚠  Introduz um número válido.")

def input_inteiro(mensagem, minimo=0, maximo=None):
    while True:
        try:
            valor = int(input(mensagem))
            if valor < minimo:
                print(f"  ⚠  O valor mínimo é {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"  ⚠  O valor máximo é {maximo}.")
                continue
            return valor
        except ValueError:
            print("  ⚠  Introduz um número inteiro válido.")

# ──────────────────────────────────────────────────────────────
# FUNÇÕES DE FICHEIROS
# ──────────────────────────────────────────────────────────────

def guardar_dados():
    """Guarda todos os produtos no ficheiro despensa.txt."""
    with open(FICHEIRO_DESPENSA, "w", encoding="utf-8") as f:
        for item in despensa:
            f.write(f"{item['nome']},{item['unidade']},{item['quantidade']},{item['quantidade_ideal']},{item['minimo']}\n")

def carregar_dados():
    """Carrega os produtos do ficheiro despensa.txt para a memória."""
    try:
        with open(FICHEIRO_DESPENSA, "r", encoding="utf-8") as f:
            linhas = f.readlines()
            for linha_txt in linhas:
                dados = linha_txt.strip().split(",")
                if len(dados) == 5:
                    despensa.append({
                        "nome": dados[0],
                        "unidade": dados[1],
                        "quantidade": float(dados[2]),
                        "quantidade_ideal": float(dados[3]),
                        "minimo": float(dados[4])
                    })
        registar_acao(f"Dados carregados do ficheiro ({len(despensa)} produtos)")
        return True
    except FileNotFoundError:
        return False
    
    
# ──────────────────────────────────────────────────────────────
# FUNÇÕES DA DESPENSA
# ──────────────────────────────────────────────────────────────

def encontrar_item(nome):
    for item in despensa:
        if item["nome"].lower() == nome.lower():
            return item
    return None

def estado_item(item):
    percentagem = (item["quantidade"] / item["quantidade_ideal"]) * 100 if item["quantidade_ideal"] > 0 else 0
    if item["quantidade"] <= item["minimo"]:
        return "🔴", "CRÍTICO"
    elif percentagem < 50:
        return "🟡", "BAIXO"
    elif percentagem >= 100:
        return "✅", "CHEIO"
    else:
        return "🟢", "OK"

def adicionar_item():
    cabecalho("  ➕  ADICIONAR ITEM À DESPENSA")
    print()
    nome = input("  Nome do produto: ").strip().title()
    if not nome:
        print("  ⚠  Nome não pode ser vazio.")
        return
    if encontrar_item(nome):
        print(f"  ⚠  '{nome}' já existe. Usa 'Atualizar' para editar.")
        pausar()
        return
    unidade = input("  Unidade (ex: kg, L, un, g): ").strip() or "un"
    quantidade = input_numero(f"  Quantidade atual ({unidade}): ")
    quantidade_ideal = input_numero(f"  Quantidade ideal p/ início de mês ({unidade}): ", permitir_zero=False)
    minimo = input_numero(f"  Quantidade mínima (alerta de compra) ({unidade}): ")
    item = {
        "nome": nome,
        "unidade": unidade,
        "quantidade": quantidade,
        "quantidade_ideal": quantidade_ideal,
        "minimo": minimo
    }
    despensa.append(item)
    guardar_dados()
    registar_acao(f"Item adicionado: {nome} ({quantidade} {unidade})")
    print(f"\n  ✅  '{nome}' adicionado e guardado no ficheiro!")
    pausar()

def listar_despensa():
    cabecalho("  📦  INVENTÁRIO DA DESPENSA")
    if not despensa:
        print("\n  A despensa está vazia. Adiciona itens primeiro.")
        pausar()
        return
    print()
    print(f"  {'PRODUTO':<20} {'QTD':>6} {'IDEAL':>6} {'MÍN':>5} {'UN':<5} {'ESTADO':<10}")
    print("  " + linha("─", 54))
    criticos = []
    for item in sorted(despensa, key=lambda x: x["nome"]):
        emoji, estado = estado_item(item)
        print(f"  {item['nome']:<20} {item['quantidade']:>6.1f} {item['quantidade_ideal']:>6.1f} {item['minimo']:>5.1f} {item['unidade']:<5} {emoji} {estado}")
        if item["quantidade"] <= item["minimo"]:
            criticos.append(item["nome"])
    print("  " + linha("─", 54))
    print(f"  Total de produtos: {len(despensa)}")
    if criticos:
        print(f"\n  🔴 Atenção! {len(criticos)} produto(s) em nível crítico:")
        for c in criticos:
            print(f"     • {c}")
    pausar()

def atualizar_quantidade():
    cabecalho("  📝  ATUALIZAR QUANTIDADE")
    print()
    if not despensa:
        print("  A despensa está vazia.")
        pausar()
        return
    for i, item in enumerate(despensa, 1):
        emoji, _ = estado_item(item)
        print(f"  {i:>2}. {emoji} {item['nome']} — {item['quantidade']} {item['unidade']}")
    print()
    escolha = input_inteiro("  Número do produto (0 para cancelar): ", 0, len(despensa))
    if escolha == 0:
        return
    item = despensa[escolha - 1]
    print(f"\n  Produto: {item['nome']} | Atual: {item['quantidade']} {item['unidade']}")
    nova_qtd = input_numero(f"  Nova quantidade ({item['unidade']}): ")
    anterior = item["quantidade"]
    item["quantidade"] = nova_qtd
    guardar_dados()
    registar_acao(f"Quantidade atualizada: {item['nome']} {anterior}→{nova_qtd} {item['unidade']}")
    emoji, estado = estado_item(item)
    print(f"\n  ✅  Atualizado e guardado! Estado: {emoji} {estado}")
    if item["quantidade"] <= item["minimo"]:
        print(f"  ⚠  Atenção! '{item['nome']}' está abaixo do mínimo.")
    pausar()

def remover_item():
    cabecalho("  🗑  REMOVER ITEM")
    print()
    if not despensa:
        print("  A despensa está vazia.")
        pausar()
        return
    for i, item in enumerate(despensa, 1):
        print(f"  {i:>2}. {item['nome']}")
    print()
    escolha = input_inteiro("  Número do produto a remover (0 para cancelar): ", 0, len(despensa))
    if escolha == 0:
        return
    item = despensa[escolha - 1]
    confirmacao = input(f"  Tens a certeza que queres remover '{item['nome']}'? (s/n): ").lower()
    if confirmacao == "s":
        despensa.remove(item)
        guardar_dados()
        registar_acao(f"Item removido: {item['nome']}")
        print(f"  ✅  '{item['nome']}' removido e ficheiro atualizado.")
    else:
        print("  ❌  Remoção cancelada.")
    pausar()
