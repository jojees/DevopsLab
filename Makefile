compose-stop:
	cd containers && docker compose -f ubuntu.yaml -f compose-environment-dev.yaml -p dev down
	cd containers && docker compose -f ubuntu.yaml -f compose-environment-uat.yaml -p uat down
	cd containers && docker compose -f ubuntu.yaml -f compose-environment-preprod.yaml -p preprod down
	cd containers && docker compose -f ubuntu.yaml -f compose-environment-prod.yaml -p prod down
	cd containers && docker compose -f ubuntu.yaml -f compose-environment-staging.yaml -p stage down
	cd containers && docker compose -f ubuntu.yaml -f compose-environment-test.yaml -p test down

compose-start:
	cd containers && docker compose -f ubuntu.yaml -f compose-environment-dev.yaml -p dev up -d --build
	cd containers && docker compose -f ubuntu.yaml -f compose-environment-uat.yaml -p uat up -d --build
	cd containers && docker compose -f ubuntu.yaml -f compose-environment-preprod.yaml -p preprod up -d --build
	cd containers && docker compose -f ubuntu.yaml -f compose-environment-prod.yaml -p prod up -d --build
	cd containers && docker compose -f ubuntu.yaml -f compose-environment-staging.yaml -p stage up -d --build
	cd containers && docker compose -f ubuntu.yaml -f compose-environment-test.yaml -p test up -d --build
