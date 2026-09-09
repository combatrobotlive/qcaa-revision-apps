(()=>{
'use strict';
if(window.__REV_APPS_SITE_V2__) return;
window.__REV_APPS_SITE_V2__=true;
const d=document;
const filename=decodeURIComponent(location.pathname.split('/').pop()||'');
const isInter=/^(NSW_|VCE_|WA_|ACT_|TAS_|SACE_|NTCET_)/i.test(filename);
const scopeLabel=isInter?'Interstate Engineering':'QCAA revision app';

const css=`
#revapps-v2-shell{position:fixed;right:14px;bottom:14px;z-index:2147483000;font-family:Inter,Arial,\"Segoe UI\",sans-serif;color:#18313e}
#revapps-v2-shell *{box-sizing:border-box}
#revapps-v2-shell .rv2-main{display:flex;gap:5px;align-items:center;padding:6px;background:rgba(255,255,255,.97);border:1px solid #cbd9df;border-radius:999px;box-shadow:0 9px 28px rgba(10,40,55,.20);backdrop-filter:blur(8px)}
#revapps-v2-shell a,#revapps-v2-shell button{appearance:none;border:0;background:transparent;color:#244653;text-decoration:none;border-radius:999px;padding:8px 10px;font:800 10px/1.1 Inter,Arial,sans-serif;cursor:pointer;white-space:nowrap}
#revapps-v2-shell a:hover,#revapps-v2-shell button:hover,#revapps-v2-shell a:focus-visible,#revapps-v2-shell button:focus-visible{background:#eaf3f5;outline:2px solid #0d7484;outline-offset:1px}
#revapps-v2-shell .rv2-home{background:#173e58;color:white}
#revapps-v2-shell .rv2-home:hover,#revapps-v2-shell .rv2-home:focus-visible{background:#245d7b;color:white}
#revapps-v2-shell .rv2-badge{padding:0 7px;font-size:9px;color:#63757e;font-weight:750}
#revapps-v2-shell .rv2-panel{position:absolute;right:0;bottom:54px;width:min(390px,calc(100vw - 28px));padding:14px;background:#fff;border:1px solid #cbd9df;border-radius:14px;box-shadow:0 15px 42px rgba(10,40,55,.22)}
#revapps-v2-shell .rv2-panel[hidden]{display:none}
#revapps-v2-shell .rv2-panel h3{margin:0 0 7px;font:900 15px/1.2 Inter,Arial,sans-serif;color:#173e58}
#revapps-v2-shell .rv2-panel p{margin:6px 0;font:400 10.5px/1.45 Inter,Arial,sans-serif;color:#60747d}
#revapps-v2-shell .rv2-actions{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}
#revapps-v2-shell .rv2-actions button,#revapps-v2-shell .rv2-actions label{border:1px solid #c8d7dd;background:#f9fbfc;color:#244653;border-radius:8px;padding:8px 9px;font:800 10px/1 Inter,Arial,sans-serif;cursor:pointer}
#revapps-v2-shell .rv2-actions button:hover,#revapps-v2-shell .rv2-actions label:hover{background:#edf5f6}
#revapps-v2-shell .rv2-small{font-size:9px!important;color:#74868d!important}
#revapps-v2-toast{position:fixed;left:50%;bottom:78px;transform:translateX(-50%);z-index:2147483640;background:#173e58;color:#fff;border-radius:9px;padding:9px 12px;font:800 10px/1.25 Inter,Arial,sans-serif;box-shadow:0 8px 24px #0003}
#revapps-v2-toast[hidden]{display:none}
:where(button,a,input,select,textarea):focus-visible{outline:3px solid #0d8190!important;outline-offset:2px!important}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{scroll-behavior:auto!important;animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}
@media(max-width:640px){#revapps-v2-shell{right:8px;bottom:8px;left:8px}#revapps-v2-shell .rv2-main{justify-content:center}#revapps-v2-shell .rv2-badge{display:none}#revapps-v2-shell a,#revapps-v2-shell button{padding:8px 8px;font-size:9.5px}}
@media print{#revapps-v2-shell,#revapps-v2-toast{display:none!important}}
`;
const style=d.createElement('style');style.id='revapps-v2-style';style.textContent=css;d.head.appendChild(style);

// Basic accessibility consistency without altering app behaviour.
d.documentElement.lang=d.documentElement.lang||'en';
d.querySelectorAll('button').forEach(b=>{if(!b.getAttribute('aria-label')){const t=(b.textContent||'').trim().replace(/\\s+/g,' ');if(t)b.setAttribute('aria-label',t.slice(0,120));}});
d.querySelectorAll('a').forEach(a=>{if(a.target==='_blank'&&!/noopener/i.test(a.rel||''))a.rel=((a.rel||'')+' noopener').trim();});

const shell=d.createElement('div');shell.id='revapps-v2-shell';
shell.innerHTML=`<div class="rv2-panel" id="rv2-panel" hidden>
  <h3>Revision Apps · website tools</h3>
  <p><b>${scopeLabel}</b><br>Collection maintenance pass: September 2026. The individual app version and subject-specific syllabus notes remain unchanged.</p>
  <p>Progress is stored in this browser by the individual apps. The backup below exports <b>all local progress/settings for this website</b> in one JSON file.</p>
  <div class="rv2-actions"><button type="button" id="rv2-export">Export site progress</button><label for="rv2-import">Import site progress</label><input id="rv2-import" type="file" accept="application/json" hidden></div>
  <p class="rv2-small">Created by Daniel Kerrison, Engineering Teacher, Southport State High School · AI-assisted development with ChattyJeeps (ChatGPT by OpenAI) · Independent resource; not produced or endorsed by the relevant curriculum authority or school.</p>
</div>
<div class="rv2-main"><a class="rv2-home" href="./index.html" aria-label="Back to all revision apps">← All apps</a><span class="rv2-badge">Site v2 · Sep 2026</span><button type="button" id="rv2-tools" aria-expanded="false" aria-controls="rv2-panel">Tools</button></div>`;
d.body.appendChild(shell);

const toast=d.createElement('div');toast.id='revapps-v2-toast';toast.hidden=true;d.body.appendChild(toast);
let toastTimer;
function say(msg){toast.textContent=msg;toast.hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>toast.hidden=true,1800)}
const panel=shell.querySelector('#rv2-panel'),tools=shell.querySelector('#rv2-tools');
tools.addEventListener('click',()=>{const open=panel.hidden;panel.hidden=!open;tools.setAttribute('aria-expanded',String(open));});
d.addEventListener('keydown',e=>{if(e.key==='Escape'&&!panel.hidden){panel.hidden=true;tools.setAttribute('aria-expanded','false');tools.focus();}});

shell.querySelector('#rv2-export').addEventListener('click',()=>{
  try{
    const data={format:'SeniorRevisionAppsSiteProgress',version:2,exported:new Date().toISOString(),origin:location.origin,localStorage:{}};
    for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);data.localStorage[k]=localStorage.getItem(k)}
    const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
    const a=d.createElement('a');a.href=URL.createObjectURL(blob);a.download='Senior_Revision_Apps_progress_backup.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),500);
    say(`Exported ${Object.keys(data.localStorage).length} saved site keys`);
  }catch(err){say('Could not export progress in this browser');}
});
shell.querySelector('#rv2-import').addEventListener('change',e=>{
  const f=e.target.files&&e.target.files[0];if(!f)return;
  const r=new FileReader();r.onload=()=>{try{const data=JSON.parse(r.result);if(data.format!=='SeniorRevisionAppsSiteProgress'||!data.localStorage||typeof data.localStorage!=='object')throw new Error('format');let n=0;Object.entries(data.localStorage).forEach(([k,v])=>{localStorage.setItem(k,String(v));n++});say(`Imported ${n} saved site keys · reload app to refresh`);}catch(err){say('That is not a valid site progress backup');}e.target.value='';};r.readAsText(f);
});
})();
