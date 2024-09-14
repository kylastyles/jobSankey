
all: up dashboard pull push

up:
	$(info Standing up Docker containers...)
	@docker compose up -d

pull:
	$(info Pulling data from $(DATA_URL)...)
	@python3 scripts/data-extractor.py

push:
	$(info Pushing data to ElasticSearch...)
	@python3 scripts/es-loader.py

dashboard:
	$(info Publishing dashboard to Kibana...)
	@cd scripts && python3 kibana-setup.py

down:
	$(info Stopping Docker containers...)
	@docker compose down
