angular.module('cappingApp.controllers', [])

.controller('MainCtrl', function($scope, $http, $window) {
  console.log("MAIN CONTROLLER STARTED");
  $scope.subjNumMap = {};
  $scope.entries = [];

  $scope.majors = [];
  $scope.cmbMajor = "";
  $scope.staticCourseReqs = [];
  $scope.internalCourses = [];
  $scope.oflistitems = [];
  $scope.ofsetitems = [];
  $scope.addedCourses = [];

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

    req.url = '/api/get_majors';
    $http(req).then(
      function(response){
        var data = response.data;
        var i = 0;
        for (i = 0; i < data.majors.length; i++) {
          $scope.majors.push(data.majors[i].major);
        }
        $scope.cmbMajor = $scope.majors[0];
        $scope.updateMajorReq();
      },
      function(response){console.log("Something broke while fetching majors");}
    );
  };

  $scope.init();

  $scope.addEntry = function() {
    $scope.entries.push(new Entry());
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


  // Major Related Functions
  $scope.majorChanged = function() {
    $scope.updateMajorReq();
  };

  $scope.updateMajorReq = function() {
    $http.get('/api/test_major_req?major=' + $scope.cmbMajor).then(
      function (response) {
        var data = response.data;
        var i = 0;
        var cr;
        $scope.staticCourseReqs = [];
        for(i = 0; i < data.courses.length; i++) {
          $scope.staticCourseReqs.push(data.courses[i]);
        }

        $scope.oflistitems = [];
        for (i = 0; i < data.oflistitems.length; i++) {
          $scope.oflistitems.push(data.oflistitems[i]);
        }

        $scope.ofsetitems = [];
        for (i = 0; i < data.ofsetitems.length; i++) {
          $scope.ofsetitems.push(data.ofsetitems[i]);
        }
      },
      function (response) {
        console.log('Failed to update major requirements.');
      });
  };

  // Report Generation
  $scope.generateReport = function() {
    var data = {
      'major': $scope.cmbMajor,
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

  /*
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
  */
})
