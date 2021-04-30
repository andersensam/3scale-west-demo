.PHONY: base api
base:
	cd base && tar -czvf dist/app.tar.gz app/*

	docker build -t 3scale-demo-base base/

	docker tag 3scale-demo-base:latest quay.io/redhat_emp1/3scale-demo-base
	docker push quay.io/redhat_emp1/3scale-demo-base
api:
	cd api && tar -czvf dist/app.tar.gz app/*

	docker build -t 3scale-demo-api api/

	docker tag 3scale-demo-api:latest quay.io/redhat_emp1/3scale-demo-api
	docker push quay.io/redhat_emp1/3scale-demo-api