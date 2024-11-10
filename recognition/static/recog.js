// WebSocket для реального времени
const socket = new WebSocket('ws://' + window.location.host + '/ws/somepath/');

socket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    console.log(data.message);
    document.querySelector('#app').innerText = data.message
};

// // Обработка формы загрузки файла
// document.getElementById('upload-form').onsubmit = function (event) {
//     event.preventDefault();

//     const formData = new FormData(this);
//     fetch("{% url 'transcribe_audio' %}", {
//         method: "POST",
//         body: formData,
//         headers: {
//             "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
//         }
//     }).then(response => {
//         if (response.ok) {
//             console.log("Transcription started...");
//         } else {
//             console.error("Error uploading file.");
//         }
//     });
// };