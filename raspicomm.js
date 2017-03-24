const express = require('express');
const util = require('util');
const app = express();
const PythonShell = require('python-shell');
const uuid = require('uuid/v4');
const fs = require('fs');
var multer  = require('multer');
var upload = multer({ dest: 'Temp' });

const port = 3000;

app.post('/image', upload.single('image'), function (req, res) {

	console.log(req.file.size);

	// generate unique identifier

	// use that to generate filename of temporary image
	fname = req.file.filename
	console.log(fname);
	// pass that to python script
	// delete temporary image

	var options = {
		args: [fname]
	};
	PythonShell.run('predictbasedonweights.py', options, function(err, message){
 		if (err){
  			console.log('finished');
  			res.status(500).send("oops");
  		} else {
  			res.send(message);
  			fs.unlink(('Temp/' + fname),function(){
				console.log('Successfully unlinked.');
			});
		}
	});
});

app.listen(port, function () {
 	console.log(`Express running on port ${port}.`);
});