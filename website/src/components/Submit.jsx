import React from 'react';
import $ from 'jquery';

class Submit extends React.Component {

    constructor() {
        super();
        this.state = {
            loggedIn: false,
            opponent: "1",
            display: false,
            loading: false,
            resultDisplay: false,
            result: "",
            displaySubmit: false,
            lastSubmitTime: -1// In minutes 
        }
    }

    componentDidMount() {
        this.displaySubmit();
        this.getlastSubmitTime();
        this.isLoggedIn();
    }

    displaySubmit() {
        $.ajax({
            url: '/api/submittoggle',
            type: 'GET',
            success: (responseData) => {
                var parsed = responseData == "True" ? true: false;
                this.setState({
                    displaySubmit: parsed
                });
            }
        });
    }

    isLoggedIn() {
        $.ajax({
            url: '/api/isloggedin',
            type: 'GET',
            success: (responseData) => {
                var parsed = responseData == "True" ? true: false;
                if (parsed) {
                    this.setState({
                        loggedIn: parsed
                    });
                }
                else {
                    window.location.replace("/");
                }
            }
        });
    }

    getlastSubmitTime() {
        $.ajax({
            url: '/api/lastsubmittime',
            type: 'GET',
            success: (responseData) => {
                var parsed = responseData["last_submitted"];
                if (parsed) {
                    this.setState({
                        lastSubmitTime: parsed
                    });
                }
            }
        });
    }

    submitFile() {
        this.setState({
            display: true,
            loading: true
        });
        var form = $('#submit-form')[0];
        var data = new FormData(form);

        $.ajax({
            url:'/api/submit',
            type: 'POST',
            enctype: 'multipart/form-data',
            data: data,
            processData: false,
            contentType: false,
            cache: false,
            success: (responseData) => {
                this.setState({
                    loading: false,
                    resultDisplay: true
                });
                this.state.getlastSubmitTime();
            },
            error: (errorData) => {
                console.log(errorData);
                var res = errorData.status == 409 ? "This user is already submitting" : "There was an error, please try again";

                this.setState({
                    loading: false,
                    resultDisplay: true,
                    result: res                
                });
            }
        });
    }

    closeModal() {
        window.location.replace("/submit");
    }

    render() {
        return (
            <div>
            {this.state.loggedIn && <div className="submit-container">
                {this.state.displaySubmit && <h1>Submit</h1>}
                {!this.state.displaySubmit && <h1>Submissions are Closed</h1>}
                {this.state.displaySubmit && <form id="submit-form"> 
                {this.state.lastSubmitTime !== -1 &&<p>Last submission time: {this.state.lastSubmitTime}</p>}
                {this.state.lastSubmitTime === -1 &&<p>No Current Submission</p>}
                    <p>Please select the file you would like to submit. Your file should be zipped</p>
                    <input type="file" name="upload" id="upload"/> 
                    <div className="submit-button" onClick={this.submitFile.bind(this)}>Upload File</div>
                    <p>Submit a new file to be used in your future challenges.</p>
                </form>}
                </div>}
                {this.state.display && <div className="delay-display">
                    <div className="delay-display-content">
                        <span className="close" onClick={this.closeModal.bind(this)}>x</span>
                        {this.state.resultDisplay && <div className="submit-result">
                            <p>{this.state.result}</p>
                            <div className="buttons-con">
                                <div className="action-link-wrap">
                                    <a href="/submit" className="link-button">Go to Home Page</a>
                                </div>
                            </div>
                        </div>}
                    </div>
                </div>}
            </div>
        );
    }
}

export default Submit;
