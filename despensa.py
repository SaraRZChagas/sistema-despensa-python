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

