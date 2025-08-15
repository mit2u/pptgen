### Building and running your application

When you're ready, start your application by running:
`docker compose up --build`.

Your application will be available at http://localhost:8000.

Add GEMINI_API_KEY=XXXXX in .env file

Create user via
`python manage.py createsuperuser `

Login through http://localhost:8000/api-auth/login/?next=/

Later use http://localhost:8000/topic-submit/ for submitting the topic
Previous Templates can be found in http://localhost:8000/slides/