import React, { Component } from 'react';

//css
import '.././Assets/css/default.min.css';

class DocumentTable extends Component {
   constructor(props) {
      super(props) //since we are extending class Table so we have to use super in order to override Component class constructor
      this.state = { //state is by default an object
         speakers: [
            { Title: "How to turn climate anxiety into action", Speaker: 'Renee Lertzman', Score: 0.89 },
            { Title: "The next outbreak?", Speaker: 'Bill Gates', Score: 0.82 }, 
            { Title: "How to make stress your friend", Speaker: 'Kelly Mcgonigal', Score: 0.78 },
            { Title: "Your body language shapes who you are", Speaker: 'Amy Cuddy', Score: 0.75 }
         ]
      }
   }

   renderDocumentTable() {
      return this.state.speakers.map((speakerName, index) => {
         const { Title, Speaker, Score } = speakerName //destructuring
         return (
            <tr key={Title}>
               <td>{Title}</td>
               <td>{Speaker}</td>
               <td>{Score}</td>
            </tr>
         )
      })
   }


   renderTableHeader() {
      let header = Object.keys(this.state.speakers[0])
      return header.map((key, index) => {
         //return <th key={index}>{key.toUpperCase()}</th>
         return <th key={index}>{key}</th>
      })
   }

    render() {
      return (
         <div>
            <h1 id='DocumentTitle'>Documents that can improve your persuasion</h1>
            <table id='speakers'>
               <tbody>
                  <tr>{this.renderTableHeader()}</tr>
                  {this.renderDocumentTable()}
               </tbody>
            </table>
         </div>
      )
   }


 }

export default DocumentTable;
