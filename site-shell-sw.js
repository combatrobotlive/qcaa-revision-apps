const CACHE='revision-apps-site-v2-shell-2026-09';
self.addEventListener('install',event=>event.waitUntil(self.skipWaiting()));
self.addEventListener('activate',event=>event.waitUntil(self.clients.claim()));
self.addEventListener('fetch',event=>{
  const req=event.request;
  if(req.method!=='GET'||req.mode!=='navigate') return;
  const url=new URL(req.url);
  if(url.origin!==self.location.origin) return;
  const name=decodeURIComponent(url.pathname.split('/').pop()||'');
  if(!/_Standalone(?:\([^)]*\))?\.html$/i.test(name)) return;
  event.respondWith((async()=>{
    try{
      const res=await fetch(req);
      const type=res.headers.get('content-type')||'';
      if(!res.ok||!type.includes('text/html')) return res;
      let text=await res.text();
      if(!text.includes('site-consistency.js')){
        const tag='<script src="./site-consistency.js" defer></script>';
        if(/<\/body>/i.test(text)) text=text.replace(/<\/body>/i,tag+'</body>');
        else text+=tag;
      }
      const headers=new Headers(res.headers);headers.delete('content-length');headers.set('x-revision-apps-shell','v2');
      return new Response(text,{status:res.status,statusText:res.statusText,headers});
    }catch(err){return fetch(req)}
  })());
});
