.PHONY: run debug clean-cache clean-logs clean-data

run: clean-cache
	@ENV_FOR_DYNACONF=production python src/bot/bot.py

debug: clean-all
	@python src/bot/bot.py

clean-all: clean-cache clean-logs clean-data

clean-cache:
	@rm -rf src/__pycache__
	@rm -rf src/bot/__pycache__
	@rm -rf src/bot/handlers/__pycache__

clean-logs:
	@rm -rf logs

clean-data:
	@rm -rf data
