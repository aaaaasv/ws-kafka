## Setup

1. Clone the repository:

```sh
$ git clone https://github.com/aaaaasv/ws-kafka.git
$ cd ws-kafka
```

2. Run:

```sh
$ docker-compose up --build
```

And navigate to `http://127.0.0.1:8001`.

To produce Kafka messages through docker-compose run:

```sh
docker-compose exec kafka bash
sh /bin/kafka-console-producer --bootstrap-server localhost:9092 --topic 1
```

Example valid data:

```json
{"data": "data", "event_type": "type"}
```