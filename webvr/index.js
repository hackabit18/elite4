const express = require("express");
const app = express();
const path = require('path');

app.use('/', express.static(path.join(__dirname, 'public')))

app.get("/", (req, res)=>{
    //console.log(__dirname);
    res.sendFile(path.join(__dirname, '/index.html'));
});



app.listen(5000, () => {
    console.log("server running at 5000");
});