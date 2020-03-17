
var video = document.querySelector('#video');

//camera will be user(selfie) if the device is mobile
var currentFacingMode = 'user';

error_message = document.querySelector('#error-message');

function displayErrorMessage(error_msg, error) {
  error = error || "";
  if (error) {
    console.log(error);
  }
  error_message.innerText = error_msg;
  error_message.classList.add("visible");
}

document.addEventListener('DOMContentLoaded', function (event) {
  // do some WebRTC checks before creating the interface
  //only works on secured connections (https).
  DetectRTC.load(function () {
    // do some checks
    if (DetectRTC.isWebRTCSupported == false) {
      alert(
        'Please use Chrome, Firefox, iOS 11, Android 5 or higher, Safari 11 or higher',
      );
      displayErrorMessage('use Chrome, Firefox, iOS 11, Android 5 or higher, Safari 11 or higher')
    } else {
      if (DetectRTC.hasWebcam == false) {
        alert('Please install an external webcam device.');
        displayErrorMessage("Please install an external webcam device.")
      } else {
        initCameraStream();
      }
    }

  });
});

function initCameraStream() {
  
  var constraints = {
    audio: false,
    video: {
      facingMode: currentFacingMode,
    },
  };
  //request the camera
  navigator.mediaDevices
    .getUserMedia(constraints)
    .then(handleSuccess)
    .catch(handleError);
  function handleSuccess(stream) {
    video.srcObject = stream;
    video.play();
  }
  function handleError(error) {
    console.log(error);
    if (error === 'PermissionDeniedError') {
      alert('Permission denied. Please refresh and allow camera access.');
    }
  }
}

function takeSnapshot() {

  var hidden_canvas = document.querySelector('#hiddenCanvas')
  var context = hidden_canvas.getContext('2d');
  
  var width = video.videoWidth;
  var height = video.videoHeight;

  if (width && height) {

    // Setup a canvas with the same dimensions as the video.
    hidden_canvas.width = width;
    hidden_canvas.height = height;

    // Make a copy of the current frame in the video on the canvas.
    context.drawImage(video, 0, 0, width, height);

    // replace the video with the picture taken
    video.classList.add("hidden")
    hidden_canvas.classList.remove('hidden')
    
    dataURL = hidden_canvas.toDataURL('image/png');

    return dataURL.replace(/^data:image\/(png|jpg);base64,/, "")
  }
}

function post(path, params, method) {
  method = method || "post"; // Set method to post by default if not specified.

  var form = document.createElement("form");
  form.setAttribute("method", method);
  form.setAttribute("action", path);

  for (var key in params) {
    if (params.hasOwnProperty(key)) {
      var hiddenField = document.createElement("input");
      hiddenField.setAttribute("type", "hidden");
      hiddenField.setAttribute("name", key);
      hiddenField.setAttribute("value", params[key]);

      form.appendChild(hiddenField);
    }
  }

  document.body.appendChild(form);
  form.submit();
}

function signUp() {
  var endpoint = "/sign_up"
  var snap = takeSnapshot();
  var firstname = $('#firstname').val();
  var lastname = $('#lastname').val();
  var email = $('#email').val();

  data = {
    "img": snap,
    "firstname": firstname,
    "lastname": lastname,
    "email": email,
  }

  post(endpoint, data)
}

function login() {
  var endpoint = "/login"
  var snap = takeSnapshot();
  post(endpoint, {
    "img": snap
  })
}
