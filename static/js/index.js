     //Open and close humberger menu
     document.getElementById("hamburger").onclick = function toggleMenu() {
        const navToggle = document.getElementsByClassName("toggle");
        for (let i = 0; i < navToggle.length; i++) {
            navToggle.item(i).classList.toggle("hidden");
        }
    };

    // Open modal
    document.getElementById("openModal").onclick = function openModal() {
        document.getElementById("modal").style.display = "block";
    };

    // Close modal
    document.getElementById("closeModal").onclick = function closeModal() {
        document.getElementById("modal").style.display = "none";
    };