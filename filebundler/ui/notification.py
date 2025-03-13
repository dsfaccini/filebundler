# filebundler/ui/notification.py
import time
import random

import streamlit as st


def show_temp_notification(message, type="info", duration=3):
    """
    Show a temporary notification that automatically disappears.

    Args:
        message: The message to display
        type: "info", "success", "warning", or "error"
        duration: Time in seconds before notification disappears
    """

    # Create a unique key for this notification
    notification_id = (
        f"notification_{int(time.time() * 1000)}_{random.randint(0, 1000)}"
    )

    # Add custom CSS for the notification
    st.markdown(
        f"""
    <style>
    #{notification_id} {{
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 9999;
        padding: 10px 20px;
        border-radius: 5px;
        background-color: {
            "#0066cc"
            if type == "info"
            else "#28a745"
            if type == "success"
            else "#ffc107"
            if type == "warning"
            else "#dc3545"  # error
        };
        color: white;
        opacity: 0;
        animation: fadeIn 0.3s ease forwards, fadeOut 0.5s ease forwards {duration}s;
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes fadeOut {{
        from {{ opacity: 1; transform: translateY(0); }}
        to {{ opacity: 0; transform: translateY(-20px); }}
    }}
    </style>
    
    <div id="{notification_id}">{message}</div>
    """,
        unsafe_allow_html=True,
    )
