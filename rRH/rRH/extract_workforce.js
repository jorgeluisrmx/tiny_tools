/**
 * MIT License
 * Copyright (c) 2017 Jorge Luis Rodriguez <jorgeluisrmx@gmail.com>

 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

/* Create and returs an array of arrays containing each
 * row of interest form the id="tblPlantilla" table
 */

/* var OFFICE = 0, JOB = 1, AUTH = 2, OCC = 3;*/
var OFFICE = 1, JOB = 3, AUTH = 4, OCC = 5;

// ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

function extract_workforce(table) {
    var wf_array = new Array();
    var contents;

    // creates an array of arrays with table info
    for (var i = 1, row; row = table.rows[i]; i++) {
        contents = Array.from(row.cells, (d) => d.textContent);
        if (contents.length==7) {
            wf_array.push(Array(contents[OFFICE],contents[JOB],contents[AUTH],contents[OCC]));
        }
    }

    return wf_array;
};

// ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

function main() {
    var workforce = null;
    var table = document.getElementById("tableplantilla");

    if (!table) {
        alert("rRH: tableplantilla not found. Schema has changed. Please contact technical support");
    }
    else {
        // capture first row
        var frow = Array.from(table.rows[0].cells, (d) => d.textContent);
        // squema validation
        if ((frow.length==7) & (frow[OFFICE]=="Oficina") & (frow[JOB]=="Puesto") & (frow[AUTH]=="Autorizado") & (frow[OCC]=="Contrado")) {
            // capture info
            workforce = extract_workforce(table);
        }
        else {
            alert("rRH: Schema on workforce table has changed. Please contact technical support");
        }
    }

    return workforce;
};

// ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

main();
