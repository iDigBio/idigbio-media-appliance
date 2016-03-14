window.$ = jQuery = require('jquery');
var React = require("react");
var ReactDOM = require("react-dom");
require('../server/static/components/bootstrap/dist/js/bootstrap.min.js');

document.config = {}
document.active = "generate"

var MainUI = require('./lib/index.js');
var UserIndicator = require('./lib/user.js');

document.setConfig = function(c) {
    $.ajax({
        type: "POST",
        url: "/api/user",
        // The key needs to match your method's input parameter (case-sensitive).
        data: JSON.stringify(c),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data){
            document.config = data;

            document.render();      

        },
        failure: function(errMsg) {
            console.log(errMsg);
        }
    });
}

document.getDir = function(e){
    var tar = $(e.target);
    var dir = tar.val();
    $.ajax({
        type: "GET",
        url: "/api/dirprompt",
        // The key needs to match your method's input parameter (case-sensitive).
        data: JSON.stringify({"dirname": dir}),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data){            
            if (data.path !== null) {
                tar.val(data.path);
                document.formPropChange({"target": tar});                
            }
        },
        failure: function(errMsg) {
            console.log(errMsg);
        }
    }); 
}

document.getFile = function(e){
    var tar = $(e.target);
    var f = tar.val();
    $.ajax({
        type: "GET",
        url: "/api/fileprompt",
        // The key needs to match your method's input parameter (case-sensitive).
        data: JSON.stringify({"filename": f}),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data){            
            if (data.path !== null && data.path != ".") {
                tar.val(data.path);
                document.formPropChange({"target": tar});
            }
        },
        failure: function(errMsg) {
            console.log(errMsg);
        }
    }); 
}

document.formPropChange = function(e) {
    var tar = $(e.target);    
    document.config[tar.attr("name")] = tar.val();
    document.setConfig(document.config)
}

document.render = function(){

        ReactDOM.render(
            <MainUI active={document.active}/>,
            document.querySelector("#main")            
        );

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

    document.setConfig(d)
    $('#loginModal').modal('hide');    
});


$.get('/api/user', function(data){
    document.config = data;
    document.render()
}).fail(function(errMsg){
    $('#loginModal').modal({
        "backdrop": "static"
    });
})