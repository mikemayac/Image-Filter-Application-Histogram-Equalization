import streamlit as st
from PIL import Image
import numpy as np
from io import BytesIO

# Configuración de la página
st.set_page_config(page_title="Filtro: Ecualización de Histograma", layout="wide")

def ecualizar_grayscale(imagen_gray: Image.Image) -> Image.Image:
    """
    Aplica ecualización de histograma a una imagen en escala de grises.
    Retorna la imagen ecualizada, también en escala de grises.
    """
    # Convertir la imagen a un array numpy
    img_array = np.array(imagen_gray)

    # Calcular el histograma
    hist, bins = np.histogram(img_array.flatten(), 256, [0, 256])

    # Calcular la función de distribución acumulada (CDF)
    cdf = hist.cumsum()

    # Normalizar la CDF para que oscile entre 0 y 255
    cdf_m = np.ma.masked_equal(cdf, 0)  # Mascarea valores donde cdf=0 para evitar división por cero
    cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
    cdf = np.ma.filled(cdf_m, 0).astype('uint8')

    # Aplicar la CDF a la imagen original
    img_eq = cdf[img_array]

    # Convertir de vuelta a PIL
    return Image.fromarray(img_eq, mode='L')


def ecualizar_ycbcr(imagen_rgb: Image.Image) -> Image.Image:
    """
    Aplica ecualización de histograma a la componente Y (luminancia) de una imagen en RGB.
    Retorna la imagen ecualizada en RGB.
    """
    # Convertir la imagen a YCbCr
    img_ycbcr = imagen_rgb.convert("YCbCr")
    y, cb, cr = img_ycbcr.split()

    # Ecualizar el canal Y (luminancia) en escala de grises
    y_eq = ecualizar_grayscale(y)

    # Combinar de nuevo Y con Cb y Cr
    img_ycbcr_eq = Image.merge("YCbCr", (y_eq, cb, cr))

    # Convertir a RGB para visualizar
    return img_ycbcr_eq.convert("RGB")


def aplicar_ecualizacion_histograma(imagen: Image.Image, modo_color: bool) -> Image.Image:
    """
    Aplica ecualización de histograma a la imagen.
    Si modo_color=True, se ecualiza la componente de luminancia (Y) de la imagen.
    Si modo_color=False, se ecualiza la imagen en escala de grises.
    """
    if modo_color:
        # Ecualización en la componente Y (luminancia) de YCbCr
        return ecualizar_ycbcr(imagen)
    else:
        # Ecualización en escala de grises
        # Convertimos a 'L', ecualizamos y regresamos a RGB (para unificar la presentación)
        imagen_gray = imagen.convert("L")
        imagen_eq_gray = ecualizar_grayscale(imagen_gray)
        return imagen_eq_gray.convert("RGB")

def main():
    st.sidebar.title("Configuraciones")
    st.sidebar.markdown("### Filtro activo: Ecualización de Histograma")

    # Checkbox para elegir si se aplica la ecualización en color o en escala de grises
    modo_color = st.sidebar.checkbox("Ecualizar imagen a color (YCbCr)", value=False)

    uploaded_file = st.sidebar.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])

    imagen_resultante = None
    buf_value = None

    if uploaded_file is not None:
        # Cargamos la imagen original
        imagen_original = Image.open(uploaded_file).convert("RGB")

        # Aplicar la ecualización
        with st.spinner("Aplicando la ecualización de histograma..."):
            imagen_resultante = aplicar_ecualizacion_histograma(imagen_original, modo_color)

        # Preparar la imagen para descarga
        buf = BytesIO()
        imagen_resultante.save(buf, format="PNG")
        buf_value = buf.getvalue()

    # Crear la fila del título con el botón de descarga
    title_col, button_col = st.columns([4, 1])

    with title_col:
        st.title("Ecualización de Histograma")

    with button_col:
        if imagen_resultante is not None and buf_value is not None:
            st.download_button(
                label="⬇️ Descargar imagen",
                data=buf_value,
                file_name="imagen_ecualizada.png",
                mime="image/png",
                key="download_button_top"
            )

    # Mostrar las imágenes si se subió un archivo
    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.image(imagen_original, caption="Imagen Original", use_container_width=True)
        with col2:
            st.image(imagen_resultante, caption="Imagen Ecualizada", use_container_width=True)
    else:
        st.info("Sube una imagen para aplicar la ecualización de histograma.")

if __name__ == "__main__":
    main()
