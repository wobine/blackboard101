# This code is used for educational purposes only. Written by wobine for a bitcoin101 video
# 

import hashlib, re, sys, os, base64, time, random, hmac, urllib2, json
from bitcoinrpc.util import *
from bitcoinrpc.exceptions import *
from bitcoinrpc.__init__ import *
from bitcoinrpc.config import *
from bitcoinrpc.proxy import *
from bitcoinrpc.data import *
from bitcoinrpc.connection import *


bitcoin = connect_to_local()
add = [1,1,1]
privkey = [1,1,1]
pubkey = [1,1,1]
mid = "\",\""
multisigprivkeyone = "L4VKzfujD6sTdWDsBMYUYWib4kFezuRNoJWNbzqYpQxgXtYJdiUP"
multisigprivkeytwo = "L3cYbSShrexaL64N7psvDMJ7617RfeVRAurZH6KMssh9qT4pS5kp"



"""
multsigtransact = '29d0e0e00d8a565817a9b550f254b0939010ba6ab1b5dfd215d38eefca74eca6'
testtransaction = 'bd488ce0d9bae299cfb83c418046a1dc61c79b34f071d66aa491292400675ea3'

print
print
rawtx = bitcoin.getrawtransaction (testtransaction)
dectx = bitcoin.decoderawtransaction(rawtx)
#print dectx
print
print dectx["vout"][0]
print
print dectx["vin"][0]
print
print
"""
unspent = bitcoin.listunspent()

#unspentfake = [ { "txid" : "2aac61e171fbe68076841d633948425d62bbb184303c289ca54dfd671c1349ab", "vout" : 0, "address" : "14P7Rkr393vwZrfXZrMizTsGP2BE9tfms8", "account" : "thing one", "scriptPubKey" : "76a9142516e4b2f3458b93d570ff0928911409463c7b3988ac", "amount" : 0.00147100, "confirmations" : 1149 }, { "txid" : "88faf4634b810a6e73238c8cdb7b953dc51362e35bc70f37e9ee12f3058bd3f2", "vout" : 0, "address" : "17majtRMjCjpSCasbXFxWiHWAmzLTSdtga", "account" : "thing two", "scriptPubKey" : "76a9144a3f38a56340577101b85c748b62e7922aaa5a3b88ac", "amount" : 0.00136500, "confirmations" : 8 } ]


print "Your Bitcoin-QT/d has",len(unspent),"unspent outputs"
for i in range(0, len(unspent)):
    print
    print "Output",i+1,"has",unspent[i]["amount"],"bitcoins, or",int(unspent[i]["amount"]*100000000),"satoshis"
    print "The transaction id for output",i+1,"is"
    print unspent[i]["txid"]
    print "The ScriptPubKey is", unspent[i]["scriptPubKey"]
    print "on Public Address",unspent[i]["address"]

print
totalcoin = int(bitcoin.getbalance()*100000000)
print "The total value of unspent satoshis is", totalcoin
print

WhichTrans = int(raw_input('Spend from which output? '))-1
if WhichTrans > len(unspent):
    print "Sorry that's not a valid output"
else:
    temp = str(unspent[WhichTrans]["address"])
    ismulti = int(temp[0:1])
    print
    if ismulti == 1:
        print "The receivng address on that tx starts with a",ismulti,"- its not multisig."
    elif ismulti== 3:
        print "The receivng address on that tx starts with a",ismulti,"which makes it a multisig."
        print "For a multisig spend we need 3 things : txid, scriptPubKey and redeemScript"
        print
        print "The txid is:",unspent[WhichTrans]["txid"]
        print "The ScriptPubKey is:", unspent[WhichTrans]["scriptPubKey"]
        print "And only multisigs have redeemScripts."
        print "The redeemScript is:",unspent[WhichTrans]["redeemScript"]
        print
        print "You have",int(unspent[WhichTrans]["amount"]*100000000),"satoshis in this output."
        HowMuch = int(raw_input('How much do you want to spend? '))
        if HowMuch > int(unspent[WhichTrans]["amount"]*100000000):
            print "Sorry not enough funds in that account"
        else:
            SendAddress = '17majtRMjCjpSCasbXFxWiHWAmzLTSdtga'
            #SendAddress = str(raw_input('To What Address '))
            print
            print "This send to",SendAddress,"will leave", int(unspent[WhichTrans]["amount"]*100000000) - HowMuch,"Satoshis in your accounts"
            print
            print "Creating the raw transaction"
            print
            
            rawtransact = bitcoin.createrawtransaction ([{"txid":unspent[WhichTrans]["txid"],
                    "vout":unspent[WhichTrans]["vout"],
                    "scriptPubKey":unspent[WhichTrans]["scriptPubKey"],
                    "redeemScript":unspent[WhichTrans]["redeemScript"]}],{SendAddress:0.0001})
            print "bitcoind decoderawtransaction", rawtransact
            print
            print "And now we'll sign the raw transaction -> this isn't final"
            print
            signedone = bitcoin.signrawtransaction (rawtransact,
                    [{"txid":unspent[WhichTrans]["txid"],
                    "vout":0,"scriptPubKey":unspent[WhichTrans]["scriptPubKey"],
                    "redeemScript":unspent[WhichTrans]["redeemScript"]}],
                    [multisigprivkeyone])
            print signedone
            print
            print signedone["hex"]
            print
            print bitcoin.signrawtransaction (signedone["hex"],
                    [{"txid":unspent[WhichTrans]["txid"],
                    "vout":0,"scriptPubKey":unspent[WhichTrans]["scriptPubKey"],
                    "redeemScript":unspent[WhichTrans]["redeemScript"]}],
                    [multisigprivkeytwo])

            
            #print "The following is a regular transaction - not multisig"
            #print "bitcoind createrawtransaction", bitcoin.createrawtransaction([{"txid": unspent[WhichTrans]["txid"],
            #        "vout": unspent[WhichTrans]["vout"]}],
            #        {SendAddress : HowMuch})

"""
bitcoind signrawtransaction (signedone["hex"],[{"txid":unspent[WhichTrans]["txid"],"vout":0,"scriptPubKey":unspent[WhichTrans]["scriptPubKey"],"redeemScript":unspent[WhichTrans]["redeemScript"]}],["1FKYGkc56CdMNm8E3ZGGH7566371nMntCs"]
"""
        


