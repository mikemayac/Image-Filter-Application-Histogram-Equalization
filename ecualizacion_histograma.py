import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="Ecualización de Histograma con Histograma Visible", layout="wide")


def ecualizar_grayscale(imagen_gray: Image.Image) -> Image.Image:
    # Convertir la imagen a un array numpy
    img_array = np.array(imagen_gray)

    # Calcular el histograma
    hist, bins = np.histogram(img_array.flatten(), 256, [0, 256])

    # Calcular la función de distribución acumulada (CDF)
    cdf = hist.cumsum()

    # Evitar división por cero. Se enmascaran valores de cdf=0
    cdf_m = np.ma.masked_equal(cdf, 0)
    cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
    cdf = np.ma.filled(cdf_m, 0).astype('uint8')

    # Aplicar la CDF a la imagen original
    img_eq = cdf[img_array]

    # Convertir de vuelta a PIL
    return Image.fromarray(img_eq, mode='L')


def ecualizar_ycbcr(imagen_rgb: Image.Image) -> Image.Image:
    # Convertir la imagen a YCbCr
    img_ycbcr = imagen_rgb.convert("YCbCr")
    y, cb, cr = img_ycbcr.split()

    # Ecualizar el canal Y (luminancia)
    y_eq = ecualizar_grayscale(y)

    # Combinar de nuevo Y ecualizado con Cb y Cr originales
    img_ycbcr_eq = Image.merge("YCbCr", (y_eq, cb, cr))

    # Convertir a RGB para el resultado final
    return img_ycbcr_eq.convert("RGB")


def aplicar_ecualizacion_histograma(imagen: Image.Image, modo_color: bool) -> Image.Image:
    """
    Aplica ecualización de histograma a la imagen.
      - Si modo_color=True: ecualiza solo la componente de luminancia en YCbCr.
      - Si modo_color=False: ecualiza la imagen en escala de grises.
    """
    if modo_color:
        return ecualizar_ycbcr(imagen)
    else:
        imagen_gray = imagen.convert("L")
        imagen_eq_gray = ecualizar_grayscale(imagen_gray)
        # Retornamos a RGB para visualizar con Streamlit
        return imagen_eq_gray.convert("RGB")


def generar_histograma(imagen: Image.Image, titulo="Histograma"):
    """
    Genera y retorna un objeto Figure de matplotlib con el histograma de la imagen (en gris).
    """
    # Convertir a escala de grises para graficar un único canal
    imagen_gray = imagen.convert("L")
    img_array = np.array(imagen_gray)

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.hist(img_array.flatten(), bins=256, range=(0, 256), color='black', alpha=0.8)
    ax.set_title(titulo)
    ax.set_xlabel("Nivel de Intensidad")
    ax.set_ylabel("Frecuencia")
    fig.tight_layout()

    return fig


def main():
    st.sidebar.title("Configuraciones")
    st.sidebar.markdown("### Filtro: Ecualización de Histograma")
    modo_color = st.sidebar.checkbox("Ecualizar en color (YCbCr)", value=False)

    uploaded_file = st.sidebar.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])

    imagen_resultante = None
    buf_value = None

    if uploaded_file is not None:
        # Cargamos la imagen original
        imagen_original = Image.open(uploaded_file).convert("RGB")

        # Aplicar la ecualización de histograma
        with st.spinner("Calculando ecualización de histograma..."):
            imagen_resultante = aplicar_ecualizacion_histograma(imagen_original, modo_color)

        # Preparar la imagen para descarga
        buf = BytesIO()
        imagen_resultante.save(buf, format="PNG")
        buf_value = buf.getvalue()

    # ---- Encabezado y botón de descarga ----
    title_col, button_col = st.columns([4, 1])
    with title_col:
        st.title("Visualización de Ecualización de Histograma")
    with button_col:
        if imagen_resultante is not None and buf_value is not None:
            st.download_button(
                label="⬇️ Descargar imagen",
                data=buf_value,
                file_name="imagen_ecualizada.png",
                mime="image/png",
                key="download_button_top"
            )

    # ---- Muestra de imagen y histogramas ----
    if uploaded_file is not None:
        # Fila 1: Imagen original y ecualizada
        col1, col2 = st.columns(2)
        with col1:
            st.image(imagen_original, caption="Imagen Original", use_container_width=True)
        with col2:
            st.image(imagen_resultante, caption="Imagen Ecualizada", use_container_width=True)

        # Fila 2: Histogramas (original y ecualizado)
        hist_col1, hist_col2 = st.columns(2)

        with hist_col1:
            fig_original = generar_histograma(imagen_original, titulo="Histograma Original")
            st.pyplot(fig_original)

        with hist_col2:
            fig_ecual = generar_histograma(imagen_resultante, titulo="Histograma Ecualizado")
            st.pyplot(fig_ecual)
    else:
        st.info("Sube una imagen para ver su histograma y la ecualización.")


if __name__ == "__main__":
    main()
