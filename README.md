Fridge chef - Year 13 project:

- Ai powered website which helps users find recipes based on ingredients they have readily available.
- Heavy on modular blocks and I used stacks like: React; Tailwind; Vite and more.
---
These are the technologies I used for the frontend and backend:

- Frontend: React; Tailwind; Vite
- Backend: Flask
- Ai: Ollama - used model llama3, even though it was slower it gave better answers
---
Main features:

- the search bar lets people write ingredients or just a type of dish they wanted to make and the AI extractts the actuala ingredients mentioned in the input.
- While searching the autosuggest dropdown will appear depending on what the user will input showing ingredients from the dataset as they type.
- the top results of the search will depend on the matching ingredients, how many missing ingredients there are and difficulty to cook.
- Favourite tab and button on each recipe card to let people save recipes they want to access quickly.
- Search history that stores the last few searches
- recipe explanation used with Ai explaiining what a recipe is exactly
- why recipe's were chosen button which also uses Ai.
- React and Tailwind focused UI devloped from the previous html focused designs, just made it look so much better.
---
Skills I learned from this project:

- Use of Frontend and Backend folders
- using external API's (Ollama) / AI integration
- designing UI with Tailwind
- Debugging
- CSV parsing
- folder structuring and modular programming
- program development through prototypes
---
Bugs I fixed throughout the current releases:

- Autosuggest dropdown covering the entire screen with a blue every time i entered a letter in the search bar.
- Incorrect ingredients matching because of plural inputs.
- AI returning weird outputs - change in prompt
- favourites not updating instantly
- layout breaking after clicking the enter button

known issues and things i want to add:

- Ability to add your own recipes
- Filters for those who are vegetarian or other topics
- larger data set for more accurate recipe answers
- Ai sometimes doesnt even know what ingredients i put in - thinks i put in cheese when i didnt
---
## Project layout
```
Fridge-Chef/
  backend/
    app.py
    utils.py
    ai_utils.py
    recipes.csv
    state.json

  frontend/
    index.html
    vite.config.js
    package.json

    src/
      App.jsx
      main.jsx

      components/
        SearchBar.jsx
        Autosuggest.jsx
        Modal.jsx
        RecipeCard.jsx

      pages/
        Home.jsx
        Favourites.jsx

      styles/
        globals.css
