var allmonthUrl = '/months';
var monthrecordUrl = '/monthdata';
var joinUrl = '/joinpage';
var leaveUrl = '/leavepage';
var paidUrl = '/paidpage';
var loanUrl = '/loanpage';
var editUrl = '/editpage';
var allnameUrl = '/names';

function options_list(response){
	$(response).each(function(index,element){
		$("#select_month_options").append(`<option value = "${element}">${element}</option>`);
	});

};

function names_list(response){
	$(response).each(function(index,element){
		$(".select_name_options").append(`<option value = "${element}">${element}</option>`);
	});

};

$.get(allnameUrl , function(response){
		names_list(response);
	});

$.get(allmonthUrl , function(response){
		options_list(response);
	});


function show_record(element){
	$("#content").append(`<tr><td>${element[0]}</td><td>${element[1]}</td><td>${element[2]}</td><td>${element[3]}</td>
		<td>${element[4]}</td><td>${element[5]}</td><td>${element[6]}</td><td>${element[7]}</td><td><button class="editing">Edit</button></td></tr>`)
};


function options_for_selection() {
	$("#content tr").remove();
	var mon = document.getElementById("select_month_options").value;


	$.post(monthrecordUrl,{"month" : mon}, function(response){
		$(response["complete"]).each(function(index,element){
		show_record(element);
	});
		var u = response["updates"]
		info(u[0],u[1],u[2],u[3],u[4]);
	});

}

function myfunc(item){
 	document.getElementById("edit-submit-button").onclick = function(){
 	var i_d = $('input[name="edit-id"]').val();
 	var name = $('input[name="edit-name"]').val();
 	var cd = $('input[name="edit-cd"]').val();
 	var installment = $('input[name="edit-installment"]').val();
 	var interest = $('input[name="edit-interest"]').val();
 	var total = $('input[name="edit-total"]').val();
 	var loan = $('input[name="edit-loan"]').val();
 	 $.post(editUrl,{"id" : i_d,"name" : name ,"cd" : cd, "installment" : installment,"interest" : interest,"total" : total,"loan" : loan, "month":item[7].innerText},function(response){
 		alert(response);
 	});
	item[0].innerText = i_d;
	item[1].innerText = name;
 	item[2].innerText = cd;
 	item[3].innerText = installment;
 	item[4].innerText = interest;
 	item[5].innerText = total;
 	item[6].innerText = loan;
	return false;
	}
	}

$(document).on('click',".editing",function(){
	var item = $(this).closest("tr").find("td");
	$("#edit").show();

	myfunc(item);
 }); 


document.getElementById("edit-close-button").onclick = function(){
	$("#edit").hide();
	}

function info(m,i,l,c,t_members){
	document.getElementById("cur-month").innerHTML = m;
	document.getElementById("total_loan").innerHTML = l;
	document.getElementById("total_interest").innerHTML = i;
	document.getElementById("c_in_hand").innerHTML = c;
	document.getElementById("total_members").innerHTML = t_members;
}


document.getElementById("join-submit-button").onclick = function(){
	var name = $('input[name="join-name"]').val();
	var cd = $('input[name="join-cd"]').val();

	$.post(joinUrl,{"name" : name,"cd" : cd},function(response){
		alert(response);
	});

	return false;
}

document.getElementById("leave-submit-button").onclick = function(){
	var name = document.getElementById("leave-name").value;

	$.post(leaveUrl,{"name" : name},function(response){
		alert(response);
	});
	return false;
}

document.getElementById("paid-submit-button").onclick = function(){
	var name = document.getElementById("paid-name").value;
	var installment = $('input[name="paid-installment"]').val();
	
	$.post(paidUrl,{"name" : name , "installment" : installment},function(response){
		alert(response);
	});

	return false;
}

document.getElementById("loan-submit-button").onclick = function(){
	var name = document.getElementById("loan-name").value;
	var amount = $('input[name="loan-amount"]').val();
	var installment = $('input[name="loan-installment"]').val();

	$.post(loanUrl,{"name" : name , "amount" : amount,"installment" : installment},function(response){
		alert(response);
	});

	return false;
}


document.getElementById("join-page").onclick = function(){
	$("#bg-content").css("filter","blur(2px)");
	$("#join").show();
}

document.getElementById("leave-page").onclick = function(){
	$("#bg-content").css("filter","blur(2px)");
	$("#leave").show();
}
document.getElementById("paid-page").onclick = function(){
	$("#bg-content").css("filter","blur(2px)");
	$("#paid").show();
}
document.getElementById("loan-page").onclick = function(){
	$("#bg-content").css("filter","blur(2px)");
	$("#loan").show();
}



document.getElementById("join-close-button").onclick = function(){
	$("#join").hide();
	$("#bg-content").css("filter","none");
}

document.getElementById("leave-close-button").onclick = function(){
	$("#leave").hide();
	$("#bg-content").css("filter","none");
}
document.getElementById("paid-close-button").onclick = function(){
	$("#paid").hide();
	$("#bg-content").css("filter","none");
}
document.getElementById("loan-close-button").onclick = function(){
	$("#loan").hide();
	$("#bg-content").css("filter","none");
}


document.getElementById("home-page").onclick = function(){
	window.location.href = '/';
}

document.getElementById("print-page").onclick = function(){
	$("#secret-info").hide();
	window.print();
	$("#secret-info").show();
}
