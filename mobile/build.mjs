import {cp,mkdir,readFile,writeFile,rm,readdir} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {build} from 'esbuild';
const here=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(here,'..'),out=path.join(here,'www');
await rm(out,{recursive:true,force:true});await mkdir(out,{recursive:true});await cp(path.join(root,'app'),out,{recursive:true});
const images=['youtopia-mark-transparent.png','youtopia-bronze-wing-logo.jpg','dire-wolf-editorial.webp','red-light-hero.webp','iherb/training-campaign.webp','ultrahuman/sleep-campaign.webp','editorial/algae-nutrition.webp','editorial/circulation-lab.webp','experience-polish.css'];
for(const name of images){const dest=path.join(out,'assets',name);await mkdir(path.dirname(dest),{recursive:true});await cp(path.join(root,'assets',name),dest);}
await build({entryPoints:[path.join(here,'native-runtime.js')],outfile:path.join(out,'native-runtime.js'),bundle:true,format:'iife',minify:true});
async function inject(dir){for(const entry of await readdir(dir,{withFileTypes:true})){const p=path.join(dir,entry.name);if(entry.isDirectory())await inject(p);else if(entry.name.endsWith('.html')){const script=path.relative(dir,path.join(out,'native-runtime.js')).split(path.sep).join('/');await writeFile(p,(await readFile(p,'utf8')).replace('</head>',`<script defer src="${script}"></script></head>`));}}}
await inject(out);console.log('Packaged Youtopia Life: library, saved reading, Ascent, memory, breathing and privacy.');
