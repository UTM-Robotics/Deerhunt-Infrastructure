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
            displaySubmit: false
        }

        this.opponents = [
            "10",
            "9",
            "8",
            "7",
            "6",
            "5",
            "4",
            "3",
            "2",
            "1"
        ]
    }

    componentDidMount() {
        this.displaySubmit();
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
                if (responseData.game_id == undefined && responseData.message == undefined) {
                    this.setState({
                        result: responseData
                    });
                } else {
                    var result = " - Game Id: " + responseData.game_id;
                    switch (responseData.message) {
                        case 'Winner: p1':
                            result = "Loss :(" + result;
                            break;
                        case 'Winner: p2':
                            result = "Winner!!!" + result;
                            break;
                        case 'Winner: tie':
                            result = "Tie game" + result;
                            break;
                    }
                    this.setState({
                        result: result
                    });
                }
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

    handleOpponentChange(e) {
        this.setState({
            opponent: e.target.value
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
                    <p>Please select the file you would like to submit. Your file should be zipped</p>
                    {/* <p>Choose your opponent:</p>
                    <select className="submit-select" name="position" onChange={this.handleOpponentChange.bind(this)}>
                        {this.opponents.map((item, key) => (
                            <option key={key} value={item}>{item}</option>
                        ))}
                    </select> */}
                    <input type="file" name="upload" id="upload"/> 
                    <div className="submit-button" onClick={this.submitFile.bind(this)}>Upload File</div>
                    {/* <p>Please note that a battle takes anywhere from 5-15 seconds to run so the page may look like it is loading during that time. In addition if other people are challenging the same position you will be queued and it will take longer for your challenge to go through.</p> */}
                    <p>Once you submit your code, it will be included in the next run every hour. If you are submitting again, it will overwrite your previous submitted version. Keep improving your bot!</p>
                </form>}
                </div>}
                {this.state.display && <div className="delay-display">
                    <div className="delay-display-content">
                        <span className="close" onClick={this.closeModal.bind(this)}>x</span>
                        {this.state.loading && <div className="lds-circle">
                            <h1>Loading</h1>
                            <div></div>
                        </div>}
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
