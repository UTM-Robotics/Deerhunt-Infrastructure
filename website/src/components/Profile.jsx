import React from 'react';
import $ from 'jquery';

class Profile extends React.Component {

    constructor() {
        super();
        this.state = {
            loggedIn: false,
            username: "",
            currentPassword: "",
            newPassword: "",
            confirmPassword: "",
        };
    }

    componentDidMount() {
        document.addEventListener("keypress", this.handleEnterKeyPress.bind(this));
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

    handleEnterKeyPress(e) {
        if (e.charCode == 13 || e.keyCode == 13) {
            this.change();
        }
    }

    handleCurrentPasswordChange(e) {
        this.setState({
            currentPassword: e.target.value
        });
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
        if (type === 'cup') {
            message = "Please enter your current password"
        }
        else if (type === 'nep') {
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
        if (this.state.currentPassword == "") {
            this.addError('cup');
            return;
        }
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
            "currentPassword": this.state.currentPassword,
            "newPassword": this.state.newPassword,
            "confirmPassword": this.state.confirmPassword
        });

        $.ajax({
            url:'/api/changepassword',
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
             this.state.loggedIn && <div className="profile-container">
              <h1>Profile</h1>
                <form className="change-form" id="change-form">
                    <input type="password" placeholder="current password" onChange={this.handleCurrentPasswordChange.bind(this)} />
                    <input type="password" placeholder="new password" onChange={this.handleNewPasswordChange.bind(this)} />
                    <input type="password" placeholder="confirm new password" onChange={this.handleConfirmPasswordChange.bind(this)} />
                    <div className="register-button" onClick={this.change.bind(this)}>update</div>
                    
                </form>
            </div>
        );
    }
}

export default Profile;
