var React = require("react");

module.exports = React.createClass({
    getInitialState: function(){
        return {
            "prefixHidden": (document.config.guid_syntax == "filename" || document.config.guid_syntax == "fullpath") ? "" : "hide"
        }
    },
    guidSyntaxChange: function(e) {
        var tar = $(e.target);
        this.state.prefixHidden = (tar.val() == "filename" || tar.val() == "fullpath") ? "" : "hide";

        document.formPropChange(e);
    },
    addonClick: function(e) {
        var tar = $(e.target);
        tar.next().click();
    },
    generateCSV: function(e, react_id, raw_event, norender){
        e.preventDefault();
        var path = "media.csv"
        if (document.config.csv_path) {
            path = document.config.csv_path
        }
        console.log("Generate");
        document.active = "upload";
        document.messages.push({
            "level": "info",
            "text": "CSV Generation to " + path + "started.",
            "ts": Date()
        });
        console.log(norender)
        if (norender === undefined) {
            document.render();
        }
        return false;
    },
    generateCSVUpload: function(e, react_id, raw_event){
        e.preventDefault();
        this.generateCSV(e, react_id, raw_event, true);
        console.log("Upload");
        document.active = "history";
        document.messages.push({
            "level": "info",
            "text": "Upload Started",
            "ts": Date()
        });
        document.render();
        return false;
    },
    render: function(){
        return (
            <div className="tab-pane container" id="generator-tab">
                <div className="row">
                    <div className="col-md-12">&nbsp;</div>
                </div>                
                <form id="csv-generation-form" className="form-horizontal">
                    <div className="form-group">
                        <label className="col-md-3 control-label">Upload Path *</label>
                        <div className="col-md-9">
                            <div className="input-group">
                                <div className="input-group-addon" onClick={this.addonClick}>Choose Directory</div>
                                <input type="text" data-provide="typeahead" className="form-control"
                                    id="upload_path" name="upload_path" placeholder="The directory or file path containing all your images."
                                    rel="tooltip" data-title="e.g. C:\\Users\bob\Pictures\ or /Users/alice/Pictures/" onClick={document.getDir} value={document.config.upload_path} onChange={document.formPropChange}/>
                            </div>
                        </div>
                    </div>

                    <div className="form-group">
                        <div className="col-md-offset-3 col-md-9 checkbox">
                            <label>
                                <input type="checkbox" id="recursive" name="recursive" checked={document.config.recursive} onChange={document.formPropChange} />  Also Search Files in Subdirectories.
                            </label>
                        </div>
                    </div>

                    <div className="form-group">
                        <label className="col-md-3 control-label"><a href="https://www.idigbio.org/sites/default/files/iDigBioGuidGuideForProviders_v1.pdf" target="_blank">GUID</a> Syntax *</label>
                        <div className="col-md-9">
                            <select id="guid_syntax" name="guid_syntax" className="form-control" value={document.config.guid_syntax} onChange={this.guidSyntaxChange} placeholder="Put in the directory path containing all your images." rel="tooltip" data-title="GUID can be constructed by hashing from media record, or contructed by combining the GUID Prefix with either the file name or the full fie path.">
                                <option value="image_hash" >GUID = hash of image contents</option>
                                <option value="hash" >GUID = hash of record information</option>
                                <option value="filename" >GUID = [GUID Prefix][File Name]</option>
                                <option value="fullpath" >GUID = [GUID Prefix][Full Path]</option>
                            </select>
                        </div>
                    </div>

                    <div className={"form-group " + this.state.prefixHidden}>
                        <label className="col-md-3 control-label">GUID Prefix *</label>
                        <div className="col-md-9">
                            <input type="text" data-provide="typeahead" className="form-control"
                                id="guid_prefix" name="guid_prefix" placeholder="Optional"
                                rel="tooltip" data-title="This is the prefix used with the GUID Syntax. e.g. http://ids.flmnh.ufl.edu/herb. GUIDs are contructed by combining the GUID Prefix with either the file name or the full fie path." 
                                value={document.config.guid_prefix} onChange={document.formPropChange} />
                        </div>
                    </div>

                    <div className="form-group">
                        <label className="col-md-3 control-label">CSV Save Location</label>
                        <div className="col-md-9">
                            <div className="input-group">
                                <div className="input-group-addon" onClick={this.addonClick}>Choose File</div>
                                <input type="text" data-provide="typeahead" className="form-control"
                                    id="csv_path" name="csv_path" placeholder="If left blank, the file will be saved to the image directory."
                                    rel="tooltip" data-title="The directory path that you want to save your CSV file." onClick={document.getFile} 
                                    value={document.config.csv_path} onChange={document.formPropChange} />
                            </div>
                        </div>
                    </div>

                    <div className="form-group">
                        <label className="col-md-3 control-label"></label>
                        <div className="col-md-9">
                            Note: Fields with * are mandatory.
                        </div>
                    </div>

                    <div className="form-group">
                        <div className="col-md-offset-3 col-md-4">
                            <button id="csv-generate-button" className="btn btn-success btn-block" onClick={this.generateCSV} >
                                <i className="icon-file icon-white"></i>
                                <span>Generate CSV</span>
                            </button>
                        </div>
                        <div className="col-md-4">
                            <button id="csv-generate-upload-button" className="btn btn-primary btn-block" onClick={this.generateCSVUpload} >
                                <i className="icon-file icon-white"></i>
                                <span>Generate CSV & Upload Files</span>
                            </button>                        
                        </div>
                    </div>

                </form>
            </div>
        )   
    }
});