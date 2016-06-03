window.$ = jQuery = require('jquery');
var React = require("react");
var ReactDOM = require("react-dom");
require('../idigbio_media_appliance/static/components/bootstrap/dist/js/bootstrap.min.js');
require("bootstrap-notify");

var hash = window.location.hash.substring(1);

if (hash == "upload-tab") {
    document.active = "upload"
} else if (hash == "history-tab") {
    document.active = "history"
} else if (hash == "generate-tab") {
    document.active = "generate"
} else {
    document.active = "upload"    
}

document.config = {}
document.save_failure = false;

var MainUI = require('./lib/index.js');
var UserIndicator = require('./lib/user.js');
var WarningIndicator = require('./lib/warning.js');
var DebugLink = require('./lib/debug.js').DebugLink;

document.setConfig = function(c) {
    // Optimistically re-render to avoid having to round trip to server before inputs change
    document.config = c;
    document.render();
    $.ajax({
        type: "POST",
        url: "/api/appuser",
        data: JSON.stringify(c),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data){

        },
        error: function(errMsg) {
            // Warning message on config failure?
            document.save_failure = true;
            document.render();
        }
    });
}

document.getDir = function(e){
    e.preventDefault();
    var tar = $(e.target);
    var dir = tar.val();
    $.ajax({
        type: "GET",
        url: "/api/dirprompt",
        // The key needs to match your method's input parameter (case-sensitive).
        data: {"dirname": dir},
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
    return false;
}

document.getFile = function(e){
    e.preventDefault();
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
    return false;
}

var configUpdateTask;
document.formPropChange = function(e) {
    var tar = $(e.target);
    var v = tar.val();
    if (tar.attr("type") == "checkbox") {
        v = e.target.checked;
    }

    document.config[tar.attr("name")] = v;
    document.setConfig(document.config);
}

document.runningTasks = {};

document.pollTask = function(taskID) {
    $.ajax({
        type: "GET",
        url: "/api/readdir/" + taskID,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data){
            console.log(data);
            if (data.status == "RUNNING") {
                setTimeout(function(){
                    document.pollTask(taskID);
                }, 5000)
            } else if (data.status == "DONE") {
                if (data.filename !== undefined) {
                    $.notify({
                        "message": "CSV Generation done."
                    },{
                        "type": "info"
                    });
                    window.location = "/api/getfile/" + data.filename
                }
            }
        },
        failure: function(errMsg) {
            console.log(errMsg);
        }
    });
}

document.render = function(){
        ReactDOM.render(
            <MainUI active={document.active}/>,
            document.querySelector("#main")
        );

        ReactDOM.render(
            <WarningIndicator />,
            document.querySelector("#warningindicator")
        );

        ReactDOM.render(
            <UserIndicator />,
            document.querySelector("#userindicator")
        );


        ReactDOM.render(
            <DebugLink />,
            document.querySelector("#debuglink")
        );

}

$("#login-button").click(function(){
    var d = {
        "user_alias": $("#login-form #accountalias").val(),
        "user_uuid": $("#login-form #accountuuid").val(),
        "auth_key": $("#login-form #apikey").val()
    }

    document.setConfig(d)
    $('#loginModal').modal('hide');

    return false;
});

$("#prev-user-activate").click(function(){
    var d = {
        "user_alias": $("#prev-user option:selected").text(),
        "user_uuid": $("#prev-user").val()
    }

    document.setConfig(d)
    $('#loginModal').modal('hide');

    return false;
});


$.get('/api/appuser', function(data){
    document.config = data;
    document.render()
}).fail(function(errMsg){
    $('#loginModal').modal({
        "backdrop": "static"
    });
})