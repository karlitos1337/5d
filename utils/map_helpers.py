"""
Helper functions for Folium mini-maps across dashboard pages
"""

import folium
import streamlit as st
from streamlit_folium import st_folium

def create_alternative_schools_map():
    """Create map showing alternative schools worldwide"""
    m = folium.Map(location=[30, 0], zoom_start=2, tiles="CartoDB positron")
    
    schools = {
        'Sudbury Valley (USA)': {'coords': [42.37, -71.36], 'type': 'Sudbury', 'color': '#00ff00'},
        'Summerhill (UK)': {'coords': [52.21, 1.40], 'type': 'Democratic', 'color': '#00ff00'},
        'ESBZ Berlin (DE)': {'coords': [52.52, 13.41], 'type': 'Democratic', 'color': '#00ff00'},
        'Tokkatsu (Japan)': {'coords': [35.68, 139.76], 'type': 'Social Learning', 'color': '#90ee90'},
        'Folk High School (DK)': {'coords': [56.26, 9.50], 'type': 'Folk HS', 'color': '#90ee90'},
        'Green School (Bali)': {'coords': [-8.54, 115.28], 'type': 'Sustainability', 'color': '#90ee90'},
    }
    
    for name, data in schools.items():
        folium.Marker(
            location=data['coords'],
            popup=f"<b>{name}</b><br>Type: {data['type']}",
            icon=folium.Icon(color='green', icon='school', prefix='fa')
        ).add_to(m)
    
    return m

def create_research_distribution_map():
    """Create map showing research paper origins"""
    m = folium.Map(location=[30, 0], zoom_start=2, tiles="CartoDB positron")
    
    research_hubs = {
        'USA': {'coords': [37.09, -95.71], 'papers': 450, 'color': '#ff0000'},
        'UK': {'coords': [55.38, -3.44], 'papers': 180, 'color': '#ff6600'},
        'Germany': {'coords': [51.17, 10.45], 'papers': 120, 'color': '#ffa500'},
        'Finland': {'coords': [61.92, 25.75], 'papers': 85, 'color': '#ffff00'},
        'Japan': {'coords': [36.20, 138.25], 'papers': 95, 'color': '#ffff00'},
        'Brazil': {'coords': [-14.24, -51.93], 'papers': 45, 'color': '#90ee90'},
    }
    
    for country, data in research_hubs.items():
        folium.CircleMarker(
            location=data['coords'],
            radius=data['papers'] / 20,
            popup=f"<b>{country}</b><br>Papers: {data['papers']}",
            color=data['color'],
            fill=True,
            fillOpacity=0.6
        ).add_to(m)
    
    return m

def create_developer_community_map():
    """Create map showing GitHub developer distribution"""
    m = folium.Map(location=[30, 0], zoom_start=2, tiles="CartoDB positron")
    
    dev_hubs = {
        'Silicon Valley (USA)': {'coords': [37.39, -122.08], 'devs': 50000, 'color': '#ff0000'},
        'London (UK)': {'coords': [51.51, -0.13], 'devs': 25000, 'color': '#ff6600'},
        'Berlin (DE)': {'coords': [52.52, 13.41], 'devs': 18000, 'color': '#ffa500'},
        'Bangalore (IN)': {'coords': [12.97, 77.59], 'devs': 35000, 'color': '#ff0000'},
        'Tel Aviv (IL)': {'coords': [32.08, 34.78], 'devs': 12000, 'color': '#ffff00'},
        'São Paulo (BR)': {'coords': [-23.55, -46.63], 'devs': 15000, 'color': '#ffff00'},
    }
    
    for city, data in dev_hubs.items():
        folium.CircleMarker(
            location=data['coords'],
            radius=data['devs'] / 2000,
            popup=f"<b>{city}</b><br>Devs: {data['devs']:,}",
            color=data['color'],
            fill=True,
            fillOpacity=0.6
        ).add_to(m)
    
    return m

def create_cooperation_examples_map():
    """Create map showing successful commons examples"""
    m = folium.Map(location=[30, 0], zoom_start=2, tiles="CartoDB positron")
    
    commons = {
        'Swiss Alpine Commons': {'coords': [46.82, 8.23], 'years': 800, 'type': 'Forest', 'color': '#00ff00'},
        'Valencia Huertas (ES)': {'coords': [39.47, -0.38], 'years': 1000, 'type': 'Water', 'color': '#00ff00'},
        'Bali Subak (ID)': {'coords': [-8.41, 115.19], 'years': 1000, 'type': 'Irrigation', 'color': '#00ff00'},
        'Maine Lobster (USA)': {'coords': [44.31, -69.78], 'years': 150, 'type': 'Fishing', 'color': '#90ee90'},
        'Nepal Forests': {'coords': [28.39, 84.12], 'years': 40, 'type': 'Forest', 'color': '#ffff00'},
    }
    
    for name, data in commons.items():
        folium.Marker(
            location=data['coords'],
            popup=f"<b>{name}</b><br>Type: {data['type']}<br>Years: {data['years']}+",
            icon=folium.Icon(color='green', icon='leaf', prefix='fa')
        ).add_to(m)
    
    return m

def create_regional_adoption_map():
    """Create map showing projected 5D adoption by region"""
    m = folium.Map(location=[30, 0], zoom_start=2, tiles="CartoDB positron")
    
    regions = {
        'Nordic Countries': {'coords': [60.0, 10.0], 'adoption_2040': 70, 'color': '#00ff00'},
        'Western Europe': {'coords': [50.0, 5.0], 'adoption_2040': 50, 'color': '#90ee90'},
        'North America': {'coords': [40.0, -100.0], 'adoption_2040': 40, 'color': '#ffff00'},
        'East Asia': {'coords': [35.0, 130.0], 'adoption_2040': 35, 'color': '#ffa500'},
        'Latin America': {'coords': [-15.0, -60.0], 'adoption_2040': 25, 'color': '#ffa500'},
        'Africa': {'coords': [0.0, 20.0], 'adoption_2040': 18, 'color': '#ff6600'},
    }
    
    for region, data in regions.items():
        folium.CircleMarker(
            location=data['coords'],
            radius=data['adoption_2040'] / 3,
            popup=f"<b>{region}</b><br>2040 Adoption: {data['adoption_2040']}%",
            color=data['color'],
            fill=True,
            fillOpacity=0.6
        ).add_to(m)
    
    return m

def render_minimap(map_obj, caption=""):
    """Render a Folium map with consistent styling"""
    st_folium(map_obj, width=700, height=350)
    if caption:
        st.caption(caption)
