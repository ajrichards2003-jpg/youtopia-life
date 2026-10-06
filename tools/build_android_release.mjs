import {access} from 'node:fs/promises';
import {spawnSync} from 'node:child_process';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const app=process.argv[2];
if(!['mobile','mobile-ascent'].includes(app)){console.error('Usage: node tools/build_android_release.mjs mobile|mobile-ascent');process.exit(1)}
const names=['YOUTOPIA_UPLOAD_STORE_FILE','YOUTOPIA_UPLOAD_STORE_PASSWORD','YOUTOPIA_UPLOAD_KEY_ALIAS','YOUTOPIA_UPLOAD_KEY_PASSWORD'];
const missing=names.filter(name=>!process.env[name]);
if(missing.length){console.error('Signing configuration required: '+missing.join(', '));process.exit(1)}
if(!path.isAbsolute(process.env.YOUTOPIA_UPLOAD_STORE_FILE)){console.error('Use an absolute keystore path.');process.exit(1)}
try{await access(process.env.YOUTOPIA_UPLOAD_STORE_FILE)}catch{console.error('Upload keystore file is unavailable.');process.exit(1)}
const run=(cmd,args,cwd)=>{const r=spawnSync(cmd,args,{cwd,stdio:'inherit',shell:process.platform==='win32',env:{...process.env,YOUTOPIA_REQUIRE_SIGNING:'true'}});if(r.error){console.error('Build tool could not start. Check your installed tooling.');process.exit(1)}if(r.status!==0)process.exit(r.status||1)};
run(process.platform==='win32'?'npm.cmd':'npm',['run','sync'],path.join(root,app));
run(process.platform==='win32'?'gradlew.bat':'./gradlew',['bundleRelease','assembleRelease','--no-daemon','--no-configuration-cache'],path.join(root,app,'android'));
console.log('Release build complete. Verify certificate, package identity and version before upload.');
