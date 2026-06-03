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
FICHEIRO_LISTA = "lista_compras.txt"


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


def guardar_lista():
    with open(FICHEIRO_LISTA, "w", encoding="utf-8") as f:
        for item in lista_compras:
            f.write(f"{item['nome']},{item['unidade']},{item['quantidade_necessaria']},{item['comprado']},{item['urgente']},{item.get('manual', False)}\n")


def carregar_lista():
    try:
        with open(FICHEIRO_LISTA, "r", encoding="utf-8") as f:
            for linha_txt in f.readlines():
                dados = linha_txt.strip().split(",")
                if len(dados) == 6:
                    lista_compras.append({
                        "nome": dados[0],
                        "unidade": dados[1],
                        "quantidade_necessaria": float(dados[2]),
                        "comprado": dados[3] == "True",
                        "urgente": dados[4] == "True",
                        "manual": dados[5] == "True"
                    })
    except FileNotFoundError:
        pass


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
        print(f"  ⚠  '{nome}' já existe. Usa 'Editar Produto' para alterar.")
        pausar()
        return
    unidade = input("  Unidade (ex: kg, L, un, g): ").strip() or "un"
    quantidade_ideal = input_numero(f"  Quantidade ideal p/ início de mês ({unidade}): ", permitir_zero=False)
    minimo = input_numero(f"  Quantidade mínima (alerta de compra) ({unidade}): ")
    item = {
        "nome": nome,
        "unidade": unidade,
        "quantidade": 0,
        "quantidade_ideal": quantidade_ideal,
        "minimo": minimo
    }
    despensa.append(item)
    guardar_dados()
    registar_acao(f"Item adicionado: {nome} (ideal: {quantidade_ideal} {unidade})")
    print(f"\n  ✅  '{nome}' adicionado! Usa 'Atualizar Quantidade' para registar o que tens em casa.")
    pausar()


def editar_produto():
    cabecalho("  ✏️   EDITAR PRODUTO")
    print()
    if not despensa:
        print("  A despensa está vazia.")
        pausar()
        return
    for i, item in enumerate(despensa, 1):
        print(f"  {i:>2}. {item['nome']} — ideal: {item['quantidade_ideal']} {item['unidade']} | mín: {item['minimo']} {item['unidade']}")
    print()
    escolha = input_inteiro("  Número do produto (0 para cancelar): ", 0, len(despensa))
    if escolha == 0:
        return
    item = despensa[escolha - 1]
    print(f"\n  Produto: {item['nome']} | Unidade: {item['unidade']} | Ideal: {item['quantidade_ideal']} | Mínimo: {item['minimo']}")
    print()

    if input("  Alterar nome? (s/n): ").lower() == "s":
        novo_nome = input(f"  Novo nome: ").strip().title()
        if novo_nome:
            item["nome"] = novo_nome

    if input("  Alterar unidade? (s/n): ").lower() == "s":
        nova_unidade = input(f"  Nova unidade (ex: kg, L, un, g): ").strip()
        if nova_unidade:
            item["unidade"] = nova_unidade

    if input("  Alterar quantidade ideal? (s/n): ").lower() == "s":
        item["quantidade_ideal"] = input_numero(f"  Nova quantidade ideal ({item['unidade']}): ", permitir_zero=False)

    if input("  Alterar quantidade mínima? (s/n): ").lower() == "s":
        item["minimo"] = input_numero(f"  Nova quantidade mínima ({item['unidade']}): ")

    guardar_dados()
    registar_acao(f"Produto editado: {item['nome']} — unidade: {item['unidade']}, ideal: {item['quantidade_ideal']}, mínimo: {item['minimo']}")
    print(f"\n  ✅  '{item['nome']}' atualizado e guardado!")
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
    na_despensa = sum(1 for i in despensa if i["quantidade"] > 0)
    por_registar = sum(1 for i in despensa if i["quantidade"] == 0)
    print(f"  Produtos cadastrados:  {len(despensa)}")
    print(f"  Com stock na despensa: {na_despensa}")
    if por_registar:
        print(f"  ⚪ Sem stock ainda:    {por_registar}  (usa 'Atualizar Quantidade')")
    if criticos:
        print(f"\n  🔴 Atenção! {len(criticos)} produto(s) em nível crítico:")
        for c in criticos:
            print(f"     • {c}")
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


# ──────────────────────────────────────────────────────────────
# FUNÇÕES DA LISTA DE COMPRAS
# ──────────────────────────────────────────────────────────────


