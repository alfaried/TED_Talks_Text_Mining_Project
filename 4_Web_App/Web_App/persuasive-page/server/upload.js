const IncomingForm = require("formidable").IncomingForm;

module.exports = function upload(req, res) {
    var form = new IncomingForm();

    form.on("file", (field, file) => {
        console.log('Uploaded ' + file.name);
        file.path = __dirname + '/uploads/' + file.name;
        // Do something with the file
        // e.g. save it to the database
        // you can access it using file.path
    });
    form.on("end", () => {
        var response = res.json();
        console.log(response)
    });
    form.parse(req);
};
