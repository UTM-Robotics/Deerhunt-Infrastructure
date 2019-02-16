import React from 'react';
import { Link } from 'react-router-dom';

class AppWrapper extends React.Component {
  render() {
    return (
      <div className='app-container'>
        <Link to={'/'}>Home</Link>
        <Link to={'/about'}>About</Link>
        <Link to={'/login'}>Login</Link>
        {this.props.children}
      </div>
    )
  }
}

export default AppWrapper;
