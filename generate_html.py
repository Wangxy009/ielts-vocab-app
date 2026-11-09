#!/usr/bin/env python3
"""Generate the complete IELTS Vocabulary Review HTML application."""

import json
import os

# Read the vocabulary data
with open("/Users/wangxiaoya/Downloads/codex/vocab_data.js", "r", encoding="utf-8") as f:
    vocab_js = f.read()

CSS = r"""
:root {
  --bg: #f8f9fa; --bg-card: #ffffff; --bg-nav: #ffffff;
  --text: #212529; --text-secondary: #6c757d; --text-muted: #adb5bd;
  --primary: #4361ee; --primary-light: #eef0ff; --primary-dark: #3a56d4;
  --success: #2ec4b6; --danger: #e63946; --warning: #f4a261; --accent: #7209b7;
  --border: #dee2e6; --shadow: 0 2px 16px rgba(0,0,0,0.08);
  --radius: 12px; --radius-sm: 8px; --radius-lg: 16px;
  --transition: 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  --font: 'Segoe UI', system-ui, -apple-system, sans-serif;
}
[data-theme="dark"] {
  --bg: #1a1a2e; --bg-card: #16213e; --bg-nav: #16213e;
  --text: #e8e8e8; --text-secondary: #a0a0b0; --text-muted: #606080;
  --primary: #6c8aff; --primary-light: #1e2a4a; --primary-dark: #5a78f0;
  --success: #3dd9c8; --danger: #ff6b6b; --warning: #ffb347; --accent: #c77dff;
  --border: #2a2a4a; --shadow: 0 2px 20px rgba(0,0,0,0.3);
}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:var(--font);background:var(--bg);color:var(--text);min-height:100vh;transition:background var(--transition),color var(--transition);line-height:1.6}
nav{position:sticky;top:0;z-index:100;background:var(--bg-nav);border-bottom:1px solid var(--border);padding:0 12px;display:flex;align-items:center;gap:2px;overflow-x:auto;-webkit-overflow-scrolling:touch;box-shadow:0 1px 8px rgba(0,0,0,0.05)}
nav .logo{font-size:1.15rem;font-weight:700;white-space:nowrap;margin-right:6px;color:var(--primary);cursor:pointer}
nav button{background:none;border:none;padding:8px 10px;cursor:pointer;font-size:0.85rem;color:var(--text-secondary);border-radius:var(--radius-sm);white-space:nowrap;transition:all var(--transition);position:relative;font-family:var(--font)}
nav button:hover{background:var(--primary-light);color:var(--primary)}
nav button.active{background:var(--primary);color:#fff}
nav button .badge{position:absolute;top:2px;right:2px;background:var(--danger);color:#fff;font-size:0.6rem;padding:1px 4px;border-radius:10px;min-width:16px;text-align:center}
#themeToggle{font-size:1.1rem;padding:6px 8px;margin-left:auto}
main{max-width:1200px;margin:0 auto;padding:20px 16px}
.page{display:none;animation:fadeIn 0.3s ease}
.page.active{display:block}
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
@keyframes slideUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.05)}}
@keyframes shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-5px)}75%{transform:translateX(5px)}}
.card{background:var(--bg-card);border-radius:var(--radius);padding:24px;box-shadow:var(--shadow);border:1px solid var(--border);transition:all var(--transition)}
.card:hover{box-shadow:0 4px 24px rgba(0,0,0,0.12)}
h2{font-size:1.5rem;margin-bottom:16px;color:var(--text)}
h3{font-size:1.15rem;margin-bottom:12px;color:var(--text)}
.btn{display:inline-flex;align-items:center;gap:6px;padding:10px 20px;border:none;border-radius:var(--radius-sm);cursor:pointer;font-size:0.9rem;font-weight:600;font-family:var(--font);transition:all var(--transition);text-decoration:none}
.btn-primary{background:var(--primary);color:#fff}.btn-primary:hover{background:var(--primary-dark);transform:translateY(-1px)}
.btn-success{background:var(--success);color:#fff}.btn-success:hover{opacity:0.9;transform:translateY(-1px)}
.btn-danger{background:var(--danger);color:#fff}.btn-danger:hover{opacity:0.9}
.btn-outline{background:transparent;border:2px solid var(--primary);color:var(--primary)}.btn-outline:hover{background:var(--primary-light)}
.btn-ghost{background:transparent;color:var(--text-secondary)}.btn-ghost:hover{background:var(--border)}
.btn-sm{padding:6px 12px;font-size:0.8rem}
.btn-lg{padding:14px 28px;font-size:1.05rem}
.btn-icon{width:40px;height:40px;padding:0;display:inline-flex;align-items:center;justify-content:center;border-radius:50%}
input,select{font-family:var(--font);padding:10px 14px;border:2px solid var(--border);border-radius:var(--radius-sm);font-size:0.95rem;background:var(--bg-card);color:var(--text);transition:border var(--transition);width:100%}
input:focus,select:focus{outline:none;border-color:var(--primary)}
input.correct{border-color:var(--success)!important;background:rgba(46,196,182,0.08)}
input.wrong{border-color:var(--danger)!important;background:rgba(230,57,70,0.08);animation:shake 0.4s ease}
.word-display{font-size:2.5rem;font-weight:700;text-align:center;padding:24px;color:var(--primary);letter-spacing:1px}
.phonetic{font-size:1.1rem;color:var(--text-secondary);text-align:center;margin-bottom:12px}
.definition{font-size:1.3rem;text-align:center;color:var(--text-secondary);margin-bottom:16px}
.example{font-size:0.95rem;text-align:center;color:var(--text-muted);font-style:italic;margin-bottom:16px}
.grid{display:grid;gap:12px}
.grid-2{grid-template-columns:repeat(auto-fill,minmax(280px,1fr))}
.grid-3{grid-template-columns:repeat(auto-fill,minmax(200px,1fr))}
.grid-4{grid-template-columns:repeat(auto-fill,minmax(150px,1fr))}
.chapter-card{cursor:pointer;text-align:center;padding:20px 16px;transition:all var(--transition);position:relative;overflow:hidden}
.chapter-card:hover{transform:translateY(-3px);border-color:var(--primary)}
.chapter-card .ch-num{font-size:2rem;font-weight:800;color:var(--primary);opacity:0.3}
.chapter-card .ch-title{font-size:1rem;font-weight:600;margin:4px 0}
.chapter-card .ch-subtitle{font-size:0.8rem;color:var(--text-muted)}
.chapter-card .progress-bar{height:4px;background:var(--border);border-radius:2px;margin-top:8px;overflow:hidden}
.chapter-card .progress-fill{height:100%;background:var(--success);border-radius:2px;transition:width 0.5s ease}
.flashcard-container{perspective:1000px;width:100%;max-width:500px;margin:0 auto;height:320px;cursor:pointer}
.flashcard{position:relative;width:100%;height:100%;transition:transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);transform-style:preserve-3d}
.flashcard.flipped{transform:rotateY(180deg)}
.flashcard .front,.flashcard .back{position:absolute;width:100%;height:100%;backface-visibility:hidden;border-radius:var(--radius-lg);display:flex;flex-direction:column;align-items:center;justify-content:center;padding:32px;box-shadow:var(--shadow);border:1px solid var(--border)}
.flashcard .front{background:var(--bg-card)}
.flashcard .back{background:var(--primary-light);transform:rotateY(180deg)}
.result-box{padding:16px;border-radius:var(--radius-sm);text-align:center;font-weight:600;margin:12px 0;animation:slideUp 0.3s ease}
.result-box.correct{background:rgba(46,196,182,0.1);color:var(--success);border:1px solid var(--success)}
.result-box.wrong{background:rgba(230,57,70,0.1);color:var(--danger);border:1px solid var(--danger)}
.stats-row{display:flex;gap:16px;flex-wrap:wrap;margin-bottom:20px}
.stat-card{flex:1;min-width:120px;background:var(--bg-card);border-radius:var(--radius);padding:16px;text-align:center;box-shadow:var(--shadow);border:1px solid var(--border)}
.stat-card .stat-value{font-size:2rem;font-weight:800;color:var(--primary)}
.stat-card .stat-label{font-size:0.8rem;color:var(--text-secondary);margin-top:4px}
.word-list-item{display:flex;align-items:center;justify-content:space-between;padding:12px 16px;border-bottom:1px solid var(--border);cursor:pointer;transition:background var(--transition);gap:12px}
.word-list-item:hover{background:var(--primary-light)}
.word-list-item .wl-english{font-weight:600;color:var(--text);min-width:140px}
.word-list-item .wl-chinese{color:var(--text-secondary);flex:1}
.word-list-item .wl-status{font-size:0.8rem;padding:2px 8px;border-radius:10px}
.status-mastered{background:rgba(46,196,182,0.15);color:var(--success)}
.status-learning{background:rgba(244,162,97,0.15);color:var(--warning)}
.status-new{background:var(--border);color:var(--text-muted)}
.controls{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin:16px 0}
.modal-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);z-index:200;display:flex;align-items:center;justify-content:center;animation:fadeIn 0.2s ease}
.modal{background:var(--bg-card);border-radius:var(--radius-lg);padding:32px;max-width:500px;width:90%;max-height:80vh;overflow-y:auto;box-shadow:0 20px 60px rgba(0,0,0,0.3)}
.hint-text{color:var(--text-muted);font-size:0.85rem;text-align:center;margin:8px 0}
.speed-control{display:flex;align-items:center;gap:8px;justify-content:center}
.speed-control input[type=range]{width:120px}
.tag{display:inline-block;padding:3px 8px;border-radius:12px;font-size:0.75rem;font-weight:600;margin:2px}
.tag-correct{background:rgba(46,196,182,0.15);color:var(--success)}
.tag-wrong{background:rgba(230,57,70,0.15);color:var(--danger)}
.word-detail{padding:20px}
.word-detail .wd-word{font-size:2rem;font-weight:700;color:var(--primary)}
.word-detail .wd-phonetic{color:var(--text-secondary);margin:4px 0}
.word-detail .wd-def{font-size:1.1rem;margin:8px 0}
.word-detail .wd-example{color:var(--text-muted);font-style:italic}
.voice-selector{margin:8px 0}
.voice-selector select{width:auto;font-size:0.85rem;padding:6px 10px}
.empty-state{text-align:center;padding:40px;color:var(--text-muted)}
.empty-state .empty-icon{font-size:3rem;margin-bottom:12px}
.review-schedule{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}
.review-badge{background:var(--primary-light);color:var(--primary);padding:6px 12px;border-radius:20px;font-size:0.8rem;font-weight:600}
.toast{position:fixed;bottom:20px;right:20px;padding:12px 20px;background:var(--bg-card);border-radius:var(--radius-sm);box-shadow:0 8px 32px rgba(0,0,0,0.2);z-index:300;animation:slideUp 0.3s ease;border-left:4px solid var(--success);font-weight:500}
@media(max-width:768px){
  nav{gap:0;padding:0 6px}
  nav button{font-size:0.75rem;padding:6px 8px}
  nav .logo{font-size:1rem}
  .word-display{font-size:1.8rem}
  .flashcard-container{height:240px}
  .stats-row{gap:8px}
  .stat-card{padding:12px}
  .stat-card .stat-value{font-size:1.4rem}
}
"""

