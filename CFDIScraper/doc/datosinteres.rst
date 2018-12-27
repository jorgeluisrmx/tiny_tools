.. _datos_de_interes:

Datos de interés
================

El diccionario que alamacena los datos de interés esta estructurado de la siguiente manera:

.. code-block:: python
    :linenos:

    doi = {
        'id': serie + folio,
        'tipo': ingreso | egreso,
        'fecha': DD/MM/AAAA,
        'de': emisor nombre + rfc,
        'para': receptor nombre + rfc,
        'subtotal': y.00,
        'descuento': y.00 | None,
        'impuestosTrasladados': True | False,
        'tTotal': y.00,
        'tIva': y.00,
        'tIeps': y.00,
        'impuestosRetenidos': True | False,
        'rTotal': y.00,
        'rIsr': y.00,
        'rIeps': y.00,
        'total': y.00
    }
        
