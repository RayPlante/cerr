function addItem(){
  var ul = document.getElementById("dynamic-list");
  var candidate = document.getElementById("candidate");
  if (candidate.value !=='')
    var li = document.createElement("li");
    var index = ul.getElementsByTagName("li").length
    li.setAttribute('id','keyword_'+index);
    li.appendChild(document.createTextNode(candidate.value));
    li.innerHTML += "<span class=\"rmBtn\" onclick=\"removeItem()\"><i class=\"fas fa-times\"></i><i id=\"circleFa\" class=\"far fa-circle\"></i></span"
    ul.appendChild(li);
    candidate.value = ''
}

function removeItem(){
    var id = event.target.closest("li");

	var ul = document.getElementById("dynamic-list");
  var candidate = document.getElementById("candidate");
  var item = document.getElementById(candidate.value);
  ul.removeChild(id);
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
            console.log('HELLO ERROR')
                console.log(data)
            }
        })
}


