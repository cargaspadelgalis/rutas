import streamlit as st
import google.generativeai as genai

# Configuración de la interfaz
st.set_page_config(page_title="Analizador de Rutas Pesadas", page_icon="🚛")
st.title("🚛 Analizador de Accesibilidad para Tráiler (40t)")
st.write("Origen fijo: **46460 Silla, Valencia** | Vehículo: **Tráiler 5 ejes (40.000 kg MMA)**")

# Configuración de API Key (Soporta Secrets de Streamlit y entrada manual)
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Introduce tu Gemini API Key:", type="password")

SYSTEM_PROMPT = """
Actúa como analista de rutas logísticas para transporte pesado.
Parámetros fijos:
- Origen: 46460 Silla, Valencia.
- Vehículo: tráiler articulado de 5 ejes (2+3), con Masa Máxima Autorizada (MMA) de 40.000 kg.

Analiza la ruta y responde directamente con:
1. Viabilidad de acceso (SÍ/NO y justificación técnica/normativa).
2. Punto alternativo (dirección concreta si no es viable).
3. Ubicación del punto alternativo (dirección completa, coordenadas GPS y enlace Google Maps).
4. Distancia restante (distancia exacta por carretera).
"""

destino = st.text_input("Dirección de entrega del cliente:", placeholder="Ej: Calle Rio Bidasoa 18, Valencia")

if st.button("Analizar accesibilidad", type="primary"):
    if not api_key:
        st.error("Por favor, introduce tu API Key en la barra lateral.")
    elif not destino:
        st.warning("Introduce una dirección de entrega válida.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=SYSTEM_PROMPT
            )
            
            with st.spinner("Verificando morfología de vía, restricciones y distancia..."):
                response = model.generate_content(f"Dirección de entrega: {destino}")
                st.markdown("### Resultado del análisis")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Error al procesar la solicitud: {e}")