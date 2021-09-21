import React from 'react'
import axios from 'axios'
import Navbar from './MenuBar/Navbar'
import { Input, Button, Box, Heading, Link } from "@chakra-ui/react"
import {
    FormControl,
    FormLabel,
  } from "@chakra-ui/react"


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
        return (
            <div>
                <Navbar/>
                <Box p={2}>
                    <Box textAlign="center">
                        <Heading>Deerhunt Admin Login</Heading>
                    </Box>
                    <Box my={4} textAlign="left">
                        <form>
                            <FormControl>
                                <FormLabel>Username</FormLabel>
                                <Input type="username" placeholder="username" />
                            </FormControl>
                            <FormControl mt={6}>
                                <FormLabel>Password</FormLabel>
                                <Input type="password" placeholder="*******" />
                            </FormControl>
                            <Button colorScheme="blue" width="full" mt={4} type="submit">
                                <Link></Link>
                            Sign In
                            </Button>
                        </form>
                    </Box>
                </Box>
            </div>
        )
    }
}

export default AdminLogin
