import base64
import io
import streamlit as st

def render_zoomable_image(image_bytes: io.BytesIO) -> None:
    encoded = base64.b64encode(image_bytes.getvalue()).decode()
    html_code = f'<div style="text-align:center;"><img src="data:image/png;base64,{encoded}" style="max-width:100%; border-radius:8px;" /></div>'
    st.components.v1.html(html_code, height=500, scrolling=True)

def show_feedback_modal():
    st.info("問題回報功能維護中")
