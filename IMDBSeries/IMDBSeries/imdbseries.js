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


/*
localStore CheatSheet

localStorage.length
localStorage.setItem("dos", {"a": "125", "b": 435});
localStorage.key(0);
localStorage.getItem("dos");
localStorage.removeItem("dos");

for (var i = 0; i<localStorage.length; i++) {
    var key = localStorage.key(i);
    alert(localStorage.getItem(key));
}
*/


// global var to store series data
var seriesData = new Array();


document.addEventListener('DOMContentLoaded', function() {

        var addSeriesButton = document.getElementById('addSeries');
        addSeriesButton.addEventListener('click', add_series, false);
        var removeSeriesButton = document.getElementById('removeSeries');
        removeSeriesButton.addEventListener('click', remove_series, false);
        
        // populate select element in UI
        fill_seriesNameSelect();

        // configure seriesData push callback
        seriesData.push = function(item) {
            Array.prototype.push.call(this, item);
            this.onPush(item);
        };
        
        seriesData.onPush = function(obj) {
            // Do your stuff here (ex: alert(this.length);)
            create_summary_table(this);
        };
        
        // execute data web scraping function
        extract_series_data();
        /*var extractInfoButton = document.getElementById('extractInfo');
        extractInfoButton.addEventListener('click', extract_series_data, false);*/
    },
    false);

// - - - - - - - - - - - - - - - - - -

//localStorage.setItem("dos", {"a": "125", "b": 435});
//a = localStorage.getItem("dos");
//localStorage.removeItem("dos");

function add_series() {
    var seriesName = document.getElementById('seriesname').value;
    var seriesUrl = document.getElementById('episodesurl').value;
    if ( (seriesName!="") && (seriesUrl!="") ) {
        localStorage.setItem(seriesName, seriesUrl);
        alert(seriesName + " has been registered");
    }
    document.getElementById('seriesname').value = "";
    document.getElementById('episodesurl').value = "";
    fill_seriesNameSelect();
};

// - - - - - - - - - - - - - - - - - -

function remove_series() {
    var selectName = document.getElementById('seriesNameSelect');
    var seriesName = selectName.options[selectName.selectedIndex].value;
    if (seriesName!="") {
        localStorage.removeItem(seriesName);
        alert(seriesName + " has been removed");
        fill_seriesNameSelect();
    }
    else {
        selectName.selectedIndex = 0;
    }
};

// - - - - - - - - - - - - - - - - - -

function fill_seriesNameSelect() {
    /*
     * Fill the options of the select element in the UI 
     */
    
    var selectName = document.getElementById('seriesNameSelect');
    // removing elements
    for (var i = selectName.options.length -1; i>=0; i--) {
        selectName.remove(i)
    }
    // adding options
    var opt = document.createElement('option');
    opt.value = "";
    opt.innerHTML = "";
    selectName.appendChild(opt);
    for (var i = 0; i<localStorage.length; i++) {
        opt = document.createElement('option');
        opt.value = localStorage.key(i);
        opt.innerHTML = localStorage.key(i);
        selectName.appendChild(opt);
    }
};

// - - - - - - - - - - - - - - - - - -

function extract_series_data() {
    /* Loop through series dictionary to extract info about each,
     * finally it is displayed in the UI   
     */
     
    var sName;
    // seriesData structure = [series1Array, series2Array, ...]
    // seriesArray structure = [seriesName, [episodeData, date, name], [...], ...]
    for (var i = 0; i<localStorage.length; i++) {
        sName = localStorage.key(i);
        get_series_info(sName, localStorage.getItem(sName));
    }
};

// - - - - - - - - - - - - - - - - - -

function get_series_info(seriesName, seriesUrl) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            var holder = document.createElement('div');
            // xhr.responseText contains the requested page
            holder.innerHTML = xhr.responseText;
            series_dom_scraping(seriesName, holder);
        }
    };
    xhr.open("GET", seriesUrl, true);
    xhr.send();
};

// - - - - - - - - - - - - - - - - - -

function series_dom_scraping(seriesName, holder) {

    var main_div = holder.getElementsByClassName('eplist')[0];
    var ep_divs = main_div.children;
    var episodes = new Array();
    for (var i = 0; i < ep_divs.length; i++) {
        var raw_episode = ep_divs[i];
        var airdate = raw_episode.getElementsByClassName('airdate')[0].textContent.trim();
        if (airdate != "") {
            if (airdate.length < 9) {
                airdate = null;
            }
            else if (airdate.length < 10) {
                var tmp_date = new Date(airdate);
                airdate = new Date(tmp_date.getYear(), tmp_date.getMonth() + 1, 0);
            }
            else {
                airdate = new Date(airdate);
            }
        }
        else {
            airdate = null;
        }
        var epseason = raw_episode.getElementsByClassName('image')[0].getElementsByTagName('div')[1].textContent.trim().replace(', ', '').replace('p', '');
        var title = raw_episode.getElementsByClassName('info')[0].getElementsByTagName('a')[0].textContent.trim();
    episodes.push([epseason, airdate, title]);
    }

    // setting date limits
    var max_date = new Date();
    max_date.setDate(max_date.getDate() + 7);
    var min_date = new Date();
    min_date.setDate(min_date.getDate() - 21);

    // filling array with episodes of interest
    var epOfInterst = new Array();
    epOfInterst.push(seriesName);
    episodes.forEach( function(d) {
        if ((d[1]!=null) && (d[1]<=max_date) && (d[1]>=min_date)) {
            epOfInterst.push([d[0], d[1].toDateString(), d[2]]);
        }  
    } );
    seriesData.push(epOfInterst);
};

// - - - - - - - - - - - - - - - - - -

function create_summary_table(seriesData) {
    var head_title = ["S|Ep", "AirDate", "Title"];
    
    var summary_div = document.getElementById("seriesdates");
    summary_div.innerHTML = "";
    
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
    for (var s_i in seriesData) {
        for (var pos in seriesData[s_i]) {
            var tr = document.createElement('tr');
            if (pos==0) {
                var td1 = document.createElement('td');
                atd = document.createElement('a');
                atd.textContent = seriesData[s_i][pos];
                atd.href = localStorage.getItem( seriesData[s_i][pos] );
                atd.target = "_blank";
                atd.className = "ser_name";
                td1.appendChild(atd);
                td1.colSpan = "3";
                tr.appendChild(td1);
            }
            else {
                for (var j in seriesData[s_i][pos]) {
                    var tdn = document.createElement('td');
                    tdn.appendChild(document.createTextNode(seriesData[s_i][pos][j]));
                    tr.appendChild(tdn);
                }
            }
            tbdy.appendChild(tr);
        }
    }
    tbl.appendChild(tbdy);

    // table style
    tbl.style.marginTop = "25px";
    tbl.style.marginBottom = "50px";

    summary_div.appendChild(tbl);
};

