from pytesseract import pytesseract
import google.generativeai as genai
from pdfquery import PDFQuery
import os
import cv2
import requests
from pyzbar import pyzbar

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
    
# Função para decodificar o QR Code
def decode_qrcode(image):
    decoded_objects = pyzbar.decode(image)
    for obj in decoded_objects:
        qr_data = obj.data.decode('utf-8')
        print(f"Data do QR Code: {qr_data}")
        return qr_data


# Função para baixar o PDF de um link (se o QR Code contiver um link para o PDF)
def download_pdf_from_link(url, output_path="downloaded_pdf.pdf"):
    try:
        response = requests.get(url)
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"PDF baixado com sucesso: {output_path}")
        return output_path
    except Exception as e:
        print(f"Erro ao baixar o PDF: {e}")
        raise e

# Função principal para ler o QR code, baixar o PDF e processá-lo
def read_qrcode_and_process_pdf(image_path):
    # Carregar a imagem do QR code
    image = cv2.imread(image_path)

    # Decodificar QR codes na imagem
    qr_data = decode_qrcode(image)

    # Se o QR code contiver um link para o PDF, fazer o download
    if qr_data.startswith("http"):
        pdf_path = download_pdf_from_link(qr_data)
    else:
        print("O QR code não contém um link válido para um PDF.")
        return

    # Processar o PDF e gerar a resposta simplificada
    pdf_text, response = process_pdf_and_generate_response(pdf_path)

    print("Texto extraído do PDF:", pdf_text)
    print("Resposta simplificada:", response)


image_path = "imagem.png"
read_qrcode_and_process_pdf(image_path)






