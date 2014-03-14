# MULTISIGS - PART TWO - SPENDING FROM A 2-of-3 MULTISIG ADDRESS
# This simple wallet works with bitcoind and will only work with 2-of-3 multisigs
# wobine code for world bitcoin network blackboard 101
# Educational Purposes only
# Python 2.7.6 and relies on bitcoind & bitcoinrpc & wobine's github connection file
# We had to change the bitcoinrpc 'connection.py' file to add multisig support
# you'll need to download our 'connection.py' file from Github & stuff it in your bitcoinrpc folder

from bitcoinrpc.util import *
from bitcoinrpc.exceptions import *
from bitcoinrpc.__init__ import *
from bitcoinrpc.config import *
from bitcoinrpc.proxy import *
from bitcoinrpc.data import *
from bitcoinrpc.connection import *


bitcoin = connect_to_local() #creates an object called 'bitcoin' that allows for bitcoind calls

# YOU NEED AT LEAST TWO OF THE PRIVATE KEYS FROM PART ONE linked to your MULTI-SIG ADDRESS
multisigprivkeyone = "L2M1uRgdwgCotoP8prWJYYwz2zwWgsMa9TJwqARG7nFxkpdvBSsm" #your key/brother one
multisigprivkeytwo = "L1M2ZgjoAtDVu9uemahiZBQPwFA5Tyj4GLd1ECkDryviFrGp6m7k" #wallet service/brother two
multisigprivkeythree = "L5PkVBzR4SdQimMsfHnRqRegJZDFJ22sGjSbfp3SsPSnVoB8vRFE" #safe deposit box/brother three
ChangeAddress = "35Z3xG92YkW5Xo4ngQw6w5b3Ce6MDw94A8" #!!! Makes Sure to set your own personal Change Address

SetTxFee = int(0.00005461*100000000) # Lets proper good etiquette & put something aside for our friends the miners

unspent = bitcoin.listunspent() # Query wallet.dat file for unspent funds to see if we have multisigs to spend from

print "Your Bitcoin-QT/d has",len(unspent),"unspent outputs"
for i in range(0, len(unspent)):
    print
    print "Output",i+1,"has",unspent[i]["amount"],"bitcoins, or",int(unspent[i]["amount"]*100000000),"satoshis"
    print "The transaction id for output",i+1,"is"
    print unspent[i]["txid"]
    print "The ScriptPubKey is", unspent[i]["scriptPubKey"]
    print "on Public Address =====>>",unspent[i]["address"]

print
totalcoin = int(bitcoin.getbalance()*100000000)
print "The total value of unspent satoshis is", totalcoin
print

WhichTrans = int(raw_input('Spend from which output? '))-1
if WhichTrans > len(unspent): #Basic idiot check. Clearly a real wallet would do more checks.
    print "Sorry that's not a valid output" 
