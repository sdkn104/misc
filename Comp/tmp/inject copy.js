// ==UserScript==
// @name         Page API Injector
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Injects API response and manages UI state
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

	// 状態管理
	window.__apiResponse = null;
	window.__apiState = 'idle'; // idle, waiting, done
	window.__apiButtonPressed = false;

	// APIを叩く
	function callApi() {
		window.__apiState = 'waiting';
		updateWaitDisplay(true);
		fetch(API_URL)
			.then(res => res.json())
			.then(data => {
				window.__apiResponse = data;
				window.__apiState = 'done';
				updateWaitDisplay(false);
				if (window.__apiButtonPressed) {
					insertResponseToTextarea();
				}
			})
			.catch(() => {
				window.__apiState = 'idle';
				updateWaitDisplay(false);
			});
	}

	// 応答をtextareaに挿入
	function insertResponseToTextarea() {
		const ta = document.querySelector(TEXTAREA_SELECTOR);
		if (ta && window.__apiResponse) {
			ta.value = window.__apiResponse.result || JSON.stringify(window.__apiResponse);
		}
	}

	// 待ち状態表示
	function updateWaitDisplay(show) {
		let ta = document.querySelector(TEXTAREA_SELECTOR);
		if (!ta) return;
		let waitDiv = document.getElementById('wait-msg-div');
		if (show) {
			if (!waitDiv) {
				waitDiv = document.createElement('div');
				waitDiv.id = 'wait-msg-div';
				waitDiv.textContent = WAIT_MSG;
				ta.parentNode.insertBefore(waitDiv, ta.nextSibling);
			}
		} else {
			if (waitDiv) waitDiv.remove();
		}
	}

	// ボタン生成
	function createInjectButton(targetDiv) {
		if (document.getElementById(BUTTON_ID)) return;
		const btn = document.createElement('button');
		btn.id = BUTTON_ID;
		btn.textContent = 'API応答挿入';
		btn.onclick = function() {
			if (window.__apiState === 'done') {
				insertResponseToTextarea();
			} else if (window.__apiState === 'waiting') {
				updateWaitDisplay(true);
				window.__apiButtonPressed = true;
			} else {
				window.__apiButtonPressed = true;
				callApi();
			}
		};
		targetDiv.appendChild(btn);
	}

	// div追加監視
	const observer = new MutationObserver(mutations => {
		for (const m of mutations) {
			for (const node of m.addedNodes) {
				if (node.nodeType === 1 && node.matches && node.matches('div.target-div')) { // ←divの条件に変更
					createInjectButton(node);
				}
			}
		}
	});
	observer.observe(document.body, { childList: true, subtree: true });

	// ページロード時
	window.addEventListener('DOMContentLoaded', () => {
		callApi();
	});

})();
