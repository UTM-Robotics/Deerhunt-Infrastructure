import React from 'react';

class Submit extends React.Component {

    render() {
        return (
            <div>
            <form action="/api/submit" method="POST" encType="multipart/form-data"> 
            <p>Please select the file you would like to upload. </p>
            <input type="text" name="position"/> <br/> 
            <input type="file" name="upload"/> <br/> 
            <input type="submit" value="Upload File"/>
            </form>
            </div>
        );
    }
}

export default Submit;
