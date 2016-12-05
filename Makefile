default: req generate run

req:
	@pip install -r requirements.txt

test:
	@python -m doctest service_builder/allocator.py

generate:
	@docker-compose -f docker-compose.builder.yml up --build generate

run:
	@docker-compose up --build nginx
