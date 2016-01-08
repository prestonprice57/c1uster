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
	app.get('/jsontest', function(req, res) {
		
	}); 

	app.get('/cluster', function(req, res) {
		//console.log(req.body);
		console.log("Cluster is running");
		var exec = require('child_process').exec;
		console.log("Executing Python");
		exec('python3 ./clustering.py 0 3 1 2 3', function (error, stdout, stderr) {
			if (error !== null) {
				console.log(stdout);
			}
		});
		console.log("Python code complete")
	});
};