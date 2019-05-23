function getItems() {

    $.get("getItemList", function (data, status) {


        var select = document.getElementById("itemList");
        console.log("Getting Items:");

        console.log(data)

        var itemJson = JSON.parse(data);

        for(var i in itemJson) {
            var option = document.createElement('option');
            console.log(i)
            option.text = i;
            option.value = itemJson[i];
            select.add(option, 0);
        }
    });

}


function clearItemList() {

    var select = document.getElementById("itemList");
    var length = select.options.length;
    for (i = 0; i < length; i++) {
      select.options[i] = null;
    }
}

function reloadItemList() {
    clearItemList();
    getItems();

}

function giveToPlayer() {
    var itemList = document.getElementById("itemList");
    var selectedText = itemList.options[itemList.selectedIndex].text;

    $.get("giveToPlayer", {"item": selectedText}, function (data, status) {});
}

function getItemScript(fileName) {

    $.get("loadItemScript", {"itemFile": fileName}, function (data, status) {


        var textbox = document.getElementById("itemScript");
        console.log("Getting Items Script:");

        console.log(data)


    });

    $("#itemScript").load("loadItemScript", {"itemFile": fileName})

}

function updateItemScript() {

    var itemList = document.getElementById("itemList");
    var selectedText = itemList.options[itemList.selectedIndex].value;

    getItemScript(selectedText);
}


function saveItemScript() {
    var itemList = document.getElementById("itemList");
    var selectedText = itemList.options[itemList.selectedIndex].value;

    var itemScript = document.getElementById("itemScript");

    $.get("saveItemScript", {"itemFile": selectedText, "text": itemScript.value}, function (data, status) {});
}

function newItemScript() {

    var fileName = prompt("Please Enter a File Name:", "NewItem");

    if (fileName == null || fileName == "") {
        return;
    }

    $.get("createNewItem", {"newItemName": fileName}, function (data, status) {});
}





getItems()

// updateItemScript()