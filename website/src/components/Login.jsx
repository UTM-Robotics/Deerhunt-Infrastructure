import React from 'react';
import $ from 'jquery';

class Login extends React.Component {
    constructor() {
        super();
        this.state = {
            email: "",
            password: ""
        }
    }

    componentDidMount() {
        document.addEventListener("keypress", this.handleEnterKeyPress.bind(this));
    }

    addLoginError(type: string) {
        $('.error-message').remove();
        var message = "";
        if (type === 'email1') {
            message = "Please enter an email"
        }
        else if (type === 'email2') {
            message = "Please enter a valid email";
        }
        else if (type === 'password') {
            message = "Please enter a password";
        }
        else if (type === 'login') {
            message = "The email or password is incorrect/invalid"
        }
        var errorMessage = '<p class="error-message">' + message + '</p>';
        $('.auth-button').after(errorMessage);
    }

    validateEmail(email) {
        var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    }

    login() {
        console.log("test");
        console.log(this.state);
        if (this.state.email == "") {
            this.addLoginError('email1');
            return;
        }
        if (!this.validateEmail(this.state.email)) {
            this.addLoginError('email2');
            return;
        }
        if (this.state.password == "") {
            this.addLoginError('password');
            return;
        }
        const requestData = JSON.stringify({
            "email": this.state.username,
            "password": this.state.password
        });

        $.ajax({
            url: 'api/login',
            type: 'POST',
            data: requestData,
            contentType: 'application/json',
            success: () => {
                window.location.replace("/home");
            },
            error: () => {
                this.addLoginError('login');
                return;
            }
        });
    }

    handleEnterKeyPress(e: any) {
        if (e.charCode == 13 || e.keyCode == 13) {
            this.login();
        }
    }

    handleEmailChange(e: any) {
        this.setState({
            email: e.target.value
        });
    }

    handlePasswordChange(e: any) {
        this.setState({
            password: e.target.value
        });
    }
    
    render() {
        return (
            <div className="auth-form-container">
                <form className="login-form" id="login-form">
                    <input type="email" placeholder="email" onChange={this.handleEmailChange.bind(this)} />
                    <input type="password" placeholder="password" onChange={this.handlePasswordChange.bind(this)} />
                    <div className="auth-button" onClick={this.login.bind(this)}>login</div>
                </form>
            </div>

        );
    }
}

export default Login;
