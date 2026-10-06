(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const RUN_KEY = 'youtopia-ascent-run-v2';
  const BEST_KEY = 'youtopia-ascent-best-v1';
  const ranks = ['Explorer', 'Investigator', 'Evidence Navigator', 'Frontier Thinker', 'Summit Mind'];
  const rank = n => n < 3 ? 'Starting the climb' : ranks[Math.min(4, Math.floor(n / 3) - 1)];
  let bank = [], state = null;
  const read = key => { try { return JSON.parse(localStorage.getItem(key) || 'null'); } catch { return null; } };
  const best = () => Math.max(0, Math.min(15, Number(read(BEST_KEY)) || 0));
  const write = (key, data) => { try { localStorage.setItem(key, JSON.stringify(data)); } catch { $('status').textContent = 'Device storage is unavailable. This run stays in this session.'; } };
  const remove = key => { try { localStorage.removeItem(key); } catch {} };
  const shuffle = list => { const a = [...list]; for (let j = a.length - 1; j > 0; j--) { const k = Math.floor(Math.random() * (j + 1)); [a[j], a[k]] = [a[k], a[j]]; } return a; };
  const q = () => bank.find(x => x.id === state.ids[state.i]);
  const persist = () => { if (state) write(RUN_KEY, state); };
  const valid = s => s && s.version === 2 && ['challenge', 'practice'].includes(s.mode) && Array.isArray(s.ids) && s.ids.length === (s.mode === 'challenge' ? 15 : bank.length) && new Set(s.ids).size === s.ids.length && s.ids.every(id => bank.some(x => x.id === id)) && Number.isInteger(s.i) && s.i >= 0 && s.i < s.ids.length && Array.isArray(s.order) && [...s.order].sort().join() === '0,1,2,3' && Array.isArray(s.hidden) && s.hidden.every(x => Number.isInteger(x) && x >= 0 && x < 4) && ['question','feedback'].includes(s.phase) && Number.isInteger(s.selected) && s.selected >= -1 && s.selected < 4 && (s.phase !== 'feedback' || s.selected >= 0) && Number.isInteger(s.score) && s.score >= 0 && s.score <= s.ids.length && Number.isInteger(s.safe) && s.safe >= 0 && s.safe <= 15 && s.used && Array.isArray(s.review) && s.review.every(x => bank.some(b => b.id === x.id));
  function refreshHome() {
    const resume = read(RUN_KEY);
    $('resume').hidden = !valid(resume);
    $('intro-best').textContent = 'Personal best: ' + rank(best()) + ' · ' + best() + '/15';
  }
  function ladder() {
    const total = state?.ids.length || 15;
    $('rungs').replaceChildren(...Array.from({ length: 15 }, (_, n) => {
      const li = document.createElement('li');
      li.className = 'rung' + ((n + 1) % 3 === 0 ? ' checkpoint' : '') + (state?.mode === 'challenge' && n === state.i ? ' current' : '') + (state?.mode === 'challenge' && n < state.score ? ' passed' : '');
      const number = document.createElement('span'); number.className = 'num'; number.textContent = String(n + 1).padStart(2, '0');
      const label = document.createElement('span'); label.textContent = (n + 1) % 3 === 0 ? ranks[Math.floor(n / 3)] : 'Step ' + (n + 1);
      li.append(number, label); return li;
    }).reverse());
    $('score').textContent = (state?.score || 0) + '/' + total;
    $('safe').textContent = state?.mode === 'practice' ? 'Practice · no rank' : rank(state?.safe || 0);
  }
  function controls() {
    const locked = state.phase !== 'question';
    for (const id of ['narrow', 'clue', 'chance']) $(id).disabled = locked || !!state.used[id];
    $('bank').disabled = locked; $('bank').textContent = state.mode === 'practice' ? 'Finish practice' : 'Bank my rank';
    $('lock').disabled = locked || state.selected < 0;
    $('chance').classList.toggle('armed', !!state.chanceArmed);
  }
  function feedback() {
    const correct = state.order[state.selected] === q().correct;
    [...$('answers').children].forEach((b, n) => { b.disabled = true; b.classList.toggle('correct', state.order[n] === q().correct); b.classList.toggle('wrong', n === state.selected && !correct); });
    $('feedback').hidden = false;
    $('verdict').textContent = correct ? 'Correct. Keep climbing.' : state.mode === 'practice' ? 'A new thing to learn.' : 'Not this time. Here’s the evidence.';
    $('explanation').textContent = q().explanation;
    $('source').href = q().source; $('source').textContent = q().sourceLabel + ' ↗';
    $('next').textContent = !correct && state.mode === 'challenge' ? 'See my result' : state.i === state.ids.length - 1 ? 'Complete this run' : 'Next question';
    $('next').focus();
  }
  function draw() {
    $('intro').hidden = true; $('result').hidden = true; $('play').hidden = false;
    $('level').textContent = (state.mode === 'practice' ? 'PRACTICE' : 'ASCENT') + ' · ' + (state.i + 1) + '/' + state.ids.length;
    $('topic').textContent = q().topic + ' · ' + ['Foundations', 'Discovery', 'Deep thinking'][q().tier - 1];
    $('question').textContent = q().text;
    $('answers').replaceChildren(...state.order.map((original, n) => {
      const b = document.createElement('button'); b.className = 'answer'; b.type = 'button';
      b.setAttribute('aria-pressed', String(n === state.selected));
      const letter = document.createElement('span'); letter.className = 'letter'; letter.textContent = 'ABCD'[n];
      const answer = document.createElement('span'); answer.textContent = q().answers[original]; b.append(letter, answer);
      b.classList.toggle('selected', n === state.selected); b.disabled = state.hidden.includes(n); b.classList.toggle('eliminated', state.hidden.includes(n));
      b.addEventListener('click', () => { if (state.phase !== 'question' || state.hidden.includes(n)) return; state.selected = n; [...$('answers').children].forEach((x, j) => { x.classList.toggle('selected', j === n); x.setAttribute('aria-pressed', String(j === n)); }); controls(); persist(); });
      return b;
    }));
    $('feedback').hidden = true; $('hint').textContent = state.hint || ''; $('status').textContent = '';
    controls(); ladder();
    if (state.phase === 'feedback') feedback(); else $('question').focus();
  }
  function nextQuestion() { state.phase = 'question'; state.order = shuffle([0,1,2,3]); state.selected = -1; state.hidden = []; state.chanceArmed = false; state.hint = ''; persist(); draw(); }
  function start(mode) {
    const ids = mode === 'practice' ? [...bank].sort((a,b) => a.tier - b.tier).map(x => x.id) : [1,2,3].flatMap(t => shuffle(bank.filter(x => x.tier === t)).slice(0,5).map(x => x.id));
    state = { version:2, mode, ids, i:0, score:0, safe:0, order:[], selected:-1, hidden:[], used:{}, chanceArmed:false, phase:'question', review:[], hint:'' };
    nextQuestion();
  }
  function finish(reason) {
    const run = state;
    remove(RUN_KEY); $('play').hidden = true; $('intro').hidden = true; $('result').hidden = false;
    $('result-label').textContent = run.mode === 'practice' ? 'PRACTICE COMPLETE' : reason === 'win' ? 'ASCENT COMPLETE' : reason === 'bank' ? 'RANK BANKED' : 'CHECKPOINT SAVED';
    $('result-title').textContent = run.mode === 'practice' ? 'Keep the questions coming.' : reason === 'win' ? 'Summit Mind. Curiosity elevated.' : 'Every answer is a new starting point.';
    $('result-score').textContent = run.mode === 'practice' ? run.score + ' correct · ' + run.review.length + ' answered' : rank(run.score) + ' · ' + run.score + '/15';
    $('result-copy').textContent = run.mode === 'practice' ? 'Practice teaches every answer. It does not change your Ascent rank.' : reason === 'miss' ? 'You keep your last protected checkpoint. Your personal best records the highest step you have reached.' : 'Your progress is saved on this device. Another climb brings a fresh question selection.';
    $('best').textContent = 'Personal best: ' + rank(best()) + ' · ' + best() + '/15';
    $('review-list').replaceChildren(...run.review.filter(x => !x.correct).map(x => {
      const item = bank.find(b => b.id === x.id), article = document.createElement('article'); article.className = 'review-card';
      const h = document.createElement('h3'); h.textContent = item.text;
      const p = document.createElement('p'); p.textContent = 'Answer: ' + item.answers[item.correct] + '. ' + item.explanation;
      const a = document.createElement('a'); a.href = item.source; a.target = '_blank'; a.rel = 'noopener'; a.textContent = 'Follow the source'; article.append(h,p,a); return article;
    }));
    $('review-heading').hidden = !$('review-list').children.length; $('result-title').focus(); state = null; refreshHome();
  }
  $('start').addEventListener('click', () => start('challenge'));
  $('practice').addEventListener('click', () => start('practice'));
  $('restart').addEventListener('click', () => start('challenge'));
  $('home').addEventListener('click', () => { $('result').hidden = true; $('intro').hidden = false; refreshHome(); $('start').focus(); });
  $('resume').addEventListener('click', () => { const s = read(RUN_KEY); if (valid(s)) { state = s; draw(); } else { remove(RUN_KEY); refreshHome(); } });
  $('bank').addEventListener('click', () => { if (state.phase === 'question') finish('bank'); });
  $('lock').addEventListener('click', () => {
    if (state.phase !== 'question' || state.selected < 0) return;
    const correct = state.order[state.selected] === q().correct;
    if (!correct && state.chanceArmed) { state.chanceArmed = false; state.hidden.push(state.selected); state.selected = -1; state.hint = 'Second chance used. That answer is out. Choose again.'; persist(); draw(); return; }
    state.phase = 'feedback'; state.review.push({id:q().id, correct});
    if (correct) { state.score++; if (state.mode === 'challenge') { if (state.score % 3 === 0) state.safe = state.score; write(BEST_KEY, Math.max(best(), state.score)); } }
    else if (state.mode === 'challenge') state.score = state.safe;
    persist(); controls(); ladder(); feedback();
  });
  $('next').addEventListener('click', () => { if (state.phase !== 'feedback') return; const correct = state.order[state.selected] === q().correct; if (!correct && state.mode === 'challenge') return finish('miss'); if (state.i === state.ids.length - 1) return finish('win'); state.i++; nextQuestion(); });
  $('narrow').addEventListener('click', () => { if (state.phase !== 'question' || state.used.narrow) return; state.used.narrow = true; const wrong = shuffle(state.order.map((original,n) => ({original,n})).filter(x => x.original !== q().correct && !state.hidden.includes(x.n))); wrong.slice(0,Math.max(0,2-state.hidden.length)).forEach(x => state.hidden.push(x.n)); if (state.hidden.includes(state.selected)) state.selected = -1; state.hint = 'Two choices remain. The decision is yours.'; persist(); draw(); });
  $('clue').addEventListener('click', () => { if (state.phase !== 'question' || state.used.clue) return; state.used.clue = true; state.hint = q().clue; persist(); draw(); });
  $('chance').addEventListener('click', () => { if (state.phase !== 'question' || state.used.chance) return; state.used.chance = true; state.chanceArmed = true; state.hint = 'Second chance armed for this question.'; persist(); draw(); });
  for (const id of ['start','practice','resume']) $(id).disabled = true;
  $('status').textContent = 'Preparing your questions…'; ladder();
  fetch('questions.json').then(r => { if (!r.ok) throw Error(); return r.json(); }).then(data => {
    if (!Array.isArray(data) || data.length < 15 || new Set(data.map(x=>x.id)).size !== data.length || data.some(x => ![1,2,3].includes(x.tier) || !Array.isArray(x.answers) || x.answers.length !== 4 || !Number.isInteger(x.correct) || x.correct<0 || x.correct>3 || !x.source.startsWith('https://')) || [1,2,3].some(t => data.filter(x=>x.tier===t).length<5)) throw Error();
    bank = data; $('status').textContent = ''; for (const id of ['start','practice','resume']) $(id).disabled = false; refreshHome();
  }).catch(() => { $('status').textContent = 'The question bank could not load. Refresh while connected to prepare the game.'; });
})();
