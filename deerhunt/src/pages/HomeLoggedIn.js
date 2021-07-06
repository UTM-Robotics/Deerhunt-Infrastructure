import React from 'react'

class Home extends React.Component {

    constructor(props) {
        super(props)

        this.state = { username: props.username }
    }

    render() {
        return <div>
        <h1>Home Page</h1>
        <p>hello {this.state.username}</p>
        </div>
    }
}

export default Home