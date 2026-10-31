const fs=require('fs'),path=require('path');
const L='/tmp/claude-0/-home-claude/46d9fd52-f990-59ce-b851-a0f7204303d3/scratchpad/lh/node_modules/';
const csso=require(L+'csso'),{minify}=require(L+'terser');
(async()=>{
const root=process.argv[2];let saved=0;
function walk(d){return fs.readdirSync(d,{withFileTypes:true}).flatMap(e=>e.name.startsWith('.')||e.name.startsWith('_')||e.name==='img'||e.name==='fonts'||e.name==='images'?[]:e.isDirectory()?walk(path.join(d,e.name)):e.name.endsWith('.html')?[path.join(d,e.name)]:[])}
for(const f of walk(root)){
 let h=fs.readFileSync(f,'utf8'),o=h.length;
 h=h.replace(/<style>([\s\S]*?)<\/style>/g,(m,c)=>'<style>'+csso.minify(c).css+'</style>');
 const re=/<script>([\s\S]*?)<\/script>/g;let out='',last=0,m;
 while((m=re.exec(h))){out+=h.slice(last,m.index);const r=await minify(m[1],{compress:true,mangle:true});if(r.error||!r.code)throw new Error(f);out+='<script>'+r.code+'</script>';last=re.lastIndex}
 h=out+h.slice(last);
 fs.writeFileSync(f,h);saved+=o-h.length}
console.log('minify: ušetrené',Math.round(saved/1024),'kB');
})();
