# Чистый запуск: сначала прочитай START-HERE.md

# MCN Blockchain: полный порядок запуска

Комплект для **двух Ubuntu 24.04 x86_64 серверов**, Geth **1.17.6** и Prysm **7.2.0**. На A работают Geth, Beacon и ключи валидаторов 0–2; на B — Geth, Beacon и ключи 3–4. Всё ниже выполняется от обычного пользователя с sudo. Генерация ключей и genesis выполняется **один раз на A**, затем один и тот же genesis копируется на B.

## 1. Зафиксированные параметры

| Параметр | Значение |
|---|---|
| Название / native coin | MCN Blockchain / MCN |
| Chain ID / Network ID | 2325 / 2325 |
| Decimals | 18 |
| Consensus | PoS, Geth + Prysm |
| Слот / epoch | 12 сек / 32 слота = 384 сек |
| Стартовые валидаторы | 6 случайных BLS ключей |
| Минимум активации | 10 000 MCN |
| Максимальный effective balance для compounding | 640 000 MCN |
| Минимальный депозит / шаг effective balance | 250 / 250 MCN |
| Ejection balance | 8 000 MCN |
| Стартовая base fee | 1 Gwei |
| Genesis gas limit | 30 000 000 — выбранный начальный лимит MCN |
| Газ после genesis | Обычная динамика Ethereum; target Geth 30 млн, заданный пользователем |
| EIP-1559 | Штатный, без фиксации комиссии в USD |
| Forks при старте | Prague / Electra; более ранние форки также активны |
| Первый upgrade | Osaka / Fulu на epoch 1: genesis + 384 сек |
| Будущие форки | Gloas / Amsterdam пока не назначены |
| Начальная общая сумма | 120 000 000 MCN |
| Liquid allocation treasury | 119 940 000 MCN |
| Премайн стейка в consensus | 6 × 10 000 = 60 000 MCN |

Адрес из прошлой переписки: `0xfE4800cA5a48670cc5f591a51F517BA8F682D4Ae`. Он получает liquid allocation, комиссии proposer и withdrawals шести genesis валидаторов. Его приватный ключ должен быть у владельца. Если нужен другой адрес, поменяй TREASURY и FEE_RECIPIENT **до** этапа 4.

120 млн — **начальное предложение**. Ethereum rewards/burn дальше меняют supply; жёсткий cap этим комплектом не реализован. Пять ключей и два сервера — исходная сеть для проверки запуска. При равном стейке для финальности нужны минимум четыре ключа; при распределении 3/2 отказ любого сервера остановит финальность.

Prysm 7.2.0 при `--fork=fulu` оставляет genesis proposer lookahead нулевым. Поэтому комплект начинает с Electra и выполняет штатный переход Fulu на epoch 1; этот переход вычисляет корректное расписание proposer без патча клиента. Время Osaka на execution layer равно времени того же перехода.

## 2. Файлы

```text
mcn-pos/
├── README.md
├── requirements.txt
├── node.env.example
├── node.env                         # создаёшь отдельно на каждом сервере
├── bin/                             # скачивает 01-install.sh
│   ├── geth
│   ├── beacon-chain
│   ├── validator
│   └── prysmctl
├── consensus/
│   ├── config.yaml                  # готовые chain parameters
│   ├── deposit_data.json            # генерируется из случайных ключей
│   ├── genesis.ssz                  # генерирует prysmctl
│   ├── genesis-state.json           # JSON для проверки genesis
│   ├── launch.json                  # время, supply, публичные ключи
│   ├── wallet/                      # импортированный Prysm wallet
│   ├── beacon-data/
│   └── validator-data/               # включая slashing protection
├── execution/
│   ├── genesis-input.json           # исходный EL genesis
│   ├── genesis.json                 # согласованный EL genesis от prysmctl
│   ├── peers.toml                   # постоянный Geth peer на B
│   └── data/
├── validators/
│   ├── node-A/{keystores/,password.txt}
│   └── node-B/{keystores/,password.txt}
├── secrets/jwt.hex                  # собственный JWT каждого сервера
├── contracts/
│   ├── deposit_contract.sol         # минимум депозита 250 MCN
│   ├── deposit-artifact.json        # ABI, init bytecode, runtime, layout
│   ├── system-alloc.json            # EIP-4788 / 2935 / 7002 / 7251
│   ├── PROVENANCE.md
│   └── UPSTREAM-LICENSE.md
├── tools/
│   ├── prepare.py                   # ключи, EIP-2335, deposits, EL allocation
│   ├── verify-genesis.py
│   ├── verify-rpc.py
│   └── set-geth-peer.py
├── scripts/
│   ├── 01-install.sh
│   ├── 02-genesis.sh
│   ├── 03-init.sh
│   ├── 04-systemd.sh
│   ├── 05-check.sh
│   ├── run-geth.sh
│   ├── run-beacon.sh
│   └── run-validator.sh
├── systemd/mcn-{geth,beacon,validator}.service
├── nginx/rpc.mcnchain.org.conf
└── GENESIS-SHA256SUMS
```

