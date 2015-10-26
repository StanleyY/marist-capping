angular.module('cappingApp.controllers', [])

.controller('MainCtrl', function($scope, $http) {
  console.log("MAIN CONTROLLER STARTED");
  $scope.internalCourses = [];
  $scope.externalCourses = [];

  $scope.getAnotherCourse = function(){
    var req_to_ext = {
      method: 'GET',
      url: '/api/external',
      headers: {
        'Content-Type': undefined
      },
    };
    var req_to_int = {
      method: 'GET',
      url: '/api/internal',
      headers: {
        'Content-Type': undefined
      },
    };
    $http(req_to_ext).then(
      function(response){
        console.log("External Course requested.");
        $scope.externalCourses.push(response.data[0].fields);
      },
      function(response){console.log("Something broke");}
    );

    $http(req_to_int).then(
      function(response){
        console.log("External Course requested.");
        $scope.internalCourses.push(response.data[0].fields);
      },
      function(response){console.log("Something broke");}
    );
  }
  $scope.getAnotherCourse(); // REMOVE LATER
})
