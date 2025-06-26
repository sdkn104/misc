---
marp: true
# ↓↓↓ これらの行はテンプレートが機能するために必要です ↓↓↓
header: ' '
footer: '-'
#footer: "Page {page} / {total}"
paginate: true
size: 16:9
---

<style>
/* Google Fontsから日本語フォントを読み込み */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap');

/* --- 色やフォントの基本設定 --- */
:root {
  --color-background: #f8f8f4;
  --color-foreground: #3a3b5a;
  --color-heading: #000000; /*#4f86c6;*/
  --color-hr: #000000;
  --font-default: 'Noto Sans JP', 'Hiragino Kaku Gothic ProN', 'Meiryo', sans-serif;
}

/* --- スライド全体のスタイル --- */
section {
  background-color: var(--color-background);
  background-image: url("\\mei660\\zzlow\\Hin_L\\buhyo\\名電電子部品委員会\\old\\ppt_template_A_16x9_JP_v1.0\\Slide2.jpg");
  background-image: url("Slide2.jpg");
  background-size: cover;
  
  color: var(--color-foreground);
  font-family: var(--font-default);
  font-weight: 400;
  box-sizing: border-box;
  /*border-bottom: 8px solid var(--color-hr);*/
  position: relative;
  line-height: 1.7;
  font-size: 22px;
  padding: 56px;
}
section:last-of-type {
  border-bottom: none;
}

/* ページ番号 */
section::after {
  font-weight: bold;
  font-size: 28px
}

/* --- 見出しのスタイル --- */
h1, h2, h3, h4, h5, h6 {
  font-weight: 700;
  color: var(--color-heading);
  margin: 0;
  padding: 0;
}

/* タイトルページ(h1)のスタイル */
h1 {
  font-size: 56px;
  line-height: 1.4;
  text-align: left;
}

/* 通常スライドのタイトル(##) */
h2 {
  position: absolute;
  top: 20px;
  left: 180px;
  right: 56px;
  font-size: 40px;
  padding-top: 0;
  padding-bottom: 16px;
}

/* h2の疑似要素(::after)を使って、短い線を実装 */
h2::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: 8px;
  width: 60px;
  height: 2px;
  /*background-color: var(--color-hr);*/
}

/* h2と後続コンテンツの間のスペースを確保 */
h2 + * {
  margin-top: 112px;
}

/* サブ見出し (例: 目的, 目標) */
h3 {
  color: var(--color-foreground);
  font-size: 28px;
  margin-top: 32px;
  margin-bottom: 12px;
}

/* --- リストのスタイル --- */
ul, ol {
  padding-left: 32px;
}
li {
  margin-bottom: 10px;
}

/* フッターとして機能する、太い青いラインを実装 */
footer {
  font-size: 18px;
  color: transparent;  
  position: absolute;
  left: 56px;
  right: 156px;
  bottom: 40px;
  height: 8px;
  /*background-color: var(--color-heading);*/
}

/* フッターにページ番号を表示 */
xxxxfooter::after {
  content: counter(page) " / " counter(pages);
  font-size: 24px;
  color: #080808;
  position: absolute;
  right: 0;
  bottom: 0;
  background: none;
  padding: 0 12px;
}

/* ★★★ ロゴの配置方法を、calc()を使った最も堅牢な方法に変更 ★★★ */
header {
  font-size: 0;
  color: transparent;
  background-image: url('ロゴ.png');
  background-repeat: no-repeat;
  background-size: contain;
  background-position: top right;
  
  position: absolute;
  top: 40px;
  
  /* rightプロパティの代わりに、calc()で左からの位置を計算して配置を安定させます */
  /* 計算式: (コンテナの幅 - ロゴの幅 - 右の余白) */
  left: calc(100% - 180px - 56px);
  
  /*
    【重要】下のwidthの値を変更した場合、
    上のcalc()内の「180px」も同じ値にしてください。
  */
  width: 180px;
  height: 50px;
}

