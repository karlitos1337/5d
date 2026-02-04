#!/usr/bin/env python3
"""Visualisierungs-Templates für 5D-Daten.

Erzeugt Plotly-Diagramme für:
- Radar-Charts (5D-Profile)
- Heatmaps (Korrelationen)
- Zeit-Serien (longitudinale Daten)
- Cluster-Visualisierungen
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def generate_dimension_radar_chart(
    profile: dict, title: str = "5D-Intelligence Profil"
) -> go.Figure:
    """Radar-Chart für einzelnes 5D-Profil."""
    dimensions = [
        "Neurobiologie",
        "Psychologie",
        "Philosophie",
        "Ökonomie",
        "Technologie",
    ]

    scores = [
        profile["dimension_scores"]["neurobiology"]["normalized_score"],
        profile["dimension_scores"]["psychology"]["normalized_score"],
        profile["dimension_scores"]["philosophy"]["normalized_score"],
        profile["dimension_scores"]["economics"]["normalized_score"],
        profile["dimension_scores"]["technology"]["normalized_score"],
    ]

    fig = go.Figure(
        data=go.Scatterpolar(
            r=scores,
            theta=dimensions,
            fill="toself",
            name="5D-Profil",
            line=dict(color="rgb(50, 184, 198)", width=2),
            fillcolor="rgba(50, 184, 198, 0.3)",
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickvals=[0, 0.25, 0.5, 0.75, 1.0],
                ticktext=["0%", "25%", "50%", "75%", "100%"],
            )
        ),
        showlegend=False,
        title=title,
        template="plotly_white",
    )

    return fig


def generate_comparison_radar(profiles: list[dict], labels: list[str]) -> go.Figure:
    """Vergleich mehrerer Profile."""
    dimensions = [
        "Neurobiologie",
        "Psychologie",
        "Philosophie",
        "Ökonomie",
        "Technologie",
    ]

    fig = go.Figure()

    colors = [
        "rgb(50, 184, 198)",
        "rgb(192, 21, 47)",
        "rgb(168, 75, 47)",
        "rgb(98, 108, 113)",
    ]

    for i, (profile, label) in enumerate(zip(profiles, labels, strict=False)):
        scores = [
            profile["dimension_scores"]["neurobiology"]["normalized_score"],
            profile["dimension_scores"]["psychology"]["normalized_score"],
            profile["dimension_scores"]["philosophy"]["normalized_score"],
            profile["dimension_scores"]["economics"]["normalized_score"],
            profile["dimension_scores"]["technology"]["normalized_score"],
        ]

        fig.add_trace(
            go.Scatterpolar(
                r=scores,
                theta=dimensions,
                fill="toself",
                name=label,
                line=dict(color=colors[i % len(colors)]),
            )
        )

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        title="5D-Profile Vergleich",
    )

    return fig


def generate_cluster_heatmap(
    cluster_centers: list[list[float]], feature_names: list[str]
) -> go.Figure:
    """Heatmap der Cluster-Zentren."""
    df = pd.DataFrame(cluster_centers, columns=feature_names)

    fig = px.imshow(
        df,
        labels=dict(x="Feature", y="Cluster", color="Wert"),
        x=feature_names,
        y=[f"Cluster {i+1}" for i in range(len(cluster_centers))],
        color_continuous_scale="RdYlGn",
        title="Cluster-Zentren Heatmap",
    )

    return fig


def generate_dimension_distribution(profiles: list[dict], dimension: str) -> go.Figure:
    """Histogramm für Dimensions-Verteilung."""
    scores = [p["dimension_scores"][dimension]["normalized_score"] for p in profiles]

    fig = go.Figure(
        data=[go.Histogram(x=scores, nbinsx=20, marker_color="rgb(50, 184, 198)")]
    )

    fig.update_layout(
        title=f"{dimension.capitalize()} Score Verteilung",
        xaxis_title="Normalized Score",
        yaxis_title="Häufigkeit",
        template="plotly_white",
    )

    return fig


def generate_correlation_matrix(profiles: list[dict]) -> go.Figure:
    """Korrelations-Matrix zwischen Dimensionen."""
    data = []
    for p in profiles:
        data.append(
            [
                p["dimension_scores"]["neurobiology"]["normalized_score"],
                p["dimension_scores"]["psychology"]["normalized_score"],
                p["dimension_scores"]["philosophy"]["normalized_score"],
                p["dimension_scores"]["economics"]["normalized_score"],
                p["dimension_scores"]["technology"]["normalized_score"],
            ]
        )

    df = pd.DataFrame(data, columns=["Neuro", "Psych", "Philo", "Econ", "Tech"])
    corr = df.corr()

    fig = px.imshow(
        corr,
        labels=dict(color="Korrelation"),
        x=["Neuro", "Psych", "Philo", "Econ", "Tech"],
        y=["Neuro", "Psych", "Philo", "Econ", "Tech"],
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        title="Dimensionen Korrelations-Matrix",
    )

    return fig


def generate_pca_scatter(pca_data: dict, cluster_labels: list[int]) -> go.Figure:
    """2D PCA Scatter mit Cluster-Färbung."""
    transformed = np.array(pca_data["transformed_data"])

    df = pd.DataFrame(
        {
            "PC1": transformed[:, 0],
            "PC2": transformed[:, 1],
            "Cluster": [
                f"Cluster {c}" if c >= 0 else "Outlier" for c in cluster_labels
            ],
        }
    )

    fig = px.scatter(
        df,
        x="PC1",
        y="PC2",
        color="Cluster",
        title=f"PCA Projektion (Varianz erklärt: {pca_data['total_variance_explained']*100:.1f}%)",
        labels={"PC1": "PC1", "PC2": "PC2"},
    )

    return fig


if __name__ == "__main__":
    # Test
    from analysis.calculate_5d_scores import calculate_5d_intelligence_profile

    test_responses = {
        "neuro_flow_frequency": 4,
        "psych_intrinsic_motivation": 5,
        "philo_critical_thinking": 5,
        "econ_participation": 4,
        "tech_open_source": 5,
    }

    profile = calculate_5d_intelligence_profile(test_responses)
    fig = generate_dimension_radar_chart(profile)
    fig.write_html("test_radar.html")
    print("Radar chart saved to test_radar.html")
