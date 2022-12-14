from abc import ABC, abstractmethod
from ast import ExceptHandler
from itertools import chain
import re
from datetime import datetime
from ..controllers.controllers_querys import HauszMapa, CallProcedureHauszMapa
from ..brands.brand_viscardi import Viscardi
from ..brands.brand_gaudi import Gaudi
from ..brands.brand_itagres import Itagres
from ..brands.brand_elizabeth import Elizabeth
from ..brands.brand_lexxa import Lexxa
from ..brands.brand_level import Level
from ..brands.brand_sense import Sense
from ..brands.brand_quikstep import QuickStep
from ..brands.update_balances import AtualizaSaldos


class Marcas(ABC):
    @abstractmethod
    def get_saldos(self) -> None: pass


class BrandGaudi(Marcas):
    def get_saldos(self, valor) -> None:
        try:
            brand = 'Gaudi'
            gaudi = Gaudi(valor)
            gaudi.converter_imgpdf()
            dicts = gaudi.reader_imagem()
            print(dicts)
            return dicts, brand
        except:
            print('erro classe Gaudi')


class BrandElizabeth(Marcas):
    def get_saldos(self, valor) -> None:
        try:
            elizabeth = Elizabeth(valor)
            brand = 'Elizabeth'
            elizabeth.converter_imgpdf()
            elizabeth.reader_imagem()
            dicts = elizabeth.group_by()
            if isinstance(dicts, list):
                return dicts, brand
        except:
            pass
            print('Erro classe Elizabeth')


'''
class BrandItagres(Marcas):
    def get_saldos(self, valor) -> None:
        try:
            itagres = Itagres(valor)
            brand = 'Itagres'
            itagres.converter_imgpdf()
            dicts = itagres.imagem_reader()
            itagres.delete_upload_files()
            itagres.delete_image_files()
            itagres.dict_writer()
            return dicts, brand
        except:
            print("erro classe Itagres")
'''


class BrandViscardi(Marcas):
    def get_saldos(self, valor):
        try:
            brand = 'Viscardi'
            viscardi = Viscardi(valor)
            viscardi.converter_imgpdf()
            dicts = viscardi.reader_imagem()

            return dicts, brand
        except:
            print("erro classe Viscardi")


class BrandLexxa(Marcas):
    def get_saldos(self, valor):
        lexxa = Lexxa(valor)
        brand = 'Lexxa'
        lexxa.converter_imgpdf()
        dicts = lexxa.reader_imagem()

        return dicts, brand


class BrandLevel(Marcas):
    def get_saldos(self, valor) -> None:
        try:
            level = Level(valor)
            brand = 'Level'
            dicts = level.read_excel()
            level.delete_upload_files()
            level.dict_writer()
            print(dicts)
            return dicts, brand
        except:
            print("erro classe Level")


'''
class BrandSense(Marcas):
    def get_saldos(self, valor):
        try:
            sense = Sense(valor)
            brand = 'Sense'
            sense.converter_imgpdf()
            dicts = sense.create_dataframe()
            sense.delete_upload_files()
            sense.delete_image_files()
            sense.dict_writer()
            return dicts, brand
        except:
            print("erro classe Sense")
'''


class BrandQuickstep(Marcas):
    def get_saldos(self, valor) -> None:
        try:
            quickstep = QuickStep(valor)
            brand = 'Quickstep'
            quickstep.converter_imgpdf()
            dicts = quickstep.reader_imagem()
            quickstep.delete_upload_files()
            quickstep.delete_image_files()
            quickstep.dict_writer()
            return dicts, brand
        except:
            print("erro classe Quickstep")


class BrandSaldoCrossDocking:
    def get_saldos(self, valor) -> None:
        try:
            crossdocking = AtualizaSaldos(valor)
            brand = 'SaldoFornecedor'
            dicts = crossdocking.reader_excel_file()
            return dicts, brand
        except:
            print("erro Class Crossdocking")


class MarcaFactory:
    @staticmethod
    def get_marca(brand: str, *args, **kwargs):
        print('factoryyy', brand)

        if re.search('gaudi.?', brand, re.IGNORECASE):
            print(brand)
            return BrandGaudi()

        if re.search('elizabeth.?', brand, re.IGNORECASE):
            return BrandElizabeth()

        # if re.search('itagres.?', brand, re.IGNORECASE):
        #    return BrandItagres()

        if re.search('viscardi.?', brand, re.IGNORECASE):
            return BrandViscardi()

        if re.search('lexxa.?', brand, re.IGNORECASE):
            return BrandLexxa()

        if re.search('level.?', brand, re.IGNORECASE):
            return BrandLevel()

        # if re.search('sense.?', brand, re.IGNORECASE):
        #    return BrandSense()

        if re.search('quick.?', brand, re.IGNORECASE):
            return BrandQuickstep()

        if re.search(r'[A-Z-a-z].*\.xlsx.?', brand, re.IGNORECASE):
            return BrandSaldoCrossDocking()


class Produto:
    def __init__(self, path):
        self.path = path

    def call_funcs(self, *args):
        lista_dicts = []
        for arg in args:
            try:
                print(arg['SKU'], arg['IDMARCA'], arg['SALDO'])
                exec_call = HauszMapa(arg['SKU'], arg['IDMARCA'], arg['SALDO'])
                dicts = exec_call.select_hausz_mapa_produtos()

                for items in dicts:

                    print(items['SKU'], items['SALDO'], items['IDMARCA'],
                          items['Marca'], items['NomeProduto'])

                    call_fornecedor_estoque = CallProcedureHauszMapa(
                        items['SKU'], items['SALDO'], items['IDMARCA'], items['Marca'], items['NomeProduto'])

                    dicts_values = call_fornecedor_estoque.call_procedure_atualiza_estoque_fornecedor()

                    lista_dicts.append(dicts_values)

                return lista_dicts
            except:
                pass

    def retorna_marca(self):
        lista_dicts = []
        valor = self.path
        marcas = MarcaFactory.get_marca(valor)

        dicts = marcas.get_saldos(valor)
        for items in dicts:
            if isinstance(items, dict):
                self.call_funcs(items)

            if isinstance(items, list):
                for item in items:
                    self.call_funcs(item)
