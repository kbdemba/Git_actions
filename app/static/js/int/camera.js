// References to all the element we will need.
var video = document.querySelector('#camera-stream'),
    start_camera = document.querySelector('#start-camera'),
    take_photo_btn = document.querySelector('#take-photo'),
    error_message = document.querySelector('#error-message');


// The getUserMedia interface is used for handling camera input.
// Some browsers need a prefix so here we're covering all the options
navigator.getMedia = ( navigator.getUserMedia ||
                      navigator.webkitGetUserMedia ||
                      navigator.mozGetUserMedia ||
                      navigator.msGetUserMedia);

if(!navigator.getMedia){
  displayErrorMessage("Your browser doesn't have support for the navigator.getUserMedia interface.");
}
else{

  // Request the camera.
  navigator.getMedia(
    {
      video: true
    },
    // Success Callback
    function(stream){
      video.src = window.URL.createObjectURL(stream);
      video.play();
    },
    // Error Callback
    function(err){
      displayErrorMessage("There was an error with accessing the camera stream: " + err.name, err);
    }
  );

}

// Mobile browsers cannot play video without user input,
// so here we're using a button to start it manually.
start_camera.addEventListener("click", function(e){
  e.preventDefault();
  // Start video playback manually.
  video.play();
  start_camera.classList.add("invisible");
  video.classList.remove("invisible")
});

take_photo_btn.addEventListener("click", function(e){
  e.preventDefault();
  var snap = takeSnapshot();
});

function takeSnapshot(){
  // Here we're using a trick that involves a hidden canvas element.

  var hidden_canvas = document.querySelector('canvas'),
      context = hidden_canvas.getContext('2d');

  var width = video.videoWidth,
      height = video.videoHeight;

  if (width && height) {

    // Setup a canvas with the same dimensions as the video.
    hidden_canvas.width = width;
    hidden_canvas.height = height;

    // Make a copy of the current frame in the video on the canvas.
    context.drawImage(video, 0, 0, width, height);

    // Turn the canvas image into a dataURL that can be used as a src for our photo.
    dataURL = hidden_canvas.toDataURL('image/png');

    data = {
        "img": dataURL.replace(/^data:image\/(png|jpg);base64,/, "")
    }

    var endpoint = "/identify"

    $.ajax({
      type: "POST",
      url: endpoint,
      data: JSON.stringify(data),
      contentType: 'application/json',
      processData: false
    });

    return dataURL
  }
}


function displayErrorMessage(error_msg, error){
  error = error || "";
  if(error){
    console.log(error);
  }

  error_message.innerText = error_msg;
  error_message.classList.add("visible");
}