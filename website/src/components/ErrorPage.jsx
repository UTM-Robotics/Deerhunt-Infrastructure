import React from 'react';
import deer from './../assets/images/deer.png';

class ErrorPage extends React.Component {
    render() {
        return (
            <div>
                <img className="error-page" src={deer} />
                <div className="message-box">
                    <h1>404</h1>
                    <p>oDeer();</p>
                    <div className="buttons-con">
                        <div className="action-link-wrap">
                            <a href="/home" className="link-button">Go to Home Page</a>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default ErrorPage;
