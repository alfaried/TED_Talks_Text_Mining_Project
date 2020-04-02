import React, { Component } from 'react';
// Use Link to allow dynamic rendering from homepage to other pages

class Header extends Component {
  render(){
    return (
      <header>

        <div className="logo">
         Text Mining G2T1
        </div>

        <nav>
          <ul>
          {/**
            <li>
              <Link to="/Results">Results</Link>
            </li>
            **/}
          </ul>
        </nav>

      </header>
    );
  }
}

export default Header;