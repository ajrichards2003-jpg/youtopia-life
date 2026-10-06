import {Capacitor} from '@capacitor/core';import {Browser} from '@capacitor/browser';import {App} from '@capacitor/app';
if(Capacitor.isNativePlatform()){
 document.addEventListener('click',async e=>{const a=e.target.closest('a[href]');if(!a)return;const url=new URL(a.href);if(url.protocol==='https:'&&url.origin!==location.origin){e.preventDefault();await Browser.open({url:url.href});}});
 App.addListener('appStateChange',({isActive})=>{if(!isActive)document.dispatchEvent(new Event('youtopia-pause'));});
 App.addListener('backButton',()=>{const dialog=Array.from(document.querySelectorAll('dialog[open]')).pop();if(dialog){dialog.close();return;}if(location.pathname.endsWith('privacy.html')){location.href='index.html';return;}const pause=document.getElementById('pause'),resume=document.getElementById('resume');if(document.getElementById('pause-screen')?.hidden===false){document.getElementById('quit')?.click();return;}if(pause&&!pause.disabled){document.dispatchEvent(new Event('youtopia-pause'));resume?.focus();return;}App.exitApp();});
 const offline=document.getElementById('enable-offline'),message=document.getElementById('offline-message');if(offline){offline.hidden=true;message.textContent='The game is bundled for offline play on this device.';}
}
