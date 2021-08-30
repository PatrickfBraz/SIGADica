# Command used to start the local api server for debugging
debug-api:
	@cd crud_api/ && uvicorn main:app --host localhost --port 8000

start:
	@echo 'Setting up compose cluster'
	@docker-compose up --force-recreate --remove-orphans -d --build
	@docker ps

stop:
	@echo 'Stopping compose cluster'
	@docker-compose stop

restart:
	@docker-compose stop
	@docker-compose up --force-recreate --remove-orphans -d --build
	@docker ps