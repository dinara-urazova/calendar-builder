build:
	docker build -t calendar_builder_image .
run:
	docker run -it -d --env-file .env --restart=unless-stopped --name calendar_builder --network=infra_storage_net --network=infra_web_net calendar_builder_image
stop:
	docker stop calendar_builder
	docker rm calendar_builder

