# Vega-Lite形式のdictを受け取りグラフを表示する関数
import json
import tempfile
import webbrowser


def show_vega_lite_chart(vega_lite_dict, code_expl=None, message=""):
		"""
		Vega-Lite形式(dict)を受け取り、ブラウザでグラフを表示する。
		編集用のテキストエリアを画面に追加し、編集・再描画できるようにする。
		"""
		html_template = f"""
		<!DOCTYPE html>
		<html>
		<head>
			<script src="https://cdn.jsdelivr.net/npm/vega@5"></script>
			<script src="https://cdn.jsdelivr.net/npm/vega-lite@5"></script>
			<script src="https://cdn.jsdelivr.net/npm/vega-embed@6"></script>
			<style>
				textarea {{ width: 100%; height: 200px; }}
				#vis {{ margin-top: 20px; }}
			</style>
		</head>
		<body>
			<div>{message}</div>
			<div class="container" style="display: flex;">
				<textarea id="spec-editor" style="width: 500px; height:30px; display: inline-block;">{json.dumps(vega_lite_dict, indent=2, ensure_ascii=False)}</textarea><br>
				<textarea id="code_expl" style="width: 300px; height:30px; display: inline-block;">{code_expl}</textarea><br>
			</div>
			<button onclick="updateChart()">グラフを再描画</button>
			<div id="vis"></div>
			<script type="text/javascript">
				function updateChart() {{
					let specText = document.getElementById('spec-editor').value;
					try {{
						const spec = JSON.parse(specText);
						vegaEmbed('#vis', spec);
					}} catch (e) {{
						document.getElementById('vis').innerHTML = '<span style="color:red">JSONエラー: ' + e + '</span>';
					}}
				}}
				// 初回描画
				updateChart();
			</script>
		</body>
		</html>
		"""
		with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html', encoding='utf-8') as f:
				f.write(html_template)
				temp_html_path = f.name
		webbrowser.open(f'file://{temp_html_path}')
