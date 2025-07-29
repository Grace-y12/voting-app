// Configuration
//const MODEL_PATH = "/static/js/models";
//const DETECTION_INTERVAL = 300; // ms
//const MIN_CONFIDENCE = 0.6;

// State variables
//let modelsLoaded = false;

// DOM Elements
//const imageUpload = document.getElementById('imageUpload');
//const imageDataInput = document.getElementById('imageDataInput');
//const registrationForm = document.getElementById('registrationForm');
//const submitBtn = document.getElementById('submitBtn');
//const loadingIndicator = document.getElementById('loadingIndicator');

// Load face-api.js dynamically
//function loadFaceAPI() {
  //  return new Promise((resolve, reject) => {
    //    const script = document.createElement('script');
     //   script.src = "/static/js/face-api.min.js";
       // script.onload = () => {
         //   console.log('face-api.js loaded');
           // resolve();
        //};
        //script.onerror = () => {
          //  reject(new Error('Failed to load face-api.js'));
        //};
        //document.head.appendChild(script);
    //});
//}

// Load face detection models
//async function loadModels() {
   // try {
        //await faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_PATH);
        //await faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_PATH);
        // await faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_PATH);
        //modelsLoaded = true;
        //console.log('Models loaded successfully');
    //} catch (error) {
        //console.error('Error loading models:', error);
        //throw error;
    //}
//}

// Handle image upload and face detection
//async function handleImageUpload(e) {
    //const file = e.target.files[0];
    //if (!file) {
      //  alert('Please select an image file.');
        //return;
    //}

    //try {
      //  const img = new Image();
        //img.onload = async function () {
            // Create canvas and draw image
          //  const canvas = document.createElement('canvas');
            //canvas.width = img.width;
            //canvas.height = img.height;
            //const ctx = canvas.getContext('2d');
            //ctx.drawImage(img, 0, 0);

            // Detect face from canvas
            //const detections = await faceapi.detectAllFaces(
              //  canvas,
                //new faceapi.TinyFaceDetectorOptions({
                  //  inputSize: 320,
                    //scoreThreshold: MIN_CONFIDENCE
                //})
            //).withFaceLandmarks().withFaceDescriptors();

            //if (detections.length === 0) {
              //  alert('No face detected in the uploaded image. Please try again.');
                //return;
            //}

            //if (detections.length > 1) {
              //  alert('Multiple faces detected. Please upload an image with only your face.');
                //return;
            //}

            // Save image data as base64
            // Save image data as base64 (stripped of the data URI prefix)
/*const imageData = canvas.toDataURL('image/jpeg');

let cleanedImageData = imageData;
if (cleanedImageData.includes('base64,')) {
    cleanedImageData = cleanedImageData.split('base64,')[1];
}

imageDataInput.value = cleanedImageData;

        };

        img.onerror = function () {
            alert('Error loading image. Please try another image.');
        };

        img.src = URL.createObjectURL(file);
    } catch (error) {
        console.error('Error processing image upload:', error);
        alert('Error processing image. Please try again.');
    }
}

// Form submission
async function handleFormSubmit(e) {
    e.preventDefault();

    if (!imageDataInput.value) {
        alert('Please upload a face image before registering.');
        return;
    }

    try {
        loadingIndicator.style.display = 'flex';
        submitBtn.disabled = true;

        const formData = new FormData(registrationForm);

        const response = await fetch('/register/api/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        });

        const data = await response.json();

        if (data.success) {
            alert(data.message);
            if (data.redirect_url) {
                window.location.href = data.redirect_url;
            }
        } else {
            alert(data.message || 'Registration failed. Please try again.');
        }
    } catch (error) {
        console.error('Submission error:', error);
        alert('An error occurred during registration. Please try again.');
    } finally {
        loadingIndicator.style.display = 'none';
        submitBtn.disabled = false;
    }
}

// Initialize everything
document.addEventListener('DOMContentLoaded', async () => {
    try {
        await loadFaceAPI();
        await loadModels();
        console.log('Initialization complete');

        imageUpload.addEventListener('change', handleImageUpload);
        registrationForm.addEventListener('submit', handleFormSubmit);
    } catch (err) {
        console.error('Initialization failed:', err);
        alert('Face detection initialization failed. Please reload the page.');
    }
});*/
