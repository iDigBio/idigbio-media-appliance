var React = require("react");

var HistoryUI = require("./history.js");
var GenerateUI = require("./generate.js");
var UploadUI = require("./upload.js");

TabNavItem = React.createClass({
    render: function(){
        var cn = "";
        if (this.props.active){
            cn = "active";
        }
        return (
            <li className={cn}>
                <a id={this.props.name} href={"#" + this.props.name + "-tab"} onClick={this.props.clicky}>{this.props.label}</a>
            </li>
        )
    }
})

module.exports = React.createClass({
    activateTab: function(e) {
        document.active = e.target.id;
        document.render();

    },
    render: function(){
        var self = this;
        var tabs = [["generate", "Generate CSV"], ["upload","Upload Via CSV"] , ["history", "Upload History"]].map(function(a){
            var n = a[0];
            var l = a[1];
            return <TabNavItem key={n} name={n} clicky={self.activateTab} label={l} active={self.props.active == n} /> 
        })
        if (this.props.active == "upload") {
            activeTab = <UploadUI />
        } else if (this.props.active == "history") {
            activeTab = <HistoryUI />
        } else if (this.props.active == "generate") {
            activeTab = <GenerateUI />
        } else {
            activeTab = <UploadUI />
        }
        return (
            <div id="upload-dashboard" className="js-required row">
                <ul className="nav nav-tabs">
                    {tabs}
                </ul>

                {activeTab}
            </div>
        )   
    }
});