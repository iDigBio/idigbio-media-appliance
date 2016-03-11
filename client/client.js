window.$ = jQuery = require('jquery');
var React = require("react");
var ReactDOM = require("react-dom");
require('../server/static/components/bootstrap/dist/js/bootstrap.min.js');

document.config = {}

// var MainUI = require('lib/index');
var UserIndicator = require('./lib/user.js');

function setConfig(c) {
    $.ajax({
        type: "POST",
        url: "/api/user",
        // The key needs to match your method's input parameter (case-sensitive).
        data: JSON.stringify(c),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data){
            console.log(data);
            document.config = data;

            render();      

        },
        failure: function(errMsg) {
            console.log(errMsg);
        }
    });
}

function render(){

        // React.render(
        //     <MainUI />
        //     document.querySelector("#main")            
        // );

        ReactDOM.render(
            <UserIndicator />,
            document.querySelector("#userindicator")
        ); 

}

$("#login-button").click(function(){
    var d = {
        "user_uuid": $("#login-form #accountuuid").val(),
        "auth_key": $("#login-form #apikey").val()
    }

    setConfig(d)
});

$.get('/api/user', function(data){
    document.config = data;
    render()
})