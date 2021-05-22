import React from 'react';
import $ from 'jquery';

class Register extends React.Component {
    constructor() {
        super();
        this.state = {
            "user": "",
            "password": "",
            "confirmPassword": ""
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
        else if (type === 'password') {
            message = "Please enter a password 10 characters or longer.";
        }
        else if(type === 'confirmPassword'){
            message =  "Passwords do not match.";
        }
        else if(type==='request_fail'){
            message = "Sorry, this user already exists, or is not verified. Please check your spam folder,\
             and if this does not work, please contact Technical Admins through Discord."
        }
        var errorMessage = '<p class="error-message">' + message + '</p>';
        $('.register-button').after(errorMessage);
    }

    register() {
        if (this.state.user == "") {
            this.addLoginError('user');
            return;
        }
        if (this.state.password == "" || this.state.password.length < 10) {
            this.addLoginError('password');
            return;
        }
        if (this.state.password != this.state.confirmPassword){
            this.addLoginError('confirmPassword');
            return;
        }
        const requestData = JSON.stringify({
            "username": this.state.user,
            "password": this.state.password
        });

        $.ajax({
            url: '/api/register',
            type: 'POST',
            data: requestData,
            contentType: 'application/json',
            success: (responseData) => {
                $('.error-message').remove();
                $('.success-message').remove();
                var successMessage = '<p class="success-message"> Success! Verification email sent(Check Spam).</p>';
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
            this.register();
        }
    }

    handleUserChange(e) {
        this.setState({
            user: e.target.value
        });
    }

    handlePasswordChange(e) {
        this.setState({
            password: e.target.value
        });
    }

    handleConfirmPasswordChange(e) {
        this.setState({
            confirmPassword: e.target.value
        });
    }

    render() {
        return (
            <div className="register-container">
                <h1>Register</h1>
                <form className="register-form" id="register-form">
                    <input type="text" placeholder="UofT Email" onChange={this.handleUserChange.bind(this)} />
                    <input type="password" placeholder="Password" onChange={this.handlePasswordChange.bind(this)} />
                    <input type="password" placeholder="Confirm your Password" onChange={this.handleConfirmPasswordChange.bind(this)} />
                    <div className="register-button" onClick={this.register.bind(this)}>Register</div>
                </form>
                <p>Already have an account?</p>
                <a href="/">Sign In</a>
            </div>
        );
    }
}

export default Register;
