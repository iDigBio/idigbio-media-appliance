var React = require("react");

  // "CC0": ["CC0", "(Public Domain)", "http://creativecommons.org/publicdomain/zero/1.0/"],
  // "CC BY": ["CC BY", "(Attribution)", "http://creativecommons.org/licenses/by/4.0/"],
  // "CC BY-SA": ["CC BY-SA", "(Attribution-ShareAlike)", "http://creativecommons.org/licenses/by-sa/4.0/"],
  // "CC BY-NC": ["CC BY-NC", "(Attribution-Non-Commercial)", "http://creativecommons.org/licenses/by-nc/4.0/"],
  // "CC BY-NC-SA": ["CC BY-NC-SA", "(Attribution-NonCommercial-ShareAlike)", "http://creativecommons.org/licenses/by-nc-sa/4.0/"]

module.exports = React.createClass({
    render: function(){
        return (
            <div className="tab-pane container" id="upload-tab">
                <div className="row">
                    <div className="col-md-12">&nbsp;</div>
                </div>              
                <form id='csv-upload-form' className="form-horizontal">
                    <div className="form-group">
                        <label className="col-md-3 control-label">Image <a href="http://creativecommons.org/licenses/" target="_blank">License</a> *</label>
                        <div className="col-md-9">
                            <select id="license" name="license" className="form-control" rel="tooltip"
                            data-title='Select the license you want to associate with the images you upload.'
                            value={document.config.license} onChange={document.formPropChange}>
                                <option value="CC0">CC0</option>
                                <option value="CC BY">CC BY</option>
                                <option value="CC BY-SA">CC BY-SA</option>
                                <option value="CC BY-NC">CC BY-NC</option>
                                <option value="CC BY-NC-SA">CC BY-NC-SA</option>
                            </select>
                        </div>
                    </div>

                    <div className="form-group">
                        <label className="col-md-3 control-label">CSV File Full Path *</label>
                        <div className='col-md-9'>
                            <div className="input-group">
                                <div className="input-group-addon" onClick={this.addonClick}>Choose File</div>
                                <input type="text" data-provide="typeahead" className="form-control"
                                    id="csv_path" placeholder="This should be the full path including the CSV file name."
                                    rel="tooltip" name="csv-path" data-title='e.g. /Users/you/collection.csv' 
                                    value={document.config.csv_path} onChange={document.formPropChange} onClick={document.getFile}/>
                            </div>
                        </div>
                    </div>

                    <div className="form-group">
                        <label className="col-md-3 control-label"></label>
                        <div className="col-md-9">
                            Note: Fields with * are mandatory.
                        </div>
                    </div>

                    <div className='col-md-offset-3 col-md-9'>

                        <div className='span3'>
                            <button id="csv-upload-button" type="submit" className="btn btn-primary btn-block">
                                <i className="icon-upload icon-white"></i>
                                <span>Upload</span>
                            </button>
                        </div>

                        <div className=''>
                            <a href="#CSVFileFormatModal" id="csv-file-format-button" role="button" className="btn btn-inverse btn-block" data-toggle="modal">
                                <i className="icon-list-alt icon-white"></i>
                                <span>CSV file format</span>
                            </a>
                        </div>
                    </div>
                </form>
            </div>
        )   
    }
});