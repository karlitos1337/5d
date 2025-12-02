#!/usr/bin/env python3
"""Clustering-Algorithmen für 5D-Profile.

Segmentiert Teilnehmer nach ähnlichen Profilen.
"""

from typing import List, Dict, Any
import numpy as np
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pandas as pd


def extract_features_from_profiles(profiles: List[Dict]) -> np.ndarray:
    """Extrahiert Feature-Vektoren aus Profilen.
    
    Features:
    - 5 Dimensions-Scores (normalized)
    - Entrance-Variablen (life_satisfaction, financial_situation)
    """
    features = []
    
    for profile in profiles:
        feature_vector = [
            profile['dimension_scores']['neurobiology']['normalized_score'],
            profile['dimension_scores']['psychology']['normalized_score'],
            profile['dimension_scores']['philosophy']['normalized_score'],
            profile['dimension_scores']['economics']['normalized_score'],
            profile['dimension_scores']['technology']['normalized_score']
        ]
        
        # Entrance-Daten
        entrance = profile.get('entrance_data', {})
        feature_vector.extend([
            entrance.get('life_satisfaction', 3) / 6,  # Normalisiert
            entrance.get('financial_situation', 3) / 5
        ])
        
        features.append(feature_vector)
    
    return np.array(features)


def kmeans_clustering(profiles: List[Dict], n_clusters: int = 5) -> Dict:
    """K-Means Clustering.
    
    Args:
        profiles: Liste von 5D-Profilen
        n_clusters: Anzahl Cluster (default: 5 für 5D)
    
    Returns:
        Dictionary mit cluster_labels, centers, etc.
    """
    features = extract_features_from_profiles(profiles)
    
    # Standardisierung
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(features_scaled)
    
    return {
        'method': 'kmeans',
        'n_clusters': n_clusters,
        'cluster_labels': cluster_labels.tolist(),
        'cluster_centers': kmeans.cluster_centers_.tolist(),
        'inertia': float(kmeans.inertia_),
        'feature_names': ['neuro', 'psych', 'philo', 'econ', 'tech', 'life_sat', 'fin_sit']
    }


def dbscan_clustering(profiles: List[Dict], eps: float = 0.5, min_samples: int = 5) -> Dict:
    """DBSCAN Clustering (Density-based).
    
    Gut für:
    - Ausreißer-Erkennung
    - Nicht-sphärische Cluster
    """
    features = extract_features_from_profiles(profiles)
    
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    cluster_labels = dbscan.fit_predict(features_scaled)
    
    n_clusters = len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)
    n_noise = list(cluster_labels).count(-1)
    
    return {
        'method': 'dbscan',
        'n_clusters': n_clusters,
        'n_noise_points': n_noise,
        'cluster_labels': cluster_labels.tolist(),
        'eps': eps,
        'min_samples': min_samples
    }


def dimensionality_reduction_pca(profiles: List[Dict], n_components: int = 2) -> Dict:
    """PCA für Visualisierung in 2D/3D."""
    features = extract_features_from_profiles(profiles)
    
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    pca = PCA(n_components=n_components)
    transformed = pca.fit_transform(features_scaled)
    
    return {
        'method': 'pca',
        'n_components': n_components,
        'transformed_data': transformed.tolist(),
        'explained_variance_ratio': pca.explained_variance_ratio_.tolist(),
        'total_variance_explained': float(sum(pca.explained_variance_ratio_))
    }


def cluster_analysis(profiles: List[Dict]) -> Dict:
    """Vollständige Cluster-Analyse."""
    results = {
        'n_profiles': len(profiles),
        'kmeans': kmeans_clustering(profiles, n_clusters=5),
        'dbscan': dbscan_clustering(profiles),
        'pca_2d': dimensionality_reduction_pca(profiles, n_components=2)
    }
    
    return results


if __name__ == '__main__':
    # Test mit Dummy-Daten
    from analysis.calculate_5d_scores import calculate_5d_intelligence_profile
    
    # Generiere Test-Profile
    test_profiles = []
    for i in range(100):
        responses = {
            'neuro_flow_frequency': np.random.randint(1, 6),
            'psych_intrinsic_motivation': np.random.randint(1, 6),
            'philo_critical_thinking': np.random.randint(1, 6),
            'econ_participation': np.random.randint(1, 6),
            'tech_open_source': np.random.randint(1, 6),
            'life_satisfaction': np.random.randint(1, 7),
            'financial_situation': np.random.randint(1, 6)
        }
        profile = calculate_5d_intelligence_profile(responses)
        test_profiles.append(profile)
    
    results = cluster_analysis(test_profiles)
    print(f"Found {results['kmeans']['n_clusters']} K-Means clusters")
    print(f"Found {results['dbscan']['n_clusters']} DBSCAN clusters ({results['dbscan']['n_noise_points']} outliers)")
