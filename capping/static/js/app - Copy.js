'use strict';

var app = angular.module('cappingApp', ['ngRoute', 'cappingApp.controllers']);

app.config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
});

app.config(function ($routeProvider,$locationProvider) {
});
