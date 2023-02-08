/*import _ from 'lodash';

function component() {
  const element = document.createElement('div');

  // Lodash, currently included via a script, is required for this line to work
  element.innerHTML = _.join(['Hello', 'webpack'], ' ');

  return element;
}

document.body.appendChild(component());*/
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
            console.log(response)
            const title = response.toLowerCase()

            getBestTitle(title)
                .then(result => {
                    const endpoint = "https://en.wikipedia.org/w/api.php";

                    const parameters = {
                        action: "query",
                        titles: result, //Person Name that comes from getBestTitle function
                        prop: "images",
                        iiprop: "url",
                        format: "json",
                        origin: "*"
                    };

                    fetch(endpoint + "?" + new URLSearchParams(parameters))
                        .then(response => response.json())
                        .then(data => {
                            // console.log(data)
                            const pageId = Object.keys(data.query.pages)[0];
                            const images = data.query.pages[pageId].images;

                            console.table(images)
                            console.log(result)


                            // Filter the images contains person name and Exclude irrelevant one
                            const filteredImages = images.filter(image => {
                                const title = image.title.toLowerCase();
                                result = result.toLowerCase();

                                return title.includes("file:" + result) || title.includes("file:" + result.replace(/ /gi,''));
                            });
                            console.table(filteredImages)

                            // Get the image URLs
                            const imageUrls = filteredImages.map(image => {
                                const imageTitle = image.title.replace("File:", "");
                                console.log("imageTitle : " + imageTitle)
                                return `https://en.wikipedia.org/wiki/Special:Redirect/file/${encodeURIComponent(imageTitle)}`;
                            });

                            console.table(imageUrls)

                            let cel_image_url =  imageUrls[0]
                            let cel_title = result;

                            document.querySelector('#cel_image').src = cel_image_url;
                            document.querySelector('#cel_title').innerHTML = cel_title

                        })
                        .catch(error => {
                            console.log("API request failed", error);
                        });
                })

        })
}

//This function get
const getBestTitle = async (title) => {
    const endpoint = "https://en.wikipedia.org/w/api.php";
    const parameters = {
        action: "query",
        list: "search",
        srsearch: title,
        format: "json",
        origin: "*"
    };
    let best_title = null;

    await fetch(endpoint + "?" + new URLSearchParams(parameters))
        .then(response => response.json())
        .then(data => {
            best_title = data.query.search[0].title
        })
        .catch(reason => {
            console.log(reason)
        })

    return best_title;
}
