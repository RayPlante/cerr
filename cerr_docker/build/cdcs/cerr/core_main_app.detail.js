
$(document).ready(function() {
    $('#btn-previous-page').on('click',backToPreviousPage);
    $(".publish-record-btn").on('click', publish);

});

function backToPreviousPage() {
    window.history.back();
}

function publish(){
    var docId=window.location.href.split('=').pop();
    $.ajax({
        url : "rest/data/"+docId+"/assign/1",
        type : "PATCH",
        dataType: "json",
        success: function(data){
            $.notify("Resource published with success.", "success");
            setTimeout(function() {
                window.location.replace(window.location.origin + "/dashboard/workspaces");
            }, 2000 /* ms to delay for*/);
        },
        error:function(data){
            console.log(data)
            var myArr = JSON.parse(data.responseText);
            $.notify(myArr.message, "danger");
        }
    });
}

