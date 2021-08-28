# Command used to start the local api server for debugging
debug-api:
	@cd crud_api/ && uvicorn main:app --host localhost --port 8000