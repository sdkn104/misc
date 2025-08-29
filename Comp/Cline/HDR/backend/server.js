const express = require('express');
const cors = require('cors');
const multer = require('multer');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 4000;

// Middleware
app.use(cors());
app.use(express.json());

// SQLite DB setup
const dbFile = path.join(__dirname, 'db.sqlite');
const db = new sqlite3.Database(dbFile);

// Create tables if not exist
db.serialize(() => {
  db.run(`
    CREATE TABLE IF NOT EXISTS hdr_files (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      filename TEXT NOT NULL,
      originalname TEXT NOT NULL,
      uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);
  db.run(`
    CREATE TABLE IF NOT EXISTS glb_files (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      filename TEXT NOT NULL,
      originalname TEXT NOT NULL,
      uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);
});

// File upload setup
const hdrStorage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, path.join(__dirname, 'uploads/hdr'));
  },
  filename: (req, file, cb) => {
    const uniqueName = Date.now() + '-' + file.originalname;
    cb(null, uniqueName);
  }
});
const glbStorage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, path.join(__dirname, 'uploads/glb'));
  },
  filename: (req, file, cb) => {
    const uniqueName = Date.now() + '-' + file.originalname;
    cb(null, uniqueName);
  }
});
const uploadHdr = multer({ storage: hdrStorage });
const uploadGlb = multer({ storage: glbStorage });

// API endpoints

// List HDR files
app.get('/assets/hdr', (req, res) => {
  db.all('SELECT * FROM hdr_files', [], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

// List GLB files
app.get('/assets/glb', (req, res) => {
  db.all('SELECT * FROM glb_files', [], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

// Upload HDR file
app.post('/assets/hdr', uploadHdr.single('file'), (req, res) => {
  if (!req.file) return res.status(400).json({ error: 'No file uploaded' });
  db.run(
    'INSERT INTO hdr_files (filename, originalname) VALUES (?, ?)',
    [req.file.filename, req.file.originalname],
    function (err) {
      if (err) return res.status(500).json({ error: err.message });
      res.json({ id: this.lastID, filename: req.file.filename, originalname: req.file.originalname });
    }
  );
});

// Upload GLB file
app.post('/assets/glb', uploadGlb.single('file'), (req, res) => {
  if (!req.file) return res.status(400).json({ error: 'No file uploaded' });
  db.run(
    'INSERT INTO glb_files (filename, originalname) VALUES (?, ?)',
    [req.file.filename, req.file.originalname],
    function (err) {
      if (err) return res.status(500).json({ error: err.message });
      res.json({ id: this.lastID, filename: req.file.filename, originalname: req.file.originalname });
    }
  );
});

// Delete HDR file
app.delete('/assets/hdr/:id', (req, res) => {
  db.get('SELECT filename FROM hdr_files WHERE id = ?', [req.params.id], (err, row) => {
    if (err || !row) return res.status(404).json({ error: 'File not found' });
    const filePath = path.join(__dirname, 'uploads/hdr', row.filename);
    fs.unlink(filePath, (fsErr) => {
      db.run('DELETE FROM hdr_files WHERE id = ?', [req.params.id], (dbErr) => {
        if (fsErr || dbErr) return res.status(500).json({ error: 'Delete failed' });
        res.json({ success: true });
      });
    });
  });
});

// Delete GLB file
app.delete('/assets/glb/:id', (req, res) => {
  db.get('SELECT filename FROM glb_files WHERE id = ?', [req.params.id], (err, row) => {
    if (err || !row) return res.status(404).json({ error: 'File not found' });
    const filePath = path.join(__dirname, 'uploads/glb', row.filename);
    fs.unlink(filePath, (fsErr) => {
      db.run('DELETE FROM glb_files WHERE id = ?', [req.params.id], (dbErr) => {
        if (fsErr || dbErr) return res.status(500).json({ error: 'Delete failed' });
        res.json({ success: true });
      });
    });
  });
});

// Serve uploaded files statically
app.use('/uploads/hdr', express.static(path.join(__dirname, 'uploads/hdr')));
app.use('/uploads/glb', express.static(path.join(__dirname, 'uploads/glb')));

app.listen(PORT, () => {
  console.log(`Backend server running on http://localhost:${PORT}`);
});
