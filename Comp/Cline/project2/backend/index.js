const express = require('express');
const multer = require('multer');
const axios = require('axios');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 5000;

// Set up multer for file uploads
const upload = multer({ dest: 'uploads/' });

// Allow CORS for local frontend development
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  next();
});

// Endpoint for image upload and captioning
app.post('/api/upload', upload.single('image'), async (req, res) => {
  try {
    const filePath = req.file.path;

    // Read the image file as base64
    const imageData = fs.readFileSync(filePath, { encoding: 'base64' });

    // Call Hugging Face Inference API (BLIP image captioning)
    const response = await axios.post(
      'https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base',
      { inputs: `data:image/jpeg;base64,${imageData}` },
      {
        headers: {
          Authorization: 'Bearer hf_xxx_your_huggingface_token', // Replace with your Hugging Face token
          'Content-Type': 'application/json',
        },
        timeout: 30000,
      }
    );

    // Remove the uploaded file after processing
    fs.unlinkSync(filePath);

    // Extract caption from response
    const caption = response.data[0]?.generated_text || 'No caption generated.';

    res.json({ caption });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Failed to generate caption.' });
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
