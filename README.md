# OpenSeaArchive

Single-file local utility for comparing OpenSea created/owned items against a Sup/p2fk keyword and optionally etching missing IPFS references with the SupSpace-style testnet3 wallet flow.

OpenSea owned-item queries include hidden items on every page of results.

Each open page shares a mempool limit of 10 request attempts per rolling 10 seconds across balances, UTXOs, fee estimates, transaction broadcasts, and confirmation checks. Concurrent identical reads share a request. HTTP 429 pauses new attempts for at least 10 seconds, or longer if the server exposes a longer `Retry-After` header.

The app starts with `https://mempool.space/testnet/api` (or your configured Testnet3 API first). If an endpoint times out after 10 seconds, is unreachable, or returns a server error, the app tries the next endpoint and uses it for new requests. The 47 regional hosts from the [Mempool monitoring dashboard](https://monitoring.mempool.space/) all use `/testnet/api`; the app never automatically switches to mainnet or Testnet4.
