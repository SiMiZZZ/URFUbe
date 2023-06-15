const videoNameInput = document.getElementById('video_name')
const videoFileInput = document.getElementById('video_file')
const submitBtn = document.getElementById('upload')
function isValid(){
    submitBtn.disabled = !(videoFileInput.value && videoNameInput.value)
}

videoNameInput.addEventListener('change', isValid)
videoFileInput.addEventListener('change', isValid)