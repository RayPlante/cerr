
// If modifying a record: load the rorles saved in the database and display them
$(document).ready(function(){
    var ul = $("#id_sequence-role_list").val()
    var prevInputs = document.getElementById("id_keywords");
    if (prevInputs){
        if (prevInputs.value) {
            val = prevInputs.value.split(',')
            for (v in val) {
                displayItem(val[v],ul)
            }
        }
    }
})

var addRole = function(event) {

    var role =  $("#id_sequence-role_list").val()
        $.ajax({
                url: "ajax/ajax_get_role/",
                type: "get",
                dataType:"json",
                data: { "role": role,
                },
            success: function(data){
                addToInputRole(role)
                $(".rolebutton").after(data);

            },
            error: function(data){
                console.log(data)
            }
        })
}

var removeRole = function() {

    var id = event.target.closest("#role_form");
    id.setAttribute('style','display:none');
    role = id.innerHTML.split('b')[1].split('>')[1]
    role = role.split('<')[0].trimRight().replace('\'','')
    var prevInputs = document.getElementById("id_roles")
    var index = (prevInputs['value'].split(',')).length
    var prevInputsVal = (prevInputs['value']).replace(role,'')
    // Check if there is a ',' at the end or at the beginning
    if (prevInputsVal.charAt(prevInputsVal.length - 1) == ","){
        var prevInputsVal = prevInputsVal.slice(0,-1)
    }
    if (prevInputsVal[0]==","){
        var prevInputsVal = prevInputsVal.slice(0,1)
    }
    prevInputs.setAttribute('value',prevInputsVal);

    id.remove()
}

var saveRoleForms = function(event) {

    var role_form = console.log(event)

}
function addToInputRole(role) {
    var Inputs = document.getElementById("id_roles");
    var pi = Inputs["value"]
    if (Inputs["value"]==''){
    Inputs.setAttribute('value',role)
    }
    else{
    Inputs.setAttribute('value',pi+','+role)
    }

}