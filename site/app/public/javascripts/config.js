window.onload = function() {
    fetch("/getConfig")
    .then(res => {
        res.json().then(config => {
            document.getElementById("edbhost").value = config.EDBSettings["edbhost"]
            document.getElementById("edbport").value = config.EDBSettings["edbport"]
            document.getElementById("edbname").value = config.EDBSettings["edbname"]
            document.getElementById("edbuser").value = config.EDBSettings["edbuser"]
            document.getElementById("edbpass").value = config.EDBSettings["edbpass"]
        })
    })
}