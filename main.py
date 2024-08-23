from pytesseract import pytesseract
import google.generativeai as genai
from pdfquery import PDFQuery
import os

# api init
genai.configure(api_key="AIzaSyCiORc74qB0QGtY0ZgZ_Z9Xw1j2aWHceNA")
model = genai.GenerativeModel('models/gemini-1.5-flash')

# Configuração do pytesseract
# path_to_tes = r"C:\Users\DIEGOGUTERRESDEFIGUE\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
path_to_tes = r"C:\Users\diego.gutterres_v4co\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tes

def process_image_and_generate_response(img_path):
    try:
        img_text = pytesseract.image_to_string(img_path)
        prompt = f"""
        Você é um advogado. Traduza todos os documentos e informações que você receber para que qualquer pessoa entenda. 
        Simplifique o MÁXIMO que conseguir, use palavras simples que todos conheçam. Faça apenas um parágrafo (se possível),
        que contenha todo o conteúdo importante do documento, como a decisão do juiz, o caso em si, decisões e escolhas das partes,
        penalidades se tiver, testemunhas de vitimas, etc, compare com outros casos para entender melhor o que são pontos importantes
        em documentos juridicos.

        Aqui vai o texto para ser simplificado: {img_text}
        """

        response_bruto = model.generate_content(contents=prompt)
        response = response_bruto.text
        return img_text, response
    except Exception as e:
        print(f"Error processing image: {e}")
        raise e
    
def process_pdf_and_generate_response(pdf):
    try:
        pdf = PDFQuery(pdf)
        pdf.load()

        text_elements = pdf.pq('LTTextLineHorizontal')
        pdf_text = [t.text for t in text_elements]

        prompt = f"""
        Você é um advogado. Traduza todos os documentos e informações que você receber para que qualquer pessoa entenda. 
        Simplifique o MÁXIMO que conseguir, use palavras simples que todos conheçam. Faça apenas um parágrafo (se possível),
        que contenha todo o conteúdo importante do documento, como a decisão do juiz, o caso em si, decisões e escolhas das partes,
        penalidades se tiver, testemunhas de vitimas, etc, compare com outros casos para entender melhor o que são pontos importantes
        em documentos juridicos.

        Aqui vai o texto para ser simplificado: {pdf_text}
        """

        response_bruto = model.generate_content(contents=prompt)
        response = response_bruto.text
        return pdf_text, response
    except Exception as e:
        print(f"Error processing pdf: {e}")
        raise e