def gerar_lista_compras():
    global lista_compras
    manuais = [i for i in lista_compras if i.get("manual")]
    automaticos = []
    for item in despensa:
        if item["quantidade"] < item["quantidade_ideal"]:
            ja_existe = any(i["nome"].lower() == item["nome"].lower() for i in manuais)
            if not ja_existe:
                quantidade_necessaria = item["quantidade_ideal"] - item["quantidade"]
                automaticos.append({
                    "nome": item["nome"],
                    "unidade": item["unidade"],
                    "quantidade_necessaria": round(quantidade_necessaria, 2),
                    "comprado": False,
                    "urgente": item["quantidade"] <= item["minimo"],
                    "manual": False
                })
    lista_compras = manuais + automaticos
    lista_compras.sort(key=lambda x: (not x["urgente"], x["nome"]))
    cabecalho("  🛒  LISTA DE COMPRAS GERADA")
    print()
    if not lista_compras:
        print("  ✅  A despensa está completa! Nenhuma compra necessária.")
    else:
        urgentes = [i for i in lista_compras if i["urgente"]]
        normais  = [i for i in lista_compras if not i["urgente"]]
        if urgentes:
            print("  🔴 URGENTE:")
            for item in urgentes:
                print(f"     • {item['nome']:<20} {item['quantidade_necessaria']:>6.1f} {item['unidade']}")
            print()
        if normais:
            print("  🟡 A REPOR:")
            for item in normais:
                print(f"     • {item['nome']:<20} {item['quantidade_necessaria']:>6.1f} {item['unidade']}")
        print(f"\n  📋 Total: {len(lista_compras)} produto(s) para comprar")
        registar_acao(f"Lista de compras gerada: {len(lista_compras)} itens")
    guardar_lista()
    pausar()


def adicionar_item_lista():
    cabecalho("  ✏️   ADICIONAR ITEM À LISTA DE COMPRAS")
    print()
    nome = input("  Nome do produto: ").strip().title()
    if not nome:
        print("  ⚠  Nome não pode ser vazio.")
        pausar()
        return
    for item in lista_compras:
        if item["nome"].lower() == nome.lower():
            print(f"  ⚠  '{nome}' já está na lista de compras.")
            pausar()
            return
    unidade = input("  Unidade (ex: kg, L, un, g): ").strip() or "un"
    quantidade = input_numero(f"  Quantidade a comprar ({unidade}): ", permitir_zero=False)
    lista_compras.append({
        "nome": nome,
        "unidade": unidade,
        "quantidade_necessaria": quantidade,
        "comprado": False,
        "urgente": False,
        "manual": True
    })
    registar_acao(f"Item adicionado manualmente à lista: {nome} ({quantidade} {unidade})")
    print(f"\n  ✅  '{nome}' adicionado à lista de compras!")
    guardar_lista()
    pausar()


def ver_lista_compras():
    cabecalho("  📋  LISTA DE COMPRAS")
    print()
    if not lista_compras:
        print("  A lista está vazia. Gera a lista automática ou adiciona itens manualmente.")
        pausar()
        return
    por_comprar = [i for i in lista_compras if not i["comprado"]]
    comprados   = [i for i in lista_compras if i["comprado"]]
    if por_comprar:
        print("  🛒 POR COMPRAR:")
        print(f"  {'Nº':<4} {'PRODUTO':<22} {'QTD':<8} {'UN':<5} URGENTE")
        print("  " + linha("─", 50))
        for i, item in enumerate(por_comprar, 1):
            urgente = "🔴 SIM" if item["urgente"] else "   não"
            print(f"  {i:<4} {item['nome']:<22} {item['quantidade_necessaria']:<8.1f} {item['unidade']:<5} {urgente}")
    if comprados:
        print()
        print("  ✅ JÁ COMPRADO:")
        for item in comprados:
            print(f"     ✔ {item['nome']}")
    print()
    print(f"  📋 Total: {len(por_comprar)} por comprar | {len(comprados)} já comprado(s)")
    pausar()

def editar_item_lista():
    cabecalho("  ✏️   EDITAR ITEM DA LISTA DE COMPRAS")
    print()
    if not lista_compras:
        print("  A lista está vazia.")
        pausar()
        return
    for i, item in enumerate(lista_compras, 1):
        estado = "✔" if item["comprado"] else "🛒"
        manual = " [manual]" if item.get("manual") else ""
        print(f"  {i:>2}. {estado} {item['nome']} — {item['quantidade_necessaria']} {item['unidade']}{manual}")
    print()
    escolha = input_inteiro("  Número do item (0 para cancelar): ", 0, len(lista_compras))
    if escolha == 0:
        return
    item = lista_compras[escolha - 1]
    print(f"\n  Item: {item['nome']} | Quantidade: {item['quantidade_necessaria']} {item['unidade']}")
    print()

    if input("  Alterar nome? (s/n): ").lower() == "s":
        novo_nome = input("  Novo nome: ").strip().title()
        if novo_nome:
            item["nome"] = novo_nome

    if input("  Alterar unidade? (s/n): ").lower() == "s":
        nova_unidade = input("  Nova unidade (ex: kg, L, un, g): ").strip()
        if nova_unidade:
            item["unidade"] = nova_unidade

    if input("  Alterar quantidade? (s/n): ").lower() == "s":
        item["quantidade_necessaria"] = input_numero(f"  Nova quantidade ({item['unidade']}): ", permitir_zero=False)

    if input("  Marcar como urgente? (s/n): ").lower() == "s":
        item["urgente"] = True
    
    guardar_lista()
    registar_acao(f"Item da lista editado: {item['nome']} ({item['quantidade_necessaria']} {item['unidade']})")
    print(f"\n  ✅  '{item['nome']}' atualizado na lista!")
    pausar()


