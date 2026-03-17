import asyncio
import sys
import winrt.windows.media.ocr as ocr
import winrt.windows.globalization as gl
import winrt.windows.graphics.imaging as imaging
import winrt.windows.storage.streams as streams

async def run_ocr(image_path):
    # 画像を読み込み
    with open(image_path, "rb") as f:
        data = f.read()

    # WinRT のストリームに変換
    ras = streams.InMemoryRandomAccessStream()
    writer = streams.DataWriter(ras)
    writer.write_bytes(data)
    await writer.store_async()
    ras.seek(0)

    # BitmapDecoder
    decoder = await imaging.BitmapDecoder.create_async(ras)
    bitmap = await decoder.get_software_bitmap_async()

    # OCRエンジン（日本語）
    engine = ocr.OcrEngine.try_create_from_language(gl.Language("ja-JP"))

    # OCR実行
    result = await engine.recognize_async(bitmap)

    print("=== OCR Result ===")
    print(result.text)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python WinRTOCR.py <image_file>")
        sys.exit(1)
    image_path = sys.argv[1]
    asyncio.run(run_ocr(image_path))
