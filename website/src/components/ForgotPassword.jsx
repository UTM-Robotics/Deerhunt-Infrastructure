import React from 'react';
import $ from 'jquery';

class ForgotPassword extends React.Component {

    constructor() {
        super();
        this.state = {
            newPassword: "",
            confirmPassword: "",
        };
    }

    handleEnterKeyPress(e) {
        if (e.charCode == 13 || e.keyCode == 13) {
            this.change();
        }
    }

    handleNewPasswordChange(e) {
        this.setState({
            newPassword: e.target.value
        });
    }

    handleConfirmPasswordChange(e) {
        this.setState({
            confirmPassword: e.target.value
        });
    }

    addError(type) {
        $('.error-message').remove();
        $('.success-message').remove();
        var message = "";
        if (type === 'nep') {
            message = "Please enter a new password";
        }
        else if (type === 'cop') {
            message = "Please confirm your new password";
        }
        else if (type === 'dif') {
            message = "Passwords do not match"
        }
        else {
            message = "Invalid Password"
        }
        var errorMessage = '<p class="error-message">' + message + '</p>';
        $('.register-button').after(errorMessage);
    }

    change() {
        if (this.state.newPassword == "") {
            this.addError('nep');
            return;
        }
        if (this.state.confirmPassword == "") {
            this.addError('cop');
            return;
        }
        if (this.state.newPassword != this.state.confirmPassword) {
            this.addError('dif');
            return;
        }

        const requestData = JSON.stringify({
            "newPassword": this.state.newPassword,
            "confirmPassword": this.state.confirmPassword,
            "code":this.props.match.params.reset_code
        });

        $.ajax({
            url:"/api/forgotpassword/*",
            type: 'POST',
            data: requestData,
            contentType: 'application/json',
            success: () => {
                $('.error-message').remove();
                $('.success-message').remove();
                var successMessage = '<p class="success-message">Successfully Changed</p>';
                $('.register-button').after(successMessage);
            },
            error: () => { 
                this.addError('');
                return;
            }
        });
    }

    render() {
        return (
             <div className="profile-container">
              <h1>Password Reset</h1>
                <form className="change-form" id="change-form">
                    <input type="password" placeholder="new password" onChange={this.handleNewPasswordChange.bind(this)} />
                    <input type="password" placeholder="confirm new password" onChange={this.handleConfirmPasswordChange.bind(this)} />
                    <div className="register-button" onClick={this.change.bind(this)}>Reset</div>
                    
                </form>
            </div>
        );
    }
}

export default ForgotPassword;
