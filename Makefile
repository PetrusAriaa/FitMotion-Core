PORT=9000
PROD_HOST=0.0.0.0
DEV_HOST=127.0.0.1

dev:
	@echo "Backend is running in port :$(PORT)"
	@echo "Access: http://$(DEV_HOST):$(PORT)/docs"
	@echo "Access: http://localhost:$(PORT)/docs"
	@uvicorn src.main:app --port $(PORT) --reload

prod:
	@export SERVER_ENV=production
	@uvicorn src.main:app --host $(PROD_HOST) --port $(PORT)