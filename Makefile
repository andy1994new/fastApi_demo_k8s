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

test:
	$(MAKE) -C user_service test
	$(MAKE) -C product_service test
	$(MAKE) -C order_service test