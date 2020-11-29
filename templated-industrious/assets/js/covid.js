// Configure AWS SDK for JavaScript & set region and credentials
// Initialize the Amazon Cognito credentials provider
// CHANGE
AWS.config.region = 'us-east-1'; // Region
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
	IdentityPoolId: 'us-east-1:5e1316c9-1ebf-425d-80a9-9a0dc3dbba29',
});
AWS.config.apiVersions = {
	lambda: '2015-03-31',
	// other service API versions
};

function positive() {
	var x = document.getElementById("posForm");
	x.style.display = "block";

	var x = document.getElementById("isolationSection");
	x.style.display = "none";

	window.delOrNot = false;
	window.isPositive = true;

}

function negative() {
	var x = document.getElementById("posForm");
	x.style.display = "none";

	var x = document.getElementById("isolationSection");
	x.style.display = "block";

	window.delOrNot = false;
	window.isPositive = false;
}

function report() {
	var x = document.getElementById("reportForm");
	x.style.display = "block";
}
function noreport() {
	var x = document.getElementById("reportForm");
	x.style.display = "none";
}

function cleared() {
	window.delOrNot = true;
}
function notcleared() {
	window.delOrNot = false;
}

function processForm() {
	if (window.posClicked != true) {
		alert("Please specify if you have recently tested positive!");
		return;
	}
	if (document.getElementById("posForm").style.display == "block" && document.getElementById("searchTextField0").value == "") {
		alert("Please input an address!");
		return;
	}
	for (var i = 0; i <= window.addrNum; i++){
		if (window.isPositive == false) break;
		if (window.autofill[i] == false){
			alert("Please make sure to select your address from the dropdown!" + "(Location" + (i + 1) + ")");
			return;
		}
	}
	if (window.clearedFromIso != true && window.isPositive == false) {
		alert("Please specify if you have recently cleared from isolation!");
		return;
	}
	if (window.reportBus != 0 && window.reportBus != 1) {
		alert("Please specify if you would like to report a business for violating COVID-19 policies!");
		return;
	}
	if (window.reportBus == 0){
		if (window.autofill[10] == false){
			alert("Please make sure to select your address from the dropdown!");
			return;
		}
		if (document.getElementById("businessReport").value == ""){
			alert("Please make sure to give a reason for reporting!");
			return;
		}
	}
	if (document.getElementById("netid").value == false) {
		alert("Please input your NetID!");
		return;
	}
	else {
		var lambda = new AWS.Lambda({ region: 'us-east-1', apiVersion: '2015-03-31' });
		console.log(JSON.stringify({ "address0": document.getElementById("searchTextField0").value, "address1": document.getElementById("searchTextField1").value,
		"address2": document.getElementById("searchTextField2").value,"address3": document.getElementById("searchTextField3").value,
		"address4": document.getElementById("searchTextField4").value,"address5": document.getElementById("searchTextField5").value,
		"address6": document.getElementById("searchTextField6").value,"address7": document.getElementById("searchTextField7").value,
		"address8": document.getElementById("searchTextField8").value,"address9": document.getElementById("searchTextField9").value,
		"NetID": document.getElementById("netid").value.toLowerCase().trim(), "Delete": window.delOrNot }));
		var params = {
			// 
			FunctionName: 'arn:aws:lambda:us-east-1:834423887668:function:submit',
			InvocationType: 'RequestResponse',
			Payload: JSON.stringify({ "address0": document.getElementById("searchTextField0").value, "address1": document.getElementById("searchTextField1").value,
			"address2": document.getElementById("searchTextField2").value,"address3": document.getElementById("searchTextField3").value,
			"address4": document.getElementById("searchTextField4").value,"address5": document.getElementById("searchTextField5").value,
			"address6": document.getElementById("searchTextField6").value,"address7": document.getElementById("searchTextField7").value,
			"address8": document.getElementById("searchTextField8").value,"address9": document.getElementById("searchTextField9").value,
			"NetID": document.getElementById("netid").value.toLowerCase().trim(), "Delete": window.delOrNot })
		};
		lambda.invoke(params, function (err, data) {
			if (err) console.log(err);
			else console.log(data);
		});
	}
	if (customerComplaints() == -1) return;
	finishSubmission();
	updateChartTest();
};

