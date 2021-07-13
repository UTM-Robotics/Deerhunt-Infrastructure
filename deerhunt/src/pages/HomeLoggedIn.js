import React from 'react'

class Home extends React.Component {

    constructor(props) {
        super(props)

        this.state = { email: props.email }
    }

    render() {
        return <div>
        <h1>Home Page</h1>
        <p>hello {this.state.email}</p>
        </div>
    }
}

export default Home
