import React from 'react'
import axios from 'axios'


import './Login.css'

class Login extends React.Component {

    constructor(props) {
        super(props)
        this.state = { email: '', password: '' }

        console.log(props)

        this.handleInputChange = this.handleInputChange.bind(this)
        this.Login = this.Login.bind(this)
        this.CreateUser = this.CreateUser.bind(this)
    }

    handleInputChange(event) {
        const name = event.target.name
        this.setState({ [name]: event.target.value })
    }

    Login(event) {
        console.log("Logging in user" + this.state)
        axios.post('http://localhost:5000/login', { email: this.state.email, password: this.state.password }).then(resp => {
            console.log(resp)
            this.props.onLogin(this.state.email)
        }).catch(err => {
            console.log(err)
        })
        event.preventDefault();
    }

    CreateUser() {
        axios.post('http://localhost:5000/register', { email: this.state.email, password: this.state.password }).then(resp => {
            console.log(resp)
            this.props.onLogin(this.state.email)
        }).catch(err => {
            console.log(err)
        })
        console.log("Creating user")
    }


    render() {
        return <div>
            <h1>Enter email and password</h1>
            <div id='form'>
                <div id='email' className='textinput'>
                    <p>Email</p>
                    <input type='text' name='email' onChange={this.handleInputChange}></input>
                </div>
                <div id='password' className='textinput'>
                    <p>Password</p>
                    <input type='password' name='password' onChange={this.handleInputChange}></input>
                </div>
                <div id='buttons'>
                    <button onClick={this.Login}>Login</button>
                    <button onClick={this.CreateUser}>Create User</button>
                </div>
            </div>
        </div>
    }
}

export default Login
