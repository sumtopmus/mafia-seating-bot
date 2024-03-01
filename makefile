.PHONY: run debug test clean-logs clean-data clean-conversations

run:
	@ENV_FOR_DYNACONF=production python src/main.py

debug: clean-logs clean-conversations
	@python src/main.py

test:
	@python src/test.py

clean-all: clean-logs clean-data

clean-logs:
	@rm -rf logs

clean-data:
	@rm -rf data

clean-conversations:
	@rm -f data/db_conversations