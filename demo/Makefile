nodes = 4
txs = 10

up: conf start

# generate keys and peers.json file
conf:
	rm -rf conf
	./scripts/build-conf.sh $(nodes)

# launch testnet
start:
	./scripts/run-testnet.sh $(nodes)

# start demo application
demo:
	./scripts/demo.sh $(nodes)

# stop testnet
stop: 
	./scripts/stop-testnet.sh

# send a bunch of transactions
bombard:
	./scripts/bombard.sh $(nodes) $(txs)

.PHONY: up conf start stop bombard