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
		res.sendfile('./public/sampleJson.py');
	}); 

	app.post('/cluster', function(req, res) {
		console.log(req.body);
	});
};