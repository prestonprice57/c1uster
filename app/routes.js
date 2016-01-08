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

	app.get('/cluster', function(req, res) {
		console.log("Cluster is running");
		console.log("Executing Python");
		
		// var sys = require('sys')
		// var exec = require('child_process').exec;
		// var child;
		// // executes `pwd`
		require('child_process').execSync("python clustering.py 0 3 1 2 3", function (error, stdout, stderr) {
			console.log(stdout);
		  if (error !== null) {
		  }
		});
		console.log("Python code complete")
		res.sendfile('./public/index.html');
	});
};