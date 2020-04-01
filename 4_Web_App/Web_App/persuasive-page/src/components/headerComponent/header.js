import React, { Component } from 'react';
// Use Link to allow dynamic rendering from homepage to other pages
import { Link } from 'react-router-dom';

class Header extends Component {
  render(){
    return (
      <header>

      	<div className="logo">
			   Kebabz Text Mining Group G2T1
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
