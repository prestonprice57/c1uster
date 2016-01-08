angular.module('sampleApp', ['ngRoute', 'appRoutes', 'MainCtrl', 'NerdCtrl', 'NerdService', 'GeekCtrl', 'GeekService']);

function loadAvgValues() {
	var mydata = JSON.parse(avgValue);
}

function loadCoordinates() {
	var mydata = JSON.parse(coordinates);
}

function loadDv() {
	var mydata = JSON.parse(loadDv);
}

var customerApp = angular.module('customerApp', [])
    .controller('customerController', function($scope, $http) {
        $scope.customerData = {"customerInfo":{"age":false,"average":false,"degree":false,"gender":false, "income": false, "marital": false, "professional":false, "type": false, "common": false, "ownership": false, "limit": false}};

        $scope.submit = function() {
                console.log("hi");
                console.log("Executing Python");
              	$http.post('/cluster', $scope.customerData);
                console.log("End Python");
        }
    });