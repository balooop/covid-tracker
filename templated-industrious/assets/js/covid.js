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

}

function negative() {
	var x = document.getElementById("posForm");
	x.style.display = "none";

	var x = document.getElementById("isolationSection");
	x.style.display = "block";

	window.delOrNot = false;
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

// called when 
function processForm() {
	if (document.getElementById("netid").value == false) {
		alert("Please input your NetID");
		return;
	}
	// CHANGE
	if (document.getElementById("posForm").style.display == "block" && document.getElementById("searchTextField0").value == "") {
		alert("Please input an address");
		return;
	}
	else {
		var lambda = new AWS.Lambda({ region: 'us-east-1', apiVersion: '2015-03-31' });
		// var addr;
		// if (document.getElementById("searchTextField0").value == "") addr = "NULL";
		// else addr = document.getElementById("searchTextField0").value;
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
		numCases = data.Payload;
		displayCasesforAddress(document.getElementById("searchTextField11").value, numCases);
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

	// add actual code below
	var numCases = 0;
	lambda.invoke(params, function (err, data) {
		if (err) console.log("err,err.stack");
		else console.log("success!");
		console.log(data);
		// numCases = data.Payload;
		// displayCasesforAddress(document.getElementById("searchTextField11").value, numCases);
	});
};

function updateChartTest() {
	// alert("in");
	// if (document.getElementById("reportForm").style.display == "none") return;
	// if (document.getElementById("businessReport").value == false) {
	// 	alert("Please input a reason");
	// 	return;
	// }
	var lambda = new AWS.Lambda({ region: 'us-east-1', apiVersion: '2015-03-31' });
	var params = {
		FunctionName: 'arn:aws:lambda:us-east-1:834423887668:function:customerIsMad',
		InvocationType: 'RequestResponse'
		// Payload: JSON.stringify({ })
	};

	// add actual code below
	var jsonOutput;
	lambda.invoke(params, function (err, data) {
		console.log(data.Payload);
		if (err) console.log("err,err.stack");
		else console.log("success!");
		jsonOutput = data.Payload;
		jsonOutput = data.Payload.replace(/\\/g, "");
		jsonOutput = JSON.parse(jsonOutput);
		console.log(jsonOutput);
		eshanSecondTest(jsonOutput);
	});
};


function finishSubmission() {
	var x = document.getElementById("thankYou");
	x.style.display = "block";

	var x = document.getElementById("formInner");
	x.style.display = "none";
}

function displayCasesforAddress(addr, count) {

	var x = document.getElementById("searchbyaddr");
	x.style.display = "none";

	var x = document.getElementById("casescardaddr");
	x.innerHTML = addr;

	var x = document.getElementById("casescardcount");
	x.innerHTML = count;

	var x = document.getElementById("casescard");
	x.style.display = "block";
}

function searchAgain() {
	var x = document.getElementById("searchbyaddr");
	x.style.display = "block";

	var x = document.getElementById("casescard");
	x.style.display = "none";
}

function eshanSecondTest(jsonOutput) {
	// alert(typeof jsonOutput);
	console.log(jsonOutput.series);
	// alert("hlllo")

	var x = document.getElementById("myChart");
	var y = document.getElementById("noDataText");

    let chartConfig = {
      type: 'treemap',
      options: {
        aspectType: 'palette',
        maxChildren: [4, 4, 4],
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
	// if (jsonOutput.series.length > 0) {
		x.style.display = "block";
		y.style.display = "none";
	// }
	// else {
	// 	x.style.display = "none";
	// 	y.style.display = "block";
	// }

}

function addSearchField(){
	if (window.addrNum == 9) return;
	window.addrNum++;
	var x = document.getElementById("field" + window.addrNum + "Div");
	x.style.display = "block";
}

function removeSearchField(){
	if (window.addrNum == 0) return;
	var x = document.getElementById("field" + window.addrNum + "Div");
	x.style.display = "none";
	document.getElementById("searchTextField2").setAttribute('value', '');
	window.addrNum--;
}



