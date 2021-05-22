import React from 'react';
import $ from 'jquery';

class Reset extends React.Component {
    constructor() {
        super();
        this.state = {
            "user": "",
        }
    }

    componentDidMount() {
        document.addEventListener("keypress", this.handleEnterKeyPress.bind(this));
    }


    addLoginError(type) {
        $('.error-message').remove();
        $('.success-message').remove();
        var message = "";
        if (type === 'user') {
            message = " Please enter a valid UofT email."
        }
        else if(type==='request_fail'){
            message = "Sorry, this user already exists, or is not verified. Please check your spam folder,\
             and if this does not work, please contact Technical Admins through Discord."
        }
        var errorMessage = '<p class="error-message">' + message + '</p>';
        $('.register-button').after(errorMessage);
    }

    reset() {
        if (this.state.user == "") {
            this.addLoginError('user');
            return;
        }
        const requestData = JSON.stringify({
            "username": this.state.user
        });

        $.ajax({
            url: '/api/reset',
            type: 'POST',
            data: requestData,
            contentType: 'application/json',
            success: (responseData) => {
                $('.error-message').remove();
                $('.success-message').remove();
                var successMessage = '<p class="success-message"> Reset link sent! (Check Spam).</p>';
                $('.register-button').after(successMessage);
            },
            error: () => {
                this.addLoginError('request_fail');
                return;
            }
        });
    }
    
    handleEnterKeyPress(e) {
        if (e.charCode == 13 || e.keyCode == 13) {
            this.reset();
        }
    }

    handleUserChange(e) {
        this.setState({
            user: e.target.value
        });
    }

    render() {
        return (
            <div className="register-container">
                <h1>Reset Password</h1>
                <form className="register-form" id="reset-form">
                    <input type="text" placeholder="UofT Email" onChange={this.handleUserChange.bind(this)} />
                    <div className="register-button" onClick={this.reset.bind(this)}>Reset</div>
                </form>
            </div>
        );
    }
}

export default Reset;
