import streamlit as st

st.set_page_config(
    page_title="Urea vs Nitroperfecto",
    page_icon="🌱",
    layout="centered"
)


from pathlib import Path
from io import BytesIO
import base64
from datetime import datetime
import streamlit as st

AZUL = "#06162E"
NARANJA = "#F39A08"
VERDE = "#5BAA1F"

def dinero(valor):
    return f"${valor:,.2f}"

def numero(valor):
    return f"{valor:,.2f}"

def calc_equivalencia(kg_base, precio_base, precio_nitro, n_base, n_nitro):
    if min(kg_base, precio_base, precio_nitro, n_base, n_nitro) <= 0:
        raise ValueError("Todos los valores deben ser mayores a cero.")

    kg_nitro = (kg_base * (n_base / 100)) / (n_nitro / 100)
    costo_base = kg_base * precio_base / 1000
    costo_nitro = kg_nitro * precio_nitro / 1000
    diferencia = costo_nitro - costo_base
    return kg_nitro, costo_base, costo_nitro, diferencia

def asset_as_data_uri(relative_path):
    path = Path(__file__).parent / relative_path
    if not path.exists():
        return ""
    suffix = path.suffix.lower()
    mime = "image/svg+xml" if suffix == ".svg" else "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{encoded}"

def logo_data_uri():
    official = Path(__file__).parent / "assets" / "isaosa.png"
    fallback = Path(__file__).parent / "assets" / "isaosa_logo.svg"
    if official.exists():
        return asset_as_data_uri("assets/isaosa.png")
    if fallback.exists():
        return asset_as_data_uri("assets/isaosa_logo.svg")
    return ""

