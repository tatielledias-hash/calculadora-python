import ast
import operator as op
import re

import streamlit as st
import streamlit_hotkeys as hotkeys


st.set_page_config(
    page_title="✿ CALCULADORA ✿",
    page_icon="✿",
    layout="centered",
)

hotkeys.activate(
    [
        *[hotkeys.hk(f"digito_{numero}", str(numero)) for numero in range(10)],
        hotkeys.hk("somar", "+"),
        hotkeys.hk("subtrair", "-"),
        hotkeys.hk("multiplicar", "*"),
        hotkeys.hk("dividir", "/"),
        hotkeys.hk("decimal_ponto", "."),
        hotkeys.hk("decimal_virgula", ","),
        hotkeys.hk("abrir_parentese", "("),
        hotkeys.hk("fechar_parentese", ")"),
        hotkeys.hk("calcular", "Enter", prevent_default=True),
        hotkeys.hk("apagar", "Backspace", prevent_default=True),
        hotkeys.hk("limpar", "Escape", prevent_default=True),
    ]
)


if "expressao" not in st.session_state:
    st.session_state.expressao = ""

if "erro" not in st.session_state:
    st.session_state.erro = False

if "resultado_mostrado" not in st.session_state:
    st.session_state.resultado_mostrado = False

if "tema_escuro" not in st.session_state:
    st.session_state.tema_escuro = False


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


def formatar_resultado(resultado):
    if isinstance(resultado, float) and resultado.is_integer():
        resultado = int(resultado)

    return str(resultado)


def alternar_tema():
    st.session_state.tema_escuro = not st.session_state.tema_escuro


def mostrar_resultado():
    expressao = st.session_state.expressao

    if not expressao:
        return

    try:
        resultado = avaliar_expressao(expressao)
        st.session_state.expressao = formatar_resultado(resultado)
        st.session_state.erro = False
        st.session_state.resultado_mostrado = True
    except (SyntaxError, ZeroDivisionError, ValueError, TypeError):
        st.session_state.erro = True



def apertar_botao(valor):
    expressao = st.session_state.expressao

    if valor == "C":
        st.session_state.expressao = ""
        st.session_state.erro = False
        st.session_state.resultado_mostrado = False
        return

    if valor == "⌫":
        if st.session_state.erro:
            st.session_state.expressao = ""
            st.session_state.erro = False
        else:
            st.session_state.expressao = expressao[:-1]

        st.session_state.resultado_mostrado = False
        return

    if valor == "=":
        mostrar_resultado()
        return

    if st.session_state.erro:
        expressao = ""
        st.session_state.expressao = ""
        st.session_state.erro = False

    if st.session_state.resultado_mostrado:
        if valor.isdigit() or valor in [".", "("]:
            expressao = ""
            st.session_state.expressao = ""
        st.session_state.resultado_mostrado = False

    if valor.isdigit():
        if expressao.endswith(")"):
            expressao += "*"

        st.session_state.expressao = expressao + valor
        return

    if valor == ".":
        parte_atual = re.split(r"[+\-*/()]", expressao)[-1]

        if "." not in parte_atual:
            if not expressao or expressao.endswith(("+", "-", "*", "/", "(")):
                expressao += "0."
            else:
                expressao += "."

        st.session_state.expressao = expressao
        return

    if valor == "(":
        if expressao.endswith(")") or expressao[-1:].isdigit():
            expressao += "*"

        st.session_state.expressao = expressao + "("
        return

    if valor == ")":
        if (
            expressao.count("(") > expressao.count(")")
            and (expressao.endswith(")") or expressao[-1:].isdigit())
        ):
            st.session_state.expressao = expressao + ")"

        return

    if valor in ["+", "-", "*", "/"]:
        if not expressao:
            if valor == "-":
                st.session_state.expressao = "-"
            return

        if expressao.endswith(("+", "-", "*", "/")):
            expressao = expressao[:-1]

        st.session_state.expressao = expressao + valor


