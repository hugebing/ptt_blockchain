#coding = utf-8
from binascii import hexlify, unhexlify
from coincurve import PublicKey
from web3 import Web3
import web3
from web3 import exceptions
import sha3


def keccak(data):
    k = sha3.keccak_256()
    k.update(data)
    return k.digest()

#私鑰轉成錢包地址
def key_to_address(key):
    bytes_privkey = unhexlify(key)
    public_key = PublicKey.from_valid_secret(bytes_privkey).format(compressed=False)[1:]
    hexlify(public_key).decode()
    address = '0x' + hexlify(keccak(public_key)[-20:]).decode()
    address = Web3.toChecksumAddress(address)
    return address

#主要功能(說明在最下方)
def create_comunity(key, comunity_name):
    external_address = key_to_address(key)
    transaction = contract_ptt.functions.createComunity(
        comunity_name).buildTransaction({
        'gas': 8000000,
        'gasPrice': web3.toWei('100', 'gwei'),
        'from': external_address,
        'nonce': web3.eth.getTransactionCount(external_address),
        'value': 0,
        'chainId': 4
    })
    signed_txn = web3.eth.account.signTransaction(transaction, private_key=key)
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    tx_hash = tx_hash.hex()
    receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    print(receipt.status)

def create_article(key, comunity_name, article_title, article):
    external_address = key_to_address(key)

    transaction = contract_ptt.functions.createArticle(
        comunity_name, article_title, article).buildTransaction({
        'gas': 8000000,
        'gasPrice': web3.toWei('100', 'gwei'),
        'from': external_address,
        'nonce': web3.eth.getTransactionCount(external_address),
        'value': 0,
        'chainId': 4
    })
    signed_txn = web3.eth.account.signTransaction(transaction, private_key=key)
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    tx_hash = tx_hash.hex()
    receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    print(receipt.status)

def create_reply_message(key, comunity_name, article_title, reply_message):
    external_address = key_to_address(key)
    transaction = contract_ptt.functions.createReplyMessage(
        comunity_name, article_title, reply_message).buildTransaction({
        'gas': 8000000,
        'gasPrice': web3.toWei('100', 'gwei'),
        'from': external_address,
        'nonce': web3.eth.getTransactionCount(external_address),
        'value': 0,
        'chainId': 4
    })
    signed_txn = web3.eth.account.signTransaction(transaction, private_key=key)
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    tx_hash = tx_hash.hex()
    receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    print(receipt.status)

def create_article_cost(key, comunity_name, article_title, cost):
    external_address = key_to_address(key)
    transaction = contract_ptt.functions.createArticleCost(
        comunity_name, article_title, cost).buildTransaction({
        'gas': 8000000,
        'gasPrice': web3.toWei('100', 'gwei'),
        'from': external_address,
        'nonce': web3.eth.getTransactionCount(external_address),
        'value': 0,
        'chainId': 4
    })
    signed_txn = web3.eth.account.signTransaction(transaction, private_key=key)
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    tx_hash = tx_hash.hex()
    receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    print(receipt.status)

def pay_article(key, comunity_name, article_title):
    external_address = key_to_address(key)
    transaction = contract_ptt.functions.payArticle(
        comunity_name, article_title).buildTransaction({
        'gas': 8000000,
        'gasPrice': web3.toWei('100', 'gwei'),
        'from': external_address,
        'nonce': web3.eth.getTransactionCount(external_address),
        'value': 0,
        'chainId': 4
    })
    signed_txn = web3.eth.account.signTransaction(transaction, private_key=key)
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    tx_hash = tx_hash.hex()
    receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    print(receipt.status)


def get_comunity():
    output = contract_ptt.functions.getComunity().call()
    return output

def get_article_title(comunity_name):
    output = contract_ptt.functions.getArticleTitle(comunity_name).call()
    return output

def get_article(comunity_name, article_title, external_address):

    output = contract_ptt.functions.getArticle(comunity_name, article_title, external_address).call()
    return output

def get_reply_message(comunity_name, article_title):
    output = contract_ptt.functions.getReplyMessage(comunity_name, article_title).call()
    return output

def get_article_cost(comunity_name, article_title):
    output = contract_ptt.functions.getArticleCost(comunity_name, article_title).call()
    return output

def get_comunity_owner(comunity_name):
    output = contract_ptt.functions.getComunityOwner(comunity_name).call()
    return output

def get_article_owner(comunity_name, article_title):
    output = contract_ptt.functions.getArticleOwner(comunity_name, article_title).call()
    return output

def get_reply_message_owner(comunity_name, article_title, replyMessage):
    output = contract_ptt.functions.getReplyMessageOwner(comunity_name, article_title, replyMessage).call()
    return output

def get_article_license(comunity_name, article_title, external_address):
    output = contract_ptt.functions.getArticleLicense(comunity_name, article_title, external_address).call()
    return output

def total_supply():
    output = contract_ptt.functions.totalSupply().call()
    return output




#合約相關&Infura_URL的資料位置
contract_abi_path = "Contract_Related/Contract_ABI.txt"
contract_address_path = "Contract_Related/Contract_Address.txt"
infura_url_path = "Contract_Related/Infura_URL.txt"

