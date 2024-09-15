import streamlit as st
import PyPDF2
import openai


# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    all_text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        all_text += page.extract_text()
    return all_text


# Function to generate HTML using OpenAI API
def generate_html_resume(pdf_text, api_key):
    openai.api_key = api_key
    prompt = f"Create a professional HTML resume from the following text: {pdf_text}"

    # Use the new ChatCompletion API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # The model to use (use GPT-3.5 or GPT-4)
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        n=1,
        temperature=0.7,
    )

    # Extract the assistant's response from the chat completion
    return response['choices'][0]['message']['content'].strip()


# Streamlit app
st.title("PDF to HTML Resume Generator")
api_key = st.text_input("Enter OpenAI API key", type="password")
uploaded_pdf = st.file_uploader("Upload LinkedIn PDF", type="pdf")

if uploaded_pdf and api_key:
    pdf_text = extract_text_from_pdf(uploaded_pdf)
    html_resume = generate_html_resume(pdf_text, api_key)
    st.markdown(html_resume, unsafe_allow_html=True)
    st.download_button("Download HTML Resume", html_resume, file_name="resume.html", mime="text/html")


