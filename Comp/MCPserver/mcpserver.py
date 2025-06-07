#from fastmcp.types import ToolArgument, ToolReturn
from fastmcp import FastMCP
#from typing import Annotated
from pydantic import Field
import oracledb

"""
FastMCP2.0を使ってOracleのテーブルをUPDATEするMCPサーバのコードを書いてください。
ツールの名前はupdate_kaiseki_yoteibi、引数は、touroku_no、yoteibiとします。
機能は、テーブルKAISEKI_MSTのtouroku_no列をtouroku_noで検索し、
yoteibi列に指定値を登録するものとします。
また、固定値を返す、テスト用のツールを追加してください。
"""

# Oracle接続情報（適宜修正してください）
ORACLE_DSN = "user/password@localhost:1521/ORCLPDB1"

mcp = FastMCP(
    name="oracle_db",
    instructions="""このサーバは、Oracleのdatabaseに接続し、テーブルを更新したり、テーブルの値を取得したりするためのツールを提供します。"""
    #port=8000,  # ポート番号は適宜変更してください
)

@mcp.tool(
    name="update_kaiseki_yoteibi",
    description="解析テーブルのtouroku_noでyoteibiを更新する",
    #returns=ToolReturn("result", str, "更新結果")
)
def update_kaiseki_yoteibi(
    touroku_no: str = Field(description="登録番号"), 
    yoteibi: str = Field(description="予定日 (YYYYMMDD)"), 
):
    try:
        with oracledb.connect(ORACLE_DSN) as conn:
            with conn.cursor() as cur:
                sql = "UPDATE KAISEKI_MST SET yoteibi = :1 WHERE touroku_no = :2"
                cur.execute(sql, [yoteibi, touroku_no])
                conn.commit()
                if cur.rowcount == 0:
                    return {"result": "該当データなし"}
                return {"result": f"{cur.rowcount}件更新"}
    except Exception as e:
        return {"result": f"エラー: {e}"}

# テスト用ツール
@mcp.tool(
    name="get_users",
    description="Oracle databaseのユーザのリストを取得する",
)
def get_users():
    return {"result": ["user1", "user2", "user3"]}


if __name__ == "__main__":
    print(mcp)  # サーバ情報を表示
    # Settings are accessible via mcp.settings
    print("mcp settings:", mcp.settings)
    #mcp.run()
    mcp.run(transport="streamable-http", host="127.0.0.1", port=9000)