/* --- 先頭ページ --- */
section.lead {
  background-image: url("Slide1.jpg");
  background-size: cover;
  //border-bottom: 8px solid var(--color-hr);
}

/* タイトルページではフッターラインとロゴ(header)を非表示にする */
section.lead footer,
section.lead header {
  display: none;
}


section.lead h1 {
  margin-bottom: 24px;
}
section.lead p {
  font-size: 24px;
  color: var(--color-foreground);
}

/* ガイドライン用のスタイル */
.bad-example {
  background-color: #fbe9e7;
  color: #c62828;
  padding: 8px 16px;
  border-radius: 4px;
}
</style>

<!-- _class: lead -->

# ABC社様
# XXXプロジェクト計画書

---

## 目次

1.  プロジェクト概要
2.  プロジェクト体制
3.  スケジュール・マイルストーン
4.  開発アプローチ
5.  使用ツール・技術スタック
6.  成果物
7.  リスク管理
8.  次のステップ

---

## プロジェクト概要

### 目的
ABC社様のデジタル変革を支援しDXを図る

### 目標
- 業務効率の向上（従来比XX%向上目標）
- 持続可能な開発体制の構築
- 組織全体へのナレッジ共有

---

## プロジェクト体制

### 体制図
| 役割 | 担当者 | 責任範囲 |
| :--- | :--- | :--- |
| プロジェクトマネージャー | [PM名] | 全体管理、進捗、課題管理 |
| テックリード | [リード名] | 技術選定、設計、コードレビュー |
| 開発担当 | [開発者名] | 機能実装、テスト |

### コミュニケーション
- **定例会議:** 毎週月曜日 10:00-10:30
- **連絡ツール:** Slack, Google Meet

---

## スケジュール・マイルストーン

### 全体期間
**[開始日] 〜 [終了日]**

### 主要マイルストーン
- **Week 2:** 要件定義完了
- **Week 5:** プロトタイプ版リリース
- **Week 8:** 全機能実装完了
- **Week 9:** 関係者テスト・検収
- **Week 10:** 正式リリース

---

## 見出し2
### 見出し3
#### 見出し4
##### 見出し5
### （ここに次のスライドを追加）


---
---
---

# Design Guideline
## このテンプレートを美しく保つためのルール

---

## スライドタイトル (`##`) のルール

### **原則: 必ず1行に収めること**
タイトルが2行になると、後続のコンテンツと重なり、レイアウトが完全に崩れてしまいます。これは最も重要なルールです。

### **目安: 全角30文字以内**
簡潔で分かりやすいタイトルを心がけてください。

<br>

#### <span class="bad-example">悪い例 (Bad) </span>
`## このプロジェクトにおける非常に重要な技術的負債とその具体的な返済計画に関する長大な考察`
（長すぎて改行され、レイアウトが崩れます）

---

## 本文・箇条書きのルール

### **原則: 1スライド・1メッセージ**
1枚のスライドに情報を詰め込みすぎず、聞き手が集中できるよう、最も伝えたいメッセージを1つに絞りましょう。

### **推奨するレイアウトと文字量**
- **1行あたりの文字数:** **全角35〜45文字**
  - これを超えると視線の移動が大きくなり、読みにくくなります。適度な位置で改行を入れましょう。
- **箇条書きの項目数:** **5〜7個**まで
- **各項目の行数:** **1〜2行**が理想
- **文章（パラグラフ）の行数:** **5〜7行**程度まで

スライドはドキュメントではありません。詳細は口頭で補うか、別途資料を配布しましょう。

---

## その他の要素のルール

### 見出し3 (`###`)
サブタイトルや小見出しとして使用します。
- **目安:** 全角15文字以内
- **役割:** これから話す内容を簡潔に示します。

### テーブル (`| |`)
情報を整理して見せる際に有効ですが、複雑になりすぎないように注意が必要です。
- **推奨カラム（列）数:** **3〜4列**まで
- **セル内のテキスト:** 可能な限り簡潔に。長いテキストは箇条書きにするなど、表現を工夫しましょう。