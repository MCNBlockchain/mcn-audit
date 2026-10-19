# Proposed auditor handoff

Project: MCN Blockchain, chain ID 2325, genesis 2026-10-17.

Please review the deposited-source/configuration snapshot identified by the supplied Git commit and SHA256SUMS. The requested scope is in SCOPE.md, open observations in RISK_REGISTER.md and pending evidence in RUNTIME_EVIDENCE.md.

MCN uses reported upstream Geth 1.17.6 and Prysm 7.2.0, custom consensus parameters (10-second slots, 100,000 MCN Electra effective cap), five genesis validators and a minimally changed genesis-preallocated deposit contract. The current operator controls all five initial validators.

Please estimate code/configuration review, integration testing, infrastructure/key-management review separately. Include retest terms and specify what is excluded from the proposed engagement.

Genesis effective balances differ from actual balances and require transition/economic review.

This submission does not claim audit completion or production readiness. The stablecoin/bridge/BNB token is not included in this contract scope. Private signing material and slashing databases will require a separate confidential review process; they are not in the source package.
