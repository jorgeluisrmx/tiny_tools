#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Extracts from XML invoice v3.3 the required info to generate CFDI printable version
"""

from __future__ import unicode_literals
import os
import argparse
import json
from pprint import pprint
from bs4 import BeautifulSoup


# percent encoding dictionary
pe = {
"!": "%21",
"#": "%23",
"$": "%24",
"&": "%26",
"'": "%27",
"(": "%28",
")": "%29",
"*": "%2A",
"+": "%2B",
",": "%2C",
"/": "%2F",
":": "%3A",
";": "%3B",
"=": "%3D",
"?": "%3F",
"@": "%40",
"[": "%5B",
"]": "%5D"
}

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def percent_econding(content):
    for key, value in pe.iteritems():
        content = content.replace(key, value)
    return content

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def filename_generation(xml_path):
    """
    Generates the outputfile name, and check that the xml_path corresponds to a valid file
    """
    
    # clean xml_path
    in_fpath = xml_path.replace('file://', '') if xml_path.startswith('file:///') else xml_path
    # xml exists
    assert os.path.isfile(in_fpath), "XML file does no exists"
    # generate output path
    dir_path, filename = os.path.split(in_fpath)
    # return im_fpath, out_fpath
    return in_fpath, os.path.join(dir_path, filename.split('-')[0] + '-info.json')


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def extract_invoice_info(in_fpath, out_fpath, verbose=False):
    """
    Extract the required info from the XML and generate the condensed file
    """
    
    info = {}

    # parse xml file
    with open(in_fpath, 'r') as fin:
        xml_doc = fin.read()
        soup = BeautifulSoup(xml_doc, 'lxml')
    comprobante = soup.find('cfdi:comprobante')
    # assert invoice version
    assert comprobante.get('version') == '3.3', 'Invoice version does not match'
    
    # info content generation
        # fecha de emision
    info['fecha_emision'] = comprobante['fecha'].replace('T', ' ')
        # folio fiscal
    timbre = comprobante.find('cfdi:complemento').find('tfd:timbrefiscaldigital')
    info['folio_fiscal'] = timbre['uuid']
        # sello CFDI
    info['sello_cfdi'] = timbre['sellocfd']
        # sello SAT
    info['sello_sat'] = timbre['sellosat']
        # no serie certificado SAT
    info['serie_cert_sat'] = timbre['nocertificadosat']
        # fecha de cerfificacion
    info['fecha_certificacion'] =  timbre['fechatimbrado']
        # cadena original
    info['cadena_original'] = '||{}|{}|{}|{}|{}|{}||'.format(timbre['version'], info['folio_fiscal'], info['fecha_certificacion'], timbre['rfcprovcertif'], info['sello_cfdi'], info['serie_cert_sat'])
        # QR code
    emisor = comprobante.find('cfdi:emisor')['rfc']
    receptor = comprobante.find('cfdi:receptor')['rfc']
    total = comprobante['total']
    contenido = 'https://verificacfdi.facturaelectronica.sat.gob.mx/default.aspx?id={}&re={}&rr={}&tt={}&fe={}'.format(info['folio_fiscal'], emisor, receptor, total, info['sello_cfdi'][-8:])
    info['qr'] = '=image("http://chart.apis.google.com/chart?cht=qr&chs=250x250&chld=H|4&chl={}")'.format(percent_econding(contenido))
    
    # output file generation
    if verbose:
        pprint(info)
    with open(out_fpath, 'w') as fout:
        json.dump(info, fout)

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def args_parser():
    """
    Creates and configure the parser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("xml_path", type=str, help="path to source xml file")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    return parser


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def main():
    """
    Entry point to invoiceinfoextractor
    """
    parser = args_parser()
    args = parser.parse_args()
    im_fpath, out_fpath = filename_generation(args.xml_path)
    extract_invoice_info(im_fpath, out_fpath, args.verbose)


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


if __name__ == '__main__':
    main()
