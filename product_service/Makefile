install:
	pip install -r requirments.txt

format:
	black *.py

lint:
	pylint *.py

database:
	#this is only for test on local machine
	#psql postgres
	brew services start postgresql

run:
	uvicorn --host 0.0.0.0 --port 8000 main:app

test:
	#test user service

build:
	docker build -t user_service .

docker_run:
	docker-compose up -d --build