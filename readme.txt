How to get started.
1. Open the project in Pycharm
2. Install requirements pip install -r requirements.txt
3. Export run.py as variable FLASK_APP
4. flask run

How to get started with docker
1. Make sure you've docker installed and running.
2. Make sure dockerfile is in the root of the project directory, i.e. IoSL
3. build docker image: docker build -t flaskapplication .
4. run container: docker run -i -t -d -v /path/to/your/folder:/app -p 5000:5000 flaskapplication
5. check container is running: docker ps
6. Should be available at localhost:5000

How to configure nginx:
will come later.


Project structure:
IOSl -- project directory
    -- database: will contain database (user logins)
    -- static: contains static files, e.g. images, css, js, etc.
    -- templates: html templates, all templates extend base.html which contains common elements
    -- flask_config.py: will contain flask configurations e.g. debug mode, application name, secret, etc.
    -- readme.txt: this document
    -- requirements.txt: all libraries / modules installed through pip generated using: pip freeze > requirements.txt
    -- run.py: where the magic happens
    -- views.py: defines routes / methods / redirects

