// Burger menus
document.addEventListener('DOMContentLoaded', function() {
    // open
    const burger = document.querySelectorAll('.navbar-burger');
    const menu = document.querySelectorAll('.navbar-menu');

    if (burger.length && menu.length) {
        for (var i = 0; i < burger.length; i++) {
            burger[i].addEventListener('click', function() {
                for (var j = 0; j < menu.length; j++) {
                    menu[j].classList.toggle('hidden');
                }
});
        }
    }

    // close
    const close = document.querySelectorAll('.navbar-close');
    const backdrop = document.querySelectorAll('.navbar-backdrop');

    if (close.length) {
        for (var i = 0; i < close.length; i++) {
            close[i].addEventListener('click', function() {
                for (var j = 0; j < menu.length; j++) {
                    menu[j].classList.toggle('hidden');
                }
});
        }
    }

    if (backdrop.length) {
        for (var i = 0; i < backdrop.length; i++) {
            backdrop[i].addEventListener('click', function() {
                for (var j = 0; j < menu.length; j++) {
                    menu[j].classList.toggle('hidden');
                }
            });
        }
    }
});
// Show spinner and loading text initially
document.getElementById('spinner').classList.add('visible');
document.getElementById('loadingText').classList.add('visible');

// Simulate loading delay
setTimeout(function() {
    // Hide spinner and loading text after a delay (e.g., 3 seconds)
    document.getElementById('spinner').classList.remove('visible');
    document.getElementById('loadingText').classList.remove('visible');
    
    // Hide both spinner and loading text
    document.getElementById('spinner').style.display = 'none';
    document.getElementById('loadingText').style.display = 'none';
    
    // Show content after the delay
    document.getElementById('content').classList.remove('hidden');
}, 3000); // Adjust the delay as needed
// Show spinner and loading text initially
document.getElementById('spinner').classList.add('visible');
document.getElementById('loadingText').classList.add('visible');

// Simulate loading delay
setTimeout(function() {
    // Hide spinner and loading text after a delay (e.g., 3 seconds)
    document.getElementById('spinner').classList.remove('visible');
    document.getElementById('loadingText').classList.remove('visible');
    
    // Hide both spinner and loading text
    document.getElementById('spinner').style.display = 'none';
    document.getElementById('loadingText').style.display = 'none';
    
    // Show content after the delay
    document.getElementById('content').classList.remove('hidden');
}, 3000); // Adjust the delay as needed

document.getElementById('searchInput').addEventListener('input', function(event) {
    const query = event.target.value.trim().toLowerCase();
    const recommendationCards = document.querySelectorAll('.recommendation-card');
    recommendationCards.forEach(function(card) {
        const name = card.querySelector('h2').textContent.toLowerCase();
        if (name.includes(query)) {
                card.style.display = 'block'; 
        } else {
                card.style.display = 'none'; 
        }
        });
    });
    document.addEventListener("DOMContentLoaded", function() {
        const filterButton = document.getElementById("filterButton");
        const priceFilter = document.getElementById("priceFilter");
        const priceRange = document.getElementById("priceRange");
        const priceOutput = document.getElementById("priceOutput");
        const recommendationCards = document.querySelectorAll(".recommendation-card");
    
        filterButton.addEventListener("click", function() {
            priceFilter.classList.toggle("hidden");
        });
    
        priceRange.addEventListener("input", function() {
            const selectedPrice = parseInt(priceRange.value);
            priceOutput.textContent = `$${selectedPrice}`;
    
            recommendationCards.forEach(card => {
                const priceElement = card.querySelector(".text-gray-800");
                const price = parseInt(priceElement.textContent.replace("$", ""));
                
                if (price <= selectedPrice) {
                    card.style.display = "block";
                } else {
                    card.style.display = "none";
                }
            });
        });
    });
    