import time
from typing import Any

import matplotlib.pyplot as plt
import streamlit as st
from sympy import plot

st.set_page_config(page_title="Fractal with IFS", page_icon="📈")

FRACTAL_IFS = {
    "Barnsley Fern": "./data/fractal_ifs/barnsley-fern.yaml",
    "Pentadentrite": "./data/fractal_ifs/pentadentrite.yaml",
    "Sierpinski": "./data/fractal_ifs/sierpinski.yaml",
    "Spiral": "./data/fractal_ifs/spiral.yaml",
    "Custom": "",
}

# Convention: {abbreviation for widget}_{widget name}
_ST_WIDGET_KEYS = [
    # Select Box
    "sb_fractal",
    # Button
    "btn_generate",
]

last_image = None

st.markdown(
    """
    # FRACTAL GENERATION

    """
)


def get_selectbox_option(key: str) -> Any:
    if not key.startswith("sb"):
        raise ValueError(f"Select box should start with sb. Received: {key}")
    if key not in _ST_WIDGET_KEYS:
        raise ValueError(
            f"Key for widget should be pre-defined.\n"
            f"Key cannot be found: {key}.\n"
            f"List of keys: {_ST_WIDGET_KEYS}"
        )

    option = st.session_state.get(key)

    if option is None:
        raise ValueError(f"SelectBox {key} is not defined")

    return option


option = st.selectbox(
    label="Select a fractal", options=list(FRACTAL_IFS.keys()), key="sb_fractal"
)


def draw_fractal():
    from src.schemas import FractalTransformation
    from src.tasks.fractal import generate_fractal, generate_points
    option: str = get_selectbox_option("sb_fractal")

    transformations = FractalTransformation.load_transformations(FRACTAL_IFS[option])
    lim_x = 1000
    lim_y = 1000
    points = generate_points(transformations, lim_x, lim_y)
    
    # global last_image
    # with plot_placeholder:
    #     global last_image
    #     for img in generate_fractal(transformations, lim_x, lim_y, "tmp.png", 10):
    #         global last_image
    #         last_image = img
    #         st.image(last_image)
    #         time.sleep(0.1)

    n = len(points) // 100
    for i in range(100):
        x = [point[0] for point in points[i * n: (i + 1) * n]]
        y = [point[1] for point in points[i * n: (i + 1) * n]]
        plt.scatter(x, y, s=0.01)

        plot_placeholder.pyplot(plt)



plot_placeholder = st.empty()
st.button(label="Generate", key="btn_generate", on_click=draw_fractal)

st.write("This is the end")