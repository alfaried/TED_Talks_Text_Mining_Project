import React, { Component } from 'react';

//css
import '.././Assets/css/default.min.css';

class DocumentTable extends Component {
    constructor(props) {
        super(props) //since we are extending class Table so we have to use super in order to override Component class constructor
    }

    renderDocumentTable() {
        return this.props.data.map((row) => {
            const score = row['persuasion_score']
            const url = row['url']
            return (
                <tr key={url}>
                    <td>{score}</td>
                    <td>{url}</td>
                </tr>
            )
        })
    }


    renderTableHeader() {
        let header = Object.keys(this.props.data[0])
        return header.map((key, index) => {
            //return <th key={index}>{key.toUpperCase()}</th>
            return <th key={index}>{key}</th>
        })
    }

    render() {
        if (this.props.data.length > 0) {
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
            );
        } else {
            return null;
        } 
    }


}

export default DocumentTable;