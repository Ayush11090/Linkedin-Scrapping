const express = require('express');
const multer = require('multer');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');

const app = express();
const port = 3000;

const uploadFolder = 'uploads';

if (!fs.existsSync(uploadFolder)) {
    fs.mkdirSync(uploadFolder);
}

const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, uploadFolder);
    },
    filename: function (req, file, cb) {
        cb(null, file.originalname);
    }
});

const upload = multer({ storage: storage });

app.use(express.static('public'));

app.post('/upload', upload.single('csvFile'), (req, res) => {
    const uploadedFilePath = path.join(uploadFolder, req.file.originalname);

    fs.renameSync(req.file.path, uploadedFilePath);

    res.json({ message: 'File uploaded successfully.' });
});

app.post('/runLinkedInScraper', (req, res) => {
    // Execute the LinkedIn scraper script here
    const pythonScriptPath = path.join(__dirname,'script.py');
    const command = `python "${pythonScriptPath}"`;  // Wrap the path in double quotes

    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error('Error executing LinkedIn Scraper script:', error);
            res.status(500).json({ error: 'Error executing LinkedIn Scraper script.' });
        } else {
            console.log('LinkedIn Scraper script executed successfully:', stdout);
            res.json({ result: 'LinkedIn Scraper script executed successfully.' });
        }
    });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
