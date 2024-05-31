const url = "https://api.github.com/repos/codemorphist/DigitalGarden/contents/gallery";

fetch(url)
    .then(response => response.json())
    .then(data => {
        const imageFiles = data.filter(file => /\.(jpg|jpeg|png|gif)$/.test(file.name));
        const imageUrls = imageFiles.map(file => file.download_url);
        const imageNames = imageFiles.map(file => file.name.split('.')[0].replace('_', ' '));
        
        preloadImages(imageUrls);
        displayImages(imageUrls, imageNames);
    })
    .catch(error => console.error('Error fetching images:', error));

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

            document.body.style.backgroundImage = `url('${img.src}')`;
            document.body.style.backgroundSize = 'cover';
            document.body.style.backgroundPosition = 'center';
            document.body.style.backgroundRepeat = 'no-repeat';
            document.body.style.backdropFilter = 'blur(20px)';
        };
    }

    document.getElementById("prev-button").addEventListener("click", () => {
        currentIndex = (currentIndex - 1 + imageUrls.length) % imageUrls.length;
        updateImage();
        preloadNextImage(); // Preload next image
    });

    document.getElementById("next-button").addEventListener("click", () => {
        currentIndex = (currentIndex + 1) % imageUrls.length;
        updateImage();
        preloadNextImage(); // Preload next image
    });

    updateImage(); 

    function preloadNextImage() {
        const nextIndex = (currentIndex + 1) % imageUrls.length;
        const img = new Image();
        img.src = imageUrls[nextIndex];
    }
}

