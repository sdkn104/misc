const https = require('https');
const fs = require('fs');
const path = require('path');

const PORT = 3000;
const SRC_DIR = path.join(__dirname, 'src');

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json',
  '.png': 'image/png',
  '.ico': 'image/x-icon',
};

async function startServer() {
  let certs;
  try {
    const devCerts = require('office-addin-dev-certs');
    certs = await devCerts.getHttpsServerOptions();
  } catch (e) {
    console.error('\n❌ 証明書の取得に失敗しました。先に以下を実行してください:');
    console.error('   npm run gen-certs\n');
    process.exit(1);
  }

  const server = https.createServer(certs, (req, res) => {
    const urlPath = decodeURIComponent(req.url.split('?')[0]);
    const filePath = path.normalize(path.join(SRC_DIR, urlPath === '/' ? 'taskpane.html' : urlPath));

    if (!filePath.startsWith(SRC_DIR)) {
      res.writeHead(403);
      res.end('Forbidden');
      return;
    }

    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404);
        res.end(`Not found: ${urlPath}`);
        return;
      }

      const ext = path.extname(filePath);
      res.writeHead(200, {
        'Content-Type': MIME_TYPES[ext] || 'application/octet-stream',
        'Access-Control-Allow-Origin': '*',
        'Cache-Control': 'no-cache, no-store',
      });
      res.end(data);
    });
  });

  server.listen(PORT, () => {
    console.log(`\n✅ サーバー起動中: https://localhost:${PORT}`);
    console.log('\n次のステップ:');
    console.log('  1. Outlookを開く');
    console.log('  2. manifest.xml をサイドロードする');
    console.log('  3. メールを開いてリボンの「返信を生成」ボタンをクリック\n');
  });
}

startServer().catch(console.error);
