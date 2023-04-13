import cv2
import numpy as np
import streamlit as st
import base64
import requests
import time


def set_page_config():
    st.set_page_config(
        page_title="Image Classification Project",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://github.com/wahyu-adi-n",
            "Report a bug": "https://github.com/wahyu-adi-n",
            "About": "**Image Classification Project | AI Resercher PT. Delameta Bilano**",
        }
    )


def readb64(uri):
    image = cv2.cvtColor(cv2.imdecode(np.frombuffer(base64.b64decode(
        uri.split(',')[-1]), np.uint8), cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
    return image


def payload(image):
    return {"image": image}


def main():
    set_page_config()
    st.title('Image Classification Project')
    st.write('This project for Coding Test AI Researcher PT Delameta Bilano.')
    file_uploader = st.file_uploader(
        label='Please upload your image here.', type=['jpg', 'jpeg', 'png'])

    if file_uploader is not None:
        image_base64 = base64.b64encode(
            file_uploader.getvalue()).decode('utf-8')
        image_original = readb64(image_base64)
        image, button, _ = st.columns(3)

        with image:
            st.image(image_original)

        with button:
            st.write('Click this button for making predictions (inference)')
            st.button('🚀 Predict')
            try:
                with st.spinner('🕔 Wait for it...'):
                    time.sleep(0.1)
                    url = 'http://localhost:5000/predict'
                    response = requests.post(
                        url = url, json = payload(image_base64)).json()
                    st.json(response)
                    st.success('✅ Request was successful!')
            except Exception as e:
                st.exception(e)

if __name__ == '__main__':
    main()
