import React, { Component } from 'react';

import {
  BrowserRouter as Router,
  Route,
  //Link
} from 'react-router-dom';

//components
import Header from './components/headerComponent/header';
//import Homepage from './components/pages/homePage';
//import Result from './components/pages/results';
import UploadSpinner from './upload/UploadSpinner';
import DocumentTable from './listDocuments/DocumentTable';

//css
import './Assets/css/default.min.css';

class App extends Component {
  render(){
    return (
      <Router>
      <div className="App">
        <Header />
          <div className="container-fluid">
            <h1 className="title">
              Document Persuasion Assessment
            </h1>
            <div className="submitArea">
                <UploadSpinner />
            </div>
          </div>
      </div>
      </Router>

    );
  }
}

export default App;