def remover_item_lista():
    cabecalho("  🗑️   REMOVER ITEM DA LISTA")
    print()
    if not lista_compras:
        print("  A lista está vazia.")
        pausar()
        return
    for i, item in enumerate(lista_compras, 1):
        estado = "✔" if item["comprado"] else "🛒"
        print(f"  {i:>2}. {estado} {item['nome']} — {item['quantidade_necessaria']} {item['unidade']}")
    print()
    escolha = input_inteiro("  Número do item a remover (0 para cancelar): ", 0, len(lista_compras))
    if escolha == 0:
        return
    item = lista_compras[escolha - 1]
    confirmacao = input(f"  Remover '{item['nome']}' da lista? (s/n): ").lower()
    if confirmacao == "s":
        lista_compras.remove(item)
        guardar_lista()
        registar_acao(f"Item removido da lista: {item['nome']}")
        print(f"  ✅  '{item['nome']}' removido da lista.")
    else:
        print("  ❌  Remoção cancelada.")
    pausar()


def ver_e_marcar_compras():
    cabecalho("  ✅  REGISTAR COMPRAS")
    print()
    if not lista_compras:
        print("  Sem lista de compras. Gera primeiro a lista automática.")
        pausar()
        return
    por_comprar = [i for i in lista_compras if not i["comprado"]]
    if not por_comprar:
        print("  ✅  Todas as compras já foram registadas!")
        pausar()
        return
    print(f"  {'Nº':<4} {'PRODUTO':<22} {'QTD':<8} {'UN':<5} URGENTE")
    print("  " + linha("─", 50))
    for i, item in enumerate(por_comprar, 1):
        urgente = "🔴 SIM" if item["urgente"] else "   não"
        print(f"  {i:<4} {item['nome']:<22} {item['quantidade_necessaria']:<8.1f} {item['unidade']:<5} {urgente}")
    print()
    print("  (Escreve o número para marcar como comprado, 0 para sair)")
    while True:
        escolha = input_inteiro("  Nº do produto comprado (0 para sair): ", 0, len(por_comprar))
        if escolha == 0:
            break
        item_comprado = por_comprar[escolha - 1]
        item_comprado["comprado"] = True
        item_despensa = encontrar_item(item_comprado["nome"])
        if item_despensa:
            item_despensa["quantidade"] = item_despensa["quantidade_ideal"]
            emoji, estado = estado_item(item_despensa)
            print(f"  ✅  '{item_comprado['nome']}' marcado! Despensa: {emoji} {estado}")
            registar_acao(f"Compra registada: {item_comprado['nome']} ({item_comprado['quantidade_necessaria']} {item_comprado['unidade']})")
        por_comprar = [i for i in lista_compras if not i["comprado"]]
        if not por_comprar:
            print("\n  🎉 Todas as compras registadas! Despensa atualizada.")
            break
    guardar_dados()
    guardar_lista()
    pausar()


# ──────────────────────────────────────────────────────────────
# RELATÓRIO E HISTÓRICO
# ──────────────────────────────────────────────────────────────


def ver_relatorio():
    cabecalho("  📊  RELATÓRIO DA DESPENSA")
    print()
    if not despensa:
        print("  Sem dados para apresentar.")
        pausar()
        return
    total    = len(despensa)
    criticos = sum(1 for i in despensa if i["quantidade"] <= i["minimo"])
    cheios   = sum(1 for i in despensa if i["quantidade"] >= i["quantidade_ideal"])
    baixos   = sum(1 for i in despensa if i["minimo"] < i["quantidade"] < i["quantidade_ideal"] * 0.5)
    ok       = total - criticos - cheios - baixos
    print(f"  📦 Total de produtos:    {total}")
    print(f"  ✅ Nível ideal (cheios): {cheios}")
    print(f"  🟢 Nível OK:             {ok}")
    print(f"  🟡 Nível baixo:          {baixos}")
    print(f"  🔴 Nível crítico:        {criticos}")
    percentagem_saude = round(((cheios + ok) / total) * 100, 1) if total > 0 else 0
    print(f"\n  💪 Saúde da despensa: {percentagem_saude}%")
    if percentagem_saude >= 80:
        print("     Excelente! A despensa está bem abastecida. 🎉")
    elif percentagem_saude >= 50:
        print("     Razoável. Há alguns produtos a repor.")
    else:
        print("     Atenção! A despensa precisa de reposição urgente.")
    pausar()