#讀檔
abi_file = open(contract_abi_path, "r")
abi = abi_file.read()
contract_address_file = open(contract_address_path, 'r')
contract_address = contract_address_file.read()
# print(contract_address)
# print(type(contract_address))
infura_url_file = open(infura_url_path, 'r')
infura_url = infura_url_file.read()

web3 = Web3(Web3.HTTPProvider(infura_url))
contract_ptt = web3.eth.contract(address=contract_address, abi=abi)

##########################################測試####################################################

# create_comunity("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93", "資科系")
#
# create_comunity("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93", "應數系")
#
# create_comunity("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93", "政治大學")
#
# create_article("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93", "1 資科系", "區塊鏈課程老師詢問", "張宏慶老師好嗎?")
#
# create_article("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93", "1 資科系", "演算法課程老師詢問", "有推薦的老師嗎?")
#
# create_article("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93", "2 應數系", "有應數系八卦嗎?", "想知道八卦?")
#
# create_article("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93", "3 政治大學", "校狗好可愛", "(圖片)")
#
# get_comunity()
#
# get_article_title("1 資科系")
#
# get_article("1 資科系", "2 演算法課程老師詢問", key_to_address("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93"))
#
# get_article("2 應數系", "1 有應數系八卦嗎?", key_to_address("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93"))
#
# get_article("3 政治大學", "1 校狗好可愛", key_to_address("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93"))
#
# get_article("1 資科系", "1 區塊鏈課程老師詢問",key_to_address("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93"))
#
# create_reply_message("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93", "1 資科系", "1 區塊鏈課程老師詢問", "老師超棒的")
#
# create_reply_message("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93", "1 資科系", "1 區塊鏈課程老師詢問", "老師教得很好")
#
# create_reply_message("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93", "1 資科系", "1 區塊鏈課程老師詢問", "老師很認真")
#
# create_reply_message("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93", "2 應數系", "1 有應數系八卦嗎?", "閉嘴啦!")
#
# create_reply_message("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93", "3 政治大學", "1 校狗好可愛", "真的很可愛!")
#
# create_article_cost("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93", "2 應數系", "1 有應數系八卦嗎?", 1)
#
# pay_article("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93", "2 應數系", "1 有應數系八卦嗎?")
#
# get_article("2 應數系", "1 有應數系八卦嗎?", key_to_address("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93"))
#
# # 回傳bool
# get_article_license( "1 資科系", "1 區塊鏈課程老師詢問", key_to_address("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93"))
# get_article_license( "2 應數系", "1 有應數系八卦嗎?", key_to_address("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93"))
#
# get_article("2 應數系", "1 有應數系八卦嗎?", key_to_address("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93"))
#
# total_supply()

##########################################功能說明&參數說明#########################################################
# 功能說明
# 創造版 參數(私鑰, 版名)
# create_comunity("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93", "政治大學")
# 創造文章 參數(私鑰, 版名(要編號), 文章標題, 文章內容)
# print(key_to_address("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93"))
# create_article("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93", "1 資科系", "assssss", "sssssss")
# 創造回復 參數(私鑰, 版名(要編號), 文章標題(要編號), 回覆內容)
# create_reply_message("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93", "1 資科系", "1 區塊鏈課程老師詢問", "老師超棒的")
# 創造文章閱讀成本 參數(私鑰, 版名(要編號), 文章標題(要編號), 成本(int))
# create_article_cost("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93", "2 應數系", "1 有應數系八卦嗎?", 1)
# 閱讀成本付費 參數(私鑰, 版名(要編號), 文章標題(要編號))
# pay_article("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93", "2 應數系", "1 有應數系八卦嗎?")
#
# 查看所有版名
# get_comunity()
# 查看文章 參數(版名(要編號), 文章標題(要編號), external_address)
# print(get_article("1 資科系", "1 演算法課程老師詢問", key_to_address("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93")))
# 查看文章標題 參數(版名(要編號), 文章標題(要編號))
# get_article_title("1 資科系")
# 查看文章成本 參數(版名(要編號), 文章標題(要編號))
# get_article_cost("1 資科系", "1 演算法課程老師詢問")
# 查看文章回復 參數(版名(要編號), 文章標題(要編號))
# get_reply_message("1 資科系", "1 演算法課程老師詢問")
# 查看版擁有者 參數(版名(要編號))
# get_comunity_owner("1 資科系")
# 查看文章擁有者 參數(版名(要編號), 文章標題(要編號))
# print(get_article_owner("1 資科系", "1 區塊鏈課程老師詢問"))
# 查看回復擁有者 參數(版名(要編號), 文章標題(要編號), 文章回復(要編號))
# get_reply_message_owner("1 資科系", "1 區塊鏈課程老師詢問", "3 老師很認真")
# 查看address是否有購買文章的licensol)
# print(get_article_license( "2 應數系", "1 有應數系八卦嗎?", key_to_address("5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93")))
#
# 查看token發行量
# total_supply()


# 5163d6cb81a01eea9847caf2b4b48827d72fe906254739458cbed8c1a8274c93
# a878269a7d45e6d814168ed869a033e29a4a24ebf82f92d7c4c88ebf7204cf40
# a5343b4f734202d704525cb453964e16afc8e82f11453691a020718ffddf8f5c


