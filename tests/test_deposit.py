"""EVM boundary tests against the exact MCN genesis preallocation; no live keys."""
import hashlib
import json
import unittest
from pathlib import Path
from eth_tester import EthereumTester, PyEVMBackend
from eth_utils import keccak
from eth_abi import encode, decode
from py_ecc.bls import G2ProofOfPossession as BLS

ROOT = Path(__file__).resolve().parents[1]
ADDR = '0x00000000219ab540356cBB839Cbe05303d7705Fa'
SHA = lambda b: hashlib.sha256(b).digest()

def root_for(pk, credentials, signature, amount):
    pk_root = SHA(pk + bytes(16))
    sig_root = SHA(SHA(signature[:64]) + SHA(signature[64:] + bytes(32)))
    return SHA(SHA(pk_root + credentials) + SHA(amount.to_bytes(8, 'little') + bytes(24) + sig_root))

class DepositTests(unittest.TestCase):
    def setUp(self):
        genesis = json.loads((ROOT / 'network/genesis.json').read_text())
        alloc = {k.lower().removeprefix('0x'): v for k,v in genesis['alloc'].items()}[ADDR[2:].lower()]
        state = PyEVMBackend.generate_genesis_state()
        state[bytes.fromhex(ADDR[2:])] = dict(balance=0, nonce=int(alloc['nonce'], 0), code=bytes.fromhex(alloc['code'][2:]), storage={int(k,16):int(v,16) for k,v in alloc['storage'].items()})
        self.chain = EthereumTester(PyEVMBackend(genesis_state=state))
        self.sender = self.chain.get_accounts()[0]
        # Public deterministic LAB key, never usable for production validators.
        self.pk = BLS.SkToPk(1)
        self.credentials = bytes.fromhex('02'+'00'*11+'11'*20)

    def view(self, signature):
        raw = self.chain.call({'from':self.sender, 'to':ADDR,'data':'0x'+keccak(text=signature)[:4].hex()})
        return bytes.fromhex(raw[2:])

    def deposit(self, amount, *, pk=None, credentials=None, signature=None, bad_root=False, dust=0):
        pk = self.pk if pk is None else pk
        credentials = self.credentials if credentials is None else credentials
        # DepositMessage signing root, DOMAIN_DEPOSIT, genesis fork 0x23251000.
        message = SHA(SHA(self.pk+bytes(16)) + self.credentials)
        message = SHA(message + SHA(amount.to_bytes(8,'little')+bytes(24)+bytes(32)))
        fork_data = SHA(bytes.fromhex('23251000')+bytes(28)+bytes(32))
        domain = bytes.fromhex('03000000') + fork_data[:28]
        signature = BLS.Sign(1, SHA(message+domain)) if signature is None else signature
        root = root_for(pk, credentials, signature, amount) if len(pk)==48 and len(credentials)==32 and len(signature)==96 else bytes(32)
        if bad_root: root=bytes(32)
        data=keccak(text='deposit(bytes,bytes,bytes,bytes32)')[:4]+encode(['bytes','bytes','bytes','bytes32'],[pk,credentials,signature,root])
        h=self.chain.send_transaction({'from':self.sender,'to':ADDR,'value':amount*10**9+dust,'gas':1000000,'data':'0x'+data.hex()})
        return self.chain.get_transaction_receipt(h)

    def test_genesis_count_and_root(self):
        self.assertEqual(decode(['bytes'],self.view('get_deposit_count()'))[0], bytes(8))
        z=bytes(32)
        for _ in range(32):z=SHA(z+z)
        self.assertEqual(self.view('get_deposit_root()'), SHA(z+bytes(32)))

    def test_minimum_rejects_249_accepts_250(self):
        self.assertEqual(self.deposit(249*10**9)['status'],0)
        r=self.deposit(250*10**9)
        self.assertEqual(r['status'],1)
        fields=decode(['bytes','bytes','bytes','bytes','bytes'],bytes.fromhex(r['logs'][0]['data'][2:]))
        self.assertEqual(int.from_bytes(fields[2],'little'),250*10**9)
        self.assertEqual(int.from_bytes(fields[4],'little'),0)
        self.assertEqual(decode(['bytes'],self.view('get_deposit_count()'))[0],(1).to_bytes(8,'little'))

    def test_activation_threshold_is_not_contract_minimum(self):
        self.assertEqual(self.deposit(10000*10**9)['status'],1)

    def test_effective_cap_is_not_deposit_ceiling(self):
        self.assertEqual(self.deposit(100001*10**9)['status'],1)

    def test_non_gwei_amount_rejected(self):
        self.assertEqual(self.deposit(250*10**9,dust=1)['status'],0)

    def test_wrong_root_rejected(self):
        self.assertEqual(self.deposit(250*10**9,bad_root=True)['status'],0)

    def test_malformed_lengths_rejected(self):
        for override in [{'pk':bytes(47)},{'credentials':bytes(31)},{'signature':bytes(95)}]:
            with self.subTest(override=list(override)):
                self.assertEqual(self.deposit(250*10**9,**override)['status'],0)

    def test_bls_verification_is_consensus_responsibility(self):
        # Correct data root with invalid proof is accepted by upstream deposit design.
        # This does NOT assert that Prysm would activate this invalid validator.
        self.assertFalse(BLS.Verify(self.pk,bytes(32),bytes(96)))
        self.assertEqual(self.deposit(250*10**9,signature=bytes(96))['status'],1)

if __name__=='__main__':unittest.main()
