Información de salida
=====================

El formato de salida para la información procesada se puede ajustar a las necesidades conforme estas se conozcan. A continuación se presentan las opciones viables en la versión mas reciente:


Fichas en terminal
~~~~~~~~~~~~~~~~~~

En terminal se presenta una ficha para cada CFDI, y mediante la tecla **enter** se avanza a la siguiente ficha. Existen __ casos para el formato de presentación de los datos de una ficha, dependiendo de la información contenida en el CFDI, estos son:

**a) Solo impuestos trasladados**

.. code-block:: html
   

    FACTURAS EMITIDAS

    # 1 / 5        INGRESO        29/05/15        A107
    
    De:   Razon Social del cliente (XXX000000X0X)
          Nombre comercial del cliente
        
    Para: Razon Social del cliente (XXX000000X0X)
          Nombre comercial del cliente
    
    SubTotal: $0.00
    ---------------------
         IVA: $0.00
        IEPS: $0.00
      totImp: $0.00
    ---------------------
       TOTAL: $0.00

**b) Impuestos trasladados + descuento**

.. code-block:: html
   

    FACTURAS EMITIDAS

    # 1 / 5        INGRESO        29/05/15        A107
    
    De:   Razon Social del cliente (XXX000000X0X)
          Nombre comercial del cliente
        
    Para: Razon Social del cliente (XXX000000X0X)
          Nombre comercial del cliente
    
    SubTotal: $0.00
    Desc:     $0.00
    ---------------------
         IVA: $0.00
        IEPS: $0.00
      totImp: $0.00
    ---------------------
       TOTAL: $0.00

**c) Impuestos trasladados y retenidos**

.. code-block:: html
   

    FACTURAS EMITIDAS

    # 1 / 5        INGRESO        29/05/15        A107
    
    De:   Razon Social del cliente (XXX000000X0X)
          Nombre comercial del cliente
        
    Para: Razon Social del cliente (XXX000000X0X)
          Nombre comercial del cliente
    
    SubTotal: $0.00
    ---------------------
      IMP. RETENIDOS
         ISR: $0.00
        IEPS: $0.00
      totRet: $0.00
    ---------------------
         IVA: $0.00
        IEPS: $0.00
      totImp: $0.00
    ---------------------
       TOTAL: $0.00

**d) Impuestos trasladados y retenidos + descuento**

.. code-block:: html
   

    FACTURAS EMITIDAS

    # 1 / 5        INGRESO        29/05/15        A107
    
    De:   Razon Social del cliente (XXX000000X0X)
          Nombre comercial del cliente
        
    Para: Razon Social del cliente (XXX000000X0X)
          Nombre comercial del cliente
    
    SubTotal: $0.00
    Desc:     $0.00
    ---------------------
      IMP. RETENIDOS
         ISR: $0.00
        IEPS: $0.00
      totRet: $0.00
    ---------------------
         IVA: $0.00
        IEPS: $0.00
      totImp: $0.00
    ---------------------
       TOTAL: $0.00
