var React = require("react");

module.exports = React.createClass({
    getInitialState: function(){
        return {
            "status": {},
            "items": [],
            "upload": {},
            "timeouts": {},
            "doUpload": false,
            "limit": 10,
            "offset": 0,
        };
    },
    componentWillMount: function(){
        this.listMedia(this.state.offset);
        this.updateState();
        this.checkUpload();
    },
    componentWillReceiveProps: function(props){
        this.listMedia(this.state.offset, props.period);
    },
    goToPage: function(e) {
        var self = this;
        var tar = $(e.target);

        if (tar.is("span")) {
            tar = $(tar.parent());
        }

        var page = tar.attr("data-page");
        var offset = (page - 1) * this.state.limit;

        self.listMedia(offset);
    },
    listMedia: function(offset, period) {
        var self = this;
        if (period === undefined) {
            period = this.props.period
        }
        $.ajax({
            type: "GET",
            url: "/api/media",
            data: {
                "limit": this.state.limit,
                "offset": offset,
                "time_period": period
            },
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data){
                self.setState({"items": data.media, "offset": offset})
            },
            failure: function(errMsg) {
                console.log(errMsg);
            }
        });
    },
    genCSV: function(e) {
        var self = this;
        $.ajax({
            type: "POST",
            url: "/api/mediacsv",
            data: JSON.stringify({ "period": self.props.period }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data){
                document.pollTask(data.task_id);

                $.notify({
                    "message": "CSV Generation for " + self.props.period + " started."
                },{
                    "type": "info"
                });

                document.render();
            },
            error: function(errMsg) {
                $.notify({
                    "message": "CSV Generation failed."
                },{
                    "type": "danger"
                });

                document.render();
            }
        });
    },
    componentWillUnmount: function(){
        $.each(this.state.timeouts,function(k, v){
            clearTimeout(v);
        })
    },
    updateState: function() {
        var self = this;

        $.ajax({
            type: "GET",
            url: "/api/media/status",
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data){
                var s = {}
                self.state.timeouts["status"] = setTimeout(self.updateState, 5000);
                s.status = data;
                self.setState(s);
            },
            failure: function(errMsg) {
                console.log(errMsg);
            }
        });
    },
    checkUpload: function(e){
        var self = this;
        $.ajax({
            type: "GET",
            url: "/api/process",
            data: {"start": self.state.doUpload},
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data){
                self.setState({"upload": data, "doUpload": false})
                if (self.state.upload.status == "STARTED" || self.state.upload.status == "RUNNING") {
                    self.state.timeouts["check"] = setTimeout(function(){
                        self.checkUpload();
                    }, 5000);
                }
            },
            failure: function(errMsg) {
                console.log(errMsg);
            }
        });
    },
    startUpload: function(e){
        this.setState({"doUpload": true}, function(){
            this.checkUpload(e);
        })
    },
    render: function(){
        var mediaItems = $.map(this.state.items,function(item){
            return (
                <tr key={item.file_reference}>
                    <td>{item.path}</td>
                    <td>{item.file_reference}</td>
                    <td>{item.status}</td>
                </tr>
            )
        });

        var pagerItems = [];
        var currentPage = (this.state.offset / this.state.limit) + 1;

        var minPage = Math.max(currentPage-5, 1);
        var maxPage = Math.max(currentPage+5, 10);

        pagerItems.push(
            <li key="pager_item_prev">
              <a href="#" aria-label="Previous" onClick={this.goToPage} data-page={Math.max(currentPage-1,1)}>
                <span aria-hidden="true">&laquo;</span>
              </a>
            </li>
        );

        for (var i = minPage; i < maxPage+1; i++) {
            if (i == currentPage) {
                pagerItems.push(<li key={"pager_item_" + i} className="active"><a href="#" data-page={i} onClick={this.goToPage}>{i}</a></li>)
            } else {
                pagerItems.push(<li key={"pager_item_" + i}><a href="#" data-page={i} onClick={this.goToPage}>{i}</a></li>)
            }
        }

        pagerItems.push(
            <li key="pager_item_next">
              <a href="#" aria-label="Next" onClick={this.goToPage} data-page={Math.min(currentPage+1,Math.floor((this.state.status.count || 0) / this.state.limit))}>
                <span aria-hidden="true">&raquo;</span>
              </a>
            </li>
        );

        var button;
        var infoActive = "";
        if (this.state.upload.status == "STARTED" || this.state.upload.status == "RUNNING") {
            button = (<button className="btn disabled">Upload Task Running</button>)
            infoActive = " progress-bar-striped active";
        } else {
            button = (<button className="btn btn-primary" onClick={this.startUpload}>Restart Upload Task</button>);
        }

        var percents = {
            "success": ((this.state.status.uploaded || 0) / (this.state.status.count || 1)) * 100,
            "info": (((this.state.status.pending || 0) + (this.state.status.file_changed || 0)) / (this.state.status.count || 1)) * 100,
            "warning": ((this.state.status.missing || 0) / (this.state.status.count || 1)) * 100,
            "error": ((this.state.status.failed || 0) / (this.state.status.count || 1)) * 100
        }

        return (
            <div className="row">
                <h3>Media Status</h3>
                <div className="col-md-3">
                    <h4>Total Media Added: <span className="badge">{this.state.status.count || "0"}</span></h4>
                    <div className="progress">
                      <div className={"progress-bar progress-bar-success" + infoActive} style={{"width": percents.success + "%"}}>
                        <span className="sr-only">percents.success + "%" Complete (success)</span>
                      </div>
                      <div className={"progress-bar progress-bar-info" + infoActive}  style={{"width": percents.info + "%"}}>
                        <span className="sr-only">percents.info + "%" Complete (warning)</span>
                      </div>
                      <div className={"progress-bar progress-bar-warning" + infoActive} style={{"width": percents.warning + "%"}}>
                        <span className="sr-only">percents.warning + "%" Complete (warning)</span>
                      </div>
                      <div className={"progress-bar progress-bar-danger" + infoActive} style={{"width": percents.error + "%"}}>
                        <span className="sr-only">percents.error + "%" Complete (danger)</span>
                      </div>
                    </div>
                    <ul className="list-group">
                        <li className="list-group-item list-group-item-success">
                            Uploaded <span className="badge">{this.state.status.uploaded || "0"}</span>
                        </li>
                        <li className="list-group-item list-group-item-info">
                            Pending <span className="badge">{this.state.status.pending || "0"}</span>
                        </li>
                        <li className="list-group-item list-group-item-info">
                            File Changed <span className="badge">{this.state.status.file_changed || "0"}</span>
                        </li>
                        <li className="list-group-item list-group-item-warning">
                            Missing <span className="badge">{this.state.status.missing || "0"}</span>
                        </li>
                        <li className="list-group-item list-group-item-danger">
                            Failed <span className="badge">{this.state.status.failed || "0"}</span>
                        </li>
                    </ul>
                    {button}
                </div>
                <div className="col-md-9 text-center">
                    <div className="row">
                        <div className="col-md-3">
                            <button className="btn btn-success" onClick={this.genCSV}><i className="glyphicon glyphicon-download"></i> Download Media as CSV</button>
                        </div>
                        <div className="col-md-6">
                            <nav>
                              <ul className="pagination" style={{"margin": "0px"}}>
                                {pagerItems}
                              </ul>
                            </nav>
                        </div>
                        <div className="col-md-3">
                            <select id="time_period" name="time_period" className="form-control" 
                            value={this.props.period} onChange={document.formPropChange} >
                                <option value="all">Show All</option>
                                <option value="day">Last Day</option>
                                <option value="week">Last 7 Days</option>
                                <option value="month">Last 30 Days</option>
                            </select>
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-md-12">
                            <table className="table table-striped text-left">
                                <thead>
                                    <tr>
                                        <th>
                                            Media Path
                                        </th>
                                        <th>
                                            GUID
                                        </th>
                                        <th>
                                            Status
                                        </th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {mediaItems}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
});