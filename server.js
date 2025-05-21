const express = require('express');
const path = require('path');
const fs = require('fs');
const app = express();
const port = process.env.PORT || 3000;

// Serve static files
app.use(express.static('real_screenshots'));
app.use(express.static('real_results'));

// Route for home page
app.get('/', (req, res) => {
  try {
    // Try to read the README.md file
    const readmePath = path.join(__dirname, 'README.md');
    const readme = fs.readFileSync(readmePath, 'utf8');
    res.send(`
      <!DOCTYPE html>
      <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Thailand Land Deed Screenshot Capture</title>
        <style>
          body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
          }
          pre {
            background-color: #f5f5f5;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
          }
          code {
            font-family: monospace;
          }
          h1, h2, h3 {
            color: #333;
          }
        </style>
      </head>
      <body>
        <h1>Thailand Land Deed Screenshot Capture</h1>
        <div>
          <pre>${readme}</pre>
        </div>
      </body>
      </html>
    `);
  } catch (err) {
    res.send('Welcome to the Thailand Land Deed Screenshot Capture Tool');
  }
});

// API endpoint to list all screenshots
app.get('/api/screenshots', (req, res) => {
  try {
    const screenshotsDir = path.join(__dirname, 'real_screenshots');
    const files = fs.readdirSync(screenshotsDir)
      .filter(file => file.endsWith('.png'))
      .map(file => ({
        filename: file,
        url: `/real_screenshots/${file}`,
        deed_number: file.split('_')[1]
      }));
    
    res.json({ screenshots: files });
  } catch (err) {
    res.status(500).json({ error: 'Failed to list screenshots', details: err.message });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
  console.log(`View screenshots at http://localhost:${port}/api/screenshots`);
}); 