JS = r"""
// ===== STATE =====
let currentPage = 'dashboard';
let currentChapter = 1;
let currentWordIdx = 0;
let currentMode = 'sequential'; // sequential | random | difficult
let darkMode = localStorage.getItem('ielts-dark-mode') === 'true';
let speechRate = parseFloat(localStorage.getItem('ielts-speech-rate') || '0.85');
let speechVoice = null;
let quizWords = [];
let quizIdx = 0;
let quizScore = 0;
let quizCombo = 0;
let dictationWords = [];
let dictationIdx = 0;
let dictationScore = 0;

// ===== PROGRESS SYSTEM =====
function loadProgress() {
  try { return JSON.parse(localStorage.getItem('ielts-progress') || '{}'); }
  catch(e) { return {}; }
}
function saveProgress(p) { localStorage.setItem('ielts-progress', JSON.stringify(p)); }
function getWordProgress(wordId) {
  const p = loadProgress();
  return p[wordId] || {m:0,lr:0,nr:0,rc:0,kc:0,uc:0};
}
function updateWordProgress(wordId, known) {
  const p = loadProgress();
  const w = p[wordId] || {m:0,lr:0,nr:0,rc:0,kc:0,uc:0};
  w.rc++; w.lr = Date.now();
  if(known) { w.kc++; if(w.m<3) w.m++; }
  else { w.uc++; if(w.m>0) w.m--; }
  const intervals = [14400000, 86400000, 259200000, 604800000];
  w.nr = Date.now() + intervals[w.m];
  p[wordId] = w; saveProgress(p);
}
function getChapterProgress(chapter) {
  const words = getChapterWords(chapter);
  if(!words.length) return 0;
  const p = loadProgress();
  let mastered = 0;
  words.forEach(w => { if(p[w.i] && p[w.i].m>=3) mastered++; });
  return Math.round((mastered/words.length)*100);
}
function getTotalStats() {
  const p = loadProgress();
  let total=0, mastered=0, reviewed=0;
  for(const ch of Object.values(VOCAB_DATA.chapters)) {
    for(const w of ch.words) {
      total++;
      if(p[w.i]) { reviewed++; if(p[w.i].m>=3) mastered++; }
    }
  }
  return {total,reviewed,mastered,pct:total?Math.round(mastered/total*100):0};
}
function getDailyStreak() {
  try { return parseInt(localStorage.getItem('ielts-streak')||'0'); } catch(e) { return 0; }
}
function updateDailyStreak() {
  const today = new Date().toDateString();
  const last = localStorage.getItem('ielts-last-study-date');
  if(last===today) return;
  const yesterday = new Date(Date.now()-86400000).toDateString();
  let streak = getDailyStreak();
  if(last===yesterday) streak++;
  else streak=1;
  localStorage.setItem('ielts-streak',streak.toString());
  localStorage.setItem('ielts-last-study-date',today);
}

// ===== CHAPTER/WORD HELPERS =====
function getChapterWords(num) {
  const ch = VOCAB_DATA.chapters[num.toString()];
  return ch ? ch.words : [];
}
function getChapterTitle(num) {
  const ch = VOCAB_DATA.chapters[num.toString()];
  return ch ? ch.title : '';
}
function getAllWords() {
  let all=[];
  for(let i=1;i<=22;i++) all=all.concat(getChapterWords(i));
  return all;
}
function getShuffledWords(chapter) {
  const words = chapter ? getChapterWords(chapter) : getAllWords();
  return [...words].sort(()=>Math.random()-0.5);
}

// ===== AUDIO / TTS =====
function initSpeech() {
  if(!window.speechSynthesis) return;
  const voices = speechSynthesis.getVoices();
  if(voices.length) {
    const en = voices.filter(v=>v.lang.startsWith('en'));
    speechVoice = en.find(v=>v.name.includes('Google')||v.name.includes('Samantha')||v.name.includes('Daniel')) || en[0] || voices[0];
  }
}
function speak(text, rate) {
  if(!window.speechSynthesis) return;
  speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.voice = speechVoice; u.rate = rate||speechRate; u.lang='en-US';
  speechSynthesis.speak(u);
}
function speakWord(word) { speak(word, speechRate); }
speechSynthesis && speechSynthesis.addEventListener('voiceschanged', initSpeech);

// ===== SPEECH RECOGNITION =====
function startRecognition(lang, callback) {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if(!SR) { callback({error:'not-supported'}); return null; }
  const rec = new SR();
  rec.lang = lang || 'en-US';
  rec.interimResults = false;
  rec.maxAlternatives = 3;
  rec.onresult = e => callback({text:e.results[0][0].transcript.trim(),alternatives:Array.from(e.results[0]).map(r=>r.transcript.trim())});
  rec.onerror = e => callback({error:e.error});
  rec.start();
  return rec;
}

// ===== NAVIGATION =====
function navigate(page, data) {
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('nav button.nav-btn').forEach(b=>b.classList.remove('active'));
  const pageEl = document.getElementById('page-'+page);
  if(pageEl) pageEl.classList.add('active');
  const navBtn = document.querySelector(`nav button[data-page="${page}"]`);
  if(navBtn) navBtn.classList.add('active');
  currentPage = page; currentWordIdx = 0;
  window.location.hash = page;
  if(data) renderPage(page,data);
  else renderPage(page);
}

function renderPage(page, data) {
  switch(page) {
    case 'dashboard': renderDashboard(); break;
    case 'browse': renderBrowse(data||1); break;
    case 'flashcard': renderFlashcard(data||1); break;
    case 'dictation': renderDictation(data||1); break;
    case 'speaking': renderSpeaking(data||1); break;
    case 'spelling': renderSpelling(data||1); break;
    case 'quiz': renderQuiz(data||1); break;
    case 'search': renderSearch(); break;
    case 'progress': renderProgress(); break;
  }
}

// ===== DASHBOARD =====
function renderDashboard() {
  const s = getTotalStats();
  const streak = getDailyStreak();
  const dueNow = getDueWords();
  let chCards = '';
  for(let i=1;i<=22;i++) {
    const pct = getChapterProgress(i);
    chCards += `<div class="card chapter-card" onclick="navigate('browse',${i})">
      <div class="ch-num">${String(i).padStart(2,'0')}</div>
      <div class="ch-title">${getChapterTitle(i)}</div>
      <div class="ch-subtitle">${getChapterWords(i).length} 词</div>
      <div class="progress-bar"><div class="progress-fill" style="width:${pct}%"></div></div>
      <div style="font-size:0.75rem;color:var(--text-muted);margin-top:4px">${pct}% 掌握</div>
    </div>`;
  }
  document.getElementById('dashboard').innerHTML = `
    <h2>📊 学习仪表盘</h2>
    <div class="stats-row">
      <div class="stat-card"><div class="stat-value">${streak}🔥</div><div class="stat-label">连续打卡</div></div>
      <div class="stat-card"><div class="stat-value">${s.mastered}</div><div class="stat-label">已掌握</div></div>
      <div class="stat-card"><div class="stat-value">${s.reviewed}</div><div class="stat-label">已学习</div></div>
      <div class="stat-card"><div class="stat-value">${s.pct}%</div><div class="stat-label">总进度</div></div>
      <div class="stat-card"><div class="stat-value">${dueNow.length}</div><div class="stat-label">待复习</div></div>
    </div>
    ${dueNow.length>0?`<div class="card" style="margin-bottom:16px;cursor:pointer" onclick="startReviewDue()">
      <h3>🔔 待复习词汇 (${dueNow.length})</h3>
      <div class="review-schedule">${dueNow.slice(0,8).map(w=>`<span class="review-badge">${w.w}</span>`).join('')}${dueNow.length>8?`<span class="review-badge">+${dueNow.length-8} 更多</span>`:''}</div>
    </div>`:''}
    <h3 style="margin-bottom:12px">📚 全部章节</h3>
    <div class="grid grid-3">${chCards}</div>`;
}

function getDueWords() {
  const p = loadProgress(); const now = Date.now(); const due=[];
  for(let i=1;i<=22;i++) {
    for(const w of getChapterWords(i)) {
      if(p[w.i] && p[w.i].nr && p[w.i].nr <= now && p[w.i].m < 3) due.push(w);
    }
  }
  return due.sort(()=>Math.random()-0.5);
}

function startReviewDue() {
  const due = getDueWords();
  if(!due.length){showToast('✅ 没有待复习的单词！');return;}
  window._reviewQueue = due;
  window._reviewIdx = 0;
  showReviewCard();
}
function showReviewCard() {
  const q = window._reviewQueue;
  const i = window._reviewIdx;
  if(i>=q.length){showToast('🎉 复习完成！');updateDailyStreak();navigate('dashboard');return;}
  const w = q[i];
  const el = document.getElementById('dashboard');
  el.innerHTML = `
    <h2>📝 复习 (${i+1}/${q.length})</h2>
    <div class="card flashcard-container" style="cursor:default" id="review-card">
      <div class="front" style="position:static;width:100%;height:100%;backface-visibility:visible" id="review-front">
        <div class="word-display">${w.w}</div>
        <div class="controls">
          <button class="btn btn-success" onclick="reviewAnswer(true)">✅ 认识</button>
          <button class="btn btn-danger" onclick="reviewAnswer(false)">❌ 不认识</button>
          <button class="btn btn-outline btn-sm" onclick="speakWord('${w.w}')">🔊</button>
        </div>
      </div>
    </div>`;
}
function reviewAnswer(known) {
  const q = window._reviewQueue;
  const i = window._reviewIdx;
  const w = q[i];
  updateWordProgress(w.i, known);
  window._reviewIdx++;
  showReviewCard();
}

// ===== BROWSE =====
function renderBrowse(chapter) {
  currentChapter = chapter;
  const words = getChapterWords(chapter);
  const p = loadProgress();
  const pct = getChapterProgress(chapter);
  let sortBy='default';
  let filtered = [...words];
  let html = `
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;flex-wrap:wrap">
      <button class="btn btn-ghost" onclick="navigate('browse',${chapter-1})" ${chapter<=1?'disabled':''}>← 上一章</button>
      <h2 style="margin:0">📚 第${chapter}章: ${getChapterTitle(chapter)}</h2>
      <button class="btn btn-ghost" onclick="navigate('browse',${chapter+1})" ${chapter>=22?'disabled':''}>下一章 →</button>
    </div>
    <div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:16px">
      <div class="stat-card"><div class="stat-value">${words.length}</div><div class="stat-label">总词汇</div></div>
      <div class="stat-card"><div class="stat-value">${pct}%</div><div class="stat-label">掌握率</div></div>
    </div>
    <div style="display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap">
      <select onchange="sortBrowse(this.value)" style="width:auto"><option value="default">默认排序</option><option value="alpha">字母A-Z</option><option value="mastered">掌握程度</option></select>
      <input type="text" placeholder="🔍 在本章中搜索..." oninput="filterBrowse(this.value)" style="max-width:250px">
      <button class="btn btn-outline btn-sm" onclick="navigate('flashcard',${chapter})">🎴 闪卡模式</button>
      <button class="btn btn-outline btn-sm" onclick="navigate('dictation',${chapter})">✍️ 听写模式</button>
      <button class="btn btn-outline btn-sm" onclick="navigate('spelling',${chapter})">📝 拼写练习</button>
    </div>
    <div class="card" id="word-list"></div>`;
  document.getElementById('browse').innerHTML = html;
  renderWordList(words, p);
}

function sortBrowse(by) {
  const words = getChapterWords(currentChapter);
  const p = loadProgress();
  let sorted=[...words];
  if(by==='alpha') sorted.sort((a,b)=>a.w.localeCompare(b.w));
  if(by==='mastered') sorted.sort((a,b)=>(getWordProgress(b.i).m)-(getWordProgress(a.i).m));
  renderWordList(sorted, p);
}
function filterBrowse(q) {
  const words = getChapterWords(currentChapter);
  const p = loadProgress();
  const f = words.filter(w=>w.w.toLowerCase().includes(q.toLowerCase())||w.d.includes(q));
  renderWordList(f, p);
}
function renderWordList(words, progress) {
  let html = '';
  words.forEach((w,i)=>{
    const wp = progress[w.i] || {m:0};
    const cls = wp.m>=3?'status-mastered':wp.m>0?'status-learning':'status-new';
    const label = wp.m>=3?'已掌握':wp.m>0?'学习中':'新词';
    html += `<div class="word-list-item" onclick="showWordDetail('${w.i}')">
      <span style="font-size:0.75rem;color:var(--text-muted)">${i+1}</span>
      <span class="wl-english">${w.w}</span>
      <span class="wl-chinese">${w.d}</span>
      <span class="wl-status ${cls}">${label}</span>
      <button class="btn btn-ghost btn-sm" onclick="event.stopPropagation();speakWord('${w.w}')">🔊</button>
    </div>`;
  });
  document.getElementById('word-list').innerHTML = html || '<div class="empty-state"><div class="empty-icon">🔍</div><p>没有匹配的词汇</p></div>';
}

function showWordDetail(wordId) {
  const w = findWordById(wordId);
  if(!w) return;
  const wp = getWordProgress(wordId);
  const overlay = document.createElement('div');
  overlay.className='modal-overlay';
  overlay.onclick = e => {if(e.target===overlay) overlay.remove();};
  overlay.innerHTML = `<div class="modal word-detail">
    <div class="wd-word">${w.w} <button class="btn btn-ghost btn-sm" onclick="speakWord('${w.w}')">🔊</button></div>
    <div class="wd-def">${w.d}</div>
    <div style="margin-top:12px;font-size:0.85rem;color:var(--text-secondary)">
      复习次数: ${wp.rc} | 认识: ${wp.kc}次 | 不认识: ${wp.uc}次 | 掌握级别: ${'⭐'.repeat(wp.m)}
    </div>
    <div class="controls" style="margin-top:16px">
      <button class="btn btn-success btn-sm" onclick="updateWordProgress('${wordId}',true);this.closest('.modal-overlay').remove();showToast('✅ 已标记为认识')">✅ 认识</button>
      <button class="btn btn-danger btn-sm" onclick="updateWordProgress('${wordId}',false);this.closest('.modal-overlay').remove();showToast('❌ 标记为不认识')">❌ 不认识</button>
      <button class="btn btn-outline btn-sm" onclick="this.closest('.modal-overlay').remove()">关闭</button>
    </div>
  </div>`;
  document.body.appendChild(overlay);
}

function findWordById(id) {
  for(let i=1;i<=22;i++)
    for(const w of getChapterWords(i))
      if(w.i===id) return w;
  return null;
}

// ===== FLASHCARD =====
function renderFlashcard(chapter) {
  currentChapter = chapter; currentWordIdx = 0;
  const words = currentMode==='random'?getShuffledWords(chapter):getChapterWords(chapter);
  window._fcWords = words;
  window._fcIdx = 0;
  showFlashcard();
}
function showFlashcard() {
  const words = window._fcWords;
  const i = window._fcIdx;
  if(i>=words.length){showToast('🎉 本章闪卡已完成！');navigate('browse',currentChapter);return;}
  const w = words[i];
  const isFlipped = window._fcFlipped || false;
  document.getElementById('flashcard').innerHTML = `
    <h2>🎴 闪卡模式 - 第${currentChapter}章 (${i+1}/${words.length})</h2>
    <div class="flashcard-container" onclick="flipCard()">
      <div class="flashcard${isFlipped?' flipped':''}" id="fc-card">
        <div class="front"><div class="word-display">${w.w}</div><button class="btn btn-ghost btn-sm" onclick="event.stopPropagation();speakWord('${w.w}')">🔊 听发音</button><div class="hint-text">点击翻转</div></div>
        <div class="back"><div class="definition">${w.d}</div><div class="hint-text">点击翻转</div></div>
      </div>
    </div>
    <div class="controls">
      <button class="btn btn-danger" onclick="fcResult(false)">❌ 不认识</button>
      <button class="btn btn-ghost" onclick="fcPrev()">⬅ 上一个</button>
      <button class="btn btn-success" onclick="fcResult(true)">✅ 认识</button>
      <button class="btn btn-ghost" onclick="fcSkip()">⏭ 跳过</button>
    </div>
    <div class="controls">
      <select onchange="currentMode=this.value;renderFlashcard(currentChapter)" style="width:auto">
        <option value="sequential">顺序模式</option><option value="random">随机模式</option>
      </select>
    </div>`;
  window._fcFlipped = false;
}
function flipCard() {
  window._fcFlipped = !window._fcFlipped;
  document.getElementById('fc-card').classList.toggle('flipped');
}
function fcResult(known) {
  const w = window._fcWords[window._fcIdx];
  updateWordProgress(w.i, known);
  updateDailyStreak();
  window._fcIdx++; window._fcFlipped = false;
  showFlashcard();
}
function fcPrev() { if(window._fcIdx>0){window._fcIdx--;window._fcFlipped=false;showFlashcard();} }
function fcSkip() { window._fcIdx++; window._fcFlipped = false; showFlashcard(); }

// ===== DICTATION =====
function renderDictation(chapter) {
  currentChapter = chapter;
  const words = getShuffledWords(chapter||currentChapter);
  dictationWords = words; dictationIdx = 0; dictationScore = 0;
  showDictation();
}
function showDictation() {
  if(dictationIdx >= dictationWords.length) {
    document.getElementById('dictation').innerHTML = `
      <div class="card" style="text-align:center">
        <div class="empty-icon" style="font-size:4rem">🎉</div>
        <h2>听写完成!</h2>
        <p style="font-size:1.5rem">得分: ${dictationScore}/${dictationWords.length}</p>
        <p style="color:var(--text-secondary)">正确率: ${Math.round(dictationScore/dictationWords.length*100)}%</p>
        <div class="controls">
          <button class="btn btn-primary" onclick="renderDictation(${currentChapter})">🔄 重新开始</button>
          <button class="btn btn-outline" onclick="navigate('browse',${currentChapter})">📚 返回章节</button>
        </div>
      </div>`;
    updateDailyStreak(); return;
  }
  const w = dictationWords[dictationIdx];
  document.getElementById('dictation').innerHTML = `
    <h2>✍️ 听写模式 (${dictationIdx+1}/${dictationWords.length})</h2>
    <div class="card" style="text-align:center">
      <button class="btn btn-lg btn-primary" onclick="speakWord('${w.w}')" style="margin:16px">🔊 播放单词</button>
      <div class="speed-control">
        <span style="font-size:0.8rem">语速:</span>
        <input type="range" min="0.5" max="1.5" step="0.05" value="${speechRate}" oninput="speechRate=parseFloat(this.value);localStorage.setItem('ielts-speech-rate',speechRate);this.nextElementSibling.textContent=speechRate+'x'">
        <span style="font-size:0.8rem">${speechRate}x</span>
      </div>
      <input type="text" id="dictation-input" placeholder="输入你听到的单词..." autocomplete="off" style="margin:16px 0;max-width:400px;text-align:center;font-size:1.2rem" onkeydown="if(event.key==='Enter')checkDictation()">
      <div class="controls">
        <button class="btn btn-success" onclick="checkDictation()">✅ 提交</button>
        <button class="btn btn-outline" onclick="showDictationHint()">💡 提示</button>
        <button class="btn btn-ghost" onclick="dictationIdx++;speakWord('${w.w}');showDictation()">⏭ 跳过</button>
      </div>
      <div id="dictation-result"></div>
    </div>`;
  setTimeout(()=>{speakWord(w.w);document.getElementById('dictation-input')?.focus();}, 400);
}
function checkDictation() {
  const input = document.getElementById('dictation-input');
  const w = dictationWords[dictationIdx];
  const userAnswer = input.value.trim().toLowerCase();
  const correct = w.w.toLowerCase() === userAnswer;
  const resultEl = document.getElementById('dictation-result');
  if(correct) {
    dictationScore++; input.className='correct';
    resultEl.innerHTML = `<div class="result-box correct">✅ 正确! ${w.w} - ${w.d}</div>`;
    updateWordProgress(w.i, true);
  } else {
    input.className='wrong';
    resultEl.innerHTML = `<div class="result-box wrong">❌ 错误! 正确答案: <strong>${w.w}</strong> - ${w.d}<br>你输入的是: ${userAnswer||'(空)'}</div>`;
    updateWordProgress(w.i, false);
  }
  updateDailyStreak();
  input.disabled = true;
  setTimeout(()=>{dictationIdx++;showDictation();}, 1500);
}
function showDictationHint() {
  const w = dictationWords[dictationIdx];
  const hint = w.w.substring(0,2)+'... (共'+w.w.length+'个字母)';
  document.getElementById('dictation-result').innerHTML = `<div class="result-box" style="color:var(--warning);border-color:var(--warning)">💡 提示: ${hint}</div>`;
}

// ===== SPEAKING =====
function renderSpeaking(chapter) {
  currentChapter = chapter;
  const words = getShuffledWords(chapter||currentChapter);
  window._spWords = words; window._spIdx = 0; window._spScore = 0;
  showSpeaking();
}
function showSpeaking() {
  const words = window._spWords;
  const i = window._spIdx;
  if(i>=words.length) {
    document.getElementById('speaking').innerHTML = `
      <div class="card" style="text-align:center">
        <div class="empty-icon" style="font-size:4rem">🎉</div>
        <h2>口语练习完成!</h2>
        <p style="font-size:1.5rem">得分: ${window._spScore}/${words.length}</p>
        <div class="controls"><button class="btn btn-primary" onclick="renderSpeaking(${currentChapter})">🔄 重新开始</button></div>
      </div>`;
    updateDailyStreak(); return;
  }
  const w = words[i];
  document.getElementById('speaking').innerHTML = `
    <h2>🎤 口语练习 (${i+1}/${words.length})</h2>
    <div class="card" style="text-align:center">
      <div class="word-display">${w.w}</div>
      <div class="definition">${w.d}</div>
      <button class="btn btn-lg btn-primary" onclick="speakWord('${w.w}')" style="margin:8px">🔊 听标准发音</button>
      <div id="sp-recording-status" style="margin:12px;padding:12px;border-radius:var(--radius-sm);background:var(--primary-light);color:var(--primary);font-weight:600;display:none">🎙️ 正在录音...</div>
      <div class="controls">
        <button class="btn btn-success btn-lg" id="sp-record-btn" onclick="startSpeakingRecognition()">🎙️ 开始朗读</button>
      </div>
      <div id="sp-result"></div>
      <div class="controls"><button class="btn btn-success" onclick="spSelfEval(true)">✅ 我读对了</button><button class="btn btn-danger" onclick="spSelfEval(false)">❌ 我读错了</button></div>
    </div>`;
}

let _spRecognition = null;
function startSpeakingRecognition() {
  const w = window._spWords[window._spIdx];
  const statusEl = document.getElementById('sp-recording-status');
  statusEl.style.display = 'block';
  _spRecognition = startRecognition('en-US', result => {
    statusEl.style.display = 'none';
    const resEl = document.getElementById('sp-result');
    if(result.error) {
      resEl.innerHTML = `<div class="result-box" style="color:var(--warning);border-color:var(--warning)">⚠️ ${result.error==='not-supported'?'您的浏览器不支持语音识别，请使用自评按钮':'语音识别出错: '+result.error}</div>`;
      return;
    }
    const spoken = result.text.toLowerCase();
    const correct = w.w.toLowerCase();
    const match = spoken === correct || result.alternatives.some(a=>a.trim().toLowerCase()===correct);
    if(match) {
      window._spScore++;
      resEl.innerHTML = `<div class="result-box correct">✅ 发音正确! "${spoken}"</div>`;
      updateWordProgress(w.i, true);
      updateDailyStreak();
      setTimeout(()=>{window._spIdx++;showSpeaking();},1500);
    } else {
      resEl.innerHTML = `<div class="result-box wrong">❌ 你说的: "${spoken}"<br>正确发音: <strong>${w.w}</strong> <button class="btn btn-ghost btn-sm" onclick="speakWord('${w.w}')">🔊</button><br><span style="font-size:0.8rem">请再试一次或使用自评按钮</span></div>`;
    }
  });
}
function spSelfEval(ok) {
  const w = window._spWords[window._spIdx];
  if(ok){window._spScore++;updateWordProgress(w.i,true);}else{updateWordProgress(w.i,false);}
  updateDailyStreak();
  window._spIdx++; showSpeaking();
}

// ===== SPELLING =====
function renderSpelling(chapter) {
  currentChapter = chapter;
  const words = getShuffledWords(chapter||currentChapter);
  window._slWords = words; window._slIdx = 0; window._slScore = 0;
  showSpelling();
}
function showSpelling() {
  const words = window._slWords;
  const i = window._slIdx;
  if(i>=words.length) {
    document.getElementById('spelling').innerHTML = `
      <div class="card" style="text-align:center">
        <div class="empty-icon" style="font-size:4rem">🎉</div>
        <h2>拼写练习完成!</h2>
        <p style="font-size:1.5rem">得分: ${window._slScore}/${words.length}</p>
        <div class="controls"><button class="btn btn-primary" onclick="renderSpelling(${currentChapter})">🔄 重新开始</button></div>
      </div>`;
    updateDailyStreak(); return;
  }
  const w = words[i];
  document.getElementById('spelling').innerHTML = `
    <h2>📝 拼写练习 (${i+1}/${words.length})</h2>
    <div class="card" style="text-align:center">
      <div class="definition" style="font-size:1.5rem;margin:24px 0">${w.d}</div>
      <input type="text" id="spelling-input" placeholder="输入对应的英文单词..." autocomplete="off" style="max-width:400px;text-align:center;font-size:1.2rem" onkeydown="if(event.key==='Enter')checkSpelling()">
      <div class="controls">
        <button class="btn btn-success" onclick="checkSpelling()">✅ 提交</button>
        <button class="btn btn-outline" onclick="showSpellingHint()">💡 提示</button>
        <button class="btn btn-ghost" onclick="window._slIdx++;showSpelling()">⏭ 跳过</button>
      </div>
      <div id="spelling-result"></div>
    </div>`;
  setTimeout(()=>document.getElementById('spelling-input')?.focus(),200);
}
function checkSpelling() {
  const input = document.getElementById('spelling-input');
  const w = window._slWords[window._slIdx];
  const ans = input.value.trim().toLowerCase();
  const correct = w.w.toLowerCase()===ans;
  const resEl = document.getElementById('spelling-result');
  if(correct) {
    window._slScore++; input.className='correct';
    resEl.innerHTML = `<div class="result-box correct">✅ 正确! ${w.w}</div>`;
    updateWordProgress(w.i, true);
  } else {
    input.className='wrong';
    let diff = ''; const t=w.w.toLowerCase();
    for(let j=0;j<Math.max(t.length,ans.length);j++) {
      if(j<t.length&&j<ans.length&&t[j]===ans[j]) diff+=t[j];
      else if(j<t.length) diff+=`<span style="color:var(--danger);font-weight:700">${t[j]}</span>`;
      else diff+=`<span style="color:var(--danger)">_</span>`;
    }
    resEl.innerHTML = `<div class="result-box wrong">❌ 正确答案: <strong>${w.w}</strong> - ${w.d}<br>对比: ${diff}</div>`;
    updateWordProgress(w.i, false);
  }
  updateDailyStreak(); input.disabled = true;
  setTimeout(()=>{window._slIdx++;showSpelling();},1800);
}
function showSpellingHint() {
  const w = window._slWords[window._slIdx];
  const t = w.w; let h='';
  for(let i=0;i<t.length;i++) h+=(i===0||i===t.length-1)?t[i]:'_ ';
  document.getElementById('spelling-result').innerHTML = `<div class="result-box" style="color:var(--warning);border-color:var(--warning)">💡 提示: ${h} (${t.length}个字母)</div>`;
}

// ===== QUIZ =====
function renderQuiz(chapter) {
  currentChapter = chapter;
  const words = getShuffledWords(chapter||currentChapter);
  quizWords = words.slice(0,Math.min(30,words.length));
  quizIdx = 0; quizScore = 0; quizCombo = 0;
  showQuiz();
}
function showQuiz() {
  if(quizIdx>=quizWords.length) {
    document.getElementById('quiz').innerHTML = `
      <div class="card" style="text-align:center">
        <div class="empty-icon" style="font-size:4rem">${quizScore>=quizWords.length*0.8?'🏆':'📝'}</div>
        <h2>测试完成!</h2>
        <p style="font-size:1.5rem">得分: ${quizScore}/${quizWords.length}</p>
        <p style="color:var(--text-secondary)">正确率: ${Math.round(quizScore/quizWords.length*100)}% | 最高连击: ${quizCombo}</p>
        <div class="controls"><button class="btn btn-primary" onclick="renderQuiz(${currentChapter})">🔄 重新测试</button></div>
      </div>`;
    updateDailyStreak(); return;
  }
  const w = quizWords[quizIdx];
  const allWords = getAllWords();
  let options = [w];
  const pool = allWords.filter(x=>x.i!==w.i);
  for(let j=0;j<3;j++){const ri=Math.floor(Math.random()*pool.length);options.push(pool.splice(ri,1)[0]);}
  options.sort(()=>Math.random()-0.5);
  document.getElementById('quiz').innerHTML = `
    <h2>📝 选择题测试 (${quizIdx+1}/${quizWords.length})</h2>
    <div class="card" style="text-align:center">
      <div class="definition" style="font-size:1.3rem;margin:24px 0">${w.d}</div>
      <div style="display:flex;align-items:center;justify-content:center;gap:8px;margin-bottom:4px">
        <button class="btn btn-ghost btn-sm" onclick="speakWord('${w.w}')">🔊 听发音</button>
        <span style="font-size:0.8rem;color:var(--text-muted)">提示：选择对应的英文单词</span>
      </div>
      <div id="quiz-options" style="display:grid;gap:10px;max-width:500px;margin:0 auto">
        ${options.map((o,idx)=>`<button class="btn btn-outline" style="padding:14px;font-size:1.05rem;text-align:left" onclick="checkQuiz('${o.i}','${o.w.replace(/'/g,"\\'")}',this)" data-key="${idx+1}"><span style="color:var(--text-muted);margin-right:8px">${String.fromCharCode(65+idx)}.</span> ${o.w}</button>`).join('')}
      </div>
      <div id="quiz-result" style="margin-top:16px"></div>
    </div>`;
}
function checkQuiz(selectedId, selectedWord, btn) {
  const w = quizWords[quizIdx];
  const correct = selectedId===w.i;
  const btns = document.querySelectorAll('#quiz-options button');
  btns.forEach(b=>b.disabled=true);
  if(correct){
    btn.classList.remove('btn-outline');btn.classList.add('btn-success');
    quizScore++;quizCombo++;
    updateWordProgress(w.i,true);
  } else {
    btn.classList.remove('btn-outline');btn.classList.add('btn-danger');
    quizCombo=0;
    btns.forEach(b=>{if(b.textContent.trim().startsWith(String.fromCharCode(65+btns.length))||b.onclick.toString().includes(w.i)){b.classList.remove('btn-outline');b.classList.add('btn-success');}});
    updateWordProgress(w.i,false);
  }
  updateDailyStreak();
  document.getElementById('quiz-result').innerHTML = correct
    ? `<div class="result-box correct">✅ 正确! ${w.w}${quizCombo>=5?` 🔥${quizCombo}连击!`:''}</div>`
    : `<div class="result-box wrong">❌ 正确答案: <strong>${w.w}</strong> - ${w.d}</div>`;
  setTimeout(()=>{quizIdx++;showQuiz();},1200);
}

// ===== SEARCH =====
let searchResults = [];
function renderSearch() {
  document.getElementById('search').innerHTML = `
    <h2>🔍 搜索词汇</h2>
    <input type="text" id="search-input" placeholder="输入英文单词或中文释义..." style="font-size:1.1rem;margin-bottom:16px" oninput="doSearch(this.value)" autofocus>
    <div id="search-results"></div>`;
  setTimeout(()=>document.getElementById('search-input')?.focus(),200);
}
function doSearch(q) {
  if(!q||q.length<1){document.getElementById('search-results').innerHTML='';return;}
  const qt = q.toLowerCase(); const results=[];
  for(let i=1;i<=22;i++){
    for(const w of getChapterWords(i)){
      if(w.w.toLowerCase().includes(qt)||w.d.includes(q)) results.push({...w,chapter:i});
    }
  }
  searchResults = results.slice(0,50);
  let html = `<p style="color:var(--text-secondary);margin-bottom:8px">找到 ${results.length} 个结果${results.length>50?' (显示前50个)':''}</p>`;
  searchResults.forEach((w,i)=>{
    html += `<div class="word-list-item" onclick="navigateToWord('${w.i}')">
      <span class="wl-english">${highlight(w.w,q)}</span>
      <span class="wl-chinese">${highlight(w.d,q)}</span>
      <span style="font-size:0.75rem;color:var(--text-muted)">第${w.chapter}章</span>
      <button class="btn btn-ghost btn-sm" onclick="event.stopPropagation();speakWord('${w.w}')">🔊</button>
    </div>`;
  });
  document.getElementById('search-results').innerHTML = html || '<div class="empty-state"><p>未找到匹配词汇</p></div>';
}
function highlight(text, query) {
  const re = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')})`,'gi');
  return text.replace(re,'<mark style="background:var(--warning);padding:1px 3px;border-radius:2px">$1</mark>');
}
function navigateToWord(wordId) {
  const w = findWordById(wordId);
  if(w){navigate('browse',w.chapter||currentChapter);setTimeout(()=>showWordDetail(wordId),500);}
}

// ===== SPEED DICTATION (批量听写) =====
function startSpeedDictation(chapter) {
  showToast('🚀 批量听写: 连续播放单词，一次性输入');
  renderDictation(chapter);
}

// ===== PROGRESS =====
function renderProgress() {
  const s = getTotalStats();
  const streak = getDailyStreak();
  let chRows='';
  for(let i=1;i<=22;i++){
    const pct=getChapterProgress(i);
    chRows+=`<div style="margin-bottom:12px">
      <div style="display:flex;justify-content:space-between;font-size:0.9rem;margin-bottom:4px"><span>第${i}章 ${getChapterTitle(i)}</span><span>${pct}%</span></div>
      <div class="progress-bar" style="height:8px"><div class="progress-fill" style="width:${pct}%;transition:width 0.5s"></div></div>
    </div>`;
  }
  document.getElementById('progress').innerHTML = `
    <h2>📊 学习进度</h2>
    <div class="stats-row">
      <div class="stat-card"><div class="stat-value">${s.total}</div><div class="stat-label">总词汇</div></div>
      <div class="stat-card"><div class="stat-value">${s.reviewed}</div><div class="stat-label">已学习</div></div>
      <div class="stat-card"><div class="stat-value">${s.mastered}</div><div class="stat-label">已掌握</div></div>
      <div class="stat-card"><div class="stat-value">${streak}🔥</div><div class="stat-label">连续打卡</div></div>
    </div>
    <div class="card"><h3>各章节完成度</h3>${chRows}</div>
    <div class="controls" style="margin-top:16px">
      <button class="btn btn-danger btn-sm" onclick="if(confirm('确定要重置所有学习进度吗？此操作不可恢复！')){localStorage.removeItem('ielts-progress');localStorage.removeItem('ielts-streak');localStorage.removeItem('ielts-last-study-date');navigate('progress');}">⚠️ 重置进度</button>
      <button class="btn btn-outline btn-sm" onclick="exportProgress()">📤 导出进度</button>
    </div>`;
}
function exportProgress() {
  const data = {progress:loadProgress(),streak:getDailyStreak(),lastDate:localStorage.getItem('ielts-last-study-date'),exportDate:new Date().toISOString()};
  const blob = new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
  const a = document.createElement('a');a.href=URL.createObjectURL(blob);a.download='ielts-progress-backup.json';a.click();
  showToast('📤 进度已导出');
}

// ===== UTILS =====
function showToast(msg) {
  const t = document.getElementById('toast') || document.createElement('div');
  t.id='toast';t.className='toast';t.textContent=msg;t.style.opacity='1';
  if(!t.parentNode) document.body.appendChild(t);
  clearTimeout(window._toastTimer);
  window._toastTimer = setTimeout(()=>{t.style.opacity='0';setTimeout(()=>t.remove(),300);},2500);
}
function randInt(min,max){return Math.floor(Math.random()*(max-min+1))+min;}

// ===== KEYBOARD SHORTCUTS =====
document.addEventListener('keydown',e=>{
  if(e.target.tagName==='INPUT'&&e.key!=='Escape') return;
  switch(e.key) {
    case '1':case '2':case '3':case '4':case '5':case '6':case '7':case '8':
      const pageMap={1:'dashboard',2:'browse',3:'flashcard',4:'dictation',5:'speaking',6:'spelling',7:'quiz',8:'search',9:'progress'};
      if(pageMap[parseInt(e.key)]) navigate(pageMap[parseInt(e.key)]);
      break;
    case 'ArrowLeft': if(currentPage==='flashcard') fcPrev(); break;
    case 'ArrowRight': if(currentPage==='flashcard'){window._fcIdx++;window._fcFlipped=false;showFlashcard();} break;
    case ' ': e.preventDefault(); if(currentPage==='flashcard') flipCard(); break;
    case 'd': navigate('dashboard'); break;
    case 'f': navigate('flashcard',currentChapter||1); break;
    case 'w': navigate('dictation',currentChapter||1); break;
    case 's': navigate('speaking',currentChapter||1); break;
    case 'p': navigate('spelling',currentChapter||1); break;
  }
});

// ===== THEME =====
function toggleTheme() {
  darkMode = !darkMode;
  document.documentElement.setAttribute('data-theme',darkMode?'dark':'light');
  localStorage.setItem('ielts-dark-mode',darkMode);
  document.getElementById('themeToggle').textContent = darkMode?'☀️':'🌙';
}

// ===== INIT =====
function init() {
  document.documentElement.setAttribute('data-theme',darkMode?'dark':'light');
  document.getElementById('themeToggle').textContent = darkMode?'☀️':'🌙';
  initSpeech();
  const page = window.location.hash.replace('#','') || 'dashboard';
  navigate(page);
}
document.addEventListener('DOMContentLoaded', init);
"""

