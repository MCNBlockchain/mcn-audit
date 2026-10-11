# MCN: чистый запуск, 3 + 3 валидатора

A: 103.228.169.164 (Fornex). B: 38.180.143.231. Linux x86_64. Chain ID 2325, газ 30 000 000, слот 12 секунд. Всего 120 000 000 MCN: 119 940 000 на treasury, 60 000 в стейке. A получает ключи 0–2, B — 3–5. Все ключи новые. Genesis создаётся только на A. Не используй предыдущий архив.

## 1. Подготовка обоих серверов

Загрузи mcn-launch-6.zip в домашнюю папку каждого сервера. Выполняй команды от обычного пользователя с sudo, не root. Имя SSH-пользователя B ниже обозначено USER_B — замени его своим.

На обоих:

```bash
cd ~
sudo apt-get update
sudo apt-get install -y curl ca-certificates python3 python3-venv openssl jq tar unzip chrony
sudo systemctl enable --now chrony
unzip mcn-launch-6.zip
cd ~/mcn-launch-6
chmod +x scripts/*.sh
./scripts/01-install.sh
sudo ufw allow 30303/tcp
sudo ufw allow 30303/udp
sudo ufw allow 13000/tcp
sudo ufw allow 13000/udp
sudo ufw allow 12000/udp
```

Разреши эти же порты в панелях обоих провайдеров. Сохрани SSH-доступ. RPC 8545, Engine API 8551, Beacon REST 3500 и gRPC 4000 остаются локальными.

## 2. node.env — целиком, без ручного редактирования

Только на A:

```bash
cd ~/mcn-launch-6
cat > node.env <<'ENV'
NODE_ROLE=A
PUBLIC_IP=103.228.169.164
BEACON_BOOTNODE=''
BEACON_PEER=''
TREASURY=0xfE4800cA5a48670cc5f591a51F517BA8F682D4Ae
FEE_RECIPIENT=0xfE4800cA5a48670cc5f591a51F517BA8F682D4Ae
ENV
chmod 600 node.env
```

Только на B:

```bash
cd ~/mcn-launch-6
cat > node.env <<'ENV'
NODE_ROLE=B
PUBLIC_IP=38.180.143.231
BEACON_BOOTNODE=''
BEACON_PEER=''
TREASURY=0xfE4800cA5a48670cc5f591a51F517BA8F682D4Ae
FEE_RECIPIENT=0xfE4800cA5a48670cc5f591a51F517BA8F682D4Ae
ENV
chmod 600 node.env
```

## 3. Новый genesis — только на A

```bash
cd ~/mcn-launch-6
./scripts/02-genesis.sh
cat consensus/launch.json
```

Создаёт execution/genesis.json, consensus/genesis.ssz и шесть зашифрованных ключей. Старт по умолчанию через два часа. До этого времени нужно успеть пройти шаги 4–7. Если не успеваешь, остановись до старта валидаторов и согласуй новый запуск; не генерируй отдельный genesis на B.

## 4. Перенос общих файлов и трёх ключей на B

На A (USER_B — SSH-пользователь нового сервера):

```bash
cd ~/mcn-launch-6
umask 077
tar -czf node-B-bootstrap.tar.gz \
  consensus/config.yaml consensus/genesis.ssz consensus/launch.json \
  execution/genesis.json GENESIS-SHA256SUMS validators/node-B
scp node-B-bootstrap.tar.gz USER_B@38.180.143.231:~/mcn-launch-6/
```

На B:

```bash
cd ~/mcn-launch-6
tar -xzf node-B-bootstrap.tar.gz
sha256sum -c GENESIS-SHA256SUMS
chmod -R go-rwx validators
```

На B не запускай 02-genesis.sh. На обоих вывод checksum должен быть OK:

```bash
cd ~/mcn-launch-6
sha256sum -c GENESIS-SHA256SUMS
./scripts/03-init.sh
./scripts/04-systemd.sh
```

На этом шаге запускаются только Geth и Beacon. Validator ещё остановлен.

## 5. Проверка доступности TCP в обе стороны

На A:

```bash
python3 - <<'PY'
import socket
for port in (30303,13000):
    with socket.create_connection(('38.180.143.231',port),timeout=5):
        print(port,'OK')
PY
```

На B:

```bash
python3 - <<'PY'
import socket
for port in (30303,13000):
    with socket.create_connection(('103.228.169.164',port),timeout=5):
        print(port,'OK')
PY
```

При timeout не запускай валидаторы. Сначала исправь связь. В run-beacon.sh уже добавлено LIBP2P_TCP_REUSEPORT=false, чтобы не использовать слушающий TCP-порт для исходящего подключения.

## 6. Соединение Geth и Beacon

На каждом получи его идентичность:

```bash
cd ~/mcn-launch-6
bin/geth --datadir=execution/data attach --exec 'admin.nodeInfo.enode' execution/data/geth.ipc
curl -fsS http://127.0.0.1:3500/eth/v1/node/identity | jq '.data | {peer_id,p2p_addresses}'
```

На A добавь enode B и TCP-multiaddr B. На B добавь enode A и TCP-multiaddr A. В командах ниже замени ENODE_OTHER и TCP_MULTIADDR_OTHER точными значениями из вывода другого сервера. Не копируй кавычки, окружающие JSON-строку, внутрь значения.

На каждом:

```bash
cd ~/mcn-launch-6
python3 tools/set-geth-peer.py 'ENODE_OTHER'
python3 tools/set-beacon-peer.py 'TCP_MULTIADDR_OTHER'
sudo systemctl restart mcn-geth mcn-beacon
```

Пример формата multiaddr A: /ip4/103.228.169.164/tcp/13000/p2p/PEER_ID_A. B: /ip4/38.180.143.231/tcp/13000/p2p/PEER_ID_B. ENR вручную не нужен.

Через 30 секунд на каждом:

```bash
cd ~/mcn-launch-6
bin/geth --datadir=execution/data attach --exec 'admin.peers.length' execution/data/geth.ipc
curl -fsS http://127.0.0.1:3500/eth/v1/node/peer_count | jq '.data'
curl -fsS http://127.0.0.1:3500/eth/v1/beacon/genesis | jq '.data'
```

Geth peers >=1, Beacon connected >=1 на обоих. Genesis time и validators root одинаковы. До genesis блок 0 и отсутствие финальности ожидаемы.

## 7. Запуск валидаторов — на обоих, только после проверки связи

```bash
sudo systemctl enable --now mcn-validator
sudo journalctl -u mcn-validator -n 25 --no-pager -l
```

Каждый wallet должен содержать три ключа. Никогда не запускай ключи B на A одновременно с B. На A сохранён комплект B для первоначального переноса, но run-validator.sh использует только wallet своей роли.

## 8. Проверка общей цепи и финальности

После genesis на обоих:

```bash
cd ~/mcn-launch-6
./scripts/05-check.sh
```

Все шесть валидаторов active_ongoing, peers есть на обоих слоях, блоки растут. Примерно через 3–4 эпохи (19–26 минут) ожидаем finalized.epoch >0 и дальнейший рост. Это ориентир, а не подтверждение здорового состояния: сравни finalized root на обоих.

```bash
curl -fsS http://127.0.0.1:3500/eth/v1/beacon/states/head/finality_checkpoints | jq '.data'
```

Когда оба execution узла прошли блок 10, сравни его hash:

```bash
cd ~/mcn-launch-6
bin/geth --datadir=execution/data attach --exec 'eth.getBlock(10).hash' execution/data/geth.ipc
```

Хеши должны совпасть. При 3+3 валидаторах каждый сервер содержит 50% начального стейка: для нормальной финальности нужны оба сервера, четыре из шести одинаково взвешенных валидаторов должны корректно голосовать.

Публичный RPC и DNS настраивай после подтверждения общей цепи. Дополнительные команды и nginx-конфигурация находятся в README.md и nginx/.
