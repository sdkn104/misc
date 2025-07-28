import React, { useState } from "react";
import "./App.css";

function App() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [caption, setCaption] = useState("");
  const [loading, setLoading] = useState(false);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      setPreview(URL.createObjectURL(file));
      setCaption("");
    }
  };

  const handleUpload = async () => {
    if (!image) return;
    setLoading(true);
    setCaption("");
    const formData = new FormData();
    formData.append("image", image);

    try {
      const res = await fetch("http://localhost:5000/api/upload", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setCaption(data.caption || "No caption generated.");
    } catch (err) {
      setCaption("Error generating caption.");
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>画像キャプション生成アプリ</h1>
      <input type="file" accept="image/*" onChange={handleImageChange} />
      {preview && (
        <div className="preview">
          <img src={preview} alt="preview" />
        </div>
      )}
      <button onClick={handleUpload} disabled={!image || loading}>
        {loading ? "生成中..." : "キャプション生成"}
      </button>
      {caption && (
        <div className="caption">
          <strong>キャプション:</strong> {caption}
        </div>
      )}
    </div>
  );
}

export default App;
