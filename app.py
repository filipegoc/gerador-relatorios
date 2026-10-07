import base64
from io import BytesIO
from math import ceil
from textwrap import fill

import matplotlib.colors as mcolors
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import streamlit as st

# Cole o conteúdo Base64 das imagens entre as aspas triplas.
# O aplicativo funciona normalmente se as constantes ficarem vazias.
LOGO_PREFEITURA_BASE64 = """
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
"""

LOGO_HOSPITAL_BASE64 = """
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
"""

A4_LANDSCAPE = (11.69, 8.27)
EXPORT_DPI = 300
COR_PADRAO = "#87CEEB"
ESPESSURA_BARRA = 0.45
FATOR_DETECCAO_OUTLIER = 2
FATOR_LIMITE_OUTLIER = 1.5

st.set_page_config(
    page_title="Criador de gráficos",
    page_icon="📊",
    layout="wide",
)


def carregar_imagem_base64(conteudo: str, nome: str = "imagem"):
    if not conteudo:
        st.warning(f"O Base64 de {nome} está vazio.")
        return None

    try:
        conteudo = conteudo.strip()

        # Remove prefixos como:
        # data:image/jpeg;base64,
        # data:image/jpg;base64,
        # data:image/png;base64,
        if conteudo.startswith("data:"):
            conteudo = conteudo.split(",", 1)[1]

        # Remove espaços, tabulações e quebras de linha
        conteudo = "".join(conteudo.split())

        # Corrige o padding do Base64, caso esteja faltando
        padding_necessario = len(conteudo) % 4
        if padding_necessario:
            conteudo += "=" * (4 - padding_necessario)

        dados_imagem = base64.b64decode(conteudo)

        if not dados_imagem:
            raise ValueError(
                "O Base64 foi decodificado, mas não gerou dados."
            )

        # Como os arquivos originais são JPG,
        # informa explicitamente o formato ao Matplotlib
        return mpimg.imread(
            BytesIO(dados_imagem),
            format="jpg",
        )

    except Exception as erro:
        st.error(f"Não foi possível carregar {nome}: {erro}")
        return None
    

def formatar_numero(valor: int) -> str:
    return f"{valor:,}".replace(",", ".")


def marcar_quebra(ax, barra, orientacao: str) -> None:
    if orientacao == "vertical":
        x = barra.get_x()
        largura = barra.get_width()
        y = barra.get_height()
        for fracao in (0.82, 0.90):
            ax.plot(
                [x + largura * 0.2, x + largura * 0.8],
                [y * fracao, y * fracao + y * 0.04],
                color="white", linewidth=2.5, solid_capstyle="butt", zorder=5,
            )
    else:
        x = barra.get_width()
        y = barra.get_y()
        altura = barra.get_height()
        for fracao in (0.82, 0.90):
            ax.plot(
                [x * fracao, x * fracao + x * 0.04],
                [y + altura * 0.2, y + altura * 0.8],
                color="white", linewidth=2.5, solid_capstyle="butt", zorder=5,
            )


def adicionar_logo_base64(
    fig: Figure,
    imagem,
    posicao: tuple[float, float],
    largura: float,
) -> Axes | None:
    if imagem is None:
        return None
    altura = largura * imagem.shape[0] / imagem.shape[1]
    caixa = fig.add_axes(
        [posicao[0] - largura / 2, posicao[1] - altura / 2, largura, altura],
        zorder=10,
    )
    caixa.imshow(imagem, aspect="auto")
    caixa.set_axis_off()
    return caixa


