var fs = require("fs");
var request = require("request");
var mv = require("mv");

/**var options = { method: 'POST',
  url: 'https://api.enface.ai/v1/detect',
  headers: 
   { 'postman-token': '8e1cb668-d525-9b63-3a45-7f6c5acbac4a',
     'cache-control': 'no-cache',
     'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' },
  formData: 
   { images: 
      { value: fs.createReadStream("/home/volodymyr/pics/15.jpg"),
        options: 
         { filename: '15.jpg',
           contentType: null } },
     token: '722cbb30-15ff-11eb-a983-d341f34204e0',
     feature_check: 'gender' } };

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});**/

fs.readdir("/home/volodymyr/Documents/res/new/", async (err, files) => {
  for (let index = 0; index < files.length; index++){ 
  //files.forEach(file => {
    var options = { method: 'POST',
    url: 'https://api.enface.ai/v1/detect',
    headers: 
     { 'postman-token': '8e1cb668-d525-9b63-3a45-7f6c5acbac4a',
       'cache-control': 'no-cache',
       'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' },
    formData: 
     { images: 
        { value: fs.createReadStream("/home/volodymyr/Documents/res/new/" + files[index]),
          options: 
           { filename: '15.jpg',
             contentType: null } },
       token: '722cbb30-15ff-11eb-a983-d341f34204e0',
       feature_check: 'gender' } };
     
  await request(options, function (error, response, body) {
    if (error) console.log(error);
	try {
	  let gender = JSON.parse(body).results[0][0].features[0].result;

	  if (gender == "male") {
	    mv("/home/volodymyr/Documents/res/new/" + files[index], "/home/volodymyr/Documents/res/male/" + files[index], (err) => {
    	      if (err) console.log(err);
            });
	  } else {
	    mv("/home/volodymyr/Documents/res/new/" + files[index], "/home/volodymyr/Documents/res/female/" + files[index], (err) => {
    	      if (err) console.log(err);
            });
	  }
	} catch (err) {
	  console.log(err);
	}
    console.log(body);
  });
    
  }//);
  
});