def inject_css():
    st.markdown("""
<style>
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(243,154,8,.10), transparent 31%),
            radial-gradient(circle at top right, rgba(91,170,31,.10), transparent 28%),
            linear-gradient(180deg, #F6F7F9 0%, #FFFFFF 44%, #F6F7F9 100%);
    }

    .block-container {
        max-width: 1050px;
        padding-top: 1.15rem;
        padding-bottom: 2.2rem;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    label, .stNumberInput label, div[data-testid="stWidgetLabel"] p {
        color: #111827 !important;
        font-weight: 850 !important;
        font-size: .96rem !important;
    }

    input {
        color: #111827 !important;
        background-color: #F2F5F8 !important;
        border-radius: 16px !important;
        border: 1px solid #E1E7EF !important;
        min-height: 48px !important;
    }

    .hero {
        background:
            radial-gradient(circle at 90% 18%, rgba(243,154,8,.48), transparent 18%),
            linear-gradient(135deg, #FFFFFF 0%, #FFFFFF 36%, #F8FAFC 100%);
        border: 1px solid #DFE6EF;
        border-radius: 32px;
        padding: 24px;
        margin-bottom: 18px;
        box-shadow: 0 18px 50px rgba(17,24,39,.08);
    }

    .hero-grid {
        display: grid;
        grid-template-columns: 190px 1fr;
        gap: 24px;
        align-items: center;
    }

    .logo-img {
        width: 175px;
        max-width: 100%;
        mix-blend-mode: multiply;
    }

    .hero-title {
        color: #06162E;
        font-size: 37px;
        line-height: 1.03;
        font-weight: 950;
        letter-spacing: -.7px;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        color: #5E6A82;
        font-size: 16px;
        line-height: 1.42;
        max-width: 720px;
    }

    .soft-card {
        background: rgba(255,255,255,.94);
        border: 1px solid #E1E7EF;
        border-radius: 28px;
        padding: 22px;
        box-shadow: 0 10px 30px rgba(17,24,39,.06);
        margin-bottom: 16px;
    }

    .section-title {
        color: #06162E;
        font-size: 22px;
        font-weight: 950;
        margin-bottom: 4px;
    }

    .section-copy {
        color: #5E6A82;
        font-size: 15px;
        line-height: 1.45;
        margin-bottom: 14px;
    }

    .locked {
        background: linear-gradient(135deg, #F8FAFC 0%, #FFFFFF 100%);
        border: 1px solid #E1E7EF;
        border-radius: 22px;
        padding: 16px;
        margin: 8px 0 16px 0;
    }

    .locked-title {
        color: #06162E;
        font-weight: 950;
        font-size: 15px;
        margin-bottom: 11px;
    }

    .locked-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
    }

    .locked-pill {
        background: white;
        border: 1px solid #E1E7EF;
        border-radius: 18px;
        padding: 14px;
    }

    .pill-name {
        color: #5E6A82;
        font-size: 12px;
        font-weight: 850;
        text-transform: uppercase;
        letter-spacing: .45px;
        margin-bottom: 5px;
    }

    .pill-value {
        color: #06162E;
        font-size: 24px;
        font-weight: 950;
    }

    .result-hero {
        background:
            radial-gradient(circle at 92% 14%, rgba(91,170,31,.18), transparent 20%),
            linear-gradient(135deg, #FFFFFF 0%, #F8FBFF 100%);
        border: 1px solid #DDE6F0;
        border-radius: 32px;
        padding: 26px;
        margin-top: 20px;
        box-shadow: 0 18px 44px rgba(17,24,39,.10);
    }

    .result-grid {
        display: grid;
        grid-template-columns: 1.08fr .92fr;
        gap: 22px;
        align-items: stretch;
    }

    .big-label {
        color: #5E6A82;
        font-size: 13px;
        font-weight: 950;
        letter-spacing: .75px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .big-value {
        color: #06162E;
        font-size: 54px;
        line-height: .98;
        font-weight: 950;
        letter-spacing: -1.4px;
        margin-bottom: 10px;
    }

    .big-unit {
        color: #06162E;
        font-size: 20px;
        font-weight: 900;
    }

    .plain-explain {
        color: #111827;
        font-size: 18px;
        line-height: 1.45;
        font-weight: 650;
    }

    .highlight {
        color: #06162E;
        font-weight: 950;
        background: linear-gradient(180deg, transparent 58%, rgba(243,154,8,.27) 58%);
    }

    .verdict {
        border-radius: 26px;
        padding: 20px;
        color: white;
        min-height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .verdict.good {
        background: linear-gradient(135deg, #2E7D16 0%, #5BAA1F 100%);
    }

    .verdict.warn {
        background: linear-gradient(135deg, #B36A00 0%, #F39A08 100%);
    }

    .verdict.neutral {
        background: linear-gradient(135deg, #06162E 0%, #24466E 100%);
    }

    .verdict-label {
        font-size: 13px;
        font-weight: 950;
        letter-spacing: .7px;
        text-transform: uppercase;
        opacity: .86;
        margin-bottom: 6px;
    }

    .verdict-value {
        font-size: 30px;
        font-weight: 950;
        line-height: 1.06;
        margin-bottom: 8px;
    }

    .verdict-copy {
        font-size: 15px;
        line-height: 1.38;
        opacity: .92;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #E1E7EF;
        border-radius: 24px;
        padding: 18px;
        box-shadow: 0 10px 26px rgba(17,24,39,.06);
    }

    div[data-testid="stMetricLabel"] {
        color: #5E6A82;
        font-weight: 850;
    }

    div[data-testid="stMetricValue"] {
        color: #06162E;
        font-weight: 950;
    }

    .metric-help {
        color: #5E6A82;
        font-size: 13px;
        line-height: 1.38;
        margin-top: -2px;
        margin-bottom: 12px;
    }

    .note-box {
        background: #FBFFF5;
        border: 1px solid #DCECCB;
        border-left: 8px solid #5BAA1F;
        color: #111827;
        border-radius: 22px;
        padding: 16px 18px;
        margin-top: 18px;
        font-size: 15px;
        line-height: 1.45;
    }

    .commercial-box {
        background: #FFF8EA;
        border: 1px solid #F3D59C;
        border-left: 8px solid #F39A08;
        color: #111827;
        border-radius: 22px;
        padding: 16px 18px;
        margin-top: 18px;
        font-size: 15px;
        line-height: 1.45;
    }

    .stButton > button, .stDownloadButton > button {
        background: linear-gradient(135deg, #F39A08 0%, #FFB534 100%);
        color: white;
        border: none;
        border-radius: 18px;
        font-weight: 950;
        padding: .82rem 1rem;
        width: 100%;
        box-shadow: 0 12px 24px rgba(243,154,8,.24);
        font-size: 1.02rem;
    }

    .stButton > button:hover, .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #DC8903 0%, #F39A08 100%);
        color: white;
        border: none;
    }

    .footer {
        color: #5E6A82;
        text-align: center;
        font-size: 12px;
        margin-top: 18px;
    }

    @media (max-width: 720px) {
        .block-container {
            padding-left: .92rem;
            padding-right: .92rem;
        }

        .hero {
            padding: 20px;
            border-radius: 26px;
        }

        .hero-grid,
        .result-grid,
        .locked-grid {
            grid-template-columns: 1fr;
        }

        .logo-img {
            width: 155px;
        }

        .hero-title {
            font-size: 30px;
        }

        .hero-subtitle {
            font-size: 15px;
        }

        .soft-card {
            padding: 18px;
            border-radius: 24px;
        }

        .big-value {
            font-size: 41px;
        }

        .plain-explain {
            font-size: 16px;
        }

        .verdict-value {
            font-size: 24px;
        }
    }
</style>
    """, unsafe_allow_html=True)