else:
    tempaddy = str(unspent[WhichTrans]["address"])
    print
    if int(tempaddy[0:1]) == 1:
        print "The public address on that account starts with a '1' - its not multisig."
    elif int(tempaddy[0:1]) == 3:
        print "The public address on that account is",tempaddy
        print "The address starts with the number '3' which makes it a multisig."
        print
        print "All multisig transactions need: txid, scriptPubKey and redeemScript"
        print "Fortunately all of this is right there in the bitcoind 'listunspent' json from before"
        print
        print "The txid is:",unspent[WhichTrans]["txid"]
        print "The ScriptPubKey is:", unspent[WhichTrans]["scriptPubKey"]
        print
        print "And only multisigs have redeemScripts."
        print "The redeemScript is:",unspent[WhichTrans]["redeemScript"]
        print
        
        print "You have",int(unspent[WhichTrans]["amount"]*100000000),"satoshis in this output."

        HowMuch = int(raw_input('How much do you want to spend? '))
        if HowMuch > int(unspent[WhichTrans]["amount"]*100000000):
            print "Sorry not enough funds in that account" # check to see if there are enough funds.
        else:
            print
            SendAddress = str(raw_input('Send funds to which bitcoin address? ')) or "1M72Sfpbz1BPpXFHz9m3CdqATR44Jvaydd" #default value Sean's Outpost
            if SendAddress == "1M72Sfpbz1BPpXFHz9m3CdqATR44Jvaydd":
                print "Nice! Your chose to send funds to Sean's Outpost in Pensacola Florida."
            print
            Leftover = int(unspent[WhichTrans]["amount"]*100000000)-HowMuch-SetTxFee
            print "This send to",SendAddress,"will leave", Leftover,"Satoshis in your accounts."
            print "A tx fee of",SetTxFee,"will be sent to the miners"
            print
            print "Creating the raw transaction for User One - Private Key One"
            print
            
            rawtransact = bitcoin.createrawtransaction ([{"txid":unspent[WhichTrans]["txid"],
                    "vout":unspent[WhichTrans]["vout"],
                    "scriptPubKey":unspent[WhichTrans]["scriptPubKey"],
                    "redeemScript":unspent[WhichTrans]["redeemScript"]}],{SendAddress:HowMuch/100000000.00,ChangeAddress:Leftover/100000000.00})
            print "bitcoind decoderawtransaction", rawtransact
            print
            print
            print "And now we'll sign the raw transaction -> The first user gets a 'False'"
            print "This makes sense because in multisig, no single entity can sign alone"
            print
            print "For fun you can paste this FIRST signrawtransaction into bitcoind to verify multisig address"
            print "%s%s%s%s%s%s%s%s%s%s%s%s%s" % ('bitcoind signrawtransaction \'',rawtransact,'\' \'[{"txid":"',unspent[WhichTrans]["txid"],'","vout":',
                                      unspent[WhichTrans]["vout"],',"scriptPubKey":"',unspent[WhichTrans]["scriptPubKey"],'","redeemScript":"',
                                      unspent[WhichTrans]["redeemScript"],'"}]\' \'["',multisigprivkeyone,'"]\'')
            print
            signedone = bitcoin.signrawtransaction (rawtransact,
                    [{"txid":unspent[WhichTrans]["txid"],
                    "vout":unspent[WhichTrans]["vout"],"scriptPubKey":unspent[WhichTrans]["scriptPubKey"],
                    "redeemScript":unspent[WhichTrans]["redeemScript"]}],
                    [multisigprivkeyone])
            print signedone
            print
            print "In a real world situation, the 'hex' part of this thing above would be sent to the second"
            print "user or the wallet provider. Notice, the private key is not there. It has been signed digitally"
            print
            print
            print "For fun you can paste this SECOND signrawtransaction into bitcoind to verify multisig address"
            print "%s%s%s%s%s%s%s%s%s%s%s%s%s" % ('bitcoind signrawtransaction \'',signedone["hex"],'\' \'[{"txid":"',unspent[WhichTrans]["txid"],'","vout":',
                                      unspent[WhichTrans]["vout"],',"scriptPubKey":"',unspent[WhichTrans]["scriptPubKey"],'","redeemScript":"',
                                      unspent[WhichTrans]["redeemScript"],'"}]\' \'["',multisigprivkeytwo,'"]\'')
            print
            doublesignedrawtransaction = bitcoin.signrawtransaction (signedone["hex"],
                    [{"txid":unspent[WhichTrans]["txid"],
                    "vout":unspent[WhichTrans]["vout"],"scriptPubKey":unspent[WhichTrans]["scriptPubKey"],
                    "redeemScript":unspent[WhichTrans]["redeemScript"]}],
                    [multisigprivkeytwo])
            print doublesignedrawtransaction
            print
            print "You are now ready to send",HowMuch,"Satoshis to",SendAddress
            print "And",Leftover,"Satoshis will be sent to the change account",ChangeAddress
            print "Finally, a miner's fee of ",SetTxFee,"Satoshis will be sent to the miners"
            print

            ReallyNow = (raw_input('If you hit return now, you will be sending these funds from your multisig account '))
            ReallyNow2 = (raw_input('No...REally...If you hit return now, you will be sending funds from your multisig account '))
            print
            print "SORRY. We won't do this. Don't want anyone to lose money playing with this code"
            print "But if you really want to send it, just"
            print "copy the HEX from the big block up above"
            print "and put it in a 'bitcoind sendrawtransaction' request"

        
