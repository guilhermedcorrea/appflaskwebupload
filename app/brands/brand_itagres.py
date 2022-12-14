

from itertools import zip_longest
import os
import sys
import pytesseract
from PIL import Image
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError)
import cv2
import numpy as np
import re
import pandas as pd
from datetime import datetime
import pytesseract
from config import UPLOADFOLDER
import os
import csv
from flask import current_app


class Itagres:
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

    def __init__(self, path):
        pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
        self.config = '--psm 4  -c preserve_interword_spaces=1 tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.[]|,,.~â ÃÂç'
        self.tesseract_language = "por"
        self.lista_produtos = []
        self.path = path
        self.imagem = os.path.join(UPLOADFOLDER,'flaskapprefatorado','app','uploads','imagens')
        self.pdffile = os.path.join(UPLOADFOLDER,'flaskapprefatorado','app','uploads')
        self.dataatual = str(datetime.today().strftime('%Y-%m-%d %H:%M'))
        self.idmarca = '37'

    
    def converter_imgpdf(self):
     
        images = convert_from_bytes(open(self.path, 'rb').read())

        for i in range(len(images)):
            images[i].save(self.imagem+'/itagres'+ str(i) +'.jpg', 'JPEG')
            print(images[i])

    def search_files(self):
        imagem = [x for x in os.listdir(self.imagem) if 'itagres']
        return imagem


    def reader_imagem(self):
        lista_dicts = []
        imagens = self.search_files()
        try:
            for im in imagens:
                if 'itagres' in im:
                    img = cv2.imread(os.path.join(self.imagem,im))
                    imagemgray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #Convertendo para rgb
                    texto = pytesseract.image_to_string(imagemgray
                        ,lang= self.tesseract_language,config= self.config)
                                                    
                    texto = texto.split("\n")
                    for x in texto:
                        dict_items = {}
                        strs = re.sub('\s+|[|]|[MONOP.]|[RET.]',' ', x)
                        remov_esps = re.sub('\s+',' ', strs)
                        valores = remov_esps.strip().split()
                        try:
                            sku = str(valores[0]).strip()
                            dict_items['SKU'] = sku
                        
                        except:
                            dict_items['SKU'] = 'notfound'
                            
                        try:
                            saldos = str(valores[-1]).replace(",",".").strip()
                            saldos = float(saldos)
                            dict_items['SALDOS'] = saldos
                          
                        except:
                            dict_items['SALDOS'] = float(0)

                        dict_items['IDMARCA'] = self.idmarca
                        print(dict_items)
                        return dict_items
                        
   
        except:
            pass
        

