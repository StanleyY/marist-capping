
var app = angular.module("cappingApp", []);

app.config(function($httpProvider)
{
  $httpProvider.defaults.useXDomain = true;
  delete $httpProvider.defaults.headers.common['X-Requested-With'];

});


app.controller("mainCtrl", function($scope,$http) {
  $scope.majors = [];
  $scope.staticCourseReqs = [];
  $scope.internalCourses = [];
  $scope.oflistitems = [];
  $scope.ofsetitems = [];
  $scope.maristEquiv = 'ART 800';
  $scope.addedCourses = [];


  $scope.init = function ()
  {
    $http.get('/api/get_majors')
        .then(
            function (response) {
              var data = response.data;
              var i = 0;
              for (i = 0; i < data.majors.length; i++) {
                $scope.majors.push(data.majors[i].major);
              }
              $scope.cmbMajor = $scope.majors[0];

              $http.get('/api/get_all_external_courses')
                  .then(
                      function (response) {
                        var data = response.data;
                        var i = 0;
                        var cr;
                        for (i = 0; i < data.courses.length; i++) {
                          cr = data.courses[i].subject + ' ' + data.courses[i].number;
                          $scope.internalCourses.push(cr );
                        }
                        $scope.cmbDutchess = $scope.internalCourses[0];

                        $scope.updateMajorReq();
                      },
                      function (response) {
                        alert('failed');

                      }
                  );


            },
            function (response) {
              alert('failed');

            }
        );

  };

  $scope.updateMajorReq = function()
  {

    $http.get('/api/test_major_req?major=' + $scope.cmbMajor)
        .then(
            function (response) {
              var data = response.data;
              var i = 0;
              var cr;
              $scope.staticCourseReqs = [];
              for( i = 0; i < data.courses.length; i++) {
                $scope.staticCourseReqs.push(data.courses[i]);
              }

              $scope.oflistitems = [];
              for( i = 0; i < data.oflistitems.length; i++)
              {
                $scope.oflistitems.push(data.oflistitems[i]);
              }

              $scope.ofsetitems = [];
              for( i = 0; i < data.ofsetitems.length; i++)
              {
                $scope.ofsetitems.push(data.ofsetitems[i]);
              }

            },
            function (response) {
              alert('failed');

            }
        );
  };

  var CourseReq = function()
  {
    this.internal_course = new Course();
    this.external_course = new Course();
  }

  var Course = function()
  {
    this.subject = "";
    this.number = "";
  }

  $scope.onAddClick = function()
  {
     var cr = new CourseReq();
    var sai = $scope.cmbDutchess.split(' ');
    var sae = $scope.maristEquiv.split(' ');
    var index = -1;
    var ecr;
    var oli;

    cr.external_course.subject = sai[0];
    cr.external_course.number = sai[1];
    cr.internal_course.subject = sae[0];
    cr.internal_course.number = sae[1];

    if( $scope.isInAddedCourses(cr.external_course) != true)
    {
      $scope.addedCourses.push(cr);

      index = $scope.findInRequirements(cr.internal_course);
      if( index != -1 )
      {

        $scope.staticCourseReqs[index].external_course = cr.external_course;
      }
      index = $scope.markOfListItems(cr);

      if( index != -1)
      {
        oli = $scope.oflistitems[index];

        oli.selected++;

        if( oli.selected >= oli.number_selected)
        {
          oli.completed = true;
        }
      }

      $scope.markOfSetItem(cr);
    }
    else
      alert('Course is already added.');
  };

  $scope.isInAddedCourses = function(cr)
  {
    var found = false;
    var i = 0;
    var addcr;
    for( i = 0; (i < $scope.addedCourses.length) && !found; i++)
    {
      addcr = $scope.addedCourses[i].external_course;

      if( (cr.subject == addcr.subject) && (cr.number == addcr.number) )
      {
        found = true;
      }
    }

    return found;
  };

  $scope.findInRequirements = function(cr)
  {
    var index = -1;
    var i = 0;
    var addcr;
    for( i = 0; (i < $scope.staticCourseReqs.length) && (index == -1); i++)
    {
      addcr = $scope.staticCourseReqs[i].internal_course;

      if( (cr.subject == addcr.subject) && (cr.number == addcr.number) )
      {
        index = i;
      }
    }

    return index;
  };

  $scope.markOfListItems = function(cr)
  {
    var index = -1;
    var oindex = -1;
    var i = 0;
    var n = 0;
    var addcr;
    var oli;
    for( i = 0; (i < $scope.oflistitems.length) && (index == -1); i++)
    {
      oli = $scope.oflistitems[i];

      for( n = 0; (n < oli.coursereqs.length) && (index == -1); n++)
      {
        addcr = oli.coursereqs[n].internal_course;
        if( (cr.internal_course.subject == addcr.subject) && (cr.internal_course.number == addcr.number) )
        {
          index = n;
          oindex = i;


        }
      }
    }

    if( index != -1)
    {
      oli = $scope.oflistitems[oindex];
      if( oli.external_course == undefined )
        oli.coursereqs[index].external_course = cr.external_course;
      else
        oindex = -1;
    }

    return oindex;
  };

  $scope.markOfSetItem = function (cr)
  {
    var index = -1;
    var oindex = -1;
    var dindex = -1;
    var i = 0;
    var n = 0;
    var x = 0;
    var crs;
    var addcr;
    var oli;

    for( i = 0; (i < $scope.ofsetitems.length) && (index == -1); i++)
    {
      oli = $scope.ofsetitems[i];

      for( n = 0; (n < oli.coursereqsets.length) && (index == -1); n++)
      {

        crs = oli.coursereqsets[n]
        for( x = 0; (  x < crs.coursereqs.length) && (index == -1); x++)
        {

          addcr = crs.coursereqs[x].internal_course;

          if ((cr.internal_course.subject == addcr.subject) && (cr.internal_course.number == addcr.number)) {

            index = n;
            oindex = i;
            dindex = x;

          }
        }
      }
    }

    if( index != -1)
    {
      oli = $scope.ofsetitems[oindex];
      crs = oli.coursereqsets[index];
      addcr = crs.coursereqs[dindex];

      if( addcr.external_course.subject == undefined )
      {

        addcr.external_course = cr.external_course;

        if( $scope.isCourseReqSetComplete(addcr) )
        {
          oli.selected++;
          if( oli.selected >= oli.number_selected)
          {
            oli.completed = true;
          }
        }
      }
      else
        oindex = -1;
    }

    return oindex;
  };

  $scope.isCourseReqSetComplete = function(crs)
  {
    var i = 0;
    var found = true;

    for( i = 0; (i < crs.length) && found; i++)
    {
      if( crs[i].external_course == undefined)
        found = false;
    }

    return found;
  }
  $scope.internalChanged = function()
  {
    var s = $scope.cmbDutchess.split(' ');
    var sub = s[0];
    var num = s[1];
    $http.get('/api/get_marist_equal?subject=' + sub + '&number=' + num)
        .then(
            function (response) {
              var data = response.data;
              $('#txtMarist')[0].innerHTML = data.courses[0];
              $scope.maristEquiv = data.courses[0];
            },
            function (response) {
              $('#txtMarist')[0].innerHTML = 'elective';

            }
        );
  };

  $scope.majorChanged = function()
      {
        $scope.updateMajorReq();
      };


});



