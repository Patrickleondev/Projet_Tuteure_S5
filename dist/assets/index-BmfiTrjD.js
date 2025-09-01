(function(){const e=document.createElement("link").relList;if(e&&e.supports&&e.supports("modulepreload"))return;for(const s of document.querySelectorAll('link[rel="modulepreload"]'))n(s);new MutationObserver(s=>{for(const r of s)if(r.type==="childList")for(const o of r.addedNodes)o.tagName==="LINK"&&o.rel==="modulepreload"&&n(o)}).observe(document,{childList:!0,subtree:!0});function t(s){const r={};return s.integrity&&(r.integrity=s.integrity),s.referrerPolicy&&(r.referrerPolicy=s.referrerPolicy),s.crossOrigin==="use-credentials"?r.credentials="include":s.crossOrigin==="anonymous"?r.credentials="omit":r.credentials="same-origin",r}function n(s){if(s.ep)return;s.ep=!0;const r=t(s);fetch(s.href,r)}})();const h={champions_league:["Real Madrid","Manchester City","Bayern Munich","PSG","Barcelona","Liverpool","Chelsea","Juventus","Inter Milan","Milan","Dortmund","Atletico Madrid","Porto","Benfica","Ajax"],ligue1:["PSG","Marseille","Lyon","Lille","Monaco","Rennes","Nice","Lens","Strasbourg","Montpellier"],premier_league:["Manchester City","Liverpool","Arsenal","Manchester United","Chelsea","Tottenham","Newcastle","West Ham","Brighton","Aston Villa"],liga:["Real Madrid","Barcelona","Atletico Madrid","Sevilla","Real Sociedad","Villarreal","Athletic Bilbao","Valencia","Betis","Osasuna"],world_cup:["France","Brazil","Argentina","England","Spain","Germany","Portugal","Netherlands","Belgium","Croatia"],euro:["France","England","Spain","Germany","Portugal","Netherlands","Belgium","Croatia","Italy","Denmark"],copa_america:["Brazil","Argentina","Uruguay","Colombia","Chile","Peru","Paraguay","Ecuador","Venezuela","Bolivia"]};function y(a,e){const t=(d,f)=>Math.floor(Math.random()*(f-d+1))+d,n=(a.precision_passes+a.possession_moyenne)/(e.precision_passes+e.possession_moyenne),s=Math.min(65,Math.max(35,Math.round(50*n))),r=100-s,o=t(8,18),c=t(8,18),u=Math.round(o*.4),l=Math.round(c*.4),g=Math.round(u*.25),_=Math.round(l*.25);return{buts_equipe1:g,buts_equipe2:_,possession_equipe1:s,possession_equipe2:r,tirs_equipe1:o,tirs_equipe2:c,tirs_cadres_equipe1:u,tirs_cadres_equipe2:l,cartons_jaunes_equipe1:t(0,3),cartons_jaunes_equipe2:t(0,3),cartons_rouges_equipe1:t(0,1),cartons_rouges_equipe2:t(0,1),passes_reussies_equipe1:t(400,600),passes_reussies_equipe2:t(400,600),coups_francs_equipe1:t(3,8),coups_francs_equipe2:t(3,8),corners_equipe1:t(3,8),corners_equipe2:t(3,8),fautes_equipe1:t(8,15),fautes_equipe2:t(8,15)}}const v=(a,e)=>{const t={possession_moyenne:50,precision_passes:80,tirs_par_match:12};return{status:"success",predictions:y(t,t),accuracy:75+Math.floor(Math.random()*15)}},M=()=>{const a=["Ligue 1","Premier League","La Liga","Champions League"],e=[];for(let t=0;t<5;t++){const n=a[Math.floor(Math.random()*a.length)],s=h[n.toLowerCase().replace(/ /g,"_")]||[];if(s.length<2)continue;const r=Math.floor(Math.random()*s.length);let o;do o=Math.floor(Math.random()*s.length);while(o===r);e.push({competition:n,date:new Date(Date.now()+Math.random()*7*24*60*60*1e3).toISOString(),homeTeam:s[r],awayTeam:s[o]})}return e},p=async()=>{try{return M()}catch(a){return console.error("API Error:",a.message),[]}},q=async(a,e,t)=>{try{if(!a||!e||!t)throw new Error("Tous les paramètres sont requis");return v(e,t)}catch(n){throw new Error(n.message||"Erreur lors de la prédiction. Veuillez réessayer.")}};function S(a){try{return new Date(a).toLocaleDateString("fr-FR",{weekday:"long",year:"numeric",month:"long",day:"numeric",hour:"2-digit",minute:"2-digit"})}catch(e){return console.error("Date formatting error:",e),a}}const E=5*60*1e3;function i(a){const e=document.getElementById("upcoming-matches");if(!(a!=null&&a.length)){e.innerHTML='<p class="text-gray-500">Aucun match à venir</p>';return}e.innerHTML=a.map(t=>`
    <div class="bg-white rounded-lg shadow p-4 mb-4">
      <div class="flex justify-between items-center mb-2">
        <span class="text-sm font-medium text-blue-600">${t.competition||""}</span>
        <span class="text-sm text-gray-500">${S(t.date)}</span>
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
  `).join("")}async function L(){try{const a=await p();i(a),setInterval(async()=>{const e=await p();i(e)},E)}catch(a){console.error("Error initializing upcoming matches:",a),i([])}}document.addEventListener("DOMContentLoaded",L);function m(a){const e=a||"Une erreur est survenue. Veuillez réessayer.";console.error(e),alert(e)}class b{constructor(e){this.container=e}display(e,t,n){this.container.innerHTML=`
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
    `}}class B{constructor(){this.leagueSelect=document.getElementById("league"),this.team1Select=document.getElementById("team1"),this.team2Select=document.getElementById("team2"),this.predictButton=document.getElementById("predict"),this.resultsDiv=document.getElementById("prediction-results"),this.matchStats=new b(document.getElementById("detailed-stats")),this.initializeEventListeners()}initializeEventListeners(){this.leagueSelect.addEventListener("change",()=>this.updateTeams()),[this.team1Select,this.team2Select].forEach(e=>{e.addEventListener("change",()=>this.updatePredictButton())}),this.predictButton.addEventListener("click",()=>this.handlePrediction())}updateTeams(){const e=this.leagueSelect.value,t=h[e]||[];[this.team1Select,this.team2Select].forEach(n=>{n.innerHTML='<option value="">Sélectionnez une équipe</option>',t.forEach(s=>{const r=new Option(s,s.toLowerCase().replace(/ /g,"_"));n.add(r)}),n.disabled=t.length===0}),this.predictButton.disabled=!0}updatePredictButton(){this.predictButton.disabled=!this.team1Select.value||!this.team2Select.value||this.team1Select.value===this.team2Select.value}async handlePrediction(){try{const e=await q(this.leagueSelect.value,this.team1Select.value,this.team2Select.value);this.displayPrediction(e)}catch(e){m(e.message)}}displayPrediction(e){if(e.status==="error"){m(e.message);return}this.resultsDiv.classList.remove("hidden");const t=this.team1Select.options[this.team1Select.selectedIndex].text,n=this.team2Select.options[this.team2Select.selectedIndex].text;document.getElementById("team1-name").textContent=t,document.getElementById("team2-name").textContent=n,document.getElementById("score1").textContent=e.predictions.buts_equipe1,document.getElementById("score2").textContent=e.predictions.buts_equipe2,document.getElementById("accuracy").textContent=e.accuracy.toFixed(1),this.matchStats.display(e.predictions,t,n)}}document.addEventListener("DOMContentLoaded",()=>new B);
