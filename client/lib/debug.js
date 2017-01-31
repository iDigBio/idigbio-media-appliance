var React = require("react");

DebugLink = React.createClass({
    getInitialState: function() {
        return {
        }
    },
    sendDebug: function(){
        var self = this;
        $.ajax({
            type: "GET",
            url: "/api/debug_pack",
            success: function(data){
                self.setState(data);
            }
        });
    },
    render: function(){
        return (
            <a href="#" onClick={this.sendDebug}>Send Debug File</a>
        )
    }
})

module.exports = {
    DebugLink: DebugLink
}