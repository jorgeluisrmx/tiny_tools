var attab;
var atcontent;

document.addEventListener('DOMContentLoaded',
    function() {
        var createSummButton = document.getElementById('createSumm');
        createSummButton.addEventListener('click', create_summary, false);
    },
    false);


// - - - - - - - - - - - - - - - - - -

// this
chrome.extension.onRequest.addListener(
  function(request, sender, sendResponse) {
    // LOG THE CONTENTS HERE
    alert("en el manehador de la response")
    alert(request.content);
  });

function create_summary() {
    // this
    chrome.tabs.getSelected(null, function(tab) {
      alert("aca ando");
      // Now inject a script onto the page
      chrome.tabs.executeScript(tab.id, {
           code: "chrome.extension.sendRequest({content: document.body.innerHTML}, function(response) { alert('success'); });"
       }, function() { alert('done'); });

    });
};

// - - - - - - - - - - - - - - - - - -

function create_summary2() {
    alert("hi there1.1!");
    chrome.tabs.executeScript({
    code: 'alert("hola");'
  });
  chrome.tabs.executeScript({
        code: 'var x=["a", "b", "c"]; x'
    }, function(results) {
        alert(results);
        atcontent = results;
    });
};

// - - - - - - - - - - - - - - - - - -

function process_tab(tab) {
    alert("hi from tab");
    attab = tab;
};

// - - - - - - - - - - - - - - - - - -

function prueba_dom(content) {
    alert("from prueba dom");
    atcontent = content;
}

// http://stackoverflow.com/questions/19758028/chrome-extension-get-dom-content
// https://developer.chrome.com/extensions/content_scripts
