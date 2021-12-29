import React from 'react'
import TopNav from '../components/TopNav'
import axios from "../config/config";


class Home extends React.Component {

    constructor(props) {
        super(props)

        this.all_events = []
    }

    get_events(){
        axios.get("http://127.0.0.1:5000/api/events")
        .then(resp => {
            console.log(resp.data)
        }).catch(err => {
            console.log(err)
        })
    }

    render() {
        console.log("rendering")
        return (
            <div>
                <TopNav/>
                <h1>Home Page</h1>
                <p>Not signed in</p>
                {this.get_events()}
            </div>
        )
    }
}

export default Home