function searchCasesByAddr() {
	if (document.getElementById("searchTextField11").value == false) {
		alert("Please input your address");
		return;
	}
	if (window.autofillSearch == false){
		alert("Please make sure to select your address from the dropdown!");
		return;
	}
	var lambda = new AWS.Lambda({ region: 'us-east-1', apiVersion: '2015-03-31' });
	var params = {
		FunctionName: 'arn:aws:lambda:us-east-1:834423887668:function:searchCases',
		InvocationType: 'RequestResponse',
		Payload: JSON.stringify({ "address": document.getElementById("searchTextField11").value })
	};
	var numCases = 0;
	lambda.invoke(params, function (err, data) {
		if (err) console.log(err);
		else console.log("success!");
		console.log(data);
		resp = data.Payload;
		resp = data.Payload.replace(/\\/g, "");
		resp = JSON.parse(resp);
		console.log(resp);
		console.log(resp['numCases']);
		displayCasesforAddress(resp);
	});
};

function customerComplaints() {
	if (document.getElementById("reportForm").style.display == "none") return;
	if (document.getElementById("searchTextField10").value == false) {
		alert("Please input an address");
		return -1;
	}
	if (document.getElementById("businessReport").value == false) {
		alert("Please input a reason");
		return -1;
	}
	var lambda = new AWS.Lambda({ region: 'us-east-1', apiVersion: '2015-03-31' });
	var params = {
		FunctionName: 'arn:aws:lambda:us-east-1:834423887668:function:customerComplaints',
		InvocationType: 'RequestResponse',
		Payload: JSON.stringify({ "Complaints": document.getElementById("businessReport").value, "Address": document.getElementById("searchTextField10").value })
	};

	var numCases = 0;
	lambda.invoke(params, function (err, data) {
		if (err) console.log("err,err.stack");
		else console.log("success!");
		console.log(data);
	});
};

function updateChartTest() {
	var lambda = new AWS.Lambda({ region: 'us-east-1', apiVersion: '2015-03-31' });
	var params = {
		FunctionName: 'arn:aws:lambda:us-east-1:834423887668:function:customerIsMad',
		InvocationType: 'RequestResponse'
	};

	var jsonOutput;
	lambda.invoke(params, function (err, data) {
		console.log(data.Payload);
		if (err) console.log("err,err.stack");
		else console.log("success!");
		jsonOutput = data.Payload;
		jsonOutput = data.Payload.replace(/\\/g, "");
		jsonOutput = JSON.parse(jsonOutput);
		console.log(jsonOutput);
		configureGraph(jsonOutput);
	});
};

function shameShame() {
	var lambda = new AWS.Lambda({ region: 'us-east-1', apiVersion: '2015-03-31' });
	var params = {
		FunctionName: 'arn:aws:lambda:us-east-1:834423887668:function:shamePeople',
		InvocationType: 'RequestResponse'
	};

	var jsonOutput;
	lambda.invoke(params, function (err, data) {
		console.log(data.Payload);
		if (err) console.log("err,err.stack");
		else console.log("success!");
		jsonOutput = data.Payload;
		jsonOutput = data.Payload.replace(/\\/g, "");
		jsonOutput = JSON.parse(jsonOutput);
		console.log(jsonOutput);
		console.log(jsonOutput["business"]);
		shamePeople(jsonOutput["people"]);
		shameBusiness(jsonOutput["business"]);
		document.getElementById("shameText").style.display = "none";
		document.getElementById("shameData").style.display = "block";
	});
};

function shamePeople(ppl){
	for (var i = 0; i < 10; i++){
		var x = document.getElementById("spreader" + i);
		if (ppl.length == 0 && i == 0){
			x.style.display = "block";
			x.innerHTML = "No one has reported having COVID-19! What liars."
			var x = document.getElementById("spreader" + 1);
			x.style.display = "block";
			x.innerHTML = "Check back later for updated data."
			i++;
		}
		else if (i < ppl.length){
			x.style.display = "block";
			x.innerHTML = (i+1) + ". " + ppl[i][0].substring(0,25) + " - " + ppl[i][1] + " Places(s)";
		}
		else {
			x.style.display = "none";
			x.innerHTML = "";
		}
	}
}

function shameBusiness(bus){
	for (var i = 0; i < 10; i++){
		var x = document.getElementById("business" + i);
		if (bus.length == 0 && i == 0){
			x.style.display = "block";
			x.innerHTML = "No troublesome businesses reported! We've got our eyes on you KAMS..."
			var x = document.getElementById("business" + 1);
			x.style.display = "block";
			x.innerHTML = "Check back later for updated data."
			i++;
		}
		else if (i < bus.length){
			x.style.display = "block";
			x.innerHTML = (i+1) + ". " + bus[i][0].split(",")[0] + " - " + bus[i][1] + " Case(s)";
		}
		else {
			x.style.display = "none";
			x.innerHTML = "";
		}
	}
}


