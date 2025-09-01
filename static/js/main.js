// Gestion du chatbot
const chatbotSection = document.getElementById('chatbot-section');
const openChatbotBtn = document.getElementById('open-chatbot');
const closeChatbotBtn = document.getElementById('close-chatbot');
const chatMessages = document.getElementById('chat-messages');
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');

// Gestion de la sélection des compétitions
const competitionButtons = document.querySelectorAll('.competition-btn');
const teamSelection = document.getElementById('team-selection');
const equipeDomicileSelect = document.getElementById('equipe-domicile');
const equipeExterieurSelect = document.getElementById('equipe-exterieur');

// Gestion du chatbot
openChatbotBtn.addEventListener('click', () => {
    chatbotSection.classList.remove('hidden');
    openChatbotBtn.classList.add('hidden');
});

closeChatbotBtn.addEventListener('click', () => {
    chatbotSection.classList.add('hidden');
    openChatbotBtn.classList.remove('hidden');
});

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = chatInput.value.trim();
    if (!message) return;

    // Ajouter le message de l'utilisateur
    addMessage('user', message);
    chatInput.value = '';

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
        });

        const data = await response.json();
        addMessage('bot', data.response);
    } catch (error) {
        console.error('Erreur:', error);
        addMessage('bot', 'Désolé, une erreur est survenue.');
    }
});

function addMessage(type, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `mb-4 ${type === 'user' ? 'text-right' : ''}`;
    
    const messageBubble = document.createElement('div');
    messageBubble.className = `inline-block p-3 rounded-lg ${
        type === 'user' 
            ? 'bg-blue-600 text-white' 
            : 'bg-gray-700 text-white'
    }`;
    messageBubble.textContent = content;
    
    messageDiv.appendChild(messageBubble);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Gestion des compétitions
competitionButtons.forEach(button => {
    button.addEventListener('click', async () => {
        // Retirer la sélection active des autres boutons
        competitionButtons.forEach(btn => {
            btn.classList.remove('ring-2', 'ring-blue-500');
        });
        
        // Ajouter la sélection au bouton cliqué
        button.classList.add('ring-2', 'ring-blue-500');
        
        const competitionId = button.dataset.competition;
        
        try {
            // Charger les équipes de la compétition
            const response = await fetch(`/api/teams/${competitionId}`);
            const teams = await response.json();
            
            // Mettre à jour les sélecteurs d'équipes
            updateTeamSelectors(teams);
            
            // Afficher la section de sélection d'équipes
            teamSelection.classList.remove('hidden');
        } catch (error) {
            console.error('Erreur lors du chargement des équipes:', error);
        }
    });
});

function updateTeamSelectors(teams) {
    // Vider les sélecteurs
    equipeDomicileSelect.innerHTML = '<option value="">Sélectionnez une équipe</option>';
    equipeExterieurSelect.innerHTML = '<option value="">Sélectionnez une équipe</option>';
    
    // Ajouter les équipes aux sélecteurs
    teams.forEach(team => {
        const option1 = document.createElement('option');
        option1.value = team.id;
        option1.textContent = team.name;
        equipeDomicileSelect.appendChild(option1);
        
        const option2 = document.createElement('option');
        option2.value = team.id;
        option2.textContent = team.name;
        equipeExterieurSelect.appendChild(option2);
    });
} 