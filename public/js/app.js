angular.module('sampleApp', ['ngRoute', 'appRoutes', 'MainCtrl', 'NerdCtrl', 'NerdService', 'GeekCtrl', 'GeekService']);

var formApp = angular.module('customerApp', [])
    .controller('customerController', function($scope) {
        $scope.customerData = {}; 
    });