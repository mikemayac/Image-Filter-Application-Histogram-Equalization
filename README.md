# Aplicación de Ecualización de Histograma

### Joel Miguel Maya Castrejón - 417112602

Esta aplicación web, construida con **Python** y **Streamlit**, permite aplicar **ecualización de histograma** a imágenes, una técnica fundamental en el procesamiento digital de imágenes que mejora el contraste redistribuyendo los valores de intensidad de los píxeles.

El proceso general consiste en:
1. **Calcular el histograma** de la imagen (distribución de intensidades de píxeles).
2. **Generar la función de distribución acumulativa (CDF)** del histograma.
3. **Transformar la imagen** aplicando esta CDF como función de mapeo.

El resultado es una imagen con mejor contraste y distribución de tonos, permitiendo visualizar detalles que pueden estar ocultos en imágenes con bajo contraste o mal expuestas.

---

## Requisitos

- Python 3.8 o superior
- [Streamlit](https://docs.streamlit.io/) para la creación de la interfaz web.
- [Pillow](https://pillow.readthedocs.io/) (PIL) para la manipulación de imágenes.
- [NumPy](https://numpy.org/) para operaciones numéricas y manejo de arrays.
- [Matplotlib](https://matplotlib.org/) para la generación de gráficos de histogramas.

En el archivo **requirements.txt** se listan las dependencias necesarias. Asegúrate de instalarlas antes de ejecutar la aplicación.

---

## Instalación

1. [**Clona** este repositorio](https://github.com/mikemayac/Image-Filter-Application-Histogram-Equalization) en tu máquina local.
2. Crea y activa un **entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/Mac
   # En Windows: venv\Scripts\activate
   ```
3. Instala los paquetes necesarios:
   ```bash
   pip install -r requirements.txt
   ```

---

## Ejecución de la Aplicación

1. Dentro del entorno virtual, ubícate en la carpeta donde se encuentra el archivo principal.
2. Ejecuta:
   ```bash
   streamlit run ecualizacion_histograma.py
   ```
3. Tu navegador abrirá la interfaz de la aplicación.  
   Si no se abre automáticamente, copia la URL que aparece en la terminal y pégala en tu navegador.

---

## Uso de la Aplicación

1. **Sube una imagen** en la barra lateral, en formatos `JPG`, `JPEG` o `PNG`.
2. Opcionalmente, puedes ajustar los parámetros:
   - **Ecualizar en color (YCbCr)**: Si está marcado, se ecualiza solo el canal de luminancia (Y) manteniendo los componentes de color, resultando en una imagen en color con mejor contraste.
   - Si no está marcado, se ecualiza la imagen en escala de grises.
3. **Observa** cómo se muestra la **imagen original** en una columna y la **imagen ecualizada** en la otra.
4. **Compara los histogramas** original y ecualizado para entender cómo ha cambiado la distribución de intensidades.
5. **Descarga** la imagen ecualizada pulsando el botón de descarga situado en la parte superior.

---

## Algoritmo Implementado

1. **Cálculo del histograma**  
   Se cuenta la frecuencia de cada nivel de intensidad (0-255) en la imagen.
   
2. **Obtención de la CDF (Función de Distribución Acumulada)**  
   Se calcula la suma acumulativa del histograma, que representa la probabilidad de encontrar un píxel con una intensidad menor o igual a cada nivel.

3. **Normalización de la CDF**  
   Se escalan los valores de la CDF al rango [0, 255].

4. **Transformación de la imagen**  
   Se aplica la CDF normalizada como una función de mapeo para transformar los valores de los píxeles originales.

El proceso completo da como resultado una imagen con una distribución de intensidades más equilibrada, mejorando el contraste global.

---

## Modos de Ecualización

La aplicación permite dos tipos de ecualización:

1. **Escala de grises**: Convierte la imagen a escala de grises y ecualiza directamente los valores de intensidad.

2. **Color (YCbCr)**: Convierte la imagen al espacio de color YCbCr, ecualiza solo el canal Y (luminancia) y mantiene los canales Cb y Cr (crominancia) para preservar los colores originales.

---

## Estructura del Proyecto

```bash
.
├── ecualizacion_histograma.py # Código principal de la aplicación
├── .streamlit/               # Configuraciones extra de Streamlit
│    └── config.toml           
├── README.md                 # Archivo de documentación (este archivo)
├── requirements.txt          # Dependencias del proyecto
└── venv/                     # Entorno virtual (puede variar según tu instalación)
```

---

## Fundamento Teórico

La ecualización de histograma es una técnica que busca obtener una distribución uniforme del histograma de una imagen. Matemáticamente, se puede expresar como:

$s_k = T(r_k) = \sum_{j=0}^{k} \frac{n_j}{n}$

Donde:
- $s_k$ es el nuevo valor del píxel
- $r_k$ es el valor original del píxel
- $n_j$ es el número de píxeles con valor j
- $n$ es el número total de píxeles

Esta transformación redistribuye los niveles de intensidad para que ocupen todo el rango disponible, mejorando así el contraste global de la imagen.