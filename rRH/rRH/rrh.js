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


var OFFICE = 0, JOB = 1, AUTH = 2, OCC = 3;
var workforce = new RHWorkforce();


document.addEventListener('DOMContentLoaded', function() {
        var createSummButton = document.getElementById('createSumm');
        createSummButton.addEventListener('click', create_summary, false);
        var createDownloadCsvButton = document.getElementById('downloadCsv');
        createDownloadCsvButton.addEventListener('click', download_csv, false);
    },
    false);

// - - - - - - - - - - - - - - - - - -

function create_summary() {
    chrome.tabs.getSelected(null, function(tab) {
        chrome.tabs.executeScript(tab.id,
            {file: 'extract_workforce.js'},
            function(results) {
                if (!results) {
                    alert("rRH executed in a blank page");
                }
                else if (results[0]!=null) {
                    // process results
                    workforce.load_data(results[0]);
                    // create result section
                    create_summary_sections();
                    // show downloadCsv button
                    var downloadButton = document.getElementById('downloadCsv');
                    downloadButton.className = "button button-red";
                }
            });
    });
};

// - - - - - - - - - - - - - - - - - -

function download_csv() {
    var a = document.getElementById("downloadLink");
    var date = new Date();
    var blob = new Blob([workforce.csv()], {type: "application/json"})
    var url = window.URL.createObjectURL(blob);
    a.href = url;
    a.download = "rRH_" + date.toISOString().substring(0, 10) + ".csv";
    a.click();
    window.URL.revokeObjectURL(url);
};

// - - - - - - - - - - - - - - - - - -

function create_summary_sections() {
    var results = document.getElementById("results");
    results.innerHTML = "";
    // creating coverage section
    var h2 = document.createElement("h2");
    h2.textContent = "Porcentaje de covertura";
    h2.className = "subtitle";
    var sect_coverage = document.createElement("section");
    sect_coverage.appendChild(h2);
    sect_coverage.appendChild(coverage_table());
    results.appendChild(sect_coverage);

    // hr line
    results.appendChild(document.createElement("hr"));

    // creating bono vacants section
    var h2 = document.createElement("h2");
    h2.textContent = "Vacantes Bono";
    h2.className = "subtitle";
    var sect_bono_vact = document.createElement("section");
    sect_bono_vact.appendChild(h2);
    sect_bono_vact.appendChild(vacant_table(workforce.bono_vacants));
    results.appendChild(sect_bono_vact);

    // hr line
    results.appendChild(document.createElement("hr"));

    // creating non bono vacants section
    var h2 = document.createElement("h2");
    h2.textContent = "Vacantes NO Bono";
    h2.className = "subtitle";
    var sect_nobono_vact = document.createElement("section");
    sect_nobono_vact.appendChild(h2);
    sect_nobono_vact.appendChild(vacant_table(workforce.non_bono_vacants));
    results.appendChild(sect_nobono_vact);
};

// - - - - - - - - - - - - - - - - - -

