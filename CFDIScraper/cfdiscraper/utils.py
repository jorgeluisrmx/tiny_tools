#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Modulo que implenta funciones utilitarias necesarias para CFDI Scraper
"""
__version__ = "1.0.0"
__author__ = "jorgeluisrmx "
__email__ = "jorgeluisrmx@gmail.com"
__copyright__ = "Copyright 2015, jorgeluisrmx"
__license__ = "GNU GPL 3"
__date__ = '11-ago-15'


def sort_cfdi(cfdis):
    """
    Construye una lista ordenada de diccionarios de datos condensados de CFDIs comenzando con los ingresos para finalizar con egresos
    
    :param cfdis: lista de diccionarios de datos condensados de CFDI
    :returns: lista ordenada de diccionarios de datos condensados de CFDIs
    :rtype: list
    """
    ingresos = []
    egresos = []
    for cfdi in cfdis:
        if cfdi['tipo'] == 'INGRESO':
            ingresos.append(cfdi)
        else:
            egresos.append(cfdi)
    return ingresos + egresos
