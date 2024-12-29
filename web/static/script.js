    // import * as THREE from 'three';
// import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// import { DragControls } from 'three/addons/controls/DragControls.js';

// Define styles before they're used
const styles = `
    .info-card {
        background: white;
        border: 1px solid #ccc;
        border-radius: 4px;
        padding: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        z-index: 1000;
    }

    .info-card-content {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .info-row {
        display: flex;
        justify-content: space-between;
        gap: 16px;
    }

    .info-label {
        font-weight: bold;
    }

    #tableView {
        height: 100%;
        position: relative;
    }

    #graphCanvas {
        position: absolute;
        top: 0;
        left: 0;
    }
`;


function showInfoCard(event, inverse, order) {
    // Remove any existing cards first
    const existingCard = document.querySelector('.info-card');
    if (existingCard) {
        existingCard.remove();
    }

    // Create card element
    const card = document.createElement('div');
    card.className = 'info-card';
    
    // Create content
    const content = `
        <div class="info-card-content">
            <div class="info-row">
                <span class="info-label">Inverse:</span>
                <span class="info-value">${inverse}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Order:</span>
                <span class="info-value">${order}</span>
            </div>
        </div>
    `;
    card.innerHTML = content;

    // Position the card next to the clicked button
    const rect = event.target.getBoundingClientRect();
    card.style.position = 'absolute';
    card.style.top = `${rect.top + window.scrollY}px`;
    card.style.left = `${rect.right + window.scrollX + 5}px`; // 5px offset from button

    // Add to document
    document.body.appendChild(card);

    // Close card when clicking outside
    document.addEventListener('click', function closeCard(e) {
        if (!card.contains(e.target) && e.target !== event.target) {
            card.remove();
            document.removeEventListener('click', closeCard);
        }
    });
}
