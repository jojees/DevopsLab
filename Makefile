compose-stop:
	cd containers && docker compose -f ubuntu.yaml -f compose-environment-dev.yaml -p infra-dev down
	cd containers && docker compose -f ubuntu.yaml -f compose-environment-uat.yaml -p infra-uat down
	cd containers && docker compose -f ubuntu.yaml -f compose-environment-preprod.yaml -p infra-preprod down
	cd containers && docker compose -f ubuntu.yaml -f compose-environment-prod.yaml -p infra-prod down
	cd containers && docker compose -f ubuntu.yaml -f compose-environment-staging.yaml -p infra-stage down
	cd containers && docker compose -f ubuntu.yaml -f compose-environment-test.yaml -p infra-test down
	cd containers && docker compose -f ubuntu.yaml -f compose-environment-uat.yaml -p infra-uat down

compose-start:
	cd containers && docker compose -f ubuntu.yaml -f compose-environment-dev.yaml -p infra-dev up -d
	cd containers && docker compose -f ubuntu.yaml -f compose-environment-uat.yaml -p infra-uat up -d
	cd containers && docker compose -f ubuntu.yaml -f compose-environment-preprod.yaml -p infra-preprod up -d
	cd containers && docker compose -f ubuntu.yaml -f compose-environment-prod.yaml -p infra-prod up -d
	cd containers && docker compose -f ubuntu.yaml -f compose-environment-staging.yaml -p infra-stage up -d
	cd containers && docker compose -f ubuntu.yaml -f compose-environment-test.yaml -p infra-test up -d
	cd containers && docker compose -f ubuntu.yaml -f compose-environment-uat.yaml -p infra-uat up -d