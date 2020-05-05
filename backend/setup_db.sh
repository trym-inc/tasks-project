docker-compose exec web python manage.py migrate
docker-compose exec web python setup_test_data.py
