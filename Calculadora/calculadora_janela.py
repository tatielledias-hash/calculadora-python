import customtkinter as ctk
import ast
import operator as op
import re


# Começa no tema claro
ctk.set_appearance_mode("light")

janela = ctk.CTk()
janela.title("✿ CALCULADORA ✿")
janela.geometry("370x590")
janela.resizable(False, False)

# Cada tupla contém a cor do tema claro e a do tema escuro
COR_FUNDO = ("#F8F0F6", "#211A25")
COR_TEXTO = ("#74436F", "#F4E8F2")
COR_VISOR = ("#FFF9FD", "#302635")
COR_BORDA_VISOR = ("#EBD9E8", "#47384A")
COR_BOTAO = ("#FFF9FD", "#382D3D")
COR_BORDA_BOTAO = ("#EBD9E8", "#514257")
COR_BOTAO_HOVER = ("#F4E5F0", "#493A50")
COR_ROSA = ("#F3D5E3", "#543849")
COR_ROSA_HOVER = ("#EBC2D5", "#68445B")
COR_LILAS = ("#DDBCE5", "#5B4265")
COR_LILAS_HOVER = ("#CFA5DB", "#70517D")
COR_DESTAQUE = ("#A94F9E", "#B975C3")
COR_DESTAQUE_HOVER = ("#93418A", "#CA8BD3")

janela.configure(fg_color=COR_FUNDO)


# Título e botão para trocar o tema
cabecalho = ctk.CTkFrame(janela, fg_color="transparent")
cabecalho.pack(fill="x", padx=20, pady=(16, 8))
cabecalho.grid_columnconfigure(0, weight=1)

titulo = ctk.CTkLabel(
    cabecalho,
    text="✿ CALCULADORA ✿",
    font=("Segoe UI", 18, "bold"),
    text_color=COR_TEXTO,
)
titulo.grid(row=0, column=0, sticky="w")

modo_atual = "light"


def alternar_tema():
    global modo_atual

    if modo_atual == "light":
        modo_atual = "dark"
        botao_tema.configure(text="☀")
    else:
        modo_atual = "light"
        botao_tema.configure(text="☾")

    ctk.set_appearance_mode(modo_atual)


botao_tema = ctk.CTkButton(
    cabecalho,
    text="☾",
    width=40,
    height=36,
    corner_radius=14,
    font=("Segoe UI", 18),
    fg_color=COR_ROSA,
    hover_color=COR_ROSA_HOVER,
    text_color=COR_TEXTO,
    command=alternar_tema,
)
botao_tema.grid(row=0, column=1, padx=(8, 0))


# Visor da calculadora
visor = ctk.CTkLabel(
    janela,
    text="0",
    height=92,
    corner_radius=22,
    font=("Segoe UI", 34),
    anchor="e",
    padx=18,
    fg_color=COR_VISOR,
    text_color=COR_TEXTO,
    border_width=2,
    border_color=COR_BORDA_VISOR,
)
visor.pack(fill="x", padx=20, pady=(8, 14))


def avaliar_expressao(expressao):
    operadores = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv,
    }

    def calcular(no):
        if isinstance(no, ast.Constant) and type(no.value) in (int, float):
            return no.value

        if isinstance(no, ast.BinOp) and type(no.op) in operadores:
            esquerda = calcular(no.left)
            direita = calcular(no.right)

            if isinstance(no.op, ast.Div) and direita == 0:
                raise ZeroDivisionError

            return operadores[type(no.op)](esquerda, direita)

        if isinstance(no, ast.UnaryOp) and isinstance(no.op, (ast.UAdd, ast.USub)):
            valor = calcular(no.operand)

            if isinstance(no.op, ast.USub):
                return -valor

            return valor

        raise ValueError

    arvore = ast.parse(expressao, mode="eval")
    return calcular(arvore.body)


expressao_atual = ""
resultado_mostrado = False


def atualizar_visor():
    if expressao_atual:
        visor.configure(text=expressao_atual)
    else:
        visor.configure(text="0")


