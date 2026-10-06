(() => {
 'use strict';
 const dialog=document.createElement('dialog');dialog.className='parent-gate';
 dialog.innerHTML='<h2>Grown-up check</h2><p>You are leaving the game for another page. Please ask a grown-up to continue.</p><form method="dialog"><label for="gate-answer" id="gate-question"></label><input id="gate-answer" type="number" inputmode="numeric" autocomplete="off" required><p id="gate-error" role="status"></p><button type="submit">Continue</button><button type="button" id="gate-cancel">Stay in game</button></form>';
 document.body.append(dialog);let pending=null,answer=0;const allowed=new WeakSet();
 document.addEventListener('click',e=>{const a=e.target.closest('a[href]');if(!a||allowed.has(a)||a.getAttribute('href').startsWith('#'))return;const u=new URL(a.href,location.href);if(u.pathname.startsWith(new URL('./',location.href).pathname)&&u.origin===location.origin)return;e.preventDefault();e.stopImmediatePropagation();pending=a;const x=12+Math.floor(Math.random()*8),y=7+Math.floor(Math.random()*5);answer=x*y;dialog.querySelector('#gate-question').textContent='Grown-up: what is '+x+' × '+y+'?';dialog.querySelector('input').value='';dialog.querySelector('#gate-error').textContent='';dialog.showModal();},true);
 dialog.querySelector('form').addEventListener('submit',e=>{e.preventDefault();if(Number(dialog.querySelector('input').value)!==answer){dialog.querySelector('#gate-error').textContent='Please ask a grown-up to try again.';return}dialog.close();if(pending){const a=pending;allowed.add(a);a.click();allowed.delete(a);pending=null}});
 dialog.querySelector('#gate-cancel').addEventListener('click',()=>{dialog.close();pending=null});
})();
