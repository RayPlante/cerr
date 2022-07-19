
// If modifying a record: load the keywords saved in the database and display them
$(document).ready(function(){
    var ul = document.getElementById("dynamic-list");
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

// On click the add button
function addItem(){
  var candidate = document.getElementById("candidate");
  if (candidate.value !==''){
      displayItem(candidate.value)
      addToInput(candidate.value)
  }
  candidate.value = ''
}

// Display the keywords above the input field
function displayItem(candidate) {
    var ul = document.getElementById("dynamic-list");
    var index = ul.getElementsByTagName("li").length
    var li = document.createElement("li");
    li.setAttribute('id','keyword_'+index);
    li.appendChild(document.createTextNode(candidate));
    li.innerHTML += "<span class=\"rmBtn\" onclick=\"removeItem()\"><i class=\"fas fa-times\"></i><i id=\"circleFa\" class=\"far fa-circle\"></i></span"
    ul.appendChild(li);
}

// Add keywords to <input> to save them in the database later
function addToInput(candidate) {
    var ul = document.getElementById("dynamic-list");
    var index = ul.getElementsByTagName("li").length
    var prevInputs = document.getElementById("id_keywords");
    var pi = prevInputs["value"]
    if (index != 1 ){
        prevInputs.setAttribute('value',pi + ','+candidate);
    }
    else {
    prevInputs.setAttribute('value',candidate);
    }
}

// Remove an item from <input> value. Set display to 'none'
function removeItem(){
    var id = event.target.closest("li");
    id.setAttribute('style','display:none');
	var ul = document.getElementById("dynamic-list");
    keyword_to_remove = (id.innerHTML.split('<'))[0]
    var prevInputs = document.getElementById("id_keywords");
    var index = (id['id'].split('_'))[1]
    if (index == 0){
        var prevInputsVal = prevInputs["value"].replace(keyword_to_remove+',','')
    }
    else {
        var prevInputsVal = prevInputs["value"].replace(','+keyword_to_remove,'')
    }
    prevInputs.setAttribute('value',prevInputsVal);
}

var saveElement = function(event) {
    event.preventDefault();
    var list =  $("#dynamic-list").children()
        $.ajax({
            url: saveListUrl,
            data: { "list": list,
                  },
            dataType:"json",
            type: "post",
            success: function(data){
            },
            error: function(data){
            }
        })
}