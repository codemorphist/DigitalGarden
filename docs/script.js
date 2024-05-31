const url = "https://api.github.com/repos/codemorphist/digitalgarden/contents/gallery?ref=github-pages";

async function fetchImages() {
    try {
        const response = await fetch(url);
        const data = await response.json();
        
        const imageFiles = data.filter(file => /\.(jpg|jpeg|png|gif)$/.test(file.name));
        const images = imageFiles.map(file => ({
            url: file.download_url,
            name: file.name.split('.')[0].replace('_', ' ')
        }));
        
        shuffleArray(images);
        
        const imageUrls = images.map(image => image.url);
        const imageNames = images.map(image => image.name);
        
        const initialLoadCount = 5; // Number of images to load initially

        await preloadImages(imageUrls.slice(0, initialLoadCount));
        displayImages(imageUrls, imageNames, initialLoadCount);
        
        // Preload the remaining images in the background
        preloadImages(imageUrls.slice(initialLoadCount));
    } catch (error) {
        console.error('Error fetching images:', error);
    }
}

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

async function preloadImages(urls) {
    const promises = urls.map(url => {
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.src = url;
            img.onload = resolve;
            img.onerror = reject;
        });
    });
    await Promise.all(promises);
}

function displayImages(imageUrls, imageNames, initialLoadCount) {
    let currentIndex = 0;

    const imgElement = document.getElementById("current-image");
    const titleElement = document.getElementById("image-title");
    const loaderElement = document.getElementById("loader");

    async function updateImage() {
        loaderElement.style.display = "block";
        document.body.style.backgroundImage = "none !important;";
        titleElement.textContent = "..."
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
            document.body.style.backdropFilter = 'blur(32px)';
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
        if (nextIndex >= initialLoadCount) {
            const img = new Image();
            img.src = imageUrls[nextIndex];
        }
    }
}

fetchImages();

