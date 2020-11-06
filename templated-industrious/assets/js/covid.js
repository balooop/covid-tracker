// Configure AWS SDK for JavaScript & set region and credentials
// Initialize the Amazon Cognito credentials provider
AWS.config.region = 'us-east-2'; // Region
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
	IdentityPoolId: 'us-east-2:fad8bf8b-3e89-436a-8120-f35b1c8c3d7e',
});
AWS.config.apiVersions = {
	lambda: '2015-03-31',
	// other service API versions
};

function positive() {
	var x = document.getElementById("posForm");
	x.style.display = "block";
}

function negative() {
	var x = document.getElementById("posForm");
	x.style.display = "none";
}

function report() {
	var x = document.getElementById("reportForm");
	x.style.display = "block";
}
function noreport() {
	var x = document.getElementById("reportForm");
	x.style.display = "none";
}

// called when 
function processForm() {
	var lambda = new AWS.Lambda({ region: 'us-east-2', apiVersion: '2015-03-31' });
	var params = {
		FunctionName: 'arn:aws:lambda:us-east-2:834423887668:function:submit',
		InvocationType: 'RequestResponse',
		Payload: JSON.stringify({ "address": document.getElementById("searchTextField0").value })
	};
	lambda.invoke(params, function (err, data) {
		if (err) console.log("err,err.stack");
		else console.log("data");
	});
	finishSubmission();
};

function searchCasesByAddr() {
	var lambda = new AWS.Lambda({ region: 'us-east-2', apiVersion: '2015-03-31' });
	var params = {
		FunctionName: 'arn:aws:lambda:us-east-2:834423887668:function:searchCases',
		InvocationType: 'RequestResponse',
		Payload: JSON.stringify({ "address": document.getElementById("searchTextField2").value })
	};
	// alert(document.getElementById("searchTextField2").value);
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