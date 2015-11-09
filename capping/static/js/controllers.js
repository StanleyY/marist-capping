angular.module('cappingApp.controllers', [])

.controller('MainCtrl', function($scope, $http, $window) {
  console.log("MAIN CONTROLLER STARTED");
  $scope.subjNumMap = {};
  $scope.entries = [];
  $scope.majors = [];
  $scope.majorsReqs = {};
  $scope.selectedMajor = "";
  $scope.requirements = [];

  $scope.init = function(){
    var req = {
      method: 'GET',
      url: '/api/get_external_data',
      headers: {
        'Content-Type': undefined
      },
    };

    $http(req).then(
      function(response){
        $scope.subjNumMap = response.data;
        $scope.addEntry(); // Add an entry once all the data is ready
      },
      function(response){console.log("Something broke while fetching subjects");}
    );

    req.url = '/api/get_major_req';
    $http(req).then(
      function(response){
        $scope.majorsReqs = response.data;
        $scope.majors = Object.keys($scope.majorsReqs).sort();
      },
      function(response){console.log("Something broke while fetching majors");}
    );
  };

  $scope.init();

  $scope.majorChanged = function() {
    console.log("MAJOR CHANGED");
    $scope.requirements = [];
    $scope.majorsReqs[$scope.selectedMajor].forEach(function(value){
      $scope.requirements.push({name: value, fulfilled: false});
    });
  };

  $scope.addEntry = function() {
    $scope.entries.push(new Entry());
  };

  $scope.generateReport = function() {
    var data = {
      'major': $scope.selectedMajor,
      'entries[]': $scope.entries.map(function(entry){
        return [entry.selectedSubject + " " + entry.selectedNumber,
                entry.selectedMaristCourse];
      })
    };
    var url = '/api/get_pdf?';
    for (var key in data) {
      if (url != '') {
          url += '&';
      }
      url += key + "=" + encodeURIComponent(data[key]);
    }
    window.open(url, '_blank', '');
  };

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
      if (this.selectedNumber == -1) return;
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

  $scope.$watch('entries', function () {
    var marist_classes = $scope.entries.map(
        function(val){return val.selectedMaristCourse.slice(0, -1);});
    $scope.requirements.forEach(function(req){
      if (marist_classes.indexOf(req.name) > -1) {
        req.fulfilled = true;
      } else {
        req.fulfilled = false;
      }
    }.bind(marist_classes))
  }, true);
})