function coverage_table() {
    var head_title = ["Oficina", "Autorizado", "Ocupado", "Proporcion", "%"];

    // table element
    var tbl = document.createElement("table");

    // header
    var thed = document.createElement("thead");
    var tr = document.createElement('tr');
    for (var i in head_title) {
        var th = document.createElement('th');
        th.appendChild(document.createTextNode(head_title[i]));
        tr.appendChild(th);
    }
    thed.appendChild(tr);
    tbl.appendChild(thed);

    // table body
    var tbdy = document.createElement("tbody");
    for (var key in workforce.coverage) {
        var c = workforce.coverage[key]
        var tr = document.createElement('tr');
        var td1 = document.createElement('td');
        var td2 = document.createElement('td');
        var td3 = document.createElement('td');
        var td4 = document.createElement('td');
        var td5 = document.createElement('td');
        td1.appendChild(document.createTextNode(key));
        td2.appendChild(document.createTextNode(c.auth));
        td3.appendChild(document.createTextNode(c.occ));
        td4.appendChild(document.createTextNode(c.prop));
        td5.appendChild(document.createTextNode(c.percent));
        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td3);
        tr.appendChild(td4);
        tr.appendChild(td5);
        tbdy.appendChild(tr);
    }

    // total coverage
    var tr = document.createElement('tr');
    var td1 = document.createElement('th');
    var td2 = document.createElement('th');
    var td3 = document.createElement('th');
    var td4 = document.createElement('th');
    var td5 = document.createElement('th');
    td2.appendChild(document.createTextNode(workforce.total_coverage.auth));
    td3.appendChild(document.createTextNode(workforce.total_coverage.occ));
    td4.appendChild(document.createTextNode(workforce.total_coverage.prop));
    td5.appendChild(document.createTextNode(workforce.total_coverage.percent));
    tr.appendChild(td1);
    tr.appendChild(td2);
    tr.appendChild(td3);
    tr.appendChild(td4);
    tr.appendChild(td5);
    tbdy.appendChild(tr);
    tbl.appendChild(tbdy);

    return tbl;
};

// - - - - - - - - - - - - - - - - - -

function vacant_table(data) {
    var head_title = ["Oficina", "Puesto", "Autorizado", "Ocupado", "Vancantes"];

    // table element
    var tbl = document.createElement("table");

    // header
    var thed = document.createElement("thead");
    var tr = document.createElement('tr');
    for (var i in head_title) {
        var th = document.createElement('th');
        th.appendChild(document.createTextNode(head_title[i]));
        if (i==4) {
            th.className = "attention";
        }
        tr.appendChild(th);
    }
    thed.appendChild(tr);
    tbl.appendChild(thed);

    // table body
    var tbdy = document.createElement("tbody");
    for (var key in data) {
        for (var i in data[key]) {
            var v = data[key][i];
            var tr = document.createElement('tr');
            var td1 = document.createElement('td');
            var td2 = document.createElement('td');
            var td3 = document.createElement('td');
            var td4 = document.createElement('td');
            var td5 = document.createElement('td');
            td1.appendChild(document.createTextNode(v.office));
            td2.appendChild(document.createTextNode(v.job));
            td3.appendChild(document.createTextNode(v.auth));
            td4.appendChild(document.createTextNode(v.occ));
            td5.appendChild(document.createTextNode(v.auth - v.occ));
            td5.className = "attention";
            tr.appendChild(td1);
            tr.appendChild(td2);
            tr.appendChild(td3);
            tr.appendChild(td4);
            tr.appendChild(td5);
            tbdy.appendChild(tr);
        }
    }
    tbl.appendChild(tbdy);

    return tbl;
};

// - - - - - - - - - - - - - - - - - -

function round(value, decimals) {
  return Number(Math.round(value+'e'+decimals)+'e-'+decimals);
};

// - - - - - - - - - - - - - - - - - -

// Workforce model
function RHWorkforce() {
    this.positions;
    this.offices;
    this.bono_vacants = {};
    this.non_bono_vacants = {};
    this.coverage = {};
    this.total_coverage = {}
    this.bono_positions = ["LIDER DE CUADRILLA", "PROMOTOR DE CAMBACEO", "PROMOTOR DE TELEMARKETING", "PROMOTOR DE VENTAS", "SUPERVISOR DE TELEMARKETING", "COORDINADOR DE CAMBACEO", "SUPERVISOR DE VENTAS"]
    // , "TECNICO INSTALADOR", "CELULA DE VENTAS", 

    this.load_data = process_workforce;
    this.coverage2csv = coverage_csv_repr;
    this.vacant2csv = vacant_csv_repr;
    this.csv = export_csv;
};

    // - - - - - -

