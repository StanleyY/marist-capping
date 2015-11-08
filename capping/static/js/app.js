
var app = angular.module("cappingApp", []);

app.config(function($httpProvider)
{
  $httpProvider.defaults.useXDomain = true;
  delete $httpProvider.defaults.headers.common['X-Requested-With'];

});

app.controller("mainCtrl", function($scope,$http) {
  $scope.majors = [];

  $scope.init = function ()
  {
    alert('what');
    var req = {
      method: 'GET',
      url: '/api/get_majors',
      headers: {
        'Content-Type': undefined
      }
    };

    $http(req)
        .then(function(response)
        {
          alert('here1');
          var data = JSON.parse(response);
          alert('here2');
          $scope.majors = data.majors.major;
          alert('here3');
          $scope.cmbMajor = data.majors.major[0];
          alert('here4');
        },
        function(response)
        {
          alert('come on');
          var data = JSON.parse(response);
          alert(data.majors.major[0]);
          alert('failed');
        });

    alert('huh?');
  };

  $scope.majorChanged = function() {
    alert('majorchanged');
  };
});



