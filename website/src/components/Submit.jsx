import React from 'react';
import $ from 'jquery';

class Submit extends React.Component {

    constructor() {
        super();
        this.state = {
            loggedIn: false
        }
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
            this.state.loggedIn && <div>
                <form action="/api/submit" method="POST" encType="multipart/form-data"> 
                    <p>Please select the file you would like to upload. </p>
                    <input type="text" name="position"/> <br/> 
                    <input type="file" name="upload"/> <br/> 
                    <input type="submit" value="Upload File"/>
                </form>
            </div>
        );
    }
}

export default Submit;
