// Function to open the modal
function openModal(id) {
    modal = document.getElementById(id);
    modal.classList.remove('hidden');
    
    // Add event listener to the background overlay
    var overlay = document.getElementById(id +'Overlay');
    overlay.addEventListener('click', function() {closeModal(id);});
}

// Function to close the modal
function closeModal(id) {
    var modal = document.getElementById(id);
    modal.classList.add('hidden');

    // Remove event listener from the background overlay
    var overlay = document.getElementById(id +'Overlay');
    overlay.removeEventListener('click', closeModal);
}