HTML_HEAD = """<!DOCTYPE html>
<html lang="zh-CN" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>雅思词汇真经 - 智能复习系统</title>
<style>
"""

HTML_MID = """</style>
</head>
<body>
<nav>
<div class="logo" onclick="navigate('dashboard')">📖 雅思词汇真经</div>
<button class="nav-btn active" data-page="dashboard" onclick="navigate('dashboard')">🏠</button>
<button class="nav-btn" data-page="browse" onclick="navigate('browse',1)">📚</button>
<button class="nav-btn" data-page="flashcard" onclick="navigate('flashcard',1)">🎴</button>
<button class="nav-btn" data-page="dictation" onclick="navigate('dictation',1)">✍️ 听写</button>
<button class="nav-btn" data-page="speaking" onclick="navigate('speaking',1)">🎤 口语</button>
<button class="nav-btn" data-page="spelling" onclick="navigate('spelling',1)">📝 拼写</button>
<button class="nav-btn" data-page="quiz" onclick="navigate('quiz',1)">📋 测试</button>
<button class="nav-btn" data-page="search" onclick="navigate('search')">🔍</button>
<button class="nav-btn" data-page="progress" onclick="navigate('progress')">📊</button>
<button id="themeToggle" onclick="toggleTheme()" style="margin-left:auto">🌙</button>
</nav>
<main>
<div class="page active" id="page-dashboard"><div id="dashboard"></div></div>
<div class="page" id="page-browse"><div id="browse"></div></div>
<div class="page" id="page-flashcard"><div id="flashcard"></div></div>
<div class="page" id="page-dictation"><div id="dictation"></div></div>
<div class="page" id="page-speaking"><div id="speaking"></div></div>
<div class="page" id="page-spelling"><div id="spelling"></div></div>
<div class="page" id="page-quiz"><div id="quiz"></div></div>
<div class="page" id="page-search"><div id="search"></div></div>
<div class="page" id="page-progress"><div id="progress"></div></div>
</main>
<script>
"""

HTML_TAIL = """
</script>
</body>
</html>"""

# Build the complete HTML
html = HTML_HEAD + CSS + HTML_MID + vocab_js + JS + HTML_TAIL

output_path = "/Users/wangxiaoya/Downloads/codex/ielts-vocab.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

# Also create a symlink/copy to a user-friendly location
size_kb = os.path.getsize(output_path) / 1024
print(f"✅ Built ielts-vocab.html ({size_kb:.0f} KB)")
print(f"   Path: {output_path}")
