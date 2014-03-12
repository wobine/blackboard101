# wobine test file for multisignatures - to be used in a world bitcoin network piece

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

"""
testadd1 = '03e0882fb32689e4ba97f127955c8411dac1e9e20c2db7c442f217e09312d624f0'
testadd2 = '020b188c6eda59cb402bfc3b620c45d1fd539f2f72004ba8a1f76bfc1c297395e5'
testadd3 = '027f5fdde085f16def08448aca24c936df218a0e8f076edde86b84e52adad3dd1a'

jsonaddy = ["02fbb44ac7ebe193af79a308a6e515a9a07c3b87ce5a9d9e13d360d1c5084a4663","02249c64bc032e05fc9a26261b514bffdf46811bbb643fa464cecb49c0c93d661e","02dab7684652cd8ec57f8e003f500a80fd2bc0cdab13f3bfe4e8c79fce02d243ab"]

jsonaddy2 = "%s%s%s%s%s%s%s" % ('["',pubkey[0],mid,pubkey[1],mid,pubkey[2],'"]')
jsonaddy3 = [testadd1,testadd2,testadd3]


print bitcoin.addmultisigaddress(2,jsonaddy)
print bitcoin.addmultisigaddress(2,jsonaddy3)

"""

for i in range(0, 3):
    print
    print "Address Pair Number", i+1
    add[i] = bitcoin.getnewaddress()
    print "Public Address is",add[i]
    #print bitcoin.getreceivedbyaddress(add)
    #print bitcoin.listtransactions(address=add)
    privkey[i] = bitcoin.dumpprivkey(add[i])
    print "Private Key is ", privkey[i]

    #isolate the public key
    ee = str(bitcoin.validateaddress(add[i]))
    splitter = ee.split('pubkey=u')
    pubkey[i] = splitter[1][1:67]
    print "Public Key is",pubkey[i]

print
print "Paste the following into bitcoind creates multisig address"
print "%s%s%s%s%s%s%s" % ('bitcoind createmultisig 2 \'["',pubkey[0],mid,pubkey[1],mid,pubkey[2],'"]\'')

print
jsonaddy = [pubkey[0],pubkey[1],pubkey[2]]
print "The multisig address is"
multisigaddy = bitcoin.addmultisigaddress(2,jsonaddy)
multiaddyandredeem = bitcoin.createmultisig(2,jsonaddy)
print multisigaddy
print
print multiaddyandredeem




"""

Address Pair Number 1
Public Address is 16XUuhSaijsRVSJ2hNksjfDZuGiqRpXc1s
Private Key is  L4VKzfujD6sTdWDsBMYUYWib4kFezuRNoJWNbzqYpQxgXtYJdiUP
Public Key is 03e0882fb32689e4ba97f127955c8411dac1e9e20c2db7c442f217e09312d624f0

Address Pair Number 2
Public Address is 1L34Q7svtr3didC2CdYfwZJD3D84kED4RG
Private Key is  L3cYbSShrexaL64N7psvDMJ7617RfeVRAurZH6KMssh9qT4pS5kp
Public Key is 020b188c6eda59cb402bfc3b620c45d1fd539f2f72004ba8a1f76bfc1c297395e5

Address Pair Number 3
Public Address is 1FKYGkc56CdMNm8E3ZGGH7566371nMntCs
Private Key is  KxAfTG5L83vkvrKQ1FQYFBJVhKALEUFnsGwVGzFSwwTnhkkdPfcW
Public Key is 027f5fdde085f16def08448aca24c936df218a0e8f076edde86b84e52adad3dd1a

Paste the following into bitcoind creates multisig address
bitcoind createmultisig 2 '["03e0882fb32689e4ba97f127955c8411dac1e9e20c2db7c442f217e09312d624f0","020b188c6eda59cb402bfc3b620c45d1fd539f2f72004ba8a1f76bfc1c297395e5","027f5fdde085f16def08448aca24c936df218a0e8f076edde86b84e52adad3dd1a"]'

The multisig address is
3QgHn6PsMuszHSMdrB6cmN5bNncyfGQTpi


"""


    