function process_workforce(raw_wf) {
    // processing raw data
    // generates an array of objects {office: , job: , auth: , occ:}
    var positions = new Array();
    raw_wf.forEach(function(d) {
        positions.push({'office': d[0], 'job': d[1], 'auth': +d[2], 'occ': +d[3]});
    });
    this.positions = positions;

    // extract offices
    var offs = Array.from(workforce.positions, (d) => d.office);
    this.offices = offs.filter(function(value, index, self) {
        return self.indexOf(value) === index;
    });
    if (this.offices.indexOf("Guadalajara") != -1) {
        this.offices.splice(this.offices.indexOf("Guadalajara"), 1)
    }
    if (this.offices.indexOf("Tecoman") != -1) {
        this.offices.splice(this.offices.indexOf("Tecoman"), 1)
    }
    if (this.offices.indexOf("Jalostotitlan") != -1) {
        this.offices.splice(this.offices.indexOf("Jalostotitlan"), 1)
    }
    if (this.offices.indexOf("Tepatitlan") != -1) {
        this.offices.splice(this.offices.indexOf("Tepatitlan"), 1)
    }

    // create offices elements in bono and non_bono vacants
    for (var i in this.offices) {
        this.bono_vacants[this.offices[i]] = new Array();
        this.non_bono_vacants[this.offices[i]] = new Array();
    }

    // coverage object
    for (var i in this.offices) {
        this.coverage[this.offices[i]] = {'auth': 0, 'occ': 0};
    }

    // extract vacants
    for (var i in this.positions) {
        var d = this.positions[i];
        // if office in offices list
        if (this.offices.indexOf(d.office) != -1) {
            // if it is a bono job
            if (this.bono_positions.indexOf(d.job) != -1) {
                this.coverage[d.office].auth += d.auth;
                this.coverage[d.office].occ += d.occ;
                // vacant positions
                if (d.auth > d.occ) {
                    this.bono_vacants[d.office].push(d);
                }
            }
            // non bono vacants
            else if (d.auth > d.occ) {
                this.non_bono_vacants[d.office].push(d);
            }
        }
    }

    // calculate coverage
    this.total_coverage['auth'] = 0;
    this.total_coverage['occ'] = 0;
    for (var key in this.coverage) {
        var d = this.coverage[key]
        this.total_coverage.auth += d.auth;
        this.total_coverage.occ += d.occ;
        d['prop'] =  d.occ.toString() + "/" + d.auth.toString();
        d['percent'] = round(100.0 * d.occ / d.auth, 2);
    }

    this.total_coverage['prop'] =  this.total_coverage.occ.toString() + "/" + this.total_coverage.auth.toString();
    this.total_coverage['percent'] = round(100.0 * this.total_coverage.occ / this.total_coverage.auth, 2);

};

    // - - - - - -

function export_csv() {
    var date = new Date();
    var csv_repr = "Porcentaje de covertura (" + date.toISOString().substring(0, 10) + "),\n,";
    csv_repr += this.coverage2csv();
    csv_repr += "\n,\n,\nVacantes Bono,\n,";
    csv_repr += this.vacant2csv(this.bono_vacants);
    csv_repr += "\n,\n,\nVacantes NO Bono,\n,";
    csv_repr += this.vacant2csv(this.non_bono_vacants);

    return csv_repr;
};

    // - - - - - -

function coverage_csv_repr() {
    var csv_repr = "\n" + ["Oficina", "Autorizado", "Ocupado", "Proporcion", "%"].join();
    for (var key in workforce.coverage) {
        var c = workforce.coverage[key]
        csv_repr += "\n" + [key, c.auth, c.occ, c.prop, c.percent].join();
    }
    csv_repr += "\nTOTAL," + [workforce.total_coverage.auth, workforce.total_coverage.occ, workforce.total_coverage.prop, workforce.total_coverage.percent].join();
    return csv_repr;
};

    // - - - - - -

function vacant_csv_repr(data) {
    var csv_repr = "\n" + ["Oficina", "Puesto", "Autorizado", "Ocupado", "Vancantes"].join();
    for (var key in data) {
        for (var i in data[key]) {
            var v = data[key][i];
            csv_repr += "\n" + [v.office, v.job, v.auth, v.occ, v.auth - v.occ].join()
        }
    }
    return csv_repr;
};
