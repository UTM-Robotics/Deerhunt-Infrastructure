import React from 'react';
import $ from 'jquery';

class Submit extends React.Component {

    constructor() {
        super();
        this.state = {
            loggedIn: false
        }

        this.opponents = [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10"
        ]
    }

    componentDidMount() {
        this.isLoggedIn();
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

    render() {
        return (
            this.state.loggedIn && <div className="submit-container">
                <h1>Submit</h1>
                <form action="/api/submit" method="POST" encType="multipart/form-data"> 
                    <p>Please select the file you would like to submit. Your file should be zipped</p>
                    <p>Choose your opponent:</p>
                    <select className="submit-select" name="opponent">
                    {this.opponents.map((item, key) => (
                        <option key={key} value={item}>{item}</option>
                    ))}
                    </select>
                    <input type="file" name="upload"/> 
                    <input className="submit-button" type="submit" value="Upload File"/>
                </form>
                <p>Please note that a battle takes anywhere from 5-15 seconds to run so the page may look like it's loading during that time. In addition if other people are challenging the same position you will be queued and it will take longer for your challenge to go through.</p>
            </div>
        );
    }
}

export default Submit;
