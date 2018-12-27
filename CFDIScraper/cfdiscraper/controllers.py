#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Modulo que implementa los distintos controladores de CFDI Scraper
"""
__version__ = "1.0.0"
__author__ = "jorgeluisrmx "
__email__ = "jorgeluisrmx@gmail.com"
__copyright__ = "Copyright 2015, jorgeluisrmx"
__license__ = "GNU GPL 3"
__date__ = '16-nov-15'


import os
import zipfile
from cfdiparser import cfdi_doc_parser
from utils import sort_cfdi
from dataoutput import terminal_output


def pure_xml(tipofact):
    """
    Controlador que procesa todos los archivos CFDI-XML que se encuentren en el directorio desde el que la herramienta sea llamada
    
    :param tipofact: tipo de facturas EMITIDAS | RECIBIDAS
    :rtype: void
    """
    # captura de todos los XMLs en directorio
    xmls = [fname for fname in os.listdir('.') if fname.endswith(('.xml', '.XML'))]
    # lista de cfdi con diccionarios de datos condensados
    cfdis = []
    no_cfdis = []
    # procesamiento de xmls
    for xmlf in xmls:
        try:
            cfdis.append(cfdi_doc_parser(xmlf))
        except NameError:
            no_cfdis.append(xmlf)
    # ordenar la lista de CFDIs
    cfdis = sort_cfdi(cfdis)
    # presentación de la informacion
    terminal_output(cfdis, tipofact)
    # aviso de no_cfdis
    if no_cfdis:
        print '  ¡¡¡ATENCION!!!\n  Los siguientes archivos fueron clasificados como NO CFDI:\n'
        for name in no_cfdis:
            print '    * {}'.format(name)
        print '\n  EFECTUE REVISION MANUAL\n\n'


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def zipped_xml(tipofact):
    """
    Controlador que procesa todos los archivos CFDI-XML contenidos un archivo ZIP que se encuentra en el directorio desde el que se llama a la herramienta. Si existe mas de un archivo ZIP en el directorio la herramienta no detiene el proceso
    
    :param tipofact: tipo de facturas EMITIDAS | RECIBIDAS
    :rtype: void
    """
    # captura de todos los ZIPs en directorio
    zips = [fname for fname in os.listdir('.') if zipfile.is_zipfile(fname)]
    if not zips:
        print '\n\n  ... No se encontraron archivos ZIP en el directorio\n\n'
    elif len(zips) > 1:
        print '\n\n  ... Se encontro mas de un archivo ZIP en el directorio\n      Escoja uno y elimine el resto\n\n'
    else:
        # lista de cfdi con diccionarios de datos condensados
        cfdis = []
        no_cfdis = []
        with zipfile.PyZipFile(zips[0], 'r') as zf:
            for fname in zf.namelist():
                data = zf.read(fname)
                print fname
                try:
                    cfdis.append(cfdi_doc_parser(data, isfile=False))
                except NameError:
                    no_cfdis.append(fname)
        # ordenar la lista de CFDIs
        cfdis = sort_cfdi(cfdis)
        # presentación de la informacion
        terminal_output(cfdis, tipofact)
        # aviso de no_cfdis
        if no_cfdis:
            print '  ¡¡¡ATENCION!!!\n  Los siguientes archivos fueron clasificados como NO CFDI:\n'
            for name in no_cfdis:
                print '    * {}'.format(name)
            print '\n  EFECTUE REVISION MANUAL\n\n'

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


if __name__ == '__main__':
    zipped_xml('EMITIDAS')

