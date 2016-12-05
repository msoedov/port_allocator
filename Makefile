default: req generate run

req:
	@pip install -r requirements.txt


generate:
	@docker-compose up generate

run:
	@docker-compose up nginx
