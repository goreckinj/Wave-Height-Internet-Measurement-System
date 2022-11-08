var express = require('express');
var router = express.Router();
const si = require("systeminformation")
var fs = require('fs')
var ini = require('ini');
const path = require('path')

// /* GET home page. */

router.get('/getStatus', async (req, res) => {
  resp = {}
  resp["uptime"] = si.time().uptime;
  await si.currentLoad()
    .then(data => {
        resp["load"] = data.currentLoad; 
        })
  await si.cpuTemperature().then(cpuTemp => {
          resp["temp"] = cpuTemp.main
        })
  await si.mem().then(temp => {
    resp["mem"] = temp.free
          })
  res.json(resp)
})

router.get('/getConfig', (req, res) => {
  res.json(ini.parse(fs.readFileSync('../../whims.ini', 'utf-8')))
})

router.post('/updateConfig', (req, res) => {
  file = ini.parse(fs.readFileSync('../../whims.ini', 'utf-8'))
  file.EDBSettings["edbpass"] = req.body.edbpass
  file.EDBSettings["edbhost"] = req.body.edbhost
  file.EDBSettings["edbport"] = req.body.edbport
  file.EDBSettings["edbname"] = req.body.edbname
  file.EDBSettings["edbuser"] = req.body.edbuser

  fs.writeFileSync('../../whims.ini', ini.stringify(file))
  res.sendStatus(200)

})

module.exports = router;
