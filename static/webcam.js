if(navigator.mediaDevices.getUserMedia){
    navigator.mediaDevices.getUserMedia({video:true})
    .then(function(stream){
        var video = document.getElementById('camera-feed');
        video.srcObject = stream
    })
    .catch(function(error){
        console.log("fuck it");
    });
}
