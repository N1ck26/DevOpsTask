1. Установка Java `sudo apt install default-jdk`
2. Скачиваем, распаковываем и переходим в директорию с Kafka
   ```
   wget https://downloads.apache.org/kafka/3.6.0/kafka_2.13-3.6.0.tgz

   tar -xzf kafka_2.13-3.6.0.tgz

   cd kafka_2.13-3.6.0

   ```

3. Kafka использует Zookeeper для управления кластерами. Запускаем сервисы:
   ```
   bin/zookeeper-server-start.sh config/zookeeper.properties

   ```

4. В новом терминале запускаем саму Kafka:
   ```
   bin/kafka-server-start.sh config/server.properties

   ```

5. Развораичваем Kafka UI в docker:
   ```
   docker run -d --name=kafka-ui -p 8080:8080 \
   -e KAFKA_CLUSTERS_0_NAME=local \
   -e KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=192.168.88.137:9092 \
   provectuslabs/kafka-ui

   ```

6. Обращение к Kafka UI через веб-форму `http://localhost:8080`

7. Создание топика: `bin/kafka-topics.sh --create --topic test-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1`

8. Проверка списка топиков: `bin/kafka-topics.sh --list --bootstrap-server localhost:9092`

9. Запуск producer: `bin/kafka-console-producer.sh --topic test-topic --bootstrap-server localhost:9092` и отправка сообщения

10. Запуск consumer: `bin/kafka-console-consumer.sh --topic test-topic --bootstrap-server localhost:9092 --from-beginning` и получение сообщения от producer