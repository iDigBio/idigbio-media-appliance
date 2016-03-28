var React = require("react");

module.exports = React.createClass({

    render: function(){
        console.log("save_failure", document.save_failure)
        if (document.save_failure) {
            return (
                <li><span className="label label-warning label-as-badge"><i className="glyphicon glyphicon-exclamation-sign" data-toggle="tooltip" title="Config Save Error."></i> </span></li>
            )
        } else {
            return (
                <li><span className="label label-success label-as-badge"><i className="glyphicon glyphicon-ok-circle" data-toggle="tooltip" title="Config OK"></i> </span></li>
            )
        }
    }

})