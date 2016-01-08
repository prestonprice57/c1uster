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
        $scope.customerData = {"customerInfo":{"gender":false,"income":false,"age":false}}

        $scope.submit = function() {
                console.log("hi");
              	console.log($scope.customerData.customerInfo);
                console.log("Executing Python");
              	$http.get('/cluster'); 
                console.log("End Python");
				        $scope.customerData = avgValue;
        }
    });
