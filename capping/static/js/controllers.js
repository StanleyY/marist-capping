angular.module('cappingApp.controllers', [])

.controller('MainCtrl', function($scope, $http) {
  alert('lskdjf');
  console.log("MAIN CONTROLLER STARTED");
  $scope.majors = [];
  $scope.selectedMajor = "";
  $scope.staticCourses = [];
  $scope.ofListItems = [];
  $scope.ofSetItems = [];

  $scope.init = function(){
    alert('startinit');
    var req = {
      method: 'GET',
      url: '/api/get_majors',
      headers: {
        'Content-Type': undefined
      },
    };

    $http(req).then(
      function(response){
        console.log("Retrieved majors.");
        alert('starthttp');
        data = JSON.parse(response);
        $scope.majors = data.majors;
        $scope.selectedMajor = data.majors[0].major;
        alert($scop.selectedMajor);
        $scope.cmbMajor = data.majors[0].major;
      },
      function(response){console.log("Something broke while fetching subjects");}
    );
  };

  $scope.init();

  $scope.majorChanged = function() {
    console.log("MAJOR CHANGED");
    alert('here');
    $scope.selectedMajor = $scope.cmbMajor;
    alert($scope.selectedMajor);
    });
  };

})
