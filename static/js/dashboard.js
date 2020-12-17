
var alldataUrl = '/names';
var individualdataUrl = '/individualdata';


function callApi(method, url, data) {
    $.ajax({
        method: method,
        url: url,
        data: data,
       
    });
};


function options_list(response){
	$(response).each(function(index,element){
		$("#select_name_options").append(`<option value = "${element}">${element}</option>`);
	});

};

$.get(alldataUrl , function(response){
		options_list(response);
	});



function show_record(element){
	$("#content").append(`<tr><th>${element[0]}</th><th>${element[1]}</th><th>${element[2]}</th><th>${element[3]}</th>
		<th>${element[4]}</th><th>${element[5]}</th><th>${element[6]}</th><th>${element[7]}</th></tr>`)
};




function options_for_selection() {
	$("#content tr").remove();
	var name = document.getElementById("select_name_options").value;
	// var res = [[[[individual]]]];
	// $.ajax({
 //          type: "POST",
 //          contentType: "application/json;charset=utf-8",
 //          url: "/takename",
 //          traditional: "true",
 //          data: JSON.stringify({op}),
 //          dataType: "json"
 //          });

	$.post(individualdataUrl,{"name" : name}, function(response){
		$(response).each(function(index,element){
		show_record(element);
	});
	});

	
}

document.getElementById("admin-page").onclick=function(){
	$("#login-control").show();
}

document.getElementById("close-button").onclick = function(){
	$("#login-control").hide();
}


document.getElementById("login-button").onclick = function(){
	$("#failed-alert").show();
}