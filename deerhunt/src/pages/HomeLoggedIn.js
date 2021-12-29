import React from 'react'
import TopNav from '../components/TopNav'
import { Heading, Box} from "@chakra-ui/react";

class HomeLoggedIn extends React.Component {

    constructor(props) {
        super(props)

        this.state = { email: props.email }
    }

    render() {
        return (
        <div>
            <TopNav isloggedin={true}/>
            <Box textAlign="center">
            <Heading > The UofT AI Competition Hub </Heading>
            
            <Heading>Welcome {this.state.email}</Heading>
            </Box>
            </div>
        )
    }
}

export default HomeLoggedIn
