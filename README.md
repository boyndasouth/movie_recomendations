# movie_recomendations

Application Name: FlickPicks

A movie recomendation system that recommends users movies based on preferences from a survey. 

So, far, users can simply view movies based on results from their survey and add and remove them from their favorites.

Components
- For user login and favorite movie list purposes, an SQLAlchemy Database is utilized
- For generating results from survey, a PyTorch Neural Network is utilized that takes in the results from the survey (all of the numerial: such as age, prefered movie length and scale of 0-10 questions)

Front End: HTML, Jinja

Back End: Flask, SQLAlchemy, UxerMixin

AI: PyTorch Neural Network

Future Developments
- Showtime viewings
- Recommendations based on favorite movie list, rather than just survey
