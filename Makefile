test:
	docker-compose run web pytest $(test_files)

install:
	docker-compose build --no-cache