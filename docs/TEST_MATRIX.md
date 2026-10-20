# Test results

## Locally reproduced

| Check | Result |
|---|---|
| Contract compilation → creation/runtime bytecode, ABI and storage layout | PASS |
| Genesis configuration, SSZ validator registry root and initial supply | PASS |
| Deposit storage and upstream system-contract bytecodes | PASS |
| Geth genesis initialization and block hash | PASS |
| Deposit EVM tests: minimum amount, amount units, lengths, data root, event/index/count and effective-cap distinction | 8 tests passed |

Commands, environment and raw outputs are in [evidence/local/RESULTS.md](../evidence/local/RESULTS.md). These checks run locally; they are separate from live-network tests.

## Network checks reported by the operator

- Deposits and validator activation work.
- Validator exit and withdrawals, including partial withdrawals, work.
- Finality advances with the configured 10-second slots.
- The beacon explorer reports an effective balance of 100,000 MCN for the supplied current validator example.

These network results are based on the operator's testing. The local test artifacts do not contain a separate end-to-end receipt bundle for those operations. Transaction hashes and relevant states can be supplied to the auditor for reproduction.
