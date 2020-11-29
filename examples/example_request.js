function send_data(){
    var formdata = new FormData();
    formdata.append("service_type", "speed");
    formdata.append("from_measurement", "mph");
    formdata.append("to_measurement", "kph");
    formdata.append("measurement_value", "4.2");

    var requestOptions = {
    method: 'POST',
    headers: {"x-api-key": "bdkdbd-dbdkdkbd-kssz"},
    body: formdata,
    redirect: 'follow'
    };

    fetch("http://127.0.0.1:3533/convert", requestOptions)
    .then(response => response.text())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));
}