`genesis.ssz`, ключи и `genesis.json` создаются на твоём сервере. Архив содержит генератор и конфигурацию; тестовые приватные ключи в него не включены.

## 3. Подготовка обоих серверов

Используй новый каталог `~/mcn-pos`. Скопируй архив на оба сервера. На каждом:

```bash
sudo apt-get update
sudo apt-get install -y curl ca-certificates python3 python3-venv openssl jq tar unzip chrony
sudo systemctl enable --now chrony
unzip mcn-launch-6.zip
mv mcn-launch-6 mcn-pos
cd ~/mcn-pos
chmod +x scripts/*.sh
./scripts/01-install.sh
cp node.env.example node.env
chmod 600 node.env
nano node.env
```

Если домашний каталог другой, расположи распакованный комплект в `~/mcn-pos`. На A поставь `NODE_ROLE=A`, на B — `NODE_ROLE=B`. `PUBLIC_IP` — IP текущего сервера. На A `BEACON_BOOTNODE` и `BEACON_PEER` пока пустые. На B их заполним на этапе 7. Значения ENR/multiaddr в node.env заключай в одинарные кавычки.

Для стартовой проверки ориентир на каждый сервер: 4 vCPU, 8–16 GB RAM, SSD и синхронизированное время. Расход диска зависит от активности сети.

Если используется UFW, сохрани свой SSH-порт, затем разреши P2P. Для стандартного SSH 22:

```bash
sudo ufw allow 22/tcp
sudo ufw allow 30303/tcp
sudo ufw allow 30303/udp
sudo ufw allow 13000/tcp
sudo ufw allow 13000/udp
sudo ufw allow 12000/udp
sudo ufw status
```

Те же порты разреши в firewall хостинга. `8545`, `8551`, `3500`, `4000` остаются на localhost. Если UFW ещё выключен, включай его после проверки правила для фактического SSH-порта.

## 4. Ключи и оба genesis — только сервер A

```bash
cd ~/mcn-pos
./scripts/02-genesis.sh
cat consensus/launch.json
cat GENESIS-SHA256SUMS
```

По умолчанию genesis назначается через час. Можно сразу выделить два часа:

```bash
GENESIS_TIME=$(( $(date +%s) + 7200 )) ./scripts/02-genesis.sh
```

Выбери одну из двух команд. Повторный запуск защищён от перезаписи ключей. `prepare.py` создаёт шесть случайных BLS ключей, EIP-2335 keystore, пароли и подписанные deposit data. Приватные ключи не выводятся в терминал. Genesis валидаторы получают withdrawal credentials `0x02`, то есть compounding, на TREASURY.

Реальная команда генерации двух согласованных genesis, уже записанная в скрипте:

```bash
bin/prysmctl testnet generate-genesis \
  --chain-config-file=consensus/config.yaml \
  --deposit-json-file=consensus/deposit_data.json \
  --num-validators=6 \
  --fork=electra \
  --genesis-time="$GENESIS_TIME" \
  --geth-genesis-json-in=execution/genesis-input.json \
  --geth-genesis-json-out=execution/genesis.json \
  --output-ssz=consensus/genesis.ssz \
  --output-json=consensus/genesis-state.json
```

Это фрагмент скрипта: переменная GENESIS_TIME задаётся внутри него. При ручном исполнении сначала задай её равной `genesis_time` из `consensus/launch.json`. Используется именно `--chain-config-file`, а `--deposit-json-file` обеспечивает соответствие genesis настоящим ключам.

В execution genesis встроены системные контракты актуальных форков и контракт депозитов. Начальный deposit tree пустой, шесть genesis валидаторов добавлены через premine в consensus state. Их 60 000 MCN вычтены из liquid allocation. Вконтрактный перевод этих шести депозитов после старта не требуется.

## 5. Перенос на сервер B

На A:

```bash
cd ~/mcn-pos
tar -czf node-B-bootstrap.tar.gz \
  consensus/config.yaml consensus/genesis.ssz consensus/launch.json \
  execution/genesis.json GENESIS-SHA256SUMS validators/node-B
scp node-B-bootstrap.tar.gz USER_B@IP_B:~/mcn-pos/
```

Замени USER_B и IP_B на SSH-пользователя и IP сервера B. При другом SSH-порте используй `scp -P PORT ...`.

На B:

