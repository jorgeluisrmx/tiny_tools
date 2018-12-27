#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Modulo que implementa las funciones que sirven como punto de entrada para la herramienta
"""
__version__ = "1.0.0"
__author__ = "jorgeluisrmx "
__email__ = "jorgeluisrmx@gmail.com"
__copyright__ = "Copyright 2015, jorgeluisrmx"
__license__ = "GNU GPL 3"
__date__ = '15-nov-15'


import argparse
from controllers import pure_xml, zipped_xml


def ep_cfdi():
    """
    Inicia el procesamiento de todos los CFDI-XML que se encuentren en el directorio desde el que la herramienta es llamada
    
    :rtype: void
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", help="indica que los CFDI a procesar son RECIBIDOS", action='store_const', const='RECIBIDAS', default='EMITIDAS')
    args = parser.parse_args()
    # llamada al procesador de CFDI
    pure_xml(args.r)
    
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


def ep_zip_cfdi():
    """
    Inicia al procesamiento de un archivo ZIP compuesto por CFDI-XMLs, y que se encuentre en el directorio desde el que se llama a la herramienta
    
    :rtype: void
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", help="indica que los CFDI a procesar son RECIBIDOS", action='store_const', const='RECIBIDAS', default='EMITIDAS')
    args = parser.parse_args()
    # llamada al procesador de CFDI
    zipped_xml(args.r)

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


if __name__ == '__main__':
    ep_zip_cfdi()


