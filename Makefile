install:
	pip instal -r requirements.txt

# Build all service Docker images
build:
	$(MAKE) -C user_service build
	$(MAKE) -C product_service build
	$(MAKE) -C order_service build

# Test all services
test:
	$(MAKE) -C user_service test
	$(MAKE) -C product_service test
	$(MAKE) -C order_service test