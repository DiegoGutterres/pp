from pytesseract import pytesseract
from openai import OpenAI

client = OpenAI(
   api_key='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'
)
path_to_tes = r"C:\Users\DIEGOGUTERRESDEFIGUE\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tes

img = pytesseract.image_to_string('./teste_3.png')

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "Você é um advogado informal, traduza todos os documentos e informações que você receber para que qualquer pessoa sem qualquer formação escolar entenda. Pessoas de baixa renda, sem convívio com a sociedade moderna, crianças e deficientes intelectuais também devem entender com clareza. Simplifique o MÁXIMO que conseguir, use palavras simples que todos conheçam"},
    {"role": "user", "content": img}
  ]
)

print(img)
print(completion)

#api key : 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