module.exports = function(app) {
	// server routes ===========================================================
	// handle things like api calls
	// authentication routes

	// frontend routes =========================================================
	// route to handle all angular requests
	app.get('/', function(req, res) {
		console.log("called here");

		res.sendfile('./public/index.html');
	});

	// testing json 
	//app.get('/jsontest', function(req, res) {
		
	//}); 

	app.post('/cluster', function(req, res) {
		var queryData = req.body;
		console.log("Cluster is running");
		console.log("THIS IS THE DATA");
		console.log(queryData["customerInfo"]["age"]);
		console.log("---");
		console.log("Executing Python");
		var arg1 = "3";
		var args = "";
		if(queryData["customerInfo"]["type"] == true) {
			arg1 = arg1 + "3";
		} else if(queryData["customerInfo"]["common"] == true) {
			arg1 = arg1 + "2";
		} else if(queryData["customerInfo"]["ownership"] == true) {
			arg1 = arg1 + "1";
		} else if(queryData["customerInfo"]["limit"] == true) {
			arg1 = arg1 + "0";
		}

		if(queryData["customerInfo"]["age"] == true) {
			args = args + " 1";
		}
		if(queryData["customerInfo"]["average"] == true) {
			args = args + " 2";
		}
		if(queryData["customerInfo"]["degree"] == true) {
			args = args + " 3";
		}
		if(queryData["customerInfo"]["gender"] == true) {
			args = args + " 4";
		}
		if(queryData["customerInfo"]["income"] == true) {
			args = args + " 5";
		}
		if(queryData["customerInfo"]["marital"] == true) {
			args = args + " 6";
		}
		if(queryData["customerInfo"]["professional"] == true) {
			args = args + " 7";
		}

		console.log(arg1);
		console.log(args);

		require('child_process').execSync("python clustering.py 0 " + arg1 + args, function (error, stdout, stderr) {
			console.log(stdout);
		  if (error !== null) {
		  }
		});
		console.log("Python code complete");
	});
};