def configurar_titulo_geral(fig: Figure, titulo: str, logos: list[Axes]) -> float:
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    limite_esquerdo = 0.06
    limite_direito = 0.94

    for logo in logos:
        caixa = logo.get_position()
        centro = (caixa.x0 + caixa.x1) / 2
        if centro < 0.5:
            limite_esquerdo = max(limite_esquerdo, caixa.x1)
        else:
            limite_direito = min(limite_direito, caixa.x0)

    limite_esquerdo += 0.025
    limite_direito -= 0.025
    largura_disponivel = max(limite_direito - limite_esquerdo, 0.05)
    texto = fig.text(
        (limite_esquerdo + limite_direito) / 2, 0.97, titulo,
        fontsize=12, fontweight="bold", ha="center", va="top",
    )

    def largura_em_figura(conteudo: str) -> float:
        largura = renderer.get_text_width_height_descent(
            conteudo, texto.get_fontproperties(), ismath=False
        )[0]
        return largura / fig.bbox.width

    def quebrar_linha(conteudo: str) -> str:
        linhas, linha = [], ""
        for palavra in conteudo.split():
            candidata = f"{linha} {palavra}".strip()
            if largura_em_figura(candidata) <= largura_disponivel:
                linha = candidata
                continue
            if linha:
                linhas.append(linha)
                linha = ""
            for caractere in palavra:
                candidata = linha + caractere
                if linha and largura_em_figura(candidata) > largura_disponivel:
                    linhas.append(linha)
                    linha = caractere
                else:
                    linha = candidata
        if linha:
            linhas.append(linha)
        return "\n".join(linhas)

    def titulo_cabe() -> bool:
        fig.canvas.draw()
        caixa = texto.get_window_extent(renderer).transformed(fig.transFigure.inverted())
        return caixa.x0 >= limite_esquerdo and caixa.x1 <= limite_direito

    for tamanho in range(12, 7, -1):
        texto.set_fontsize(tamanho)
        texto.set_text(quebrar_linha(titulo))
        if titulo_cabe():
            break

    fig.canvas.draw()
    caixa = texto.get_window_extent(renderer).transformed(fig.transFigure.inverted())
    return caixa.y0


