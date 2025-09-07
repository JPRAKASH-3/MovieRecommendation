document.addEventListener("DOMContentLoaded", function() {
    const movieInput = document.querySelector('input[name="movie"]');

    // Array of all movie titles from your CSV
    const movies = [
        "Inception","Interstellar","The Dark Knight","Titanic","The Matrix",
        "Forrest Gump","Gladiator","Avengers: Endgame","The Lion King","Parasite",
        "Joker","Spider-Man: No Way Home","Avatar","The Godfather","The Shawshank Redemption",
        "Avengers: Infinity War","Black Panther","La La Land","The Avengers","The Departed"
    ];

    const createSuggestions = (matches) => {
        closeSuggestions();
        if (!matches.length) return;

        const list = document.createElement("div");
        list.setAttribute("class", "autocomplete-items");
        movieInput.parentNode.appendChild(list);

        matches.forEach(title => {
            const item = document.createElement("div");
            item.innerHTML = title;
            item.addEventListener("click", function() {
                movieInput.value = this.innerHTML;
                closeSuggestions();
            });
            list.appendChild(item);
        });
    }

    const closeSuggestions = () => {
        const items = document.querySelectorAll(".autocomplete-items");
        items.forEach(item => item.parentNode.removeChild(item));
    }

    movieInput.addEventListener("input", function() {
        const val = this.value.toLowerCase();
        const matches = movies.filter(m => m.toLowerCase().includes(val));
        createSuggestions(matches);
    });

    document.addEventListener("click", function(e) {
        if (e.target !== movieInput) closeSuggestions();
    });
});
