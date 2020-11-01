function positive(){
	var x = document.getElementById("posForm");
	  x.style.display = "block";
}

function negative(){
	var x = document.getElementById("posForm");
	  x.style.display = "none";
}

function report(){
	var x = document.getElementById("reportForm");
	  x.style.display = "block";
}
function noreport(){
	var x = document.getElementById("reportForm");
		x.style.display = "none";
}


function finishSubmission(){
	var x = document.getElementById("thankYou");
	x.style.display = "block";

	var x = document.getElementById("formInner");
	x.style.display = "none";

	// alert(document.getElementById("searchTextField0").value);
	// alert(document.getElementById("searchTextField1").value);

}