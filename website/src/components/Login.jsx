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
            message = "The user or password is incorrect/invalid"
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

        console.log(requestData);
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

    handleEnterKeyPress(e: any) {
        if (e.charCode == 13 || e.keyCode == 13) {
            this.login();
        }
    }

    handleUserChange(e: any) {
        this.setState({
            user: e.target.value
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
                    <input type="text" placeholder="username" onChange={this.handleUserChange.bind(this)} />
                    <input type="password" placeholder="password" onChange={this.handlePasswordChange.bind(this)} />
                    <div className="auth-button" onClick={this.login.bind(this)}>login</div>
                </form>
            </div>

        );
    }
}

export default Login;