atalhos_calculadora = {
    **{f"digito_{numero}": str(numero) for numero in range(10)},
    "somar": "+",
    "subtrair": "-",
    "multiplicar": "*",
    "dividir": "/",
    "decimal_ponto": ".",
    "decimal_virgula": ".",
    "abrir_parentese": "(",
    "fechar_parentese": ")",
    "calcular": "=",
    "apagar": "⌫",
    "limpar": "C",
}

for atalho, valor in atalhos_calculadora.items():
    if hotkeys.pressed(atalho):
        apertar_botao(valor)


if st.session_state.tema_escuro:
    fundo = "#211A25"
    texto = "#F4E8F2"
    visor_fundo = "#302635"
    botao_fundo = "#382D3D"
    borda = "#514257"
    destaque = "#B975C3"
else:
    fundo = "#F8F0F6"
    texto = "#74436F"
    visor_fundo = "#FFF9FD"
    botao_fundo = "#FFF9FD"
    borda = "#EBD9E8"
    destaque = "#A94F9E"


st.markdown(
    f"""
    <style>
    [data-testid="stMainBlockContainer"] {{
        max-width: 480px;
        padding: 1.5rem 1.25rem 2rem;
        transform: translateY(15vh);
        border: 2px solid {borda};
        border-radius: 28px;
        background-color: {fundo};
        box-shadow: 0 10px 28px rgba(116, 67, 111, 0.14);
    }}

    .stApp {{
        background-color: {fundo};
        color: {texto};
    }}

    h1, p, label {{
        color: {texto} !important;
    }}

    h1 {{
        margin: 0 !important;
        font-size: 1.65rem !important;
        text-align: center;
        white-space: nowrap;
    }}

    .st-key-theme_switch button {{
        width: 44px !important;
        height: 44px !important;
        padding: 0 !important;
        border-radius: 50% !important;
        font-size: 25px !important;
    }}

    div.stButton > button {{
        width: 100%;
        height: 72px;
        border-radius: 20px;
        border: 1px solid {borda};
        background-color: {botao_fundo};
        color: {texto};
        font-size: 24px;
        font-weight: bold;
    }}

    div.stButton > button:hover {{
        border-color: {destaque};
        color: {destaque};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

coluna_titulo, coluna_tema = st.columns([5, 1], vertical_alignment="center")

with coluna_titulo:
    st.markdown('<h1>✿ CALCULADORA ✿</h1>', unsafe_allow_html=True)

with coluna_tema:
    st.button(
        "☼" if st.session_state.tema_escuro else "☾",
        key="theme_switch",
        on_click=alternar_tema,
        help="Alternar tema claro/escuro",
    )

texto_visor = "Erro" if st.session_state.erro else (st.session_state.expressao or "0")
st.markdown(
    f"""
    <div style="
        min-height: 52px;
        padding: 20px 18px;
        margin: 8px 0 18px;
        border: 2px solid {borda};
        border-radius: 22px;
        background: {visor_fundo};
        color: {texto};
        text-align: right;
        font-size: 36px;
        overflow-wrap: anywhere;
    ">{texto_visor}</div>
    """,
    unsafe_allow_html=True,
)

botoes = [
    ["C", "(", ")", "⌫"],
    ["7", "8", "9", "÷"],
    ["4", "5", "6", "×"],
    ["1", "2", "3", "−"],
    [".", "0", "=", "+"],
]

valores = {
    "÷": "/",
    "×": "*",
    "−": "-",
}

for numero_linha, linha in enumerate(botoes):
    colunas = st.columns(4)

    for numero_coluna, rotulo in enumerate(linha):
        valor = valores.get(rotulo, rotulo)

        colunas[numero_coluna].button(
            rotulo,
            key=f"botao_{numero_linha}_{numero_coluna}",
            on_click=apertar_botao,
            args=(valor,),
            use_container_width=True,
        )

st.caption("♡ Feito com carinho por Tati ♡")
