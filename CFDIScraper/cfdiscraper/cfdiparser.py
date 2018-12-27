#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Modulo que implementa las funciones que generar el diccionario de informacion condensada del CFDI-XML para CFDI Scraper
"""
__version__ = "1.0.0"
__author__ = "jorgeluisrmx "
__email__ = "jorgeluisrmx@gmail.com"
__copyright__ = "Copyright 2015, jorgeluisrmx"
__license__ = "GNU GPL 3"
__date__ = '16-nov-15'


from xml.dom import minidom


def format_date(date):
    """
    Da formato a la cadena de texto que representa la fecha
    
    :param date: string con formato yyyy-mm-ddThh:mm:ss
    :type date: str
    :returns: string con formato dd/mm/yy
    :rtype: str 
    """
    base_date = date.split('T')[0]
    components = base_date.split('-')
    return u'{0}/{1}/{2}'.format(components[-1], components[-2], components[0][-2:])


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def format_quantity(quantity):
    """
    Da formato separado por comas a la cantidad recibida
    
    :param quantity: representacion en texto de la cantidad en formato 0.00
    :type quantity: str
    :returns: cantidad con formato de separacion por comas
    :rtype: str
    """
    return '{:,.2f}'.format(float(quantity))
    
    
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def cfdi_doc_parser(fname, isfile=True):
    """
    Realiza la extracción de interes de un documento XML correspondiente a un CFDI. Entrega como salida un diccionario con la informacion de interes
    
    :param fname: nombre del archivo CFDI-XML a ser procesado
    :returns: infromacion de interes condensada
    :rtype: dict
    """
    # XML document parsing
    if isfile:
        xmldoc = minidom.parse(fname)
    else:
        xmldoc = minidom.parseString(fname)
    data = {}                               # diccionario de retorno
    # procesamiento nodo Comprobante
    comprobante = xmldoc.getElementsByTagName('cfdi:Comprobante')
    if not comprobante:
        raise NameError('Comprobante node not found')
    data['id'] = comprobante[0].getAttribute('serie') + comprobante[0].getAttribute('folio')
    data['tipo'] = comprobante[0].getAttribute('tipoDeComprobante').upper()
    data['fecha'] = format_date(comprobante[0].getAttribute('fecha'))
    data['subtotal'] = format_quantity(comprobante[0].getAttribute('subTotal'))
    data['total'] = format_quantity(comprobante[0].getAttribute('total'))
    if comprobante[0].hasAttribute('descuento'):
        data['descuento'] = format_quantity(comprobante[0].getAttribute('descuento'))
    else:
        data['descuento'] = None
    # procesamiento nodo Emisor
    emisor = comprobante[0].getElementsByTagName('cfdi:Emisor')
    if not emisor:
        raise NameError('Emisor node not found')
    data['de'] = u'{0} ({1})'.format(emisor[0].getAttribute('nombre'), 
                                    emisor[0].getAttribute('rfc'))
    # procesamiento nodo Receptor
    receptor = comprobante[0].getElementsByTagName('cfdi:Receptor')
    if not receptor:
        raise NameError('Receptor node not found')
    data['para'] = u'{0} ({1})'.format(receptor[0].getAttribute('nombre'),
                                       receptor[0].getAttribute('rfc'))
    # procesamiento nodo Impuestos
    impuestos = comprobante[0].getElementsByTagName('cfdi:Impuestos')
    if not impuestos:
        raise NameError('Impuestos node not found')
        # impuestos TRASLADADOS
    if impuestos[0].hasAttribute('totalImpuestosTrasladados'):
        data['impuestosTrasladados'] = True
        data['tTotal'] = format_quantity(impuestos[0].getAttribute('totalImpuestosTrasladados'))
        traslados = impuestos[0].getElementsByTagName('cfdi:Traslado') 
        data['tIva'] = u'0.00'                          # presets
        data['tIeps'] = u'0.00'
        for tr in traslados:                            # traslados processing
            imp_name = tr.getAttribute('impuesto')
            if imp_name == 'IVA':
                data['tIva'] = format_quantity(tr.getAttribute('importe'))
            elif imp_name == 'IEPS':
                data['tIeps'] = format_quantity(tr.getAttribute('importe'))
    else:
        data['impuestosTrasladados'] = False
        data['tTotal'] = u'0.00'
        data['tIva'] = u'0.00'
        data['tIeps'] = u'0.00'
        # impuestos RETENIDOS
    data['impuestosRetenidos'] = False 
    # finaliza procesaminto de CFDI-XML
    return data

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


if __name__ == '__main__':
    print cfdi_doc_parser('726A068F-ABDC-4560-90B3-CD905589C278.xml')


