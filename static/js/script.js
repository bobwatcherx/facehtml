let video;
let canvas;
let nameInput;

function init() {
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    nameInput = document.getElementById('name');

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
        })
        .catch(error => {
            console.error('Error accessing webcam:', error);
            alert('Tidak dapat mengakses webcam. Pastikan Anda memberikan izin untuk mengakses kamera.');
        });
}

function capture() {
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas.style.display = 'block';
    video.style.display = 'none';
}

function register() {
    const name = nameInput.value;
    const photo = dataURItoBlob(canvas.toDataURL());

    if (!name || !photo) {
        alert('Nama dan foto wajah harus diisi!');
        return;
    }

    const formData = new FormData();
    formData.append('name', name);
    formData.append('photo', photo, `${name}.jpg`);

    fetch('/register', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Data berhasil didaftarkan.');
            window.location.href = '/';
        } else {
            alert('Gagal menyimpan data. Silakan coba lagi.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function login() {
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const photo = dataURItoBlob(canvas.toDataURL());

    if (!photo) {
        alert('Ambil foto terlebih dahulu sebelum login.');
        return;
    }

    const formData = new FormData();
    formData.append('photo', photo, 'login.jpg');

    fetch('/login', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data); // Add this line to see the actual response received from the server
        if (data.success) {
            alert('Login berhasil.');
            window.location.href = '/success?user_name=' + nameInput.value;
        } else {
            alert('Login gagal. Silakan coba lagi.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


function dataURItoBlob(dataURI) {
    const byteString = atob(dataURI.split(',')[1]);
    const mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
    const ab = new ArrayBuffer(byteString.length);
    const ia = new Uint8Array(ab);
    for (let i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }
    return new Blob([ab], { type: mimeString });
}

init();