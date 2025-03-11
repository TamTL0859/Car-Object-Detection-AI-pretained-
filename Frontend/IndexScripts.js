const inputElement = document.getElementById("input");
inputElement.addEventListener("change", async function (event) {
    const file = event.target.files[0];
    const uploadLabel = document.getElementById("upload-label");
    //http://127.0.0.1:8001/index.html

    if (file.name.substr(file.name.length - 3) !== "mp4") {
        uploadLabel.style.color = "red";
        document.getElementById("upload-label").textContent = "You have to upload one .mp4 file";
        return;
    }
    let video = document.getElementById("uploaded-video");
    const fileURL = URL.createObjectURL(file);
    video.src = fileURL;

    const formData = new FormData();
    formData.append("file", file);

    const loadingBar = document.getElementById("loading-bar");
    loadingBar.style.visibility = "visible";

    try {
        //sends the video to the API which will return the processed video
        const response = await fetch("http://127.0.0.1:8000/video/upload-video", {
            method: "POST",
            body: formData
        });

        if (response.ok) {
            console.log("inside if");
            uploadLabel.style.color = "green";
            uploadLabel.textContent = "Status: " + response.statusText;

            const processedVideo = await response.blob();
            const processedVideoURL = URL.createObjectURL(processedVideo);

            const processedVideoPlayer = document.getElementById("processed-video");
            processedVideoPlayer.src = processedVideoURL;
            
            loadingBar.style.visibility = "hidden";
            processedVideoPlayer.style.visibility = "visible";

            processedVideoPlayer.play();
        }
    } catch (error) {
        loadingBar.style.visibility = "hidden";
        console.log(error);
        alert("Error");
    }
}

);
function updateProgressBar() {

}