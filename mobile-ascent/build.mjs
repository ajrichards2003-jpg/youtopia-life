import {cp,mkdir,readFile,writeFile,rm} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {build} from 'esbuild';
const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,'..'),source=path.join(root,'ascent-app'),out=path.join(here,'www');
// The standalone edition owns its bank and engine; do not overwrite it from the paused main app.
await rm(out,{recursive:true,force:true});await mkdir(out,{recursive:true});await cp(source,out,{recursive:true});
await mkdir(path.join(out,'assets'),{recursive:true});
for(const name of ['youtopia-mark-transparent.png','experience-polish.css'])await cp(path.join(root,'assets',name),path.join(out,'assets',name));
await build({entryPoints:[path.join(here,'native-runtime.js')],outfile:path.join(out,'native-runtime.js'),bundle:true,format:'iife',minify:true});
for(const name of ['index.html','privacy.html']){const p=path.join(out,name);await writeFile(p,(await readFile(p,'utf8')).replace('</head>','<script defer src="native-runtime.js"></script></head>'));}
console.log('Packaged Youtopia Ascent with local questions, assets and native link handling.');
