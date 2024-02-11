document.getElementById('openModal').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the default action (e.g., form submission)

    // Toggle the visibility of the modal
    document.getElementById('modal').classList.toggle('hidden');
});

document.getElementById('closeModal').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the default action (e.g., form submission)

    // Close the modal
    document.getElementById('modal').classList.add('hidden');
});

