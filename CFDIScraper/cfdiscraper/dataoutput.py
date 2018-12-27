#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Modulo que implementa las funciones relacionadas con la creacion de la salida con formato de los datos colectados por CFDI Scraper
"""
__version__ = "1.0.0"
__author__ = "jorgeluisrmx "
__email__ = "jorgeluisrmx@gmail.com"
__copyright__ = "Copyright 2015, jorgeluisrmx"
__license__ = "GNU GPL 3"
__date__ = '16-nov-15'


import os


def terminal_data_card(data, tipofact, num, total):
    """
    Formatea una cadena de texto unicode que representa la ficha de informacion de un CFDI
    
    :param data: diccionario de infromacion condensada del CFDI
    :param tipofact: tipo de facturas EMITIDAS | RECIBIDAS
    :param num: numero de ficha en la secuencia completa
    :param total: total de fichas a procesar
    :returns: string unicode con la ficha formateada del CFDI
    :rtype: str
    """
    # Impuestos trasladados y retenidos + descuento
    if data['descuento'] and data['impuestosRetenidos']:
        card = "Not yet implemented case: t, r + d"
    # Impuestos trasladados + descuento
    elif data['descuento']:
        card = u'''\n\n    FACTURAS {0}

    # {1} / {2}        {tipo}        {fecha}        {id}
    
    De:    {de}

    Para:  {para}

    SubTotal: ${subtotal}
    Desc:     ${descuento}
    ---------------------
         IVA: ${tIva}
        IEPS: ${tIeps}
      totImp: ${tTotal}
    ---------------------
       TOTAL: ${total}
\n'''.format(tipofact, num, total, **data)
    # Impuestos trasladados y retenidos
    elif data['impuestosRetenidos']:
        card = "Not yet implemented case: t, r"
    # Solo impuestos trasladados
    else:
        card = u'''\n\n    FACTURAS {0}

    # {1} / {2}        {tipo}        {fecha}        {id}
    
    De:    {de}

    Para:  {para}

    SubTotal: ${subtotal}
    ---------------------
         IVA: ${tIva}
        IEPS: ${tIeps}
      totImp: ${tTotal}
    ---------------------
       TOTAL: ${total}
\n'''.format(tipofact, num, total, **data)
    return card

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def terminal_output(cfdis, tipofact):
    """
    Controla la visualizacion de resultados en terminal, mostrando una ficha a la vez
    
    :param cfdis: lista de diccionarios de datos condensados de CFDI
    :param tipofact: tipo de facturas EMITIDAS | RECIBIDAS
    :rtype: void
    """
    for i, cfdi in enumerate(cfdis):
        os.system('clear')
        print terminal_data_card(cfdi, tipofact, i+1, len(cfdis))
        if i+1 < len(cfdis):
            res = raw_input('Siguiente [s/n]: ')
            if res =='n': break
        else:
            print '   ... REVISION FINALIZADA ...\n\n'
    

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


if __name__ == '__main__':
    data = {'para': u'Leobardo D\xedaz Vertti (DIVL740515E13)', 'tipo': u'INGRESO', 'ieps': u'0.00', 'fecha': u'28/07/15', 'de': u'JORGE LUIS RODRIGUEZ MENDOZA (ROMJ850217NGA)', 'totalImpuestos': u'2400.00', 'total': u'17400.00', 'subtotal': u'15000.00', 'id': u'A7', 'iva': u'2400.00'}
    print terminal_data_card(data,1,5)


    
