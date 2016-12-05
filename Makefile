default: req generate run

req:
	@pip install -r requirements.txt


generate:
	@docker-compose -f docker-compose.builder.yml up --build generate

run:
	@docker-compose up --build nginx
