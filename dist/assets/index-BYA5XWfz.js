(function(){const e=document.createElement("link").relList;if(e&&e.supports&&e.supports("modulepreload"))return;for(const a of document.querySelectorAll('link[rel="modulepreload"]'))n(a);new MutationObserver(a=>{for(const r of a)if(r.type==="childList")for(const o of r.addedNodes)o.tagName==="LINK"&&o.rel==="modulepreload"&&n(o)}).observe(document,{childList:!0,subtree:!0});function t(a){const r={};return a.integrity&&(r.integrity=a.integrity),a.referrerPolicy&&(r.referrerPolicy=a.referrerPolicy),a.crossOrigin==="use-credentials"?r.credentials="include":a.crossOrigin==="anonymous"?r.credentials="omit":r.credentials="same-origin",r}function n(a){if(a.ep)return;a.ep=!0;const r=t(a);fetch(a.href,r)}})();const f={champions_league:["Real Madrid","Manchester City","Bayern Munich","PSG","Barcelona","Liverpool","Chelsea","Juventus","Inter Milan","Milan","Dortmund","Atletico Madrid","Porto","Benfica","Ajax"],ligue1:["PSG","Marseille","Lyon","Lille","Monaco","Rennes","Nice","Lens","Strasbourg","Montpellier"],premier_league:["Manchester City","Liverpool","Arsenal","Manchester United","Chelsea","Tottenham","Newcastle","West Ham","Brighton","Aston Villa"],liga:["Real Madrid","Barcelona","Atletico Madrid","Sevilla","Real Sociedad","Villarreal","Athletic Bilbao","Valencia","Betis","Osasuna"],world_cup:["France","Brazil","Argentina","England","Spain","Germany","Portugal","Netherlands","Belgium","Croatia"],euro:["France","England","Spain","Germany","Portugal","Netherlands","Belgium","Croatia","Italy","Denmark"],copa_america:["Brazil","Argentina","Uruguay","Colombia","Chile","Peru","Paraguay","Ecuador","Venezuela","Bolivia"]};function b(s,e){const t=(h,L)=>Math.floor(Math.random()*(L-h+1))+h,n=(s.precision_passes+s.possession_moyenne)/2,a=(e.precision_passes+e.possession_moyenne)/2,r=n/a,o=Math.min(65,Math.max(35,Math.round(50*r))),i=Math.min(70,Math.max(30,o+t(-5,5))),c=100-i,l=t(8,18)*(i/50),d=t(8,18)*(c/50),p=Math.round(l*.4),m=Math.round(d*.4),y=Math.round(p*.25),M=Math.round(m*.25),v=t(400,600),S=t(400,600),q=Math.round(v*(i/50)),E=Math.round(S*(c/50));return{buts_equipe1:y,buts_equipe2:M,possession_equipe1:i,possession_equipe2:c,tirs_equipe1:Math.round(l),tirs_equipe2:Math.round(d),tirs_cadres_equipe1:p,tirs_cadres_equipe2:m,cartons_jaunes_equipe1:t(0,3),cartons_jaunes_equipe2:t(0,3),cartons_rouges_equipe1:t(0,1),cartons_rouges_equipe2:t(0,1),passes_reussies_equipe1:q,passes_reussies_equipe2:E,coups_francs_equipe1:t(3,8),coups_francs_equipe2:t(3,8),corners_equipe1:t(3,8),corners_equipe2:t(3,8),fautes_equipe1:t(8,15),fautes_equipe2:t(8,15)}}const B=(s,e)=>{const t={possession_moyenne:50,precision_passes:80,tirs_par_match:12};return{status:"success",predictions:b(t,t),accuracy:75+Math.floor(Math.random()*15)}},x=()=>{const s=["Ligue 1","Premier League","La Liga","Champions League"],e=[];for(let t=0;t<5;t++){const n=s[Math.floor(Math.random()*s.length)],a=f[n.toLowerCase().replace(/ /g,"_")]||[];if(a.length<2)continue;const r=Math.floor(Math.random()*a.length);let o;do o=Math.floor(Math.random()*a.length);while(o===r);e.push({competition:n,date:new Date(Date.now()+Math.random()*7*24*60*60*1e3).toISOString(),homeTeam:a[r],awayTeam:a[o]})}return e},g=async()=>{try{return x()}catch(s){return console.error("API Error:",s.message),[]}},C=async(s,e,t)=>{try{if(!s||!e||!t)throw new Error("Tous les paramètres sont requis");return B(e,t)}catch(n){throw new Error(n.message||"Erreur lors de la prédiction. Veuillez réessayer.")}};function w(s){try{return new Date(s).toLocaleDateString("fr-FR",{weekday:"long",year:"numeric",month:"long",day:"numeric",hour:"2-digit",minute:"2-digit"})}catch(e){return console.error("Date formatting error:",e),s}}const $=5*60*1e3;function u(s){const e=document.getElementById("upcoming-matches");if(!(s!=null&&s.length)){e.innerHTML='<p class="text-gray-500">Aucun match à venir</p>';return}e.innerHTML=s.map(t=>`
    <div class="bg-white rounded-lg shadow p-4 mb-4">
      <div class="flex justify-between items-center mb-2">
        <span class="text-sm font-medium text-blue-600">${t.competition||""}</span>
        <span class="text-sm text-gray-500">${w(t.date)}</span>
      </div>
      <div class="flex justify-between items-center">
        <div class="flex-1 text-right">
          <span class="font-semibold">${t.homeTeam||""}</span>
        </div>
        <div class="mx-4 font-bold text-gray-600">VS</div>
        <div class="flex-1 text-left">
          <span class="font-semibold">${t.awayTeam||""}</span>
        </div>
      </div>
    </div>
  `).join("")}async function P(){try{const s=await g();u(s),setInterval(async()=>{const e=await g();u(e)},$)}catch(s){console.error("Error initializing upcoming matches:",s),u([])}}document.addEventListener("DOMContentLoaded",P);function _(s){const e=s||"Une erreur est survenue. Veuillez réessayer.";console.error(e),alert(e)}class I{constructor(e){this.container=e}display(e,t,n){this.container.innerHTML=`
      <div class="grid grid-cols-2 gap-4">
        <div class="bg-gray-50 p-4 rounded">
          <h4 class="font-semibold mb-3">${t}</h4>
          <div class="space-y-2">
            <p>Score: ${e.buts_equipe1}</p>
            <p>Possession: ${e.possession_equipe1}%</p>
            <p>Tirs: ${e.tirs_equipe1}</p>
            <p>Tirs cadrés: ${e.tirs_cadres_equipe1}</p>
            <p>Cartons jaunes: ${e.cartons_jaunes_equipe1}</p>
            <p>Cartons rouges: ${e.cartons_rouges_equipe1}</p>
            <p>Passes réussies: ${e.passes_reussies_equipe1}</p>
            <p>Coups francs: ${e.coups_francs_equipe1}</p>
            <p>Corners: ${e.corners_equipe1}</p>
            <p>Fautes: ${e.fautes_equipe1}</p>
          </div>
        </div>
        <div class="bg-gray-50 p-4 rounded">
          <h4 class="font-semibold mb-3">${n}</h4>
          <div class="space-y-2">
            <p>Score: ${e.buts_equipe2}</p>
            <p>Possession: ${e.possession_equipe2}%</p>
            <p>Tirs: ${e.tirs_equipe2}</p>
            <p>Tirs cadrés: ${e.tirs_cadres_equipe2}</p>
            <p>Cartons jaunes: ${e.cartons_jaunes_equipe2}</p>
            <p>Cartons rouges: ${e.cartons_rouges_equipe2}</p>
            <p>Passes réussies: ${e.passes_reussies_equipe2}</p>
            <p>Coups francs: ${e.coups_francs_equipe2}</p>
            <p>Corners: ${e.corners_equipe2}</p>
            <p>Fautes: ${e.fautes_equipe2}</p>
          </div>
        </div>
      </div>
    `}}class T{constructor(){this.leagueSelect=document.getElementById("league"),this.team1Select=document.getElementById("team1"),this.team2Select=document.getElementById("team2"),this.predictButton=document.getElementById("predict"),this.resultsDiv=document.getElementById("prediction-results"),this.matchStats=new I(document.getElementById("detailed-stats")),this.initializeEventListeners()}initializeEventListeners(){this.leagueSelect.addEventListener("change",()=>this.updateTeams()),[this.team1Select,this.team2Select].forEach(e=>{e.addEventListener("change",()=>this.updatePredictButton())}),this.predictButton.addEventListener("click",()=>this.handlePrediction())}updateTeams(){const e=this.leagueSelect.value,t=f[e]||[];[this.team1Select,this.team2Select].forEach(n=>{n.innerHTML='<option value="">Sélectionnez une équipe</option>',t.forEach(a=>{const r=new Option(a,a.toLowerCase().replace(/ /g,"_"));n.add(r)}),n.disabled=t.length===0}),this.predictButton.disabled=!0}updatePredictButton(){this.predictButton.disabled=!this.team1Select.value||!this.team2Select.value||this.team1Select.value===this.team2Select.value}async handlePrediction(){try{const e=await C(this.leagueSelect.value,this.team1Select.value,this.team2Select.value);this.displayPrediction(e)}catch(e){_(e.message)}}displayPrediction(e){if(e.status==="error"){_(e.message);return}this.resultsDiv.classList.remove("hidden");const t=this.team1Select.options[this.team1Select.selectedIndex].text,n=this.team2Select.options[this.team2Select.selectedIndex].text;document.getElementById("team1-name").textContent=t,document.getElementById("team2-name").textContent=n,document.getElementById("score1").textContent=e.predictions.buts_equipe1,document.getElementById("score2").textContent=e.predictions.buts_equipe2,document.getElementById("accuracy").textContent=e.accuracy.toFixed(1),this.matchStats.display(e.predictions,t,n)}}document.addEventListener("DOMContentLoaded",()=>new T);
