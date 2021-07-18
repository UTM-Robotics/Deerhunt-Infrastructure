import React from 'react'
import './Home.css'

class Home extends React.Component {

    constructor(props) {
        super(props)

        this.state = { email: props.email }
    }

    render() {
        return <div>
        <h1>Home Page</h1>
        {/* TODO: Add a conditional statement for when user not logged in */}
        <h3>Welcome {this.state.email}</h3>
        <div>
        </div>
        </div>
    }
}

export default Home
