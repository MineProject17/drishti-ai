import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="Drishti AI", page_icon="💊")

# 2. UI Layout
st.title("💊 Drishti: Safe Meds for Everyone")
st.subheader("Upload a medicine strip. Get instructions in YOUR language.")

# 3. Sidebar for API Key
api_key = st.sidebar.text_input("Enter Google Gemini API Key", type="password")

# 4. The Logic
if api_key:
    genai.configure(api_key=api_key)
    
    uploaded_file = st.file_uploader("Take a photo of the medicine...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Medicine", use_column_width=True)

        prompt = """
        You are an expert pharmacist helper for rural India. 
        Analyze this image of a medicine.
        
        Output format:
        1. **Medicine Name**: [Name]
        2. **Main Use**: [Simple explanation like 'For Fever', 'For Heart']
        3. **Expiry Check**: Check the date on the pack against December 2025. If expired, say WARNING in capital letters.
        4. **Instructions (Hindi)**: Translate the usage instructions into simple Hindi.
        5. **Instructions (Telugu/Tamil)**: Translate the usage instructions into a South Indian language.
        """

        if st.button("Analyze Medicine"):
            with st.spinner("Consulting the AI Pharmacist..."):
                try:
                    # TRY 1: The Standard Flash Model (Exact Version)
                    model = genai.GenerativeModel('gemini-1.5-flash-001')
                    response = model.generate_content([prompt, image])
                    st.markdown(response.text)
                    st.success("Analysis Complete (via Flash-001)!")
                
                except Exception as e1:
                    # TRY 2: Fallback to Pro (Slower but often available)
                    try:
                        st.warning("Flash model busy, switching to Pro model...")
                        model = genai.GenerativeModel('gemini-1.5-pro')
                        response = model.generate_content([prompt, image])
                        st.markdown(response.text)
                        st.success("Analysis Complete (via Pro)!")
                    except Exception as e2:
                        st.error(f"Critical Error. Details: {e1}")
                        # Debugging helper: List available models
                        st.write("Debug Info - Available Models for your Key:")
                        for m in genai.list_models():
                            if 'generateContent' in m.supported_generation_methods:
                                st.code(m.name)
else:
    st.warning("Please enter your API Key in the sidebar to start.")

st.markdown("---")
st.caption("Built for Google Build the Future Showcase")
