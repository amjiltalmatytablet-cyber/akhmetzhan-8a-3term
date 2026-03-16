import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Бет баптаулары
st.set_page_config(page_title="ҚР Денсаулық сақтау талдауы", layout="wide")
st.title("🏥 Қазақстанның денсаулық сақтау индикаторлары (Аналитика)")

# --- 1. ДЕРЕКТЕРДІ ГЕНЕРАЦИЯЛАУ (Демонстрация үшін) ---
regions = ['Алматы', 'Астана', 'Шымкент', 'Абай', 'Ақмола', 'Ақтөбе', 'Алматы обл.', 'Атырау', 
           'Батыс Қазақстан', 'Жамбыл', 'Жетісу', 'Қарағанды', 'Қостанай', 'Қызылорда', 
           'Маңғыстау', 'Павлодар', 'Солтүстік Қазақстан', 'Түркістан', 'Ұлытау', 'Шығыс Қазақстан']

data = pd.DataFrame({
    'Өңір': regions,
    'lat': [43.2, 51.1, 42.3, 50.4, 53.2, 50.3, 45.0, 47.1, 51.2, 44.9, 45.0, 49.8, 53.2, 44.8, 43.6, 52.3, 54.8, 43.3, 48.3, 49.9],
    'lon': [76.9, 71.4, 69.6, 80.2, 69.3, 57.1, 78.0, 51.9, 51.3, 71.3, 78.4, 73.1, 63.6, 65.5, 51.1, 76.9, 69.1, 68.2, 67.7, 82.6],
    'Дәрігерлер тапшылығы': np.random.randint(50, 500, size=len(regions)),
    'Төсек қоры (%)': np.random.randint(60, 95, size=len(regions)),
    'Жабдықталу (%)': np.random.randint(40, 90, size=len(regions)),
    'Ана өлімі (коэф)': np.random.uniform(5, 25, size=len(regions))
})

# --- 2. HEALTH SCORE ЕСЕПТЕУ АЛГОРИТМІ ---
# Формула: (Жабдықталу + Төсек қоры) - (Тапшылықтың нормаланған мәні)
data['Health Score'] = (
    (data['Жабдықталу (%)'] * 0.4) + 
    (data['Төсек қоры (%)'] * 0.3) - 
    ((data['Дәрігерлер тапшылығы'] / data['Дәрігерлер тапшылығы'].max()) * 20)
).round(1)

# --- ИНТЕРФЕЙС ---
tab1, tab2, tab3 = st.tabs(["Географиялық талдау", "Ресурстар салыстырмасы", "Трендтер"])

# 1. Дәрігерлер тапшылығы (Scatter Mapbox - Координаттармен)
with tab1:
    st.subheader("📍 Өңірлердегі дәрігерлер тапшылығы")
    fig_map = px.scatter_mapbox(data, lat="lat", lon="lon", size="Дәрігерлер тапшылығы", 
                                color="Дәрігерлер тапшылығы", hover_name="Өңір",
                                color_continuous_scale=px.colors.sequential.Reds,
                                zoom=3, height=500)
    fig_map.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig_map, use_container_width=True)
    st.info("Шеңбер өлшемі дәрігер кадрларының жетіспеушілігін білдіреді.")

# 2. Radar Chart (Төсек қоры мен Жабдықталу)
with tab2:
    st.subheader("📡 Ресурстар мен Health Score")
    selected_region = st.selectbox("Өңірді таңдаңыз:", regions)
    region_info = data[data['Өңір'] == selected_region].iloc[0]
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
          r=[region_info['Төсек қоры (%)'], region_info['Жабдықталу (%)'], region_info['Health Score']],
          theta=['Төсек қоры', 'Жабдықталу', 'Health Score'],
          fill='toself',
          name=selected_region
    ))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])))
    st.plotly_chart(fig_radar)
    

# 3. Өмір сүру ұзақтығы (Area Chart)
with tab3:
    st.subheader("📈 Өмір сүру ұзақтығының динамикасы (ҚР бойынша)")
    years = pd.DataFrame({
        'Жыл': np.arange(2010, 2024),
        'Жас': [73.5, 73.8, 74.2, 74.5, 75.1, 75.4, 75.8, 76.2, 76.5, 77.0, 75.0, 75.5, 76.8, 77.4]
    })
    fig_area = px.area(years, x='Жыл', y='Жас', title="Өмір сүру ұзақтығының өсуі")
    st.plotly_chart(fig_area, use_container_width=True)

# --- РЕЙТИНГ КЕСТЕСІ ---
st.divider()
st.subheader("🏆 Өңірлердің Health Score рейтингі")
st.dataframe(data[['Өңір', 'Health Score', 'Дәрігерлер тапшылығы']].sort_values(by='Health Score', ascending=False))