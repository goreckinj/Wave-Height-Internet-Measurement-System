window.onload = function() {
    fetch("/getStatus")
    .then(res => {
        res.json().then(data => {
            document.getElementById("cpu_load").innerHTML = data.load
            var date = new Date();
            date.setSeconds(data.uptime); // specify value for SECONDS here
            var result = date.toISOString().substr(11, 8);
            document.getElementById("cpu_temp").innerHTML = data.temp
            document.getElementById("cpu_uptime").innerHTML = result
            document.getElementById("cpu_memory").innerHTML = data.mem
        })
    })
}
