'use strict';

angular.module('confusionApp')

        .controller('MenuController', ['$scope', 'menuFactory', function($scope, menuFactory) {            
            $scope.tab = 1;
            $scope.filtText = '';
            $scope.showDetails = false;
            $scope.showMenu = false;
            $scope.message = "Loading ...";
			
			menuFactory.getDishes().query(
                function(response) {
                    $scope.dishes = response;
                    $scope.showMenu = true;
                },
                function(response) {
                    $scope.message = "Error: "+response.status + " " + response.statusText;
                });
            //$scope.dishes= menuFactory.getDishes();
            //$scope.dishes= [];			
            /*menuFactory.getDishes()
            .then(
                function(response) {
                    $scope.dishes = response.data;
					$scope.showMenu = true;
                },
                function(response) {
                    $scope.message = "Error: "+response.status + " " + response.statusText;
                }
            );*/			
			
            $scope.select = function(setTab) {
                $scope.tab = setTab;
                
                if (setTab === 2) {
                    $scope.filtText = "appetizer";
                }
                else if (setTab === 3) {
                    $scope.filtText = "mains";
                }
                else if (setTab === 4) {
                    $scope.filtText = "dessert";
                }
                else {
                    $scope.filtText = "";
                }
            };

            $scope.isSelected = function (checkTab) {
                return ($scope.tab === checkTab);
            };
    
            $scope.toggleDetails = function() {
                $scope.showDetails = !$scope.showDetails;
            };
        }])

        .controller('ContactController', ['$scope', function($scope) {

            $scope.feedback = {mychannel:"", firstName:"", lastName:"", agree:false, email:"" };
            
            var channels = [{value:"tel", label:"Tel."}, {value:"Email",label:"Email"}];
            
            $scope.channels = channels;
            $scope.invalidChannelSelection = false;
                        
        }])

        .controller('FeedbackController', ['$scope', function($scope) {
            
            $scope.sendFeedback = function() {
                
                console.log($scope.feedback);
                
                if ($scope.feedback.agree && ($scope.feedback.mychannel === "")) {
                    $scope.invalidChannelSelection = true;
                    console.log('incorrect');
                }
                else {
                    $scope.invalidChannelSelection = false;
                    $scope.feedback = {mychannel:"", firstName:"", lastName:"", agree:false, email:"" };
                    $scope.feedback.mychannel="";
                    $scope.feedbackForm.$setPristine();
                    console.log($scope.feedback);
                }
            };
        }])

        //.controller('DishDetailController', ['$scope', 'menuFactory', function($scope, menuFactory) {

        //    $scope.dish= menuFactory.getDish(3);
        //    $scope.sortby = "";
        //}])
        /*.controller('DishDetailController', ['$scope', '$routeParams', 'menuFactory', function($scope, $routeParams, menuFactory) {

            var dish= menuFactory.getDish(parseInt($routeParams.id,10));                        
			$scope.dish = dish;
			$scope.sortby = "";
                    }]) */
        .controller('DishDetailController', ['$scope', '$stateParams', 'menuFactory', function($scope, $stateParams, menuFactory) {
            //var dish= menuFactory.getDish(parseInt($stateParams.id,10));
            //$scope.dish = dish;
            //$scope.dish = {};
			$scope.showDish = true;
            $scope.message="Loading ...";
            
			$scope.dish = menuFactory.getDishes().get({id:parseInt($stateParams.id,10)})
            .$promise.then(
                            function(response){
                                $scope.dish = response;
                                $scope.showDish = true;
                            },
                            function(response) {
                                $scope.message = "Error: "+response.status + " " + response.statusText;
                            }
            );			
            /*menuFactory.getDish(parseInt($stateParams.id,10))
            .then(
                function(response){
                    $scope.dish = response.data;
                    $scope.showDish=true;
                },
                function(response) {
                    $scope.message = "Error: "+response.status + " " + response.statusText;
                }
            );*/
			
			$scope.sortby = "";
                    }])					
					
        .controller('DishCommentController', ['$scope', 'menuFactory', function($scope,menuFactory){
            
            //Step 1: Create a JavaScript object to hold the comment from the form
            
            $scope.submitComment = function () {
                $scope.fb.date = new Date().toISOString();
                console.log($scope.fb);
                $scope.dish.comments.push($scope.fb);

                menuFactory.getDishes().update({id:$scope.dish.id},$scope.dish);
                $scope.commentForm.$setPristine();
                $scope.fb = {rating:5, comment:"", author:"", date:""};
            };
			
        }])

		// implement the IndexController and About Controller here
        .controller('IndexController', ['$scope', 'menuFactory', 'corporateFactory', function($scope, menuFactory,corporateFactory) {
            var prom= menuFactory.getPromotion(0);
            $scope.promotion = prom;
			//$scope.dish = menuFactory.getDish(0);
			//$scope.dish = {};
			$scope.showDish = false;
			$scope.message="Loading ...";
			
			$scope.dish = menuFactory.getDishes().get({id:0})
			.$promise.then(
				function(response){
					$scope.dish = response;
					$scope.showDish = true;
				},
				function(response) {
					$scope.message = "Error: "+response.status + " " + response.statusText;
				}
			);
			
			/*menuFactory.getDish(0)
			.then(
				function(response){
					$scope.dish = response.data;
					$scope.showDish = true;
				},
				function(response) {
					$scope.message = "Error: "+response.status + " " + response.statusText;
				}
			);*/	
			
			$scope.cheif = corporateFactory.getLeader(3);

                    }])	

        .controller('AboutController', ['$scope', '$stateParams', 'corporateFactory', function($scope, $stateParams, corporateFactory) {

			$scope.leaders = corporateFactory.getLeaders();
			
                    }])					
;
