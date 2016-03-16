var React = require("react");

module.exports = React.createClass({

    render: function(){
        console.log("save_failure", document.save_failure)
        if (document.save_failure) {
            return (
                <li>Warning! {document.messages.length} </li>
            )
        } else {
            return (
                <li>Config OK {document.messages.length} </li>
            )
        }
    }

})