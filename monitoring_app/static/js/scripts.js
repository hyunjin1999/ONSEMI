document.addEventListener('DOMContentLoaded', function() {
    var seniorImage = document.getElementById('seniorImage');
    var infoBox = document.getElementById('infoBox');

    seniorImage.addEventListener('click', function() {
        if (infoBox.style.display === 'none' || infoBox.style.display === '') {
            infoBox.style.display = 'block';
        } else {
            infoBox.style.display = 'none';
        }
    });
});