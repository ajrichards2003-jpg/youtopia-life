import {Capacitor} from '@capacitor/core';import {Browser} from '@capacitor/browser';import {App} from '@capacitor/app';
if(Capacitor.isNativePlatform()){
 document.addEventListener('click',async e=>{const a=e.target.closest('a[href]');if(!a)return;const url=new URL(a.href);if(url.protocol==='https:'&&url.origin!==location.origin){e.preventDefault();await Browser.open({url:url.href});}});
 App.addListener('backButton',()=>{const dialogs=Array.from(document.querySelectorAll('dialog[open]')),dialog=dialogs.pop();if(dialog){dialog.close();return;}if(location.pathname.endsWith('privacy.html'))location.href='index.html';else App.exitApp();});
 const offline=document.getElementById('enable-offline'),message=document.getElementById('offline-message');if(offline){offline.hidden=true;message.textContent='All 90 questions are bundled for offline play on this device. External sources need internet.';}
}