def gerar_figura(dados: dict) -> Figure:
    graficos = dados["graficos"]
    total = len(graficos)
    colunas = min(total, 3)
    linhas = ceil(total / colunas)
    fig, eixos = plt.subplots(
        nrows=linhas, ncols=colunas, figsize=A4_LANDSCAPE, squeeze=False
    )

    img_prefeitura = carregar_imagem_base64(
        LOGO_PREFEITURA_BASE64,
        "logo da prefeitura",
    )

    img_hospital = carregar_imagem_base64(
        LOGO_HOSPITAL_BASE64,
        "logo do hospital",
    )
    logos = [
        logo for logo in (
            adicionar_logo_base64(fig, img_prefeitura, (0.12, 0.92), 0.17),
            adicionar_logo_base64(fig, img_hospital, (0.88, 0.92), 0.11),
        ) if logo is not None
    ]
    margem_titulo = configurar_titulo_geral(fig, dados["titulo_geral"], logos)
    orientacao = dados["orientacao_barras"].lower()
    cor = dados["cor_barras"]
    legenda_angulada = dados.get("legenda_categorias", "Angulada") == "Angulada"

    for indice_grafico, info in enumerate(graficos):
        ax = eixos.flat[indice_grafico]
        categorias = info["categorias"]
        ordenados = sorted(
            categorias, key=lambda item: item["valor"],
            reverse=orientacao == "vertical",
        )
        indice_outlier = None
        limite_outlier = None
        positivos = sorted((item["valor"] for item in categorias if item["valor"] > 0), reverse=True)
        if len(positivos) >= 2:
            maior, segundo = positivos[:2]
            if maior > segundo * FATOR_DETECCAO_OUTLIER:
                indice_outlier = next(i for i, item in enumerate(ordenados) if item["valor"] == maior)
                limite_outlier = segundo * FATOR_LIMITE_OUTLIER

        valores_plot = [
            min(item["valor"], limite_outlier) if limite_outlier is not None else item["valor"]
            for item in ordenados
        ]
        limite_eixo = max(max(valores_plot, default=0) * 1.5, 1)

        if orientacao == "horizontal":
            barras = ax.barh(
                [item["nome"] for item in ordenados], valores_plot,
                height=ESPESSURA_BARRA, color=cor, edgecolor="#5DADE2", alpha=0.9,
            )
            ax.set_ylim(-0.8, len(ordenados) - 0.2)
            ax.set_xlim(right=limite_eixo)
            for indice, (barra, item) in enumerate(zip(barras, ordenados)):
                ax.text(
                    barra.get_width() + limite_eixo * 0.015,
                    barra.get_y() + barra.get_height() / 2,
                    formatar_numero(item["valor"]), ha="left", va="center",
                    fontsize=10, fontweight="bold", color="#2E4053",
                )
                if indice == indice_outlier:
                    marcar_quebra(ax, barra, orientacao)
            ax.grid(axis="x", linestyle="--", alpha=0.3)
            ax.tick_params(axis="y", labelsize=9)
        else:
            nomes = [
                item["nome"] if legenda_angulada else fill(
                    item["nome"], width=max(16, min(24, 48 // len(ordenados))),
                    break_long_words=False, break_on_hyphens=False,
                ) for item in ordenados
            ]
            barras = ax.bar(
                nomes, valores_plot, width=ESPESSURA_BARRA,
                color=cor, edgecolor="#5DADE2", alpha=0.9,
            )
            ax.set_xlim(-0.8, len(ordenados) - 0.2)
            ax.set_ylim(top=limite_eixo)
            for indice, (barra, item) in enumerate(zip(barras, ordenados)):
                ax.text(
                    barra.get_x() + barra.get_width() / 2,
                    barra.get_height() + limite_eixo * 0.015,
                    formatar_numero(item["valor"]), ha="center", va="bottom",
                    fontsize=10, fontweight="bold", color="#2E4053",
                )
                if indice == indice_outlier:
                    marcar_quebra(ax, barra, orientacao)
            ax.grid(axis="y", linestyle="--", alpha=0.3)
            ax.tick_params(
                axis="x", labelsize=8,
                rotation=40 if legenda_angulada else 0,
                pad=8 if legenda_angulada else 6,
            )
            if legenda_angulada:
                for rotulo in ax.get_xticklabels():
                    rotulo.set_ha("right")
                    rotulo.set_rotation_mode("anchor")

        titulo = fill(
            info["titulo"], width=max(24, 48 // colunas),
            break_long_words=True, break_on_hyphens=False,
        )
        ax.set_title(titulo, fontsize=12, fontweight="bold", pad=10)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    for indice in range(total, linhas * colunas):
        eixos.flat[indice].set_visible(False)

    fig.subplots_adjust(
        top=0.72, bottom=0.22,
        left=0.24 if orientacao == "horizontal" else 0.08,
        right=0.96, wspace=0.45, hspace=0.8,
    )
    fig.subplots_adjust(top=max(0.55, min(0.72, margem_titulo - 0.08)))
    return fig


def novo_grafico(titulo="Novo gráfico", nome="", valor=0) -> dict:
    return {"titulo": titulo, "categorias": [{"nome": nome, "valor": valor}]}


def inicializar_estado() -> None:
    if "graficos" not in st.session_state:
        st.session_state.graficos = [
            novo_grafico("Centro Cirúrgico", "Cirurgias Realizadas", 134)
        ]
    if "figura_png" not in st.session_state:
        st.session_state.figura_png = None


def adicionar_grafico() -> None:
    st.session_state.graficos.append(
        novo_grafico(f"Gráfico {len(st.session_state.graficos) + 1}")
    )
    st.session_state.figura_png = None


def remover_grafico(indice: int) -> None:
    if len(st.session_state.graficos) > 1:
        st.session_state.graficos.pop(indice)
        st.session_state.figura_png = None


def adicionar_categoria(indice: int) -> None:
    st.session_state.graficos[indice]["categorias"].append({"nome": "", "valor": 0})
    st.session_state.figura_png = None


def remover_categoria(indice_grafico: int, indice_categoria: int) -> None:
    categorias = st.session_state.graficos[indice_grafico]["categorias"]
    if len(categorias) > 1:
        categorias.pop(indice_categoria)
        st.session_state.figura_png = None


def validar_dados(titulo: str, cor: str) -> None:
    if not titulo.strip():
        raise ValueError("Informe o título do relatório.")
    if not mcolors.is_color_like(cor):
        raise ValueError("Escolha uma cor válida para as barras.")
    for ig, grafico in enumerate(st.session_state.graficos, 1):
        if not grafico["titulo"].strip():
            raise ValueError(f"Informe o nome do gráfico {ig}.")
        for ic, categoria in enumerate(grafico["categorias"], 1):
            if not categoria["nome"].strip():
                raise ValueError(f"Informe o nome da categoria {ic} do gráfico {ig}.")
            if categoria["valor"] < 0:
                raise ValueError(f"O valor da categoria {ic} não pode ser negativo.")


inicializar_estado()
st.title("📊 Criador de gráficos")
st.caption("Configure o relatório, visualize o resultado e baixe a imagem em PNG.")

col_formulario, col_previa = st.columns([0.42, 0.58], gap="large")

with col_formulario:
    st.subheader("Configure seu relatório")
    titulo_geral = st.text_input(
        "Título do relatório", "RELATÓRIO GERAL DE PRODUÇÃO 05/2026"
    )
    coluna_1, coluna_2 = st.columns(2)
    orientacao = coluna_1.selectbox("Orientação das barras", ["Vertical", "Horizontal"])
    legenda = coluna_2.selectbox("Legenda das categorias", ["Angulada", "Reta"])
    cor = st.color_picker("Cor das barras", COR_PADRAO)

    st.markdown("### Gráficos e categorias")
    for ig, grafico in enumerate(st.session_state.graficos):
        with st.container(border=True):
            cabecalho, botao_remover = st.columns([0.82, 0.18])
            cabecalho.markdown(f"**Gráfico {ig + 1}**")
            botao_remover.button(
                "Remover", key=f"remover_grafico_{ig}",
                disabled=len(st.session_state.graficos) == 1,
                on_click=remover_grafico, args=(ig,), use_container_width=True,
            )
            grafico["titulo"] = st.text_input(
                "Nome do gráfico", value=grafico["titulo"], key=f"titulo_grafico_{ig}"
            )
            st.caption("Categorias")
            for ic, categoria in enumerate(grafico["categorias"]):
                coluna_nome, coluna_valor, coluna_excluir = st.columns([0.60, 0.25, 0.15])
                categoria["nome"] = coluna_nome.text_input(
                    "Categoria", value=categoria["nome"], key=f"nome_{ig}_{ic}",
                    label_visibility="collapsed", placeholder="Nome da categoria",
                )
                categoria["valor"] = coluna_valor.number_input(
                    "Valor", min_value=0, step=1, value=int(categoria["valor"]),
                    key=f"valor_{ig}_{ic}", label_visibility="collapsed",
                )
                coluna_excluir.button(
                    "×", key=f"remover_categoria_{ig}_{ic}",
                    disabled=len(grafico["categorias"]) == 1,
                    on_click=remover_categoria, args=(ig, ic), use_container_width=True,
                )
            st.button(
                "+ Adicionar categoria", key=f"adicionar_categoria_{ig}",
                on_click=adicionar_categoria, args=(ig,), use_container_width=True,
            )

    st.button("+ Adicionar gráfico", on_click=adicionar_grafico, use_container_width=True)
    gerar = st.button("Gerar gráfico", type="primary", use_container_width=True)

with col_previa:
    st.subheader("Prévia do relatório")
    if gerar:
        try:
            validar_dados(titulo_geral, cor)
            dados = {
                "titulo_geral": titulo_geral.strip(),
                "orientacao_barras": orientacao.lower(),
                "legenda_categorias": legenda,
                "cor_barras": cor,
                "graficos": st.session_state.graficos,
            }
            figura = gerar_figura(dados)
            arquivo = BytesIO()
            figura.savefig(arquivo, format="png", dpi=EXPORT_DPI, bbox_inches="tight")
            arquivo.seek(0)
            st.session_state.figura_png = arquivo.getvalue()
            plt.close(figura)
        except ValueError as erro:
            st.error(str(erro))
        except Exception as erro:
            st.exception(erro)

    if st.session_state.figura_png:
        st.image(st.session_state.figura_png, use_container_width=True)
        st.download_button(
            "Baixar imagem PNG",
            data=st.session_state.figura_png,
            file_name="Relatorio_Dinamico_A4.png",
            mime="image/png",
            type="primary",
            use_container_width=True,
        )
    else:
        st.info("Preencha os campos e clique em **Gerar gráfico**.")
