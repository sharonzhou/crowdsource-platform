/**
 * UserController
 * @namespace crowdsource.worker.controllers
 */
(function () {
    'use strict';

    angular
        .module('crowdsource.user.controllers')
        .controller('UserController', UserController);

    UserController.$inject = ['$location', '$scope',
        '$window', '$mdToast', '$mdDialog', 'Authentication', 'User', 'Payment', '$http'];

    /**
     * @namespace UserController
     */
    function UserController($location, $scope,
                            $window, $mdToast, $mdDialog, Authentication, User, Payment, $http) {

        var vm = this;
        vm.paypal_payment = paypal_payment;
        vm.toggleEdit = toggleEdit;
        vm.updateProfileDesc = updateProfileDesc;
        vm.edit=false;
        vm.genders=[
            {"key":"M", "value":"Male"},
            {"key":"F", "value":"Female"},
            {"key":"O", "value":"Other"}
        ];
        vm.countries = [];
        vm.cities = [];

        $http({
            method: "GET",
            url: "/api/country/"
        }).then(function success(response){
            console.log(response);
            response.data.forEach(function(data){
                console.log("data: " + data);
                vm.countries.push(data);
            })
        });

        $http({
            method: "GET",
            url: "/api/city/"
        }).then(function success(response){
            console.log(response);
            response.data.forEach(function(data){
                console.log("data: " + data);
                vm.cities.push(data);
            })
        });



        var userAccount = Authentication.getAuthenticatedAccount();
        if (!userAccount) {
            $location.path('/login');
            return;
        }

        User.getProfile(userAccount.username)
            .then(function (data) {
                var user = data[0];
                user.first_name = userAccount.first_name;
                user.last_name = userAccount.last_name;

                if (user.hasOwnProperty('financial_accounts') && user.financial_accounts) {
                    user.financial_accounts = _.filter(user.financial_accounts.map(function (account) {
                        var mapping = {
                            'general': 'general',
                            'requester': 'Deposits',
                            'worker': 'Earnings'
                        };

                        account.type = mapping[account.type];
                        return account;
                    }), function (account) {
                        return account.type != 'general';
                    });
                }

                vm.user = user;
                vm.user.birthday = new Date(vm.user.birthday);
                vm.user.birthday_string = vm.user.birthday.yyyymmdd();
                // Make worker id specific
                vm.user.workerId = user.id;
            });

        function toggleEdit(){
            vm.edit = !vm.edit;
        }

        function updateProfileDesc(){
            var updated_user = JSON.parse(JSON.stringify(vm.user));
            updated_user.birthday = vm.user.birthday;
            updated_user.birthday = updated_user.birthday.yyyymmdd();
            User.updateProfile(userAccount.username, updated_user)
                .then(function(data){
                    console.log(data);
                    if(data[1] === 200 && data[0].status === "updated profile"){
                        toggleEdit();
                    }
                });
        }

        function getCountries(){
            var result = [];
            var data = $.get("/api/country/");
            data = data.responseJSON;
            data.forEach(function(x){
                result.append(x);
            });
            return result;
        }

        function paypal_payment($event){
            $mdDialog.show({
                clickOutsideToClose: false,
                preserveScope: false,
                targetEvent: $event,
                templateUrl: '/static/templates/payment/payment.html',
                locals: {
                    dialog: $mdDialog
                },
                controller: DialogController
            });

            function DialogController($scope, dialog) {

                $scope.payment_in_progress= false;

                $scope.payment_methods = [
                    {name:'Paypal', method:'paypal'},
                    {name:'Credit Card', method:'credit_card'}
                ];

                $scope.card_types = [
                    {name:'Visa', type:'visa'},
                    {name:'MasterCard', type:'mastercard'},
                    {name:'Discover', type:'discover'},
                    {name:'American Express', type:'american_express'}
                ];

                $scope.payment={
                    amount:1.00,
                    method:'paypal',
                    type:'self'
                };

                $scope.$watch('payment.method', function(newValue, oldValue){
                   if(newValue!=oldValue && newValue == 'paypal'){
                       if($scope.payment.hasOwnProperty('credit_card')){
                            delete $scope.payment.credit_card;
                        }
                   }
                });

                $scope.pay = function(){
                  $scope.payment_in_progress= true;

                  var data = angular.copy($scope.payment);

                  if(data.method=='credit_card'){
                      data.credit_card.number = ''+data.credit_card.number;
                  }

                  Payment.create(data).then(
                      function success(response){
                          if(data.method=='credit_card'){
                              $mdToast.showSimple(response.message);
                              $location.url('/profile');
                          }else {
                              $window.location.href = response[0].redirect_url;
                          }
                      },
                      function error(response){
                          $mdToast.showSimple('Error during payment. Please try again.');
                      }
                  ).finally(function () {
                        $scope.payment_in_progress= false;
                    });
                };

                $scope.hide = function() {
                    dialog.hide();
                };
                $scope.cancel = function() {
                    dialog.cancel();
                };


            }
        }
    }
})();