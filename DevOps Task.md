1. SSH:
	1.1 Создание SSH ключа `ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa`
	1.2 Настроить параметры SSH-сервера в /etc/ssh/.
		1)  PasswordAuthentication no
		2) PubkeyAuthentication yes
		3) AuthorizedKeysFile .ssh/authorized_keys
		4) ssh-copy-id -i ~/.ssh/id_rsa.pub user@192.168.88.138

2. SYSTEMD:
	2.1 
