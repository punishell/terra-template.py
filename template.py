from terra_sdk.client.localterra import LocalTerra
from terra_sdk.core.wasm import msgs
from terra_sdk.core.wasm.msgs import MsgExecuteContract, MsgInstantiateContract
from terra_sdk.util.contract import read_file_as_b64, get_code_id, get_contract_address
from terra_sdk.core.auth import StdFee
from terra_sdk.core.wasm import MsgStoreCode



lt = LocalTerra()

deployer = lt.wallets["test1"]
addres_1 = lt.wallets["test2"]

def store_contract(contract_path: str) -> str:
    contract_bytes = read_file_as_b64(f"{contract_path}")
    store_code =MsgStoreCode(
        deployer.key.acc_address,
        contract_bytes
    )
    tx = deployer.create_and_sign_tx(
        msgs=[store_code], fee=StdFee(4000000, "10000000uluna")
    )
    result = lt.tx.broadcast(tx)
    code_id = get_code_id(result)
    #print(result)
    return code_id

def initate_contract(code_id: str, init_msg)->str:
    initiate = MsgInstantiateContract(
        sender=deployer.key.acc_address,
        admin=deployer.key.acc_address, #ASK Louis 
        code_id=code_id,
        init_msg=init_msg
    )
    tx = deployer.create_and_sign_tx(
        msgs=[initiate], fee=StdFee(4000000, "10000000uluna")
    )

    result = lt.tx.broadcast(tx)
    contract_address = get_contract_address(result)
    return contract_address
    
def execute_contract(sender:str, contrac_address:str, execute_msg):
    execute = MsgExecuteContract(
    sender=sender.key.acc_address,
    contract=contrac_address,
    execute_msg=execute_msg
    )
    tx = sender.create_and_sign_tx(
        msgs=[execute], fee=StdFee(4000000, "10000000uluna")
    )
    result = lt.tx.broadcast(tx)
    return result