function finishSubmission() {
	var x = document.getElementById("thankYou");
	x.style.display = "block";

	var x = document.getElementById("formInner");
	x.style.display = "none";
}

function displayCasesforAddress(resp) {
	var x = document.getElementById("searchbyaddr");
	x.style.display = "none";

	var x = document.getElementById("casescardaddr");
	x.innerHTML = resp["Address"];
	var x = document.getElementById("casescardcount");
	x.innerHTML = resp["numCases"];
	var x = document.getElementById("casescardcountmask");
	x.innerHTML = resp["maskViolations"];
	var x = document.getElementById("casescardcountsocdist");
	x.innerHTML = resp["sdViolations"];
	var x = document.getElementById("casescardcountsick");
	x.innerHTML = resp["sickViolations"];
	var x = document.getElementById("casescardcountdirt");
	x.innerHTML = resp["dirtyViolations"];
	if (resp["complaints"].length > 0){
		var x = document.getElementById("block1");
		x.style.display = "block";
		var x = document.getElementById("quote1");
		x.innerHTML = "\"" + resp["complaints"][0] + "\"";
	}
	else {
		for (var e = 1; e < 4; e++){
			var x = document.getElementById("block" + e);
			x.style.display = "none";
			var x = document.getElementById("quote" + e);
			x.innerHTML = "";
		}
	}


	if (resp["complaints"].length > 1){
		var x = document.getElementById("block2");
		x.style.display = "block";
		var x = document.getElementById("quote2");
		x.innerHTML = "\"" + resp["complaints"][1] + "\"";
	}
	else {
		for (var e = 2; e < 4; e++){
			var x = document.getElementById("block" + e);
			x.style.display = "none";
			var x = document.getElementById("quote" + e);
			x.innerHTML = "";
		}
	}
	
	if (resp["complaints"].length > 2){
		var x = document.getElementById("block3");
		x.style.display = "block";
		var x = document.getElementById("quote3");
		x.innerHTML = "\"" + resp["complaints"][2] + "\"";
	}
	else {
		for (var e = 3; e < 4; e++){
			var x = document.getElementById("block" + e);
			x.style.display = "none";
			var x = document.getElementById("quote" + e);
			x.innerHTML = "";
		}
	}

	var x = document.getElementById("casescard");
	x.style.display = "block";
}

function searchAgain() {
	var x = document.getElementById("searchbyaddr");
	x.style.display = "block";

	var x = document.getElementById("casescard");
	x.style.display = "none";

	document.getElementById('searchTextField11').value = "";
	$('html, body').animate({ scrollTop: 0 }, 'fast');
}

function configureGraph(jsonOutput) {
	console.log(jsonOutput.series);

	var x = document.getElementById("myChart");
	var y = document.getElementById("noDataText");
	// https://www.zingchart.com/docs/chart-types/treemap
    let chartConfig = {
      type: 'treemap',
      options: {
        aspectType: 'palette',
        maxChildren: [100, 100, 100],
        tooltipBox: {
          text: '%text'
        }
      },
      series: jsonOutput.series
    };
	zingchart.render({
		id: 'myChart',
		data: chartConfig,
		hideprogresslogo: true,
		output: 'canvas',
		height: '100%',
		width: '100%',
	  });
	  if (jsonOutput.series == null || jsonOutput.series.length < 1){
		x.style.display = "none";
		y.style.display = "block";
	  }
	  else{
		x.style.display = "block";
		y.style.display = "none";
	  }
}

function addSearchField(){
	if (window.addrNum == 9) return;
	window.addrNum++;
	var x = document.getElementById("field" + window.addrNum + "Div");
	x.style.display = "block";
	var x = document.getElementById("searchTextField" + window.addrNum);
	x.style.display = "block";
}

function removeSearchField(){
	if (window.addrNum == 0) {
		document.getElementById('searchTextField' + window.addrNum).value = "";
		return;
	}
	var x = document.getElementById("field" + window.addrNum + "Div");
	x.style.display = "none";
	var x = document.getElementById("searchTextField" + window.addrNum);
	x.style.display = "none";
	document.getElementById('searchTextField' + window.addrNum).value = "";
	window.addrNum--;
}
