Fridge chef - Year 13 project:

- Ai powered website which helps users find recipes based on ingredients they have readily available.
- Heavy on modular blocks and I used stacks like: React; Tailwind; Vite and more.

These are the technologies I used for the frontend and backend:

- Frontend: React; Tailwind; Vite
- Backend: Flask
- Ai: Ollama - used model llama3, even though it was slower it gave better answers

Structure:

for the frontend I used React to let me split the website into smaller parts (components) making it easier to work on different sections of code or seperate sections of Javascript and JSX. I was able to refer / import classes between the files so they were in one space - easy organisation makes easy to manage program.

Components folder: has things that appear more than once and have their own functions such as the search bar which
handles inputs and calls autosuggest, the autosuggest list also has its own file to make the dropdown list appear when
the user enters a specific letter. The recipecard file is meant to add details of what goes on the cards such as the recipe name, if it's makeable with current ingrediants, any missing ingrediant and even AI explainations on why it was chosen.

Pages folder: contains the two main tabs of the website being the main home page (home.jsx) and the saved recipe cards in a favourites tab (Favourites.jsx).

globals.css holds styling effects which i added on cards, the background, the history selection and other interatable buttons, it has styles like the glow effect, animations and helpers like .glass-dark.

For the backend there was more focus on the coding behind the UI features such as in app.py the main api file its features included the searching with Ai, the autosuggestions, saving recipe code and the history.

ai_utils.py has the main AI functions by sending the prompt i made to Ollama and returning that into an output in another file.

recipes.csv is the main dataset which i generated using AI because there were no specific pre made data sets around this - limited to like 200 recipes which can make the searches a little innaccurate.

Main features:

- the search bar lets people write ingredients or just a type of dish they wanted to make and the AI extractts the actuala ingredients mentioned in the input.
- While searching the autosuggest dropdown will appear depending on what the user will input showing ingredients from the dataset as they type.
- the top results of the search will depend on the matching ingredients, how many missing ingredients there are and difficulty to cook.
- Favourite tab and button on each recipe card to let people save recipes they want to access quickly.
- Search history that stores the last few searches
- recipe explanation used with Ai explaiining what a recipe is exactly
- why recipe's were chosen button which also uses Ai.
- React and Tailwind focused UI devloped from the previous html focused designs, just made it look so much better.

Skills I learned from this project:

- Use of Frontend and Backend folders
- using external API's (Ollama) / AI integration
- designing UI with Tailwind
- Debugging
- CSV parsing
- folder structuring and modular programming
- program development through prototypes

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
