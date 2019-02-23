import React from 'react';
import $ from 'jquery';

class Register extends React.Component {
    constructor() {
        super();
        this.state = {
            "user": "",
            "password": "",
            "isadmin": false
        }
    }

    componentDidMount() {
        document.addEventListener("keypress", this.handleEnterKeyPress.bind(this));
        this.isAdmin()
    }

    isAdmin() {
        $.ajax({
            url: '/api/isadmin',
            type: 'GET',
            success: (responseData) => {
                var parsed = responseData == "True" ? true : false;
                if (parsed) {
                    this.setState({
                        "isadmin": true
                    });
                }
            }
        });
    }

    addError(type: string) {
        $('.error-message').remove();
        $('.success-message').remove();
        var message = "";
        if (type === 'user') {
            message = "Please enter an user"
        }
        else if (type === 'password') {
            message = "Please enter a password";
        }
        else {
            message = "user already exists"
        }
        var errorMessage = '<p class="error-message">' + message + '</p>';
        $('.register-button').after(errorMessage);
    }

    register() {
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
            url: '/api/register',
            type: 'POST',
            data: requestData,
            contentType: 'application/json',
            success: (responseData) => {
                $('.error-message').remove();
                $('.success-message').remove();
                var successMessage = '<p class="success-message">Successfully Added</p>';
                $('.register-button').after(successMessage);
            },
            error: () => {
                this.addLoginError('user');
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

    render() {
        return (
            <div className="register-container">
                <h1>Register</h1>
                <form className="register-form" id="register-form">
                    <input type="text" placeholder="username" onChange={this.handleUserChange.bind(this)} />
                    <input type="password" placeholder="password" onChange={this.handlePasswordChange.bind(this)} />
                    <div className="register-button" onClick={this.register.bind(this)}>register</div>
                </form>
            </div>
        );
    }
}

export default Register;
