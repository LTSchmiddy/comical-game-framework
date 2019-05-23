
// Functions:
// function iterDict(inDict){
//     for (var key in inDict) {
//
//     }
// }

var globalRecentString = "";
var globalArchiveString = "";

// Execution Start:
function loadRecentBlogPostList () {
    $.post("getJson", {"dataID":"blogRecent"}, function (recentStr) {
        $.post("getJson", {"dataID":"blogArchive"}, function (archiveStr) {
            // console.log(recentStr);
            // console.log(archiveStr);


            var retVal = "";


            recentData = JSON.parse(recentStr);
            archiveData = JSON.parse(archiveStr);


            // Let's Build the List on the Page:
            for (var i = 0; i < recentData["recentPosts"].length; i++) {

                var postYear = recentData["recentPosts"][i]["Year"];
                var postMonth = recentData["recentPosts"][i]["Month"];
                var postDay = recentData["recentPosts"][i]["Day"];
                var fileName = recentData["recentPosts"][i]["Post"];

                retVal = retVal + "<a href=\"getServerBlogPost?Year=" + postYear + ";Month=" + postMonth + ";Day=" + postDay + ";FileName=" + fileName + "\">" + archiveData[postYear][postMonth][postDay][fileName]["Title"] + "</a><br/>";
            }



            document.getElementById("blogPostList").innerHTML = retVal;
        });
    });



}

loadRecentBlogPostList ();
