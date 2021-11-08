import streamlit as st
from time import sleep


def vanishing_logs(area, category, message: str):
    """Animated logs area location"""
    with st.empty():
        for _ in range(4):
            if category == 'info':
                area.info(message)
            elif category == 'error':
                area.error(message)
            elif category == 'success':
                area.success(message)    
            sleep(1)
    area.write("")