def ver_historico():
    cabecalho("  📜  HISTÓRICO DE AÇÕES")
    print()
    if not historico:
        print("  Sem histórico de ações.")
    else:
        for entrada in historico[-15:]:
            print(f"  {entrada}")
        if len(historico) > 15:
            print(f"\n  ... e mais {len(historico) - 15} ações anteriores.")
    pausar()


# ──────────────────────────────────────────────────────────────
# MENUS INTERATIVOS
# ──────────────────────────────────────────────────────────────


def menu_despensa():
    while True:
        limpar_ecra()
        cabecalho("  📦  GESTÃO DA DESPENSA")
        print()
        print("  1. ➕  Adicionar produto")
        print("  2. ✏️   Editar produto")
        print("  3. 📝  Atualizar quantidade")
        print("  4. 📋  Ver inventário")
        print("  5. 🗑️   Remover produto")
        print("  0. ⬅️   Voltar")
        print()
        opcao = input("  Escolhe uma opção: ").strip()
        if opcao == "1":
            adicionar_item()
        elif opcao == "2":
            editar_produto()
        elif opcao == "3":
            atualizar_quantidade()
        elif opcao == "4":
            listar_despensa()
        elif opcao == "5":
            remover_item()
        elif opcao == "0":
            break
        else:
            print("  ⚠  Opção inválida.")
            pausar()


def menu_compras():
    while True:
        limpar_ecra()
        cabecalho("  🛒  LISTA DE COMPRAS")
        print()
        print("  1. 🔄  Gerar lista automática")
        print("  2. ✏️   Adicionar item manualmente")
        print("  3. 📋  Ver lista de compras")
        print("  4. 🔧   Editar item da lista")
        print("  5. 🗑️   Remover item da lista")
        print("  6. ✅  Registar compras efetuadas")
        print("  0. ⬅️   Voltar")
        print()
        opcao = input("  Escolhe uma opção: ").strip()
        if opcao == "1":
            gerar_lista_compras()
        elif opcao == "2":
            adicionar_item_lista()
        elif opcao == "3":
            ver_lista_compras()
        elif opcao == "4":
            editar_item_lista()
        elif opcao == "5":
            remover_item_lista()
        elif opcao == "6":
            ver_e_marcar_compras()
        elif opcao == "0":
            break
        else:
            print("  ⚠  Opção inválida.")
            pausar()


def menu_principal():
    limpar_ecra()
    print("\n  🔄  A carregar dados...")
    dados_carregados = carregar_dados()
    carregar_lista()
    if not dados_carregados:
        print("  📄  Nenhum ficheiro encontrado. A iniciar com despensa vazia.")
    else:
        print(f"  ✅  {len(despensa)} produto(s) carregados do ficheiro.")
    pausar()
    while True:
        limpar_ecra()
        print()
        print("╔══════════════════════════════════════════════════════╗")
        print("║         🏠  SISTEMA DE GESTÃO DE DESPENSA            ║")
        print("╚══════════════════════════════════════════════════════╝")
        if despensa:
            na_despensa = sum(1 for i in despensa if i["quantidade"] > 0)
            criticos = sum(1 for i in despensa if i["quantidade"] <= i["minimo"])
            print(f"  📦 {len(despensa)} produto(s) cadastrado(s)  |  🏠 {na_despensa} na despensa", end="")
            if criticos:
                print(f"  |  🔴 {criticos} em nível crítico", end="")
            print()
        print()
        print("  1. 📦  Gestão da Despensa")
        print("  2. 🛒  Lista de Compras")
        print("  3. 📊  Relatório")
        print("  4. 📜  Histórico")
        print()
        print("  0. 🚪  Sair")
        print()
        opcao = input("  Escolhe uma opção: ").strip()
        if opcao == "1":
            menu_despensa()
        elif opcao == "2":
            menu_compras()
        elif opcao == "3":
            ver_relatorio()
        elif opcao == "4":
            ver_historico()
        elif opcao == "0":
            limpar_ecra()
            print()
            print("  👋  Obrigada por usar o Sistema de Gestão de Despensa!")
            print("      Até à próxima! 🏠")
            print()
            break
        else:
            print("  ⚠  Opção inválida. Tenta novamente.")
            pausar()


# ──────────────────────────────────────────────────────────────
# PONTO DE ENTRADA
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    menu_principal()