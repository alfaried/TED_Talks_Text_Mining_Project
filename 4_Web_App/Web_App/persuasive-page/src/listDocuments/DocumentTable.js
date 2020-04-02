import React, { Component } from 'react';

//css
import '.././Assets/css/default.min.css';

class DocumentTable extends Component {
   constructor(props) {
      super(props) //since we are extending class Table so we have to use super in order to override Component class constructor
      this.state = { //state is by default an object
         speakers: [
            { Topic: "Environmental Awareness", Title: "How to turn climate anxiety into action", Speaker: 'Renee Lertzman', Score: 0.89 }
         ]
      }
   }

   renderDocumentTable() {
      return this.state.speakers.map((speakerName, index) => {
         const { Topic, Title, Speaker, Score } = speakerName //destructuring
         return (
            <tr key={Title}>
               <td>{Topic}</td>
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
            <h1 id='DocumentTitle'>Refer to this document to improve your persuasiveness</h1>
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
