# Required test matrix

Status: **L = locally reproduced**, **P = pending current-network / isolated integration evidence**. An old network's successful test is not evidence for this genesis. Use an isolated clone for adversarial and destructive tests; avoid live signing conflicts.

| Test | Status | Acceptance evidence |
|---|---|---|
| Compiler source → creation/runtime/ABI/layout | L | Exact solc reproduction |
| Genesis files, validator registry root, supply, deposit storage/system code | L | Offline checker and Geth genesis hash |
| Minimum 249 rejected / 250 accepted | L | EVM receipt, event units, index/count |
| 10k accepted; above 100k accepted by contract | L | EVM receipts; consensus cap documented |
| Invalid lengths/root/non-gwei amount rejected | L | EVM rejection receipts |
| Contract accepts invalid BLS proof with correct data root | L | Negative proof test; consensus behavior NOT tested |
| Valid deposit → consumed request/log → validator activation | P | Same canonical chain, valid PoP, entry/status, epoch and balance |
| Invalid PoP cannot activate | P | CL rejection without funds/state accounting corruption |
| Genesis and post-genesis effective balance update | P | Epoch 0/1/later state comparison, 0x01/0x02 behavior |
| Partial withdrawal authorization/amount/queue/delay | P | Source credentials, requested gwei, queue eligibility, actual execution payout |
| Full exit and full withdrawal | P | Exit, withdrawable epoch, payout; no duplicate payment |
| Withdrawal wrong sender/unknown key/insufficient excess | P | Document request handling, no unauthorized payout |
| Reorg with deposits/requests/withdrawals | P | Canonical accounting, no duplicate processing |
| One validator offline and restored | P | Missed duties, penalty delta, continuous finality and safe catch-up |
| Two validators offline / partition / restoration | P | Expected finality behavior and eventual safe convergence |
| Double/surround vote / double proposal | P | Disposable lab keys only; inclusion/evidence and exact penalty accounting |
| 60M gas and geographic 10s-slot load | P | Representative workloads, resources, propagation, missed slots, finality |
| Archive historical balance + transaction trace | P | Repeated current deployment evidence, block/state roots |
| Public RPC and private Engine boundary | P | Approved method/error probes and config review |
| Restart/restore with protected slashing DB | P | Offline backup integrity and safe signing continuity |

Economics: use inherited Prysm constants plus MCN overrides, actual effective balances, participation and elapsed epochs. Record proposer/sync rewards, penalties, leakage and execution fees separately. APR projections are not security evidence.
