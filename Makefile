.PHONY: up down test test-contracts seed reset demo e2e clean help

help:
	@echo "ZeroTrace Monorepo Commands:"
	@echo "  make up             Start local docker stack (orchestrator, minio, postgres, redis)"
	@echo "  make down           Stop local stack and remove volumes"
	@echo "  make test           Run unit and proof tests"
	@echo "  make e2e            Run headless end-to-end golden path pipeline test"
	@echo "  make seed           Seed 50,000 customers & 480 Parquet lakehouse files"
	@echo "  make reset          Reset demo state to clean baseline"
	@echo "  make demo           Run Demo Director interactive CLI"

up:
	docker compose -f infra/docker-compose.yml up -d

down:
	docker compose -f infra/docker-compose.yml down -v

test:
	pytest services/orchestrator/tests -v

e2e:
	python scripts/e2e_golden_path.py

seed:
	curl -s -X POST http://localhost:8001/api/v1/demo/seed -H "Content-Type: application/json" -d '{"profile":"showtime"}'

reset:
	curl -s -X POST http://localhost:8001/api/v1/demo/reset

demo:
	python demo/director/scenario_runner.py

clean:
	rm -rf .pytest_cache *.db
