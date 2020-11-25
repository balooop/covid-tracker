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
	// if (document.getElementById("posForm").style.display == "block" && document.getElementById("searchTextField0").value != "") {
		var lambda = new AWS.Lambda({ region: 'us-east-1', apiVersion: '2015-03-31' });
		var params = {
			// 
			FunctionName: 'arn:aws:lambda:us-east-1:834423887668:function:submit',
			InvocationType: 'RequestResponse',
			Payload: JSON.stringify({ "address": document.getElementById("searchTextField0").value, "NetID": document.getElementById("netid").value.toLowerCase().trim(), "Delete": window.delOrNot })
		};
		lambda.invoke(params, function (err, data) {
			if (err) console.log(err);
			else console.log(data);
		});
	// }
	// else if (document.getElementById("posForm").style.display == "block"){
	// 	alert("Please input an address");
	// 	return;
	// }
	customerComplaints();
	finishSubmission();
};

function searchCasesByAddr() {
	if (document.getElementById("searchTextField2").value == false) {
		alert("Please input your address");
		return;
	}
	var lambda = new AWS.Lambda({ region: 'us-east-1', apiVersion: '2015-03-31' });
	var params = {
		FunctionName: 'arn:aws:lambda:us-east-1:834423887668:function:searchCases',
		InvocationType: 'RequestResponse',
		Payload: JSON.stringify({ "address": document.getElementById("searchTextField2").value })
	};
	var numCases = 0;
	lambda.invoke(params, function (err, data) {
		if (err) console.log(err);
		else console.log("success!");
		console.log(data);
		numCases = data.Payload;
		displayCasesforAddress(document.getElementById("searchTextField2").value, numCases);
	});
};

function customerComplaints() {
	if (document.getElementById("reportForm").style.display == "none") return;
	if (document.getElementById("businessReport").value == false) {
		alert("Please input a reason");
		return;
	}
	var lambda = new AWS.Lambda({ region: 'us-east-1', apiVersion: '2015-03-31' });
	var params = {
		FunctionName: 'arn:aws:lambda:us-east-1:834423887668:function:searchCases',
		InvocationType: 'RequestResponse',
		Payload: JSON.stringify({ "Complaints": document.getElementById("businessReport").value })
	};

	// add actual code below
	var numCases = 0;
	lambda.invoke(params, function (err, data) {
		if (err) console.log("err,err.stack");
		else console.log("success!");
		console.log(data);
		numCases = data.Payload;
		displayCasesforAddress(document.getElementById("searchTextField2").value, numCases);
	});
};

function finishSubmission() {
	var x = document.getElementById("thankYou");
	x.style.display = "block";

	var x = document.getElementById("formInner");
	x.style.display = "none";

	// alert(document.getElementById("searchTextField0").value);
	// alert(document.getElementById("searchTextField1").value);

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

function eshanSecondTest() {
	var myConfig = {
		"type": "treemap",
		"options": {
			"split-type": "balanced",
			"color-type": "palette",
			"palette": ["#1ab7ea", "#ff5700", "#cd201f", "#25D366", "#FFFC00", "#3aaf85", "#f1c40f", "#17968e",
				"#f7b362", "#F58F84", "#5B3256", "#317589", "#6B9362"]
		},
		"plotarea": {
			"margin": "0 0 35 0"
		},
		"series": [{
			"text": "North America - ",
			"children": [{
				"text": "United States",
				"children": [{
					"text": "Texas",
					"value": 90
				}]
			},
			{
				"text": "Canada",
				"value": 113
			},
			{
				"text": "Mexico",
				"value": 78
			}
			]
		},
		{
			"text": "Europe",
			"children": [{
				"text": "France",
				"value": 42
			},
			{
				"text": "Spain",
				"value": 28
			}
			]
		},
		{
			"text": "Africa",
			"children": [{
				"text": "Egypt",
				"value": 22
			},
			{
				"text": "Congo",
				"value": 38
			}
			]
		},
		{
			"text": "Asia",
			"children": [{
				"text": "India",
				"value": 92
			},
			{
				"text": "China",
				"value": 68
			}
			]
		},
		{
			"text": "South America",
			"children": [{
				"text": "Brazil",
				"value": 42
			},
			{
				"text": "Argentina",
				"value": 28
			}
			]
		},
		{
			"text": "Australia (continent)",
			"children": [{
				"text": "Australia (country)",
				"value": 121
			},
			{
				"text": "New Zealand",
				"value": 24
			}
			]
		}
		]
	};
	var x = document.getElementById("myChart");
	var y = document.getElementById("noDataText");
	if (myConfig.series.length > 0) {
		x.style.display = "block";
		y.style.display = "none";
	}
	else {
		x.style.display = "none";
		y.style.display = "block";
	}

	zingchart.render({
		id: 'myChart',
		data: myConfig,
		height: '100%',
		width: '100%'
	});

	//   document.getElementById('treemap-layout').addEventListener('change', function(e) {
	// 	myConfig.options['split-type'] = e.srcElement.value;
	// 	zingchart.exec('myChart', 'setdata', {
	// 	  data: myConfig
	// 	});
	//   })
}