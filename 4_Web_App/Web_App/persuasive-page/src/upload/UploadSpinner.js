import React, { Component } from "react";
import Dropzone from "../dropzone/Dropzone";
import "./Upload.css";
import Progress from "../progress/Progress";
import Spinner from 'react-bootstrap/Spinner';
import DocumentTable from '.././listDocuments/DocumentTable';



class UploadSpinner extends Component {
    constructor(props) {
        super(props);
        this.state = {
            files: [],
            uploading: false,
            uploadProgress: {},
            successfullUploaded: false,
            clearAfterSuccess: false,
            scoreStatus: false, // to show the score after the fake timeout call is done
            persuasionScore: null,
            topicTheme: '',
            topicKeywords: [],
            topPersuasiveTalks: []
        };

        this.onFilesAdded = this.onFilesAdded.bind(this);
        this.uploadFiles = this.uploadFiles.bind(this);
        this.sendRequest = this.sendRequest.bind(this);
        this.renderActions = this.renderActions.bind(this);
    }

    onFilesAdded(files) {
        this.setState(prevState => ({
            files: prevState.files.concat(files)
        }));
    }


    async uploadFiles() {
        this.setState({ uploadProgress: {}, uploading: true });
        const promises = [];
        this.state.files.forEach(file => {
            promises.push(this.sendRequest(file));
        });
        try {
            promises[0].then(() => {
                this.setState({ successfullUploaded: true, uploading: false, scoreStatus: true });
            });
        } catch (e) {
            // Not Production ready! Do some error handling here instead...
            this.setState({ successfullUploaded: true, uploading: false });
        }
    }

    sendRequest(file) {
        return new Promise((resolve, reject) => {
            const req = new XMLHttpRequest();
            let response;
            req.upload.addEventListener("progress", event => {
                if (event.lengthComputable) {
                    const copy = { ...this.state.uploadProgress };
                    copy[file.name] = {
                        state: "pending",
                        percentage: (event.loaded / event.total) * 100
                    };
                    this.setState({ uploadProgress: copy });
                }
            });

            req.upload.addEventListener("load", event => {
                const copy = { ...this.state.uploadProgress };
                copy[file.name] = { state: "done", percentage: 100 };
                this.setState({ uploadProgress: copy });
            });

            req.upload.addEventListener("error", event => {
                const copy = { ...this.state.uploadProgress };
                copy[file.name] = { state: "error", percentage: 0 };
                this.setState({ uploadProgress: copy });
            });

            const formData = new FormData();
            formData.append("input", file, file.name);

            req.open("POST", "http://localhost:8088/api/persuasion-score");
            req.onload = function () {
                if (req.readyState === 4) {
                    if (req.status === 200) {
                        var response = JSON.parse(req.responseText);
                        this.setState({
                            persuasionScore: response['persuasion-score'].toFixed(20) * 100,
                            topicKeywords: response['topic-keywords'].join(', '),
                            topicTheme: response['topic-theme'],
                            topPersuasiveTalks: response['top-5-persuasive-talks']
                        });
                        resolve(req.response)
                    } else {
                        console.error(req.statusText);
                        reject(req.response);
                    }
                }
            }.bind(this);
            req.send(formData);
        });
    }

    renderProgress(file) {
        const uploadProgress = this.state.uploadProgress[file.name];
        if (this.state.uploading || this.state.successfullUploaded) {
            return (
                <div className="ProgressWrapper">
                    <Progress progress={uploadProgress ? uploadProgress.percentage : 0} />
                    <img
                        className="CheckIcon"
                        alt="done"
                        src="baseline-check_circle_outline-24px.svg"
                        style={{
                            opacity:
                                uploadProgress && uploadProgress.state === "done" ? 0.5 : 0
                        }}
                    />
                </div>
            );
        }
    }


