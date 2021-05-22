import React from 'react';
import $ from 'jquery';
import logo from './../assets/images/deerhuntcropped.png'
import discord from './../assets/images/discord_logo.png';

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
                var parsed = responseData == "True" ? true : false;
                if (parsed) {
                    window.location.replace("/home");
                }
            }
        });
    }


    addLoginError(type) {
        $('.error-message').remove();
        var message = "";
        if (type === 'user') {
            message = "Please enter an user"
        }
        else if (type === 'password') {
            message = "Please enter a password";
        }
        else if (type === 'login') {
            message = "The user or password is incorrect or unverified(check spam). If you still cannot log in, please contact us via the Discord below!"
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
            <div>
                <img src={logo} alt="Deer Hunt Logo" className="deer-hunt-logo"/>
                <div className="auth-form-container">
                    <form className="login-form" id="login-form">
                        <input id="username" type="text" placeholder="Username/Email" onChange={this.handleUserChange.bind(this)} />
                        <input id="password" type="password" placeholder="Password" onChange={this.handlePasswordChange.bind(this)} />
                        <div className="auth-button" onClick={this.login.bind(this)}>login</div>
                    </form>
                    <p>Haven't made an account yet?</p>
                    <a href="/register">Sign Up</a>
                    <br></br>
                    <a href="/reset"> Forgot Password?</a>
                </div>
                <div className="discord-container">
                    <p> Join the Discord Community for updates!</p>
                    <a href="https://discord.gg/xW6AB6MT">

                    <img width="100px" src={discord}></img>
                    </a>
                </div>
            </div>
        );
    }
}

export default Login;
