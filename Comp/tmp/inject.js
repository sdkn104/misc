// ==UserScript==
// @name         Page API Injector (Class Version)
// @namespace    http://tampermonkey.net/
// @version      0.2
// @description  Injects API response and manages UI state with classes
// @author       Copilot
// @match        *://*/*
// @grant        none
// ==/UserScript==

(function() {
	'use strict';

	// 設定
	const API_URL = 'https://example.com/api'; // ←APIエンドポイントに変更
	const TEXTAREA_SELECTOR = 'textarea#target'; // ←挿入先textareaセレクタに変更
	const WAIT_MSG = '応答待ち...';
	const BUTTON_ID = 'inject-api-btn';

	// API管理クラス
	class ApiManager {
		constructor(apiUrl) {
			this.apiUrl = apiUrl;
			this.state = 'idle'; // idle, waiting, done
			this.response = null;
			this.onResponse = null;
		}
		callApi() {
			this.state = 'waiting';
			fetch(this.apiUrl)
				.then(res => res.json())
				.then(data => {
					this.response = data;
					this.state = 'done';
					if (typeof this.onResponse === 'function') this.onResponse(data);
				})
				.catch(() => {
					this.state = 'idle';
				});
		}
		getState() {
			return this.state;
		}
		getResponse() {
			return this.response;
		}
	}

	// UI管理クラス
	class UIManager {
		constructor(textareaSelector, waitMsg, buttonId) {
			this.textareaSelector = textareaSelector;
			this.waitMsg = waitMsg;
			this.buttonId = buttonId;
			this.buttonPressed = false;
		}
		getTextarea() {
			return document.querySelector(this.textareaSelector);
		}
		insertResponse(response) {
			const ta = this.getTextarea();
			if (ta && response) {
				ta.value = response.result || JSON.stringify(response);
			}
			this.updateWaitDisplay(false);
		}
		updateWaitDisplay(show) {
			let ta = this.getTextarea();
			if (!ta) return;
			let waitDiv = document.getElementById('wait-msg-div');
			if (show) {
				if (!waitDiv) {
					waitDiv = document.createElement('div');
					waitDiv.id = 'wait-msg-div';
					waitDiv.textContent = this.waitMsg;
					ta.parentNode.insertBefore(waitDiv, ta.nextSibling);
				}
			} else {
				if (waitDiv) waitDiv.remove();
			}
		}
		setButtonPressed(val) {
			this.buttonPressed = val;
		}
		isButtonPressed() {
			return this.buttonPressed;
		}
		createInjectButton(targetDiv, apiManager) {
			if (document.getElementById(this.buttonId)) return;
			const btn = document.createElement('button');
			btn.id = this.buttonId;
			btn.textContent = 'API応答挿入';
			btn.onclick = () => {
				if (apiManager.getState() === 'done') {
					this.insertResponse(apiManager.getResponse());
				} else if (apiManager.getState() === 'waiting') {
					this.updateWaitDisplay(true);
					this.setButtonPressed(true);
				} else {
					this.setButtonPressed(true);
					this.updateWaitDisplay(true);
					apiManager.callApi();
				}
			};
			targetDiv.appendChild(btn);
		}
	}

	// インスタンス生成
	const apiManager = new ApiManager(API_URL);
	const uiManager = new UIManager(TEXTAREA_SELECTOR, WAIT_MSG, BUTTON_ID);

	// API応答時の処理
	apiManager.onResponse = (data) => {
		if (uiManager.isButtonPressed()) {
			uiManager.insertResponse(data);
			uiManager.setButtonPressed(false);
		}
	};

	// div追加監視
	const observer = new MutationObserver(mutations => {
		for (const m of mutations) {
			for (const node of m.addedNodes) {
				if (node.nodeType === 1 && node.matches && node.matches('div.target-div')) { // ←divの条件に変更
					uiManager.createInjectButton(node, apiManager);
				}
			}
		}
	});
	observer.observe(document.body, { childList: true, subtree: true });

	// ページロード時
	window.addEventListener('DOMContentLoaded', () => {
		apiManager.callApi();
	});

	// グローバル参照用
	window.__apiManager = apiManager;
	window.__uiManager = uiManager;

})();
