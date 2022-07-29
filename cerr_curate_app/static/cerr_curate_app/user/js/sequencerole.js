
// If modifying a record: load the rorles saved in the database and display them
$(document).ready(function(){
    var rolebutton = document.getElementsByClassName(' rolebutton btn btn-primary')
    var prevInputs = JSON.parse(document.getElementById("id_roles").value)
    if (prevInputs){
        if (Object.keys(prevInputs.database[0]).length!=0) {
            addRoleStartup('Database',prevInputs) ;
            }
        if (Object.keys(prevInputs.software[0]).length!=0) {
            addRoleStartup('Software',prevInputs) ;
        }
        if (Object.keys(prevInputs.semanticasset[0]).length!=0) {
            addRoleStartup('SemanticAsset',prevInputs) ;
            }
        if (Object.keys(prevInputs.service[0]).length!=0) {
            addRoleStartup('ServiceApi',prevInputs) ;
        }
    }
    }
)
var createDatabase = function() {
    var rolebutton = document.getElementsByClassName(' rolebutton btn btn-primary')


}
var addRoleStartup = function(role, prevInputs) {

        $.ajax({
                url: "ajax/ajax_get_role/",
                type: "get",
                dataType:"json",
                data: { "role": role,
                },
            success: function(data){
              //  addToInputRole(role)
                $(".rolebutton").after(data);
                if (role=='Database'){
                    document.getElementById('id_database_label').value =  prevInputs.database[0].database_label
                    }
                if (role=='SemanticAsset'){
                    document.getElementById('id_semanticasset_label').value = prevInputs.semanticasset[0].semanticasset_label
                }
                if (role=='Software'){
                       for (const [key, value] of Object.entries(prevInputs.software[0])) {
                        document.getElementById('id_'+`${key}`).value = `${value}`
                }

                }
                if (role=='ServiceApi'){
                       for (const [key, value] of Object.entries(prevInputs.service[0])) {
                        document.getElementById('id_'+`${key}`).value = `${value}`
                }

                }

            },
            error: function(data){
                console.log(data)
            }
        })
}
var addRole = function(event) {

    var role =  $("#id_sequence-role_list").val()
        $.ajax({
                url: "ajax/ajax_get_role/",
                type: "get",
                dataType:"json",
                data: { "role": role,
                },
            success: function(data){
              //  addToInputRole(role)
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