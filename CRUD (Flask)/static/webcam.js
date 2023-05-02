var video = document.querySelector(".video");
var videoBtn = document.querySelector(".videoBtn");
var videoIcon = document.querySelector(".videoIcon");
var captureBtn = document.querySelector(".captureBtn");
var resetBtn = document.querySelector(".resetBtn");
var uploadBtn = document.querySelector(".uploadBtn");
var uploadWebcamImageForm = document.querySelector('.uploadWebcamImageForm');

captureBtn.addEventListener("click", () => {
    video.pause()

    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const image_data = canvas.toDataURL();

    document.querySelector('.image_data').value = image_data
    document.querySelector('.filename').value = 'captured_image.jpg'

});

videoBtn.addEventListener("click", () => {
    if(videoBtn.firstElementChild.classList.contains("bi-camera-video-off-fill")) {
        videoBtn.setAttribute("class","videoBtn btn btn-danger shadow mx-4");
        videoBtn.firstElementChild.setAttribute("class","bi bi-camera-video-fill");
        attachCamera();
    } else {
        videoBtn.setAttribute("class","videoBtn btn btn-dark shadow mx-4")
        videoBtn.firstElementChild.setAttribute("class","bi bi-camera-video-off-fill")
        detachCamera(video);
    }
});

resetBtn.addEventListener("click",  () => video.play());

uploadBtn.addEventListener("click", () => {
    document.forms[4].submit()
    // console.log(uploadWebcamImageForm.value);
    // uploadWebcamImageForm.submit()
})
 
var detachCamera = element => {
    try {
        element.srcObject.getTracks().forEach(track => track.stop())
        video.srcObject = null;
    } catch {
        console.log("No camera attached");
    }
}

var attachCamera = () => {
    navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
        video.srcObject = stream;
        video.play();
    }).catch(err => {
        console.log("An error occurred: " + err);
    });
}