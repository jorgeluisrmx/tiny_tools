# Recipe to create Forecasting: Principles and Practice Epub form its website


1. Download ebook content using ```wget```.
    
    wget -k -p -r -l 1 https://otexts.org/fpp2/index.html

1. Move contents dir (fpp2) to working directorie's root.
1. Save https://otexts.org/fpp2/index.html as "FPP_index.html" to generate index containing chapter titles and original urls.
1. Edit "FPP_index.html" to preserve the summary list, including the original url of each section.
1. Change data-level of preface to "0"
1. Clean section 2.1 title (delete code tag)
1. Run code in fpp.ipynb
1. Create a cover for the epub in calibre epub editor (Tools -> Add Cover)


## Requirements

* [Pypub](https://github.com/wcember/pypub)
    
    sudo pip install pypub