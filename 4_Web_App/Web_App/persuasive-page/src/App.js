import React, { Component } from 'react';

//components
import Header from './components/headerComponent/header';
import UploadSpinner from './upload/UploadSpinner';

//css
import './Assets/css/default.min.css';

class App extends Component {
  render(){
    return (
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

    );
  }
}

export default App;
