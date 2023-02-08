
import Dropzone from "dropzone"

import "dropzone/dist/dropzone.css";
import "../css/styles.css";

let myDropzone = new Dropzone("#upload_form", {
    uploadMultiple: false,
    maxFilesize: 10,
    maxFiles: 1,
    acceptedFiles: "image/jpeg,image/jpg,image/png",
    success: (file) => {
        getPredict(file.name)
        // console.log(file.name)
    }
});

function getPredict(image) {
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'image': image
        })
    })
        .then(r => r.text())
        .then(response => {
            // console.log(response)
        })
}
