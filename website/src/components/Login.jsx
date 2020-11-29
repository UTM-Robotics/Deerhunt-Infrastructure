import React from 'react';
import $ from 'jquery';

class Login extends React.Component {
    constructor() {
        super();
        this.state = {
            user: "",
            password: ""
        }
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
                    window.location.replace("/home");
                }
            }
        });
    }


    addLoginError(type: string) {
        $('.error-message').remove();
        var message = "";
        if (type === 'user') {
            message = "Please enter an user"
        }
        else if (type === 'password') {
            message = "Please enter a password";
        }
        else if (type === 'login') {
            message = "The user or password is incorrect/invalid/not verified"
        }
        var errorMessage = '<p class="error-message">' + message + '</p>';
        $('.auth-button').after(errorMessage);
    }

    login() {
        if (this.state.user == "") {
            this.addLoginError('user');
            return;
        }
        if (this.state.password == "") {
            this.addLoginError('password');
            return;
        }
        const requestData = JSON.stringify({
            "username": this.state.user,
            "password": this.state.password
        });

        $.ajax({
            url: '/api/login',
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

    handleEnterKeyPress(e) {
        if (e.charCode == 13 || e.keyCode == 13) {
            this.login();
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
    
    render() {
        return (
            <div className="auth-form-container">
                <form className="login-form" id="login-form">
                    <input id="username" type="text" placeholder="username" onChange={this.handleUserChange.bind(this)} />
                    <input id="password" type="password" placeholder="password" onChange={this.handlePasswordChange.bind(this)} />
                    <div className="auth-button" onClick={this.login.bind(this)}>login</div>
                </form>
            </div>
        );
    }
}

export default Login;