def render_hero(title, subtitle):
    src = logo_data_uri()
    st.markdown(f"""
<div class="hero">
    <div class="hero-grid">
        <div><img class="logo-img" src="{src}" /></div>
        <div>
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
        </div>
    </div>
</div>
    """, unsafe_allow_html=True)

def render_locked_values(items):
    pills = ""
    for name, value in items:
        pills += f"""
<div class="locked-pill">
    <div class="pill-name">{name}</div>
    <div class="pill-value">{value}</div>
</div>
        """
    st.markdown(f"""
<div class="locked">
    <div class="locked-title">🔒 Valores técnicos fijos</div>
    <div class="locked-grid">
        {pills}
    </div>
</div>
    """, unsafe_allow_html=True)

def render_equiv_result(producto, kg_base, kg_eq, costo_base, costo_nitro, diferencia):
    if diferencia < 0:
        verdict_class = "good"
        verdict_label = "Resultado"
        verdict_value = f"Ahorra {dinero(abs(diferencia))}"
        verdict_copy = "Nitroperfecto cuesta menos para aportar el mismo nitrógeno."
    elif diferencia > 0:
        verdict_class = "warn"
        verdict_label = "Resultado"
        verdict_value = f"{dinero(diferencia)} más"
        verdict_copy = "Nitroperfecto requiere mayor inversión para aportar el mismo nitrógeno."
    else:
        verdict_class = "neutral"
        verdict_label = "Resultado"
        verdict_value = "Mismo costo"
        verdict_copy = "Ambas opciones tienen el mismo costo equivalente."

    st.markdown(f"""
<div class="result-hero">
    <div class="result-grid">
        <div>
            <div class="big-label">Dato principal</div>
            <div class="big-value">{numero(kg_eq)} <span class="big-unit">kg/ha</span></div>
            <div class="plain-explain">
                Necesitas <span class="highlight">{numero(kg_eq)} kg/ha de Nitroperfecto</span>
                para igualar el nitrógeno de <span class="highlight">{numero(kg_base)} kg/ha de {producto}</span>.
            </div>
        </div>
        <div class="verdict {verdict_class}">
            <div class="verdict-label">{verdict_label}</div>
            <div class="verdict-value">{verdict_value}</div>
            <div class="verdict-copy">{verdict_copy}</div>
        </div>
    </div>
</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="metric-help">Comparación de costo con el mismo aporte de nitrógeno:</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric(f"Costo con {producto}", dinero(costo_base))
    c2.metric("Costo con Nitroperfecto", dinero(costo_nitro))
    c3.metric("Diferencia", dinero(diferencia))

def generar_pdf_equivalencia(producto, kg_base, precio_base, precio_nitro, n_producto, n_nitro, kg_eq, costo_base, costo_nitro, diferencia):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=42, leftMargin=42, topMargin=42, bottomMargin=42)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        textColor=colors.HexColor("#06162E"),
        spaceAfter=10,
    )

    subtitle_style = ParagraphStyle(
        "SubtitleCustom",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        textColor=colors.HexColor("#5E6A82"),
        spaceAfter=16,
    )

    normal = ParagraphStyle(
        "NormalCustom",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#111827"),
    )

    story = []
    story.append(Paragraph("ISAOSA", title_style))
    story.append(Paragraph(f"Resultado de calculadora: {producto} vs Nitroperfecto", subtitle_style))
    story.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}", normal))
    story.append(Spacer(1, 16))

    story.append(Paragraph(f"<b>Dato principal:</b> {numero(kg_eq)} kg/ha de Nitroperfecto", normal))
    story.append(Paragraph(
        f"Necesitas {numero(kg_eq)} kg/ha de Nitroperfecto para igualar el nitrógeno de {numero(kg_base)} kg/ha de {producto}.",
        normal
    ))
    story.append(Spacer(1, 16))

    data = [
        ["Concepto", "Valor"],
        [f"Dosis {producto}", f"{numero(kg_base)} kg/ha"],
        [f"Precio {producto}", dinero(precio_base)],
        ["Precio Nitroperfecto", dinero(precio_nitro)],
        [f"N {producto}", f"{n_producto:g}%"],
        ["N Nitroperfecto", f"{n_nitro:g}%"],
        [f"Costo con {producto}", dinero(costo_base)],
        ["Costo con Nitroperfecto", dinero(costo_nitro)],
        ["Diferencia", dinero(diferencia)],
    ]

    table = Table(data, colWidths=[3.1 * inch, 2.6 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#06162E")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDE6F0")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(table)
    story.append(Spacer(1, 18))

    if diferencia < 0:
        lectura = f"Nitroperfecto ahorra {dinero(abs(diferencia))} en costo equivalente."
    elif diferencia > 0:
        lectura = f"Nitroperfecto cuesta {dinero(diferencia)} más en costo equivalente."
    else:
        lectura = "Ambas opciones tienen el mismo costo equivalente."

    story.append(Paragraph(f"<b>Lectura comercial:</b> {lectura}", normal))
    story.append(Spacer(1, 16))
    story.append(Paragraph("Este archivo no es una cotización oficial; es una herramienta comercial de apoyo para mostrar eficiencias de productos ISAOSA. Los precios pueden variar de acuerdo con la fecha, zona de cotización, distribuidor, tipo de cambio y demás condiciones comerciales aplicables.", subtitle_style))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

def generar_pdf_urea(precio_urea, precio_nitro, costo_urea, costo_nitro, diferencia, n_urea, ef_urea, n_nitro, ef_nitro):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=42, leftMargin=42, topMargin=42, bottomMargin=42)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        textColor=colors.HexColor("#06162E"),
        spaceAfter=10,
    )

    subtitle_style = ParagraphStyle(
        "SubtitleCustom",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        textColor=colors.HexColor("#5E6A82"),
        spaceAfter=16,
    )

    normal = ParagraphStyle(
        "NormalCustom",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#111827"),
    )

    story = []
    story.append(Paragraph("ISAOSA", title_style))
    story.append(Paragraph("Resultado de calculadora: Urea vs Nitroperfecto", subtitle_style))
    story.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}", normal))
    story.append(Spacer(1, 16))

    story.append(Paragraph(f"<b>Dato principal:</b> {dinero(costo_nitro)} por kg de nitrógeno aprovechado con Nitroperfecto.", normal))
    story.append(Spacer(1, 16))

    data = [
        ["Concepto", "Valor"],
        ["Precio Urea", dinero(precio_urea)],
        ["Precio Nitroperfecto", dinero(precio_nitro)],
        ["N Urea", f"{n_urea:g}%"],
        ["Eficiencia Urea", f"{ef_urea:g}%"],
        ["N Nitroperfecto", f"{n_nitro:g}%"],
        ["Eficiencia Nitroperfecto", f"{ef_nitro:g}%"],
        ["Costo kg/N aprovechado Urea", dinero(costo_urea)],
        ["Costo kg/N aprovechado Nitroperfecto", dinero(costo_nitro)],
        ["Diferencia", dinero(diferencia)],
    ]

    table = Table(data, colWidths=[3.3 * inch, 2.5 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#06162E")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDE6F0")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(table)
    story.append(Spacer(1, 18))

    if diferencia < 0:
        lectura = f"Nitroperfecto ahorra {dinero(abs(diferencia))} por kg de nitrógeno aprovechado."
    elif diferencia > 0:
        lectura = f"Nitroperfecto cuesta {dinero(diferencia)} más por kg de nitrógeno aprovechado."
    else:
        lectura = "Ambos productos tienen el mismo costo por kg de nitrógeno aprovechado."

    story.append(Paragraph(f"<b>Lectura comercial:</b> {lectura}", normal))
    story.append(Spacer(1, 16))
    story.append(Paragraph("Este archivo no es una cotización oficial; es una herramienta comercial de apoyo para mostrar eficiencias de productos ISAOSA. Los precios pueden variar de acuerdo con la fecha, zona de cotización, distribuidor, tipo de cambio y demás condiciones comerciales aplicables.", subtitle_style))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

def render_footer():
    st.markdown("""
<div class="footer">
    Herramienta comercial de apoyo. Los valores técnicos se modifican únicamente desde el código.
</div>
    """, unsafe_allow_html=True)


N_UREA = 46.0
EF_UREA = 60.0
N_NITRO = 38.0
EF_NITRO = 90.0

def calc_urea(precio_urea, precio_nitro):
    if min(precio_urea, precio_nitro) <= 0:
        raise ValueError("Todos los valores deben ser mayores a cero.")

    costo_100_urea = precio_urea / 10
    costo_100_nitro = precio_nitro / 10

    n_aprov_urea = N_UREA * (EF_UREA / 100)
    n_aprov_nitro = N_NITRO * (EF_NITRO / 100)

    costo_kg_n_urea = costo_100_urea / n_aprov_urea
    costo_kg_n_nitro = costo_100_nitro / n_aprov_nitro
    diferencia = costo_kg_n_nitro - costo_kg_n_urea

    return costo_kg_n_urea, costo_kg_n_nitro, diferencia, n_aprov_urea, n_aprov_nitro

inject_css()
render_hero(
    "Urea vs Nitroperfecto",
    "Compara el costo por kg de nitrógeno aprovechado."
)

st.markdown('<div class="section-title">Ingresa los datos</div>', unsafe_allow_html=True)
st.markdown('<div class="section-copy">Captura los precios para calcular la comparación.</div>', unsafe_allow_html=True)

with st.form("form_urea"):
    precio_urea = st.number_input("Precio de Urea por tonelada", min_value=0.0, value=400.0, step=100.0)
    precio_nitro = st.number_input("Precio de Nitroperfecto por tonelada", min_value=0.0, value=12950.0, step=100.0)

    render_locked_values([
        ("Urea", f"{N_UREA:g}% N · {EF_UREA:g}% aprovechamiento"),
        ("Nitroperfecto", f"{N_NITRO:g}% N · {EF_NITRO:g}% aprovechamiento")
    ])

    calcular = st.form_submit_button("Calcular comparación")


if calcular:
    try:
        costo_urea, costo_nitro, diferencia, n_aprov_urea, n_aprov_nitro = calc_urea(precio_urea, precio_nitro)

        if diferencia < 0:
            verdict_class = "good"
            verdict_value = f"Ahorra {dinero(abs(diferencia))}"
            verdict_copy = "Nitroperfecto cuesta menos por kg de nitrógeno aprovechado."
        elif diferencia > 0:
            verdict_class = "warn"
            verdict_value = f"{dinero(diferencia)} más"
            verdict_copy = "Nitroperfecto cuesta más por kg de nitrógeno aprovechado."
        else:
            verdict_class = "neutral"
            verdict_value = "Mismo costo"
            verdict_copy = "Ambos productos tienen el mismo costo por kg de nitrógeno aprovechado."

        st.markdown(f"""
<div class="result-hero">
    <div class="result-grid">
        <div>
            <div class="big-label">Dato principal</div>
            <div class="big-value">{dinero(costo_nitro)} <span class="big-unit">/ kg N</span></div>
            <div class="plain-explain">
                Ese es el costo estimado de cada <span class="highlight">kg de nitrógeno aprovechado</span> con Nitroperfecto.
            </div>
        </div>
        <div class="verdict {verdict_class}">
            <div class="verdict-label">Resultado</div>
            <div class="verdict-value">{verdict_value}</div>
            <div class="verdict-copy">{verdict_copy}</div>
        </div>
    </div>
</div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="metric-help">Comparación directa por kg de nitrógeno aprovechado:</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("Urea", dinero(costo_urea))
        c2.metric("Nitroperfecto", dinero(costo_nitro))
        c3.metric("Diferencia", dinero(diferencia))

        st.markdown("""
<div class="commercial-box">
    <b>Lectura sencilla:</b> El resultado compara el costo del nitrógeno que realmente se aprovecha.
</div>
        """, unsafe_allow_html=True)

        st.markdown("""
<div class="note-box">
    <b>Mensaje comercial:</b> Con Nitroperfecto Super KBRN obtén sin costo Potasio, Calcio,
    Magnesio, Zinc y Boro que ayudan a mejorar la polinización y el llenado del cultivo.
</div>
        """, unsafe_allow_html=True)

        pdf_data = generar_pdf_urea(
            precio_urea, precio_nitro, costo_urea, costo_nitro, diferencia,
            N_UREA, EF_UREA, N_NITRO, EF_NITRO
        )

        st.download_button(
            "Descargar resultado en PDF",
            data=pdf_data,
            file_name="resultado_urea_vs_nitroperfecto.pdf",
            mime="application/pdf"
        )

    except Exception as e:
        st.error(str(e))
else:
    st.info("Captura los datos y presiona **Calcular comparación**.")

render_footer()
