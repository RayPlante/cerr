 $(document).ready(function(){
    fieldNames=['title','publisher','description','url','audience','product','material','lifecycle','keywords','role']
    fieldNames.forEach((fieldName, index) => {
        addFunctions(fieldName)
    });
 })

 function addFunctions(fieldName){
     var title = document.getElementById("div_id_"+fieldName);
     title.setAttribute('onclick',"openDetails('"+fieldName+"_details')")
 }

 function openDetails(id) {
     var detailsOpen = document.getElementById(id);
     detailsOpen.setAttribute('open',"True")
     setTimeout(function(){
        detailsOpen.removeAttribute('open')
    }, 3000);
 }