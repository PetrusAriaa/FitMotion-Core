PORT=9000

dev:
	uvicorn src.main:app --port $(PORT) --reload

prod:
	export SERVER_ENV=production && \
	uvicorn src.main:app --host 0.0.0.0 --port $(PORT)