#!/usr/bin/env python3
"""
Streamlit-Seite: NN Playground (externes iFrame)
- Integriert den TensorFlow Playground als Referenz/Ideengeber für Interaktiv-Grafiken
- Verweist klar auf die Quelle (Google/TensorFlow)
"""
import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="NN Playground (Demo)",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():
    with st.sidebar:
        st.title("🧪 NN Playground (Demo)")
        st.markdown("Interaktive Demo via externes iFrame.")
        st.markdown("Quelle: TensorFlow Playground")
        st.divider()
        st.caption("Nützlich als Design-/Interaktions-Referenz für eigene 5D-Visualisierungen.")

    st.title("🧪 Neural Network Playground – Referenz")
    mode = st.radio("Betriebsart", ["Extern (TensorFlow)", "Offline (vereinfachte Demo)"], index=0, horizontal=True)
    st.caption("Quelle extern: https://playground.tensorflow.org – Offline: Plotly Demo")

    if mode == "Extern (TensorFlow)":
        iframe_html = (
            "<iframe src='https://playground.tensorflow.org/?hl=de' "
            "style='width: 100%; height: 900px; border: 0; border-radius: 8px; overflow: hidden' "
            "loading='lazy' allowfullscreen></iframe>"
        )
        st.components.v1.html(iframe_html, height=920, scrolling=False)
    else:
        st.subheader("Offline-Demo: Entscheidungsfläche (synthetisch)")
        # Parameter
        noise = st.slider("Rauschen", 0.0, 1.0, 0.15, 0.01)
        n = st.slider("Punkte", 100, 2000, 400, 100)

        # Datensatz: XOR-ähnlich
        rng = np.random.default_rng(42)
        X = rng.uniform(-1, 1, size=(n, 2))
        y = (X[:, 0] * X[:, 1] > 0).astype(int)
        X_noisy = X + noise * rng.normal(size=X.shape)

        # Einfache Scorefunktion (nicht-trainiert, nur Demo):
        # S(x,y) = tanh(5*x*y)
        def score(xx, yy):
            return np.tanh(5 * xx * yy)

        grid = 200
        gx = np.linspace(-1.2, 1.2, grid)
        gy = np.linspace(-1.2, 1.2, grid)
        GX, GY = np.meshgrid(gx, gy)
        Z = score(GX, GY)

        fig = go.Figure()
        fig.add_trace(
            go.Contour(
                x=gx,
                y=gy,
                z=Z,
                contours=dict(showlines=False),
                colorscale=[[0, "#f59322"], [0.5, "#e8eaeb"], [1, "#0877bd"]],
                opacity=0.9,
                name="Decision field",
                showscale=False,
            )
        )
        fig.add_trace(
            go.Scattergl(
                x=X_noisy[y == 0, 0],
                y=X_noisy[y == 0, 1],
                mode="markers",
                marker=dict(size=6, color="#f59322"),
                name="Klasse 0",
            )
        )
        fig.add_trace(
            go.Scattergl(
                x=X_noisy[y == 1, 0],
                y=X_noisy[y == 1, 1],
                mode="markers",
                marker=dict(size=6, color="#0877bd"),
                name="Klasse 1",
            )
        )
        fig.update_layout(
            height=720,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis_title="X1",
            yaxis_title="X2",
        )
        st.plotly_chart(fig, width="stretch")


if __name__ == "__main__":
    main()
