1. Генерирую ssh-ключ: `ssh-keygen -t rsa -b 4096`
     ```
    -t rsa указывает тип ключа (RSA).
    -b 4096 задает длину ключа в битах.
    ```
2. Прокидываю ssh-ключ на удаленный сервер: `ssh-copy-id <user>@<ip>`
3. Заходим на удаленный сервер и в файле конфигурации ssh-сервера `/etc/ssh/sshd_config` раскомменчиваем данные строки
    ```
    PasswordAuthentication no
    PubkeyAuthentication yes
    AuthorizedKeysFile .ssh/authorized_keys
    ```
4. Выполняем перезапуск служб ssh: `sudo systemctl restart ssh`