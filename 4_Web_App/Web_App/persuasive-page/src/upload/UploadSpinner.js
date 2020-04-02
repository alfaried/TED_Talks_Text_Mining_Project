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
      await Promise.all(promises);

      this.setState({ successfullUploaded: true, uploading: false });
    } catch (e) {
      // Not Production ready! Do some error handling here instead...
      this.setState({ successfullUploaded: true, uploading: false });
    }
  }

  sendRequest(file) {
    return new Promise((resolve, reject) => {
      const req = new XMLHttpRequest();

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
        resolve(req.response);
      });

      req.upload.addEventListener("error", event => {
        const copy = { ...this.state.uploadProgress };
        copy[file.name] = { state: "error", percentage: 0 };
        this.setState({ uploadProgress: copy });
        reject(req.response);
      });

      const formData = new FormData();
      formData.append("file", file, file.name);

      req.open("POST", "http://localhost:8000/upload");
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
    if (!this.state.successfullUploaded && this.state.files.length >= 0 && !this.state.clearAfterSuccess){
      return (
        <button
          disabled={this.state.files.length <= 0 || this.state.uploading}
          //onClick={this.uploadFiles} //originally
          onClick={()=>
            this.setState({ successfullUploaded: true, clearAfterSuccess: true }, this.uploadFiles)}
        >
          Calculate Score
        </button>
      );
    }

    // if there is a file already uploaded, create a clear button
    if(this.state.clearAfterSuccess){
      return (
        <button
          disabled={this.state.files.length < 0 || this.state.uploading}
          onClick={()=>
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

    if(this.state.uploading || this.state.files.length <= 0){
      statusSpinner = "hidden";
      showScore = "hidden";
      display = "none"
    }

    if(this.state.successfullUploaded){
      statusSpinner = "visible";
      showScore = "hidden";
      display = "none"
    }


    if(this.state.scoreStatus){
      statusSpinner = "hidden";
      showScore = "visible";
      display = "";
    }

    // fake fetch for spinner expiration
    const fetchData = () => {
      setTimeout(()=>{
        //statusSpinner = "hidden";}, 2000)
        this.setState({ successfullUploaded : false, scoreStatus : true });}, 3000)
    }

    if(statusSpinner === "visible"){
      fetchData()
    }

    return (
      <div className="everything">
      <div className="main">
        <div className="Card">
          <div className="Upload">
            <span className="Title" style={{alignSelf: 'stretch'}}>Assess your document's persuasive score</span>
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
            <Spinner className="spinner" animation="border" variant="light" role="status" style={{visibility: statusSpinner}}>
              <span className="sr-only">Loading...</span>
            </Spinner>      

          <div className="finalScore" style={{visibility: showScore}}>
            <h1>88%</h1>
          </div>

          <div style={{visibility: showScore}}>
            <p style={{textDecoration: "underline"}}>Topic Keywords</p>
            <p>fuck, vagina</p>
          </div>   

        </div>
      </div>
      <div className="documentScore">
        <div className="scoreTable" style={{display: display }}>
          <DocumentTable />
        </div>
        </div>
      </div>
    );
  }
}

export default UploadSpinner;