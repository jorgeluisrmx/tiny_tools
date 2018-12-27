# StarUMLExportReNamer


Rename the files inside the "all export" directory generate by StartUML. Remove the ID-number at the end of the filename, e.g:
    
    BigPicture__BigPicture_Flow_5.png
    
becomes,

    BigPicture__BigPicture_Flow.png
    

## Usage

Execute command in terminal, from the forlder containing the exported file to be renamed

    umlrename
    

# Alis registration

    alias umlrename='python /.../NatureTech/TinyTools/StarUMLExportReNamer/umlrenamer.py'
    
