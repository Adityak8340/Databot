import os
import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from dotenv import load_dotenv
from langchain_groq.chat_models import ChatGroq
import pandasai as pai

pai.clear_cache()

load_dotenv()
GROQ_API_KEY=os.getenv('GROQ_API_KEY')

llm = ChatGroq(model_name='llama3-70b-8192', api_key=GROQ_API_KEY)
st.set_page_config(page_title="Databot", page_icon="🐼", layout="wide")

st.title("Prompt-driven Data Visualization 🙌")
uploaded_file = st.file_uploader("Upload the dataset file", type=['csv', 'xlsx'])

if uploaded_file is not None:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.info("Upload completed")
        if uploaded_file.name.endswith('.csv'):
            data = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            data = pd.read_excel(uploaded_file)
        st.dataframe(data, use_container_width=True)
        df = SmartDataframe(data, config={"llm": llm})

    with col2:
        st.info("Start chatting here💬")
        prompt = st.text_area("Enter your query:")

        if st.button("Generate"):
            if prompt:
                with st.spinner("Result is generating, please wait..."):
                    result = df.chat(prompt)
                    st.write(result)  # Display the returned result

                    # Check if the result is a valid image path
                    if isinstance(result, str) and os.path.exists(result):
                        if result.lower().endswith(('.png', '.jpg', '.jpeg')):
                            st.image(result, caption="Generated Chart")
                        else:
                            st.warning("The returned result is not an image path.")
                    else:
                        st.warning("No image generated or the path does not exist.")
            else:
                st.warning("Please enter a prompt")