    renderActions() {


        /**
        if (this.state.successfullUploaded) {
          return (
            <button
              onClick={() =>
                this.setState({ files: [], successfullUploaded: false })
              }
            >
              Clear
            </button>
          );
        } else {
          return (
            <button
              disabled={this.state.files.length < 0 || this.state.uploading}
              //onClick={this.uploadFiles}
              onClick={()=>
                this.setState({ successfullUploaded: true }, this.uploadFiles)}
            >
              Calculate Score
            </button>
          );
        }
      }
    
      **/

        //if file got uploaded, show clear button
        if (this.state.successfullUploaded) {
            return (
                <button
                    onClick={() =>
                        this.setState({ files: [], successfullUploaded: false })
                    }
                >
                    Clear
                </button>
            );
        }

        // if there are no files, create calculate function, enable when a file is selected
        if (!this.state.successfullUploaded && this.state.files.length >= 0 && !this.state.clearAfterSuccess) {
            return (
                <button
                    disabled={this.state.files.length <= 0 || this.state.uploading}
                    //onClick={this.uploadFiles} //originally
                    onClick={() =>
                        this.setState({ successfullUploaded: true, clearAfterSuccess: true }, this.uploadFiles)}
                >
                    Calculate Score
                </button>
            );
        }

        // if there is a file already uploaded, create a clear button
        if (this.state.clearAfterSuccess) {
            return (
                <button
                    disabled={this.state.files.length < 0 || this.state.uploading}
                    onClick={() =>
                        this.setState({ files: [], successfullUploaded: false, clearAfterSuccess: false, scoreStatus: false })}
                >
                    Clear
                </button>
            );

        }
    }

    render() {
        //for spinner visibility
        let statusSpinner = "hidden"; //for spinner
        let showScore = "hidden";
        // Toggle table
        let display = "none";

        if (this.state.uploading || this.state.files.length <= 0) {
            statusSpinner = "hidden";
            showScore = "hidden";
            display = "none"
        }

        if (this.state.successfullUploaded) {
            statusSpinner = "visible";
            showScore = "hidden";
            display = "none"
        }


        if (this.state.scoreStatus) {
            statusSpinner = "hidden";
            showScore = "visible";
            display = "";
        }


        return (
            <div className="everything">
                <div className="main">
                    <div className="Card">
                        <div className="Upload">
                            <span className="Title" style={{ alignSelf: 'stretch' }}>Assess your document's persuasive score</span>
                            <div className="Content">
                                <div>
                                    <Dropzone
                                        onFilesAdded={this.onFilesAdded}
                                        disabled={this.state.uploading || this.state.successfullUploaded}
                                    />
                                </div>
                                <div className="Files">
                                    {this.state.files.map(file => {
                                        return (
                                            <div key={file.name} className="Row">
                                                <span className="Filename">{file.name}</span>
                                                {this.renderProgress(file)}
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>
                            <div className="Actions">{this.renderActions()}</div>
                        </div>
                    </div>


                    <div className="resultBufferArea">
                        <p>
                            Persuasive Score:
                        </p>
                        <Spinner className="spinner" animation="border" variant="light" role="status" style={{ visibility: statusSpinner }}>
                            <span className="sr-only">Loading...</span>
                        </Spinner>

                        <div className="finalScore" style={{ visibility: showScore }}>
                            <h1>{this.state.persuasionScore}%</h1>
                        </div>

                        <div style={{ visibility: showScore }}>
                            <p style={{ textDecoration: "underline" }}>Topic Theme</p>
                            <p>{this.state.topicTheme}</p>
                            <p style={{ textDecoration: "underline" }}>Topic Keywords</p>
                            <p>{this.state.topicKeywords}</p>
                        </div>

                    </div>
                </div>
                <div className="documentScore">
                    <div className="scoreTable" style={{ display: display }}>
                        <DocumentTable data={this.state.topPersuasiveTalks}/>
                    </div>
                </div>
            </div>
        );
    }
}

export default UploadSpinner;