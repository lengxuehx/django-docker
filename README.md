# django-docker
 A production-ready setup for running Django on Docker
 
 1. build mysite-base
 
        docker build -f dockerfile-mysite-base -t mysite-base:latest ./
        
 2. collect static files
        
        python manage.py collectstatic
        
 3. create secrets
 
        docker secret create db_password secret\db_password
        docker secret create db_root_password secret\db_root_password
        
 4. build service images
 
        docker-compose -f production.yml build
        
 5. deploy
         
        docker stack deploy -c production.yml mysite
        
