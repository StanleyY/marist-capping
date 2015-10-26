'use strict';

// Declare app level module which depends on views, and components
angular.module('capping', [
  'ngRoute',
  'capping.controllers'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.otherwise({redirectTo: '/view1'});
}]);
