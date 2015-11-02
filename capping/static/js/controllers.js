angular.module('cappingApp.controllers', [])

.controller('MainCtrl', function($scope, $http) {
  console.log("MAIN CONTROLLER STARTED");
  $scope.subjNumMap = {};
  $scope.entries = [];

  $scope.init = function(){
    var req_to_ext = {
      method: 'GET',
      url: '/api/get_external_data',
      headers: {
        'Content-Type': undefined
      },
    };

    $http(req_to_ext).then(
      function(response){
        $scope.subjNumMap = response.data;
        $scope.addEntry(); // Add an entry once all the data is ready
      },
      function(response){console.log("Something broke");}
    );
  };

  $scope.init();

  $scope.addEntry = function() {
    $scope.entries.push(new Entry());
  }

  // Entry Object definition
  function Entry() {
    this.subjects = Object.keys($scope.subjNumMap).sort();
    this.maristOptionsDisabled = true;
    this.numberList = [];
    this.maristCourseList = [];
    this.selectedSubject = this.subjects[0];
    this.selectedNumber = -1;
    this.selectedMaristCourse = "";

    this.numberChange = function() {
      var req = {
        method: 'GET',
        url: '/api/get_marist_equal',
        params: {
          subject: this.selectedSubject,
          number: this.selectedNumber
        },
      };

      $http(req).then(
        function(response){
          console.log(response.data.courses);
          console.log(this);
          this.maristCourseList = response.data.courses;
          this.selectedMaristCourse = this.maristCourseList[0];
        }.bind(this),
        function(response){console.log("Something broke");}
      );
    };

    this.numberChange();

    this.subjectChange = function() {
      this.maristOptionsDisabled = true;
      this.numberList = $scope.subjNumMap[this.selectedSubject];
      this.selectedNumber = this.numberList[0];
      this.numberChange();
    };

    this.subjectChange();
  }
})
