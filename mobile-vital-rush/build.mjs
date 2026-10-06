import {cp,mkdir,readFile,writeFile,rm} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';import path from 'node:path';import {build} from 'esbuild';
const here=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(here,'..'),source=path.join(root,'vital-rush'),out=path.join(here,'www');
await rm(out,{recursive:true,force:true});await mkdir(out,{recursive:true});
for(const name of ['index.html','style.css','engine.js','game.js','offline.js','family.js','privacy.html','manifest.webmanifest','icon-192.png','icon-512.png'])await cp(path.join(source,name),path.join(out,name));
await build({entryPoints:[path.join(here,'native-runtime.js')],outfile:path.join(out,'native-runtime.js'),bundle:true,format:'iife',minify:true});
for(const name of ['index.html','privacy.html']){const p=path.join(out,name);await writeFile(p,(await readFile(p,'utf8')).replace('</head>','<script defer src="native-runtime.js"></script></head>'));}
console.log('Packaged Vital Rush with local gameplay, privacy, family links and lifecycle controls.');
