const xhr = new XMLHttpRequest();
const url = "https://api.github.com/repos/codemorphist/DigitalGarden/contents/gallery";

xhr.open("GET", url, true);

xhr.onload = function() {
    const data = JSON.parse(this.response);

    const imageFiles = data.filter(file => /\.(jpg|jpeg|png|gif)$/.test(file.name));
    const imageUrls = imageFiles.map(file => file.download_url);
    const imageNames = imageFiles.map(file => file.name);

    preloadImages(imageUrls); 
    displayImages(imageUrls, imageNames);
};

xhr.send();

function preloadImages(urls) {
    urls.forEach(url => {
        const img = new Image();
        img.src = url;
    });
}

function displayImages(imageUrls, imageNames) {
    let currentIndex = 0;

    const imgElement = document.getElementById("current-image");
    const titleElement = document.getElementById("image-title");
    const loaderElement = document.getElementById("loader");

    function updateImage() {
        loaderElement.style.display = "block"; 
        imgElement.classList.remove('show');

        const img = new Image();
        img.src = imageUrls[currentIndex];
        img.onload = function() {
            imgElement.src = img.src;
            titleElement.textContent = imageNames[currentIndex];
            loaderElement.style.display = "none"; 
            imgElement.classList.add('show');
        };
    }

    document.getElementById("prev-button").addEventListener("click", () => {
        currentIndex = (currentIndex - 1 + imageUrls.length) % imageUrls.length;
        updateImage();
    });

    document.getElementById("next-button").addEventListener("click", () => {
        currentIndex = (currentIndex + 1) % imageUrls.length;
        updateImage();
    });

    updateImage(); 

    function preloadNextImage() {
        const nextIndex = (currentIndex + 1) % imageUrls.length;
        const img = new Image();
        img.src = imageUrls[nextIndex];
    }
}

