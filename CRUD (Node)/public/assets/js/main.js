let app = angular.module("app",[]);

app.run($rootScope => {
    $rootScope.levels = ["1","2","3","4"];
    $rootScope.courses = ["BSIT","BSCS","BSCPE","BSAMT"]
    $rootScope.studentIdNo = null;
    $rootScope.studentImgPath = null;
    $rootScope.userId = null;
    $rootScope.username = null;
})

app.controller("userList",($scope,$http,$rootScope) => {
    $scope.header=["username","password","edit | delete"];
    $http.get("/user").then(response => {
        $scope.users=response.data;
        if(response.data.length === 0) $scope.setDisplay = {"display":"none"}
        else $scope.setDisplay = {"display":"block"}
    });
    $scope.remove = id => {
        document.querySelector(".yesBtn").onclick = () => {
            $http.delete(`/user/${id}`).then(() => location.reload())
        }
    }
    $scope.updateUser = (username,id) => {
        $rootScope.userId = id;
        $rootScope.username = username;
    }
})

app.controller("studentList",($scope,$http,$rootScope) => {
    $scope.header=["lastname","firstname","course","level","edit | delete"];
    $http.get("/student").then(response => {
        $scope.students=response.data;
        if(response.data.length === 0) $scope.setDisplay = {"display":"none"}
        else $scope.setDisplay = {"display":"block"}
    });
    $scope.remove = idno => {
        document.querySelector(".yesBtn").onclick = () => {
            $http.delete(`/student/${idno}`).then(() => location.reload())
        }
    } 
    $scope.updateStudent = (idno,lastname,firstname,imagepath) => {
        $rootScope.studentIdNo = idno;
        $rootScope.lastname = lastname;
        $rootScope.firstname = firstname;
        $rootScope.studentImgPath = imagepath;
    }
})

app.controller("updateUser",($scope,$http,$rootScope) => {
    $scope.updateUser = () => {
        if($scope.password){
            $http.put("/user/update", {
                id: $rootScope.userId,
                username: $rootScope.username,
                password: $scope.password
            }).then(() => location.reload())
        } else alert("Fill in the empty fields!")
    }
})

app.controller("updateStudent",($scope,$http,$rootScope) => {
    $rootScope.$watch(() => $scope.image = $rootScope.studentImgPath)
    $scope.updateStudent = () => {
        $http.put("/student/update",{
            idno: $rootScope.studentIdNo,
            lastname: $scope.lastname,
            firstname: $scope.firstname,
            course: $scope.selectedCourse,
            level: $scope.selectedLevel
        }).then(() => location.reload())
    }
})

let lastname = document.querySelector(".lastname"), firstname = document.querySelector(".firstname");
let course = document.querySelector(".course"), level = document.querySelector(".level");
let video = document.querySelector(".video");

Webcam.set({
    width: 550,
    height: 310,
    dest_width: 1080,
    dest_height: 720,
    image_format: 'jpeg',
    jpeg_quality: 100,
    flip_horiz: true,
})

document.querySelector(".capture").addEventListener("click", () => Webcam.freeze())
document.querySelector(".reset").addEventListener("click", () => Webcam.unfreeze())
document.querySelector(".upload").addEventListener("click", () => {
    if(lastname.value != "" && firstname.value != ""){
        Webcam.snap(data_uri => {
            Webcam.upload(data_uri,`/student?lastname=${lastname.value}&firstname=${firstname.value}&course=${course.value}&level=${level.value}`,(code,image) => {
                alert("New Student Added!")
                location.reload();
            })
        })
    } else alert('Fill in the empty fields!')
})

video.addEventListener("click", () => {
    if(video.firstChild.classList.contains("bi-camera-video-off-fill")){
        video.setAttribute("class","video btn btn-dark mx-3")
        video.firstChild.setAttribute("class","bi bi-camera-video-fill")
        Webcam.attach('.camera')
    } else {
        video.setAttribute("class","video btn btn-danger mx-3")
        video.firstChild.setAttribute("class","bi bi-camera-video-off-fill")
        Webcam.reset('.camera')
    }
})