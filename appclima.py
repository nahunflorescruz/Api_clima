import streamlit as st
import pandas as pd
from api_clima import obtener_apiclima

st.set_page_config(page_title="Dashboard Meteorológico", page_icon="🌤️", layout="wide")

opcion = st.sidebar.selectbox(
    "Selecciona una opción",
    ["Inicio", "Consumir Clima", "Selector de Ciudad"]
)

if opcion == "Inicio":
    st.title("Bienvenid@ al Dashboard Meteorológico")
    st.write("""
    Esta aplicación te permite monitorear y analizar las condiciones climáticas en tiempo real 
    utilizando datos de una API pública de meteorología.
    
    ### Características principales:
    * **Visualización en tiempo real:** Consulta datos actuales del clima.
    * **Estructura limpia:** Datos organizados mediante tablas y métricas interactivas.
    * **Búsqueda personalizada:** Filtra la información según la ciudad de tu interés.
    """)
    st.info(" Usa el menú de la izquierda para navegar entre las diferentes secciones.")

elif opcion == "Consumir Clima":
    st.title(" Datos Climáticos Globales")
    st.write("Haz clic en el botón de abajo para obtener el pronóstico meteorológico actual y por horas.")
    
    if st.button("Consultar Clima", type="primary"):
        with st.spinner("Conectando con el servicio de clima..."):
            try:
                # Petición a través de la función importada
                datos = obtener_apiclima()
                
                # 1. Mostrar Clima Actual de forma visual
                st.subheader(" Condiciones Actuales (Berlín / Coordenadas Base)")
                actual = datos.get("current", {})
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="Temperatura Actual", value=f"{actual.get('temperature_2m')} °C")
                with col2:
                    st.metric(label="Velocidad del Viento", value=f"{actual.get('wind_speed_10m')} km/h")
                
                # 2. Procesar y ordenar los datos por hora en una tabla de Pandas
                st.subheader(" Pronóstico por Horas")
                por_hora = datos.get("hourly", {})
                
                # Creamos el DataFrame estructurando las listas que devuelve la función
                df_clima = pd.DataFrame({
                    "Fecha y Hora": por_hora.get("time"),
                    "Temperatura (2m)": por_hora.get("temperature_2m"),
                    "Humedad Relativa (%)": por_hora.get("relative_humidity_2m"),
                    "Vel. Viento (10m)": por_hora.get("wind_speed_10m")
                })
                
                # Mostramos la tabla interactiva de Pandas
                st.dataframe(df_clima, use_container_width=True)
                st.success("¡Datos actualizados correctamente!")
                
            except Exception as e:
                st.error(f"Hubo un problema al obtener los datos de la API: {e}")

# --- SECCIÓN: SELECTOR DE CIUDAD ---
elif opcion == "Selector de Ciudad":
    st.title("Consulta por Ciudad")
    
    ciudades = ["Tegucigalpa", "San Pedro Sula", "Miami", "Madrid", "Tokio"]
    ciudad_seleccionada = st.selectbox("Selecciona una ciudad:", ciudades)
    
    st.markdown(f"###  Clima actual en **{ciudad_seleccionada}**")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Temperatura", value="28 °C", delta=" Despejado")
    with col2:
        st.metric(label="Humedad", value="65%")
    with col3:
        st.metric(label="Velocidad del Viento", value="14 km/h")
    with col4:
        st.metric(label="Presión", value="1012 hPa")