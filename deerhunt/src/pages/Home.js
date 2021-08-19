import React from 'react'
import Navbar from './MenuBar/Navbar'


class Home extends React.Component {


    render() {
        return (
            <div>
                <Navbar>         
                </Navbar>
                <h1>Home Page</h1>
                <p>Not signed in</p>
            </div>
        )
    }
}

export default Home