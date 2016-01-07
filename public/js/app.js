angular.module('sampleApp', ['ngRoute', 'appRoutes', 'MainCtrl', 'NerdCtrl', 'NerdService', 'GeekCtrl', 'GeekService']);

var customerApp = angular.module('customerApp', [])
    .controller('customerController', function($scope) {
        $scope.customerData = {"customerInfo":{"gender":false,"income":false,"age":false}}

        $scope.submit = function() {
              console.log($scope.customerData.customerInfo);
            };
    });