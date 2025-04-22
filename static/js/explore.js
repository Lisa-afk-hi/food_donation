document.addEventListener('DOMContentLoaded', function() {
    // Only target non-video items
    const exploreItems = document.querySelectorAll('.explore-item:not(.explore-video)');
    
    exploreItems.forEach(item => {
        item.addEventListener('click', function(e) {
            if (!e.target.closest('video')) {  // Extra protection
                openModal(this);
            }
        });
    });

    // Modal close handlers
    const modal = document.getElementById('modal');
    modal.addEventListener('click', function(e) {
        if (e.target === this) closeModal();
    });
});

function openModal(item) {
    const modal = document.getElementById('modal');
    const modalMedia = document.getElementById('modal-media');
    modalMedia.innerHTML = '';

    // Close button
    const closeBtn = document.createElement('span');
    closeBtn.className = 'close-btn';
    closeBtn.innerHTML = '&times;';
    closeBtn.addEventListener('click', closeModal);
    
    // Handle images
    if (item.querySelector('img')) {
        const img = document.createElement('img');
        img.src = item.querySelector('img').src;
        img.alt = item.querySelector('img').alt;
        modalMedia.appendChild(img);
    } 
    // Handle text
    else if (item.classList.contains('text-item')) {
        const textContent = document.createElement('div');
        textContent.className = 'text-content';
        textContent.innerHTML = item.innerHTML;
        modalMedia.appendChild(textContent);
    }
    
    modalMedia.appendChild(closeBtn);
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    const modal = document.getElementById('modal');
    modal.classList.remove('active');
    document.body.style.overflow = 'auto';
}

// ESC key support
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeModal();
});