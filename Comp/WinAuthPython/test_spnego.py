from flask import Flask, request, Response, jsonify
import spnego  # pip install pyspnego
import base64

app = Flask(__name__)

def _unauthorized(out_token: str | None = None) -> Response:
    # Negotiate チャレンジ（必要なら次トークンを付ける）
    hdr = "Negotiate"
    if out_token:
        hdr += f" {out_token}"
    return Response("Unauthorized", 401, {"WWW-Authenticate": hdr})

@app.route("/whoami")
def whoami():
    # Authorization ヘッダーを確認
    authz = request.headers.get("Authorization", "")
    if not authz.startswith("Negotiate"):
        # 1回目: 認証開始を促す
        return _unauthorized()

    in_token = authz.split(" ", 1)[1] if " " in authz else ""
    print("in_token", in_token)

    # Windows では SSPI、Linux では GSSAPI を自動選択
    server_ctx = spnego.server(
        options=spnego.NegotiateOptions.use_negotiate  # Kerberos/NTLM 自動ネゴ
    )
    in_token_bytes = base64.b64decode(in_token)
    out_token = server_ctx.step(in_token_bytes)

    if not server_ctx.complete:
        # まだハンドシェイクが続く（NTLM など）→ 次トークンを返す
        return _unauthorized(out_token)

    # 完了。peer_name は 'DOMAIN\\username' 等
    user = server_ctx.peer_name
    return jsonify(user=user)

if __name__ == "__main__":
    # 開発起動（本番は waitress-serve 推奨）
    app.run(host="0.0.0.0", port=8000)
