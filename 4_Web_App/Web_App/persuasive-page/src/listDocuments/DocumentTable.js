import React, { Component } from 'react';

//css
import '.././Assets/css/default.min.css';

class DocumentTable extends Component {
   constructor(props) {
      super(props) //since we are extending class Table so we have to use super in order to override Component class constructor
      this.state = { //state is by default an object
         topFiveScripts: [
            { url: "url1", score: 0.45 },
            { url: "url2", score: 0.51 },
            { url: "url3", score: 0.62 },
            { url: "url4", score: 0.44 },
            { url: "url5", score: 0.78 }

         ]
      }
   }

   renderDocumentTable() {
      return this.state.topFiveScripts.map((transcript, index) => {
         const { url, score } = transcript //destructuring
         return (
            <tr key={url}>
               <td>{url}</td>
               <td>{score}</td>
            </tr>
         )
      })
   }


   renderTableHeader() {
      let header = Object.keys(this.state.topFiveScripts[0])
      return header.map((key, index) => {
         //return <th key={index}>{key.toUpperCase()}</th>
         return <th key={index}>{key}</th>
      })
   }

    render() {
      return (
         <div>
            <h1 id='DocumentTitle'>Refer to this document to improve your persuasiveness</h1>
            <table id='topFiveScripts'>
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