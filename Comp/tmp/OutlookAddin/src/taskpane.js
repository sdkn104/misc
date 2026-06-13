/* global Office */

let emailData = { subject: '', senderName: '', senderEmail: '', body: '' };

Office.onReady((info) => {
  if (info.host !== Office.HostType.Outlook) return;

  document.getElementById('loading').style.display = 'none';
  document.getElementById('app').style.display = 'block';

  document.getElementById('generate-btn').addEventListener('click', generateReply);
  document.getElementById('insert-btn').addEventListener('click', insertReply);
  document.getElementById('copy-btn').addEventListener('click', copyToClipboard);

  loadEmailInfo();
});

function loadEmailInfo() {
  const item = Office.context.mailbox.item;

  item.subject.getAsync((result) => {
    if (result.status === Office.AsyncResultStatus.Succeeded) {
      emailData.subject = result.value || '';
      const el = document.getElementById('subject');
      el.textContent = emailData.subject || '(件名なし)';
      el.title = emailData.subject;
    }
  });

  if (item.from) {
    emailData.senderName = item.from.displayName || '';
    emailData.senderEmail = item.from.emailAddress || '';
    document.getElementById('sender').textContent =
      emailData.senderName
        ? `${emailData.senderName} <${emailData.senderEmail}>`
        : emailData.senderEmail;
  }

  item.body.getAsync(Office.CoercionType.Text, (result) => {
    if (result.status === Office.AsyncResultStatus.Succeeded) {
      emailData.body = result.value || '';
    }
  });
}

function generateReply() {
  const tone = document.getElementById('tone-select').value;
  const sender = emailData.senderName || '担当者';
  const subject = emailData.subject || '';

  const templates = {
    formal: [
      `${sender}様`,
      '',
      'いつもお世話になっております。',
      `「${subject}」の件、ご連絡いただきありがとうございます。`,
      '',
      '内容を確認いたしました。詳細につきましては、改めてご回答申し上げます。',
      '',
      '引き続き、どうぞよろしくお願いいたします。',
    ],
    casual: [
      `${sender}さん`,
      '',
      'ご連絡ありがとうございます！',
      `「${subject}」の件、了解しました。`,
      '',
      'また何かあればお気軽にご連絡ください。よろしくお願いします！',
    ],
    thankyou: [
      `${sender}様`,
      '',
      'お世話になっております。',
      `「${subject}」についてご連絡いただき、誠にありがとうございます。`,
      '',
      'ご丁寧なご対応に感謝申し上げます。',
      '今後ともどうぞよろしくお願いいたします。',
    ],
    acknowledge: [
      `${sender}様`,
      '',
      'お世話になっております。',
      `「${subject}」の件、承りました。`,
      '',
      '内容を確認の上、速やかに対応いたします。',
      'ご連絡いただきありがとうございます。',
      '',
      'よろしくお願いいたします。',
    ],
    decline: [
      `${sender}様`,
      '',
      'いつもお世話になっております。',
      `「${subject}」の件につきまして、ご連絡いただきありがとうございます。`,
      '',
      '誠に恐縮ではございますが、今回は諸事情によりご要望に応じることが難しい状況でございます。',
      'ご期待に添えず、大変申し訳ございません。',
      '',
      '引き続き、よろしくお願いいたします。',
    ],
  };

  const lines = templates[tone] || templates.formal;
  lines.push('', '---', '[署名]');

  document.getElementById('reply-preview').value = lines.join('\n');
  document.getElementById('insert-btn').disabled = false;
  document.getElementById('copy-btn').disabled = false;

  showStatus('返信文を生成しました', 'success');
}

function insertReply() {
  const text = document.getElementById('reply-preview').value.trim();
  if (!text) {
    showStatus('先に返信を生成してください', 'error');
    return;
  }

  const htmlBody = text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\n/g, '<br>');

  try {
    Office.context.mailbox.item.displayReplyForm({ htmlBody });
    showStatus('返信フォームを開きました', 'success');
  } catch (e) {
    showStatus('エラー: ' + e.message, 'error');
  }
}

function copyToClipboard() {
  const text = document.getElementById('reply-preview').value;
  if (!text) return;

  if (navigator.clipboard) {
    navigator.clipboard.writeText(text)
      .then(() => showStatus('クリップボードにコピーしました', 'success'))
      .catch(() => fallbackCopy(text));
  } else {
    fallbackCopy(text);
  }
}

function fallbackCopy(text) {
  const ta = document.getElementById('reply-preview');
  ta.select();
  document.execCommand('copy');
  showStatus('クリップボードにコピーしました', 'success');
}

function showStatus(message, type) {
  const el = document.getElementById('status');
  el.textContent = message;
  el.className = `status-${type}`;
  setTimeout(() => { el.textContent = ''; el.className = ''; }, 3000);
}
