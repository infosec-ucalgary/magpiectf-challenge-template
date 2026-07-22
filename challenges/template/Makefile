.PHONY build dist run clean

build:
	docker build -t <CHALLENGE_NAME> .

dist:
	rm -rf dist
	docker build --target dist --output type=local,dest=./dist .

run:
	docker compose up -d --build

clean:
	rm -rf dist
	docker compose down