def digitar_numero(valor):
    global expressao_atual, resultado_mostrado

    if valor == "C":
        expressao_atual = ""
        resultado_mostrado = False
        atualizar_visor()
        return

    if valor == "<":
        if visor.cget("text") == "Erro":
            expressao_atual = ""
        else:
            expressao_atual = expressao_atual[:-1]

        resultado_mostrado = False
        atualizar_visor()
        return

    if valor == "=":
        if not expressao_atual:
            return

        try:
            resultado = avaliar_expressao(expressao_atual)

            if isinstance(resultado, float) and resultado.is_integer():
                resultado = int(resultado)

            expressao_atual = str(resultado)
            visor.configure(text=expressao_atual)
        except (SyntaxError, ZeroDivisionError, ValueError, TypeError):
            expressao_atual = ""
            visor.configure(text="Erro")

        resultado_mostrado = True
        return

    if visor.cget("text") == "Erro":
        if valor.isdigit() or valor in ["(", "."]:
            expressao_atual = ""
            resultado_mostrado = False
        else:
            return

    if valor.isdigit():
        if resultado_mostrado:
            expressao_atual = ""
            resultado_mostrado = False

        if expressao_atual.endswith(")"):
            expressao_atual += "*"

        expressao_atual += valor
        atualizar_visor()
        return

    if valor == ".":
        if resultado_mostrado:
            expressao_atual = ""
            resultado_mostrado = False

        if expressao_atual.endswith(")"):
            return

        parte_atual = re.split(r"[+\-*/()]", expressao_atual)[-1]

        if "." not in parte_atual:
            if not expressao_atual or expressao_atual.endswith(("+", "-", "*", "/", "(")):
                expressao_atual += "0."
            else:
                expressao_atual += "."

        atualizar_visor()
        return

    if valor == "(":
        if resultado_mostrado:
            expressao_atual = ""
            resultado_mostrado = False

        if expressao_atual.endswith(")") or expressao_atual[-1:].isdigit():
            expressao_atual += "*"

        expressao_atual += "("
        atualizar_visor()
        return

    if valor == ")":
        if expressao_atual.endswith(")") or expressao_atual[-1:].isdigit():
            expressao_atual += ")"

        atualizar_visor()
        return

    if valor in ["+", "-", "*", "/"]:
        if not expressao_atual and valor != "-":
            return

        resultado_mostrado = False
        expressao_atual += valor
        atualizar_visor()

def tratar_tecla(evento):
    teclas_especiais = {
        "Return": "=",
        "KP_Enter": "=",
        "BackSpace": "<",
        "Delete": "<",
        "Escape": "C",
        "KP_Add": "+",
        "KP_Subtract": "-",
        "KP_Multiply": "*",
        "KP_Divide": "/",
        "KP_Decimal": ".",
    }

    if evento.keysym in teclas_especiais:
        valor = teclas_especiais[evento.keysym]
    elif evento.char == ",":
        valor = "."
    elif evento.char and evento.char in "0123456789+-*/().":
        valor = evento.char
    else:
        return

    digitar_numero(valor)
    return "break"


janela.bind_all("<Key>", tratar_tecla)

# Texto visível e valor enviado para a calculadora
botoes = [
    [("C", "C"), ("(", "("), (")", ")"), ("⌫", "<")],
    [("7", "7"), ("8", "8"), ("9", "9"), ("÷", "/")],
    [("4", "4"), ("5", "5"), ("6", "6"), ("×", "*")],
    [("1", "1"), ("2", "2"), ("3", "3"), ("−", "-")],
    [(".", "."), ("0", "0"), ("=", "="), ("+", "+")],
]

quadro = ctk.CTkFrame(janela, fg_color="transparent")
quadro.pack(expand=True, fill="both", padx=16, pady=(0, 8))

for linha, botoes_da_linha in enumerate(botoes):
    for coluna, (texto, valor) in enumerate(botoes_da_linha):
        if valor == "=":
            cor = COR_DESTAQUE
            cor_hover = COR_DESTAQUE_HOVER
            cor_texto = ("#FFFFFF", "#FFFFFF")
        elif valor in ["+", "-", "*", "/"]:
            cor = COR_LILAS
            cor_hover = COR_LILAS_HOVER
            cor_texto = ("#FFFFFF", "#FFFFFF")
        elif valor in ["C", "<"]:
            cor = COR_ROSA
            cor_hover = COR_ROSA_HOVER
            cor_texto = COR_TEXTO
        else:
            cor = COR_BOTAO
            cor_hover = COR_BOTAO_HOVER
            cor_texto = COR_TEXTO

        botao = ctk.CTkButton(
            quadro,
            text=texto,
            height=62,
            corner_radius=18,
            font=("Segoe UI", 21, "bold"),
            fg_color=cor,
            hover_color=cor_hover,
            text_color=cor_texto,
            border_width=1,
            border_color=COR_BORDA_BOTAO,
            command=lambda valor=valor: digitar_numero(valor),
        )
        botao.grid(
            row=linha,
            column=coluna,
            sticky="nsew",
            padx=4,
            pady=4,
        )

for linha in range(5):
    quadro.rowconfigure(linha, weight=1)

for coluna in range(4):
    quadro.columnconfigure(coluna, weight=1)


rodape = ctk.CTkLabel(
    janela,
    text="♡ FEITO COM CARINHO POR TATI ♡",
    font=("Segoe UI", 10),
    text_color=COR_TEXTO,
)
rodape.pack(pady=(0, 12))


janela.mainloop()