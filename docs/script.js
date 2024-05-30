const xhr = new XMLHttpRequest();
const url = "https://api.github.com/repos/codemorphist/DigitalGarden/contents/gallery";

xhr.open('GET', url, true);

xhr.onload = function() {
    const data = JSON.parse(this.response);

    // Фильтруем только файлы изображений
    const imageFiles = data.filter(file => /\.(jpg|jpeg|png|gif)$/.test(file.name));

    // Создаем массив URL изображений
    const imageUrls = imageFiles.map(file => file.download_url);

    // Создаем массив названий изображений
    const imageNames = imageFiles.map(file => file.name.split(".")[0]);

    // Вызываем функцию для отображения изображений на странице
    displayImages(imageUrls, imageNames);
};

xhr.send();

function displayImages(imageUrls, imageNames) {
    let currentIndex = 0;

    const imgElement = document.getElementById('current-image');
    const titleElement = document.getElementById('image-title');

    // Обновляем изображение и название на странице
    function updateImage() {
        imgElement.src = imageUrls[currentIndex];
        titleElement.textContent = imageNames[currentIndex];
    }

    // Переключаемся на предыдущее изображение
    document.getElementById('prev-button').addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + imageUrls.length) % imageUrls.length;
        updateImage();
    });

    // Переключаемся на следующее изображение
    document.getElementById('next-button').addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % imageUrls.length;
        updateImage();
    });

    // Показываем первое изображение
    updateImage();
}

