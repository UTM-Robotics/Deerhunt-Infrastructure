import React from 'react'
import axios from 'axios'
import Navbar from './MenuBar/Navbar'
import { Input, Button, Box, Heading } from "@chakra-ui/react"
import {
    FormControl,
    FormLabel,
  } from "@chakra-ui/react"


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
        console.log("Logging in user" + this.state.email)
        axios.post('http://localhost:5000/api/login', { email: this.state.email, password: this.state.password }).then(resp => {
            console.log(resp)
            this.props.onLogin(this.state.email)
        }).catch(err => {
            console.log(err)
        })
        event.preventDefault();
    }

    CreateUser() {
        axios.post('http://localhost:5000/api/register', { email: this.state.email, password: this.state.password }).then(resp => {
            console.log(resp)
            this.props.onLogin(this.state.email)
        }).catch(err => {
            console.log(err)
        })
        console.log("Creating user")
    }


    render() {
        return (
            <div>
                <Navbar/>
                <Box p={2}>
                <Box textAlign="center">
                    <Heading>Sign in to Deerhunt</Heading>
                </Box>
                <Box my={4} textAlign="left">
                    <form>
                        <FormControl>
                            <FormLabel>Email</FormLabel>
                            <Input type="email" placeholder="UofT email" />
                        </FormControl>
                        <FormControl mt={6}>
                            <FormLabel>Password</FormLabel>
                            <Input type="password" placeholder="*******" />
                        </FormControl>
                    <Button colorScheme="blue" width="full" mt={4} type="submit">
                    Sign In
                    </Button>
                </form>
                </Box>
            </Box>
          </div>
        )
    }
}

export default Login
