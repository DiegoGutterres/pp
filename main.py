from pytesseract import pytesseract
import google.generativeai as genai
from pdfquery import PDFQuery
from pyzbar.pyzbar import decode
import os
from PIL import Image
import requests

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
            em documentos juridicos. Coloque também, se tiver, datas, valores em Reais e nomes dos envolvidos, tudo contextualizado e coerente.

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
        em documentos juridicos. Coloque também, se tiver, datas, valores em Reais e nomes dos envolvidos, tudo contextualizado e coerente.

        Aqui vai o texto para ser simplificado: {pdf_text}
        """

        response_bruto = model.generate_content(contents=prompt)
        response = response_bruto.text
        return pdf_text, response
    except Exception as e:
        print(f"Error processing pdf: {e}")
        raise e
    
def process_qr_and_generate_response(img_path):
    try:
        # Abrir a imagem com Pillow (PIL)
        image = Image.open(img_path)

        # Detectar QR codes na imagem
        qr_codes = decode(image)
        if qr_codes:
            # Pegar o dado do primeiro QR code detectado
            qr_data = qr_codes[0].data.decode('utf-8')
            print(f"QR Code detectado: {qr_data}")

            # Preparar o prompt para enviar à IA
            prompt = f"""
            Você é um advogado. Traduza todos os documentos e informações que você receber para que qualquer pessoa entenda. 
            Simplifique o MÁXIMO que conseguir, use palavras simples que todos conheçam. Faça apenas um parágrafo (se possível),
            que contenha todo o conteúdo importante do documento, como a decisão do juiz, o caso em si, decisões e escolhas das partes,
            penalidades se tiver, testemunhas de vítimas, etc. Coloque também, se tiver, datas, valores em Reais e nomes dos envolvidos,
            tudo contextualizado e coerente. O que você vai ler é um QR-Code extraido, se não tiver nada dentro, ou for apenas um link,
            diga ao usuário que é um link e que está incorreto a forma que o qrcode foi gerado

            Aqui vai o texto para ser simplificado: {qr_data}
            """

            # Enviar para o modelo de IA (GEMINI)
            response_bruto = model.generate_content(contents=prompt)
            response = response_bruto.text

            # Retornar o dado do QR code e a resposta simplificada
            return qr_data, response
        else:
            return None, "Nenhum QR Code detectado."
    except Exception as e:
        print(f"Error processing image: {e}")
        raise e