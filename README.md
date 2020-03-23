# Noobchain (Fullstack Flask App)

Blockchain Project for 'Distributed Systems' M.Sc. Course 2019-2020.

## Routing Table

##### Backend
| URL                  | Type | Action  |
|:--------------------:|:----:|:-------:|
| /transactions/create | POST |         |
| /broadcast/ring      | POST |         |
| broadcast/block      | POST |         |
| /nodes/register      | POST |         |
| /transactions/view   | GET  |         |
| /show_balance        | GET  |         |
| /receive/chain       | GET  | Current version of Node's chain|

##### Frontend
| URL      | Type| Action                     |
|:--------:|:---:|:--------------------------:|
| /        | GET | Home Page                  |
| /profile | GET | Node's Profile             |
| /contact | GET | Contact                    |
| /faq     | GET | Frequently Asked Questions |
| /about   | GET | About                      |
| /help    | GET | User Manual                |

### TODO

##### Node
```
[o] generate_wallet()
Δημιουργεί νέο wallet, δλδ ξεύγος public/private key χρησιμοποιώντας τον κρυπτογραφικό αλγόριθμο
RSA.

[x] create_transaction()
Δημιουργείται ένα νέο transaction που περιέχει όλα τα στοιχεία που απαιτούνται. Εδώ το πεδίο
transaction_inputs γεμίζει με τα Transaction Input που περιέχουν τα ids των UTXOs που απαιτούνται
για να συμπληρωθεί το ποσό που θέλουμενα ξοέψουμε.

[x] sign_transaction()
Υπογράφεται το transaction με το private key του wallet.

[x] broadcast_transaction()
Το transaction αποστέλλεται με broadcast σε όλους τους κόμβους

[x] verify_signature()
Επαληθεύεται η υπογραφή του transaction αμέσως μετά τη λήψη του

[x] validate_transaction()
Eπαληθεύεται η ορθότητα του transaction που έχει ληφθεί. Η επαλήθευση περιλαμβάνει (α) την
επαλήθευση της υπογραφής (verify_signature) και (β) τον έλεγχο των transaction inputs/outputs για να
εξασφαλίσουμε ότι το wallet αποστολέας έχει το ποσό amount που μεταφέρει στον παραλήπτη. Για να
επιτευχθεί το (β) ελέγχεται αν τα transaction inputs είναι πράγματι unspent transactions, αν είναι
αφαιρούνται από τη λίστα των UTXO του κόμβου. Δημιουργούνται τα δύο Transaction Outputs και
προστίθενται στη λίστα στη λίστα UTXO του node μας.

[x] wallet_balance()
Μπορούμενα βρούμε το υπόλοιπο οποιουδήποτε wallet προσθέτοντας όλα τα UTXOs που έχουν
παραλήπτη το συγκεκριμένο wallet.
```


##### Blockchain
```
[o] mine_block()
Η συνάρτηση αυτή καλείται μόλις capacity transactions έχουν ληφθεί και επαληθευτεί από κάποιον
κόμβο και υλοποιεί το proof of work δοκιμάζοντας διαφορετικές τιμές της μεταβλητής nonce και
hashάροντας το block μέχρι το hash που θα προκύψει να αρχίζει από έναν συγκεκριμένο αριθμό από
μηδενικά. Ο αριθμός αυτός καθορίζεται από τη σταθερά difficulty.

[o] broadcast_block()
Μόλις βρεθεί ο κατάλληλος nonce, ο κόμβος κάνει broadcast το επαληθευμένο block σε όλους τους
υπόλοιπους κόμβους.

[o] validate_block()
Αυτή η συνάρτηση καλείται από τους nodes κατά τη λήψη ενός νέου block (εκτός του genesis block).
Επαληθεύεται ότι (a) το πεδίο current_hash είναι πράγματι σωστό και ότι (b) το πεδίο previous_hash
ισούται πράγματι με το hash του προηγούμενου block.

[o] validate_chain()
Αυτή η συνάρτηση καλείται από τους νεοεισερχόμενους κόμβους, οι οποίοι επαληθεύουν την
ορθότητα του blockchain που λαμβάνουν από τον bootstrap κόμβο. Στην πραγματικότητα καλείται η
validate_block για όλα τα blocks εκτός του genesis.

[o] resolve_conflict()
Αυτή η συνάρτηση καλείται όταν ένα κόμβος λάβει ένα block το οποίο δεν μπορεί να κάνει validate
γιατί το πεδίο previous_hash δεν ισούται με το hash του προηγούμενου block. Αυτό μπορεί να σημαίνει
ότι έχει δημιουργηθεί κάποια διακλάδωση, η οποία πρέπει να επιλυθεί. Ο κόμβος ρωτάει τους
υπόλοιπους για το μήκος του blockchain και επιλέγει να υιοθετήσει αυτό με το μεγαλύτερο μήκος
```

## Contributors


Nick Nikitas [(03400043)](https://github.com/nikoshet) - ΕΔΕΜΜ.

Dimitris Zografakis [(03400050)](https://github.com/dimzog) - ΕΔΕΜΜ.

Dimitris Lambrakis [()](https://github.com) - ΕΔΕΜΜ.


#### Setup 

```
pip install -r requirements.txt
```
##### Run Server
```
python3 main.py -ip IP -port PORT -bootstrap TRUE -ip_boostrap IP_OF_BOOTSTRAP -port_bootstrap PORT_OF_BOOTSTRAP -nodes NO_OF_NODES -cap CAPACITY -dif DIFFICULTY
```

### Specs

### Licence

css used is under the MIT License and can be found here: [darkly](https://bootswatch.com/darkly/)

Nick Nikitas, Dimitris Zografakis, Dimitris Lambrakis.

Copyright © 2020

