var React = require("react");

module.exports = React.createClass({

    login: function() {
        $('#loginModal').modal({
            "backdrop": "static"
        });
    },
    logout: function() {
        $.ajax({
            type: "DELETE",
            url: "/api/user",        
            success: function(){
                document.config = {};
            }
        });
    },

    render: function(){
        if (document.config.user_uuid !== undefined) {
            return (
                <li><label>{document.config.user_uuid}</label><button id="logout-btn" className="navbar-btn btn btn-warning" type="button" onClick={this.logout}>Logout</button></li>
            )
        } else {
            return (
                <li><button id="login-btn" className="navbar-btn btn btn-warning" type="button" onClick={this.login}>Login</button></li>
            )
        }
    }

})