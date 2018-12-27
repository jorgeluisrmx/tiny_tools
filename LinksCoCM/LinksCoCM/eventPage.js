var menuContxtItem = {
    "id": "linkGetter",
    "title": "CreateLink",
    "contexts": ["selection"]
};

function copyToClipboard(text) {
    const input = document.createElement('input');
    input.style.position = 'fixed';
    input.style.opacity = 0;
    input.value = text;
    document.body.appendChild(input);
    input.select();
    document.execCommand('Copy');
    document.body.removeChild(input);
};

chrome.contextMenus.create(menuContxtItem);

chrome.contextMenus.onClicked.addListener(function(clickData){
    if (clickData.menuItemId == "linkGetter" && clickData.selectionText) {
        chrome.tabs.query({"active": true, "lastFocusedWindow": true}, function(tabs){
            var tablink = tabs[0].url;
            copyToClipboard("[" + clickData.selectionText+"](" + tablink + ")");
        });
    }
});