const express = require("express");
const app = express();
const path = require('path');
const obj2gltf = require('obj2gltf');
const fs = require('fs');

app.use('/static', express.static(path.join(__dirname, 'public')));
app.use('/loud', express.static(__dirname));

app.get("/", (req, res)=>{
    //console.log(__dirname);
    res.sendFile(path.join(__dirname, '/index.html'));
});

app.get("/left", (req, res) => {
    obj2gltf('left.obj')
        .then(function (gltf) {
            var data = Buffer.from(JSON.stringify(gltf));
            fs.writeFileSync('left.gltf', data);
        })
        .catch((err) => {
            console.log("Error Encountered: " + err);
            res.status(500).json({
                status:  "fail",
                message:  "Some error occured"
            });
        });
});

app.get("/right", (req, res) => {
    obj2gltf('right.obj')
        .then(function (gltf) {
            var data = Buffer.from(JSON.stringify(gltf));
            fs.writeFileSync('right.gltf', data);
        })
        .catch((err) => {
            console.log("Error Encountered: " + err);
            res.status(500).json({
                status: "fail",
                message: "Some error occured"
            });
        });
});

app.listen(5000, () => {
    console.log("server running at 5000");
});