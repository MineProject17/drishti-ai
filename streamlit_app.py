import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="Drishti AI", page_icon="💊")

# 2. UI Layout
st.title("💊 Drishti: Safe Meds for Everyone")
st.subheader("Upload a medicine strip. Get instructions in YOUR language.")

# 3. Secure API Key Configuration (Read from Streamlit Secrets)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    st.error("⚠️ API Key not configured. Please set GOOGLE_API_KEY in Streamlit secrets.")
    st.stop()

# 4. The Logic
genai.configure(api_key=api_key)

# Upload Image
uploaded_file = st.file_uploader("Take a photo of the medicine...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Medicine", use_column_width=True)

    # The Golden Prompt
    prompt = """
    You are an expert pharmacist helper for rural India. 
    Analyze this image of a medicine.
    
    Output format:
    1. **Medicine Name**: [Name]
    2. **Main Use**: [Simple explanation like 'For Fever', 'For Heart']
    3. **Expiry Check**: Check the date on the pack against December 2025. If expired, say WARNING in capital letters.
    4. **Instructions (Hindi)**: Translate the usage instructions into simple Hindi.
    5. **Instructions (Telugu/Tamil)**: Translate the usage instructions into a South Indian language.
    
    Keep it very simple. No complex medical jargon.
    """

    if st.button("Analyze Medicine"):
        with st.spinner("Consulting the AI Pharmacist..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content([prompt, image])
                st.markdown(response.text)
                st.success("Analysis Complete!")
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.info("Please upload a medicine image to start.")

st.markdown("---")
st.caption("Built for Google Build the Future Showcase | Powered by Gemini 1.5")
