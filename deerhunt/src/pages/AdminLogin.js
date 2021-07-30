import React from 'react'
import axios from 'axios'


import './Login.css'

class AdminLogin extends React.Component {

    constructor(props) {
        super(props)
        this.state = { username: '', password: '' }

        console.log(props)

        this.handleInputChange = this.handleInputChange.bind(this)
        this.Login = this.Login.bind(this)
    }

    handleInputChange(event) {
        const name = event.target.name
        this.setState({ [name]: event.target.value })
    }

    Login(event) {
        console.log("Logging in user" + this.state)
        axios.post('http://localhost:5000/api/admin', { username: this.state.username, password: this.state.password }).then(resp => {
            console.log(resp)
            this.props.onLogin(this.state.username)
        }).catch(err => {
            console.log(err)
        })
        event.preventDefault();
    }


    render() {
        return <div>
            <h1>Admin Login</h1>
            <div id='form'>
                <div id='username' className='textinput'>
                    <p>username</p>
                    <input type='text' name='username' onChange={this.handleInputChange}></input>
                </div>
                <div id='password' className='textinput'>
                    <p>Password</p>
                    <input type='password' name='password' onChange={this.handleInputChange}></input>
                </div>
                <div id='buttons'>
                    <button onClick={this.Login}>Login</button>
                </div>
            </div>
        </div>
    }
}

export default AdminLogin
