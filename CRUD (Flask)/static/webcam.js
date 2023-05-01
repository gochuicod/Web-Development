var video = document.querySelector(".video");
var captureBtn = document.querySelector(".captureBtn");
var resetBtn = document.querySelector(".resetBtn");
var videoBtn = document.querySelector(".videoBtn");
var closeBtn = document.querySelector(".closeBtn");
var canvas = document.querySelector(".canvas");

var videoIcon = document.querySelector(".videoIcon");

canvas.style.display = "none";

videoBtn.addEventListener("click", () => {
    if(videoBtn.firstChild.classList.contains("bi-camera-video-off-fill")) {
        videoBtn.setAttribute("class","video btn btn-dark mx-3");
        videoBtn.firstChild.setAttribute("class","bi bi-camera-video-fill");
        attachCamera();
    } else {
        videoBtn.setAttribute("class","video btn btn-danger mx-3")
        videoBtn.firstChild.setAttribute("class","bi bi-camera-video-off-fill")
        detachCamera(video);
    }
});

captureBtn.addEventListener("click", () => {
    video.pause()
    var photo = document.querySelector(".photo")
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    
    var dataURL = canvas.toDataURL('image/jpeg');
    console.log(dataURL);
    
    photo.setAttribute('src', dataURL);
});

resetBtn.addEventListener("click", () => video.play());
closeBtn.addEventListener("click", () => {
    videoBtn.setAttribute("class","video btn btn-danger mx-3")
    videoBtn.firstChild.setAttribute("class","bi bi-camera-video-off-fill")
    detachCamera(video)
});

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