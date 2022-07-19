var addRole = function(event) {

    var role =  $("#id_role_list").val()
        $.ajax({
                url: "../ajax/ajax_get_role",
                type: "get",
                dataType:"json",
                data: { "role": role,
                },
            success: function(data){
                $(".rolebutton").after(data);

            },
            error: function(data){
                console.log(data)
            }
        })
}

var removeRole = function() {

    var id = event.target.closest("#role_form")
    id.remove()
}


