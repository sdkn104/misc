# Spring Boot REST API Example

このプロジェクトは、`GET /api/sample` エンドポイントで `{ "result": "OK" }` を返すサンプルAPIです。

## プロジェクト構成
- `SampleController.java` : RESTコントローラー
- `SampleDto.java` : レスポンスDTO

## 実行方法
1. Java 17+ と Maven が必要です。
2. 以下のコマンドで起動します。
   ```powershell
   mvn spring-boot:run
   ```
3. エンドポイントにアクセス:
   - http://localhost:8080/api/sample

# https://blog.tech-monex.com/entry/2025/05/09/111249