```bash
cd ~/mcn-pos
tar -xzf node-B-bootstrap.tar.gz
sha256sum -c GENESIS-SHA256SUMS
chmod -R go-rwx validators
```

На B **не выполняй 02-genesis.sh**. Общие файлы EL/CL genesis должны совпадать байт в байт. JWT на B будет создан локально: он обязан совпадать между Geth и Beacon одного сервера.

## 6. Инициализация обоих серверов

На A и B:

```bash
cd ~/mcn-pos
./scripts/03-init.sh
```

Скрипт проверяет checksum, создаёт локальный JWT, выполняет `geth init` и импортирует только ключи своего NODE_ROLE в wallet.

Команды внутри него:

```bash
bin/geth --datadir=execution/data --state.scheme=path init execution/genesis.json

bin/validator accounts import \
  --wallet-dir=consensus/wallet \
  --keys-dir="validators/node-$NODE_ROLE/keystores" \
  --account-password-file="validators/node-$NODE_ROLE/password.txt" \
  --wallet-password-file="validators/node-$NODE_ROLE/password.txt" \
  --accept-terms-of-use
```

При ручном исполнении сначала `source node.env`.

## 7. Первый старт и соединение узлов

Сначала A:

```bash
cd ~/mcn-pos
./scripts/04-systemd.sh
sudo systemctl status mcn-geth mcn-beacon mcn-validator --no-pager
```

Получить execution enode и Beacon ENR:

```bash
bin/geth --datadir=execution/data attach --exec 'admin.nodeInfo.enode' execution/data/geth.ipc
curl -fsS http://127.0.0.1:3500/eth/v1/node/identity | jq '.data'
```

Если Beacon API ещё не отвечает, проверь `journalctl -u mcn-beacon -n 60 --no-pager` и повтори запрос после старта API. Для Geth используй enode с публичным IP A и портом 30303; если напечатан внутренний адрес, замени только host, сохрани публичный ключ enode.

В `node.env` на B впиши:

```bash
BEACON_BOOTNODE='enr:...полный ENR сервера A...'
BEACON_PEER='/ip4/IP_A/tcp/13000/p2p/PEER_ID_A'
```

Полный multiaddr возьми из `p2p_addresses` ответа identity API A. Выбери TCP-адрес с публичным IP A; если IP в ответе внутренний, используй публичный IP с тем же peer ID. ENR уже содержит discovery UDP-port.

На B сохраняем постоянный execution peer и запускаем сервисы:

```bash
cd ~/mcn-pos
python3 tools/set-geth-peer.py 'enode://PUBLIC_KEY_A@IP_A:30303'
./scripts/04-systemd.sh
sudo systemctl status mcn-geth mcn-beacon mcn-validator --no-pager
```

Скрипт создаст `execution/peers.toml`; run-geth.sh читает его при каждом старте. `--p2p-static-id` сохраняет Beacon peer ID между рестартами.

## 8. Команды запуска каждого процесса

Для systemd используется содержимое следующих файлов. Для ручного запуска открой три отдельных терминала на каждом сервере:

```bash
cd ~/mcn-pos
./scripts/run-geth.sh
```

```bash
cd ~/mcn-pos
./scripts/run-beacon.sh
```

```bash
cd ~/mcn-pos
./scripts/run-validator.sh
```

Сначала останови соответствующие systemd сервисы, если переходишь на ручной запуск:

```bash
sudo systemctl stop mcn-validator mcn-beacon mcn-geth
```

Подробные CLI-аргументы находятся в самих трёх `run-*.sh`; там нет майнинга Clique, разблокировки EOA или старых interop-флагов. Proposer fee recipient передаётся validator client, Engine API Geth доступен только локальному Beacon через JWT.

## 9. Проверка запуска

На обоих серверах:

```bash
cd ~/mcn-pos
./scripts/05-check.sh
sudo journalctl -u mcn-geth -u mcn-beacon -u mcn-validator -n 100 --no-pager
```

Chain ID должен быть `0x915`. Peer count обоих слоёв после соединения — минимум 1. После назначенного genesis time номер execution block растёт, а все шесть ключей видны как активные.

Проверка финальности:

```bash
curl -fsS http://127.0.0.1:3500/eth/v1/beacon/states/head/finality_checkpoints | jq
curl -fsS http://127.0.0.1:3500/eth/v1/node/syncing | jq
```

Не считай запуск завершённым по одному сообщению `started`: нужен растущий block number **и** рост finalized epoch. Epoch длится 6 мин 24 сек; первая финальность требует нескольких эпох. У шести ключей sparse committees, поэтому проверяй реальное участие, а не обещание финальности по таймеру.

Проверка одинаковой исходной истории на A и B:

```bash
curl -fsS http://127.0.0.1:8545 \
  -H 'Content-Type: application/json' \
  --data '{"jsonrpc":"2.0","id":1,"method":"eth_getBlockByNumber","params":["0x0",false]}' | jq '.result.hash'
```

Хеши должны совпасть. Дополнительная проверка EL/CL header на A:

```bash
python3 tools/verify-rpc.py
```

Проверка allocation:

```bash
curl -fsS http://127.0.0.1:8545 \
  -H 'Content-Type: application/json' \
  --data '{"jsonrpc":"2.0","id":1,"method":"eth_getBalance","params":["0xfE4800cA5a48670cc5f591a51F517BA8F682D4Ae","0x0"]}' | jq
```

Для запуска сети доступ к приватному ключу treasury не нужен. Для первого денежного перевода подпиши транзакцию из своего кошелька treasury: Chain ID 2325, валюта MCN, 18 decimals. Geth через RPC принимает подписанные raw transactions; premine не создаёт и не разблокирует treasury key.

## 10. Публичный RPC и MetaMask

После проверки роста блоков и финальности на A:

1. Создай DNS A-запись `rpc.mcnchain.org` на публичный IP A.
2. Открой 80/tcp и 443/tcp в firewall хостинга и UFW.
3. Установи Nginx и сертификат:

```bash
sudo apt-get install -y nginx certbot python3-certbot-nginx
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo install -m 644 nginx/rpc.mcnchain.org.conf /etc/nginx/sites-available/rpc.mcnchain.org
sudo ln -s /etc/nginx/sites-available/rpc.mcnchain.org /etc/nginx/sites-enabled/rpc.mcnchain.org
sudo nginx -t
sudo systemctl reload nginx
sudo certbot --nginx -d rpc.mcnchain.org
```

Если symlink уже существует, пропусти `ln -s`. Certbot запросит email и настройки HTTPS.

Проверка:

```bash
curl -fsS https://rpc.mcnchain.org \
  -H 'Content-Type: application/json' \
  --data '{"jsonrpc":"2.0","id":1,"method":"eth_chainId","params":[]}'
```

В MetaMask добавь сеть:

```text
Network name: MCN Blockchain
RPC URL: https://rpc.mcnchain.org
Chain ID: 2325
Currency symbol: MCN
```

Explorer URL добавляется после отдельного развёртывания explorer и проверки его индексации; в этом комплекте развернуты blockchain nodes и RPC. Сайт `mcnchain.org` и explorer требуют отдельного приложения.

## 11. Остановка, рестарт, резервная копия

```bash
sudo systemctl stop mcn-validator mcn-beacon mcn-geth
sudo systemctl start mcn-geth mcn-beacon mcn-validator
sudo systemctl restart mcn-beacon
sudo journalctl -u mcn-validator -f
```

Для согласованной резервной копии сначала останови три сервиса, сохрани `validators/`, `consensus/wallet/`, `consensus/validator-data/` со slashing protection, оба genesis, config и launch.json. Пароли сохраняй вместе с зашифрованными keystore в защищённой копии. Один validator key должен подписывать на одном сервере; при переносе сначала останови исходный validator и перенеси историю slashing protection.

Если время genesis уже прошло во время установки, сохрани текущие ключи и genesis и запусти сеть: клиенты умеют обработать прошедшие пустые слоты. Если нужна принципиально новая сеть, используй новый каталог и новый Chain ID; не перезаписывай работающий genesis и базы.

## 12. Что проверено при сборке

Проверены генерация случайных BLS ключей и подписи депозитов, создание Electra genesis через release prysmctl 7.2.0, совпадение ключей/балансов/withdrawal credentials, суммы предложения, времени EL/CL forks, импорт keystore в release Prysm wallet, выполнение контракта в тестовой EVM, bash syntax и Python syntax.

Контракт с preallocated constructor storage возвращает правильный пустой deposit root/count, отклоняет 249 MCN и принимает корректный депозит 10 000 MCN с событием. Результат полноценного запуска двух узлов и финальности см. VALIDATION.md. Установка на твоих VPS здесь не выполнялась.

Источники:
- https://github.com/OffchainLabs/prysm/blob/v7.2.0/cmd/prysmctl/testnet/generate_genesis.go
- https://github.com/OffchainLabs/prysm/blob/v7.2.0/INTEROP.md
- https://github.com/OffchainLabs/prysm/blob/v7.2.0/config/params/config.go
- https://github.com/OffchainLabs/prysm/releases/tag/v7.2.0
- https://github.com/ethereum/go-ethereum/releases/tag/v1.17.6
- https://github.com/ethereum/go-ethereum/blob/v1.17.6/params/config.go
- https://github.com/ethereum/go-ethereum/blob/v1.17.6/params/protocol_params.go
