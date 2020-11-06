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

// called when 
function processForm() {
	var lambda = new AWS.Lambda({region: 'us-east-2', apiVersion: '2015-03-31'});
	var params = {
		FunctionName: 'arn:aws:lambda:us-east-2:834423887668:function:submit',
		InvocationType: 'RequestResponse',
		Payload: JSON.stringify({"address": document.getElementById("searchTextField0").value})
	};
	lambda.invoke(params, function(err,data){
		if (err) 	alert("err,err.stack");
		else		alert("success!");
	});
	finishSubmission(); 
};

function finishSubmission(){
	var x = document.getElementById("thankYou");
	x.style.display = "block";

	var x = document.getElementById("formInner");
	x.style.display = "none";

	// alert(document.getElementById("searchTextField0").value);
	// alert(document.getElementById("searchTextField1").value);

}