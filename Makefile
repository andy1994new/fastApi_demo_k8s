install:
	pip install -r requirements.txt

format:
	black user_service/*.py product_service/*.py order_service/*.py

lint:
	pylint user_service/*.py product_service/*.py order_service/*.py

build:
	$(MAKE) -C user_service build
	$(MAKE) -C product_service build
	$(MAKE) -C order_service build

tag:
	docker tag user_service:latest andy2025/user_service:latest
	docker tag product_service:latest andy2025/product_service:latest
	docker tag order_service:latest andy2025/order_service:latest

push:
	docker push andy2025/user_service:latest
	docker push andy2025/product_service:latest
	docker push andy2025/order_service:latest

deploy:
	kubectl apply -f k8s/


port:
	kubectl port-forward service/order-service 8002:8002
	kubectl port-forward service/user-service 8000:8000
	kubectl port-forward service/product-service 8001:8001

test:
	$(MAKE) -C user_service test
	$(MAKE) -C product_service test
	$(MAKE) -C order_service test