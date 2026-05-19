INSTRUCCIONES

Archivos:
- app_sulfato.py
- app_urea.py
- app_can27.py
- requirements.txt
- assets/isaosa.png

Para probar local:
py -m pip install -r requirements.txt
py -m streamlit run app_sulfato.py
py -m streamlit run app_urea.py
py -m streamlit run app_can27.py

Cambios de esta versión:
- Se corrigió el bloque que mostraba HTML como texto.
- Texto superior más simple para usuario final.
- Valores técnicos no editables.
- Botón para descargar resultado en PDF.
- Logo real de ISAOSA dentro de assets/isaosa.png si fue posible copiarlo.
