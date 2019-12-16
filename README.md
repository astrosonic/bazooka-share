# protexon v0.02
Node-based shared network protocol with an emphasis on security and decentralization

## Decentralised Union of Connected Environments (DUCE)
### Under development

## File Archive Dispersal and Encryption (FADE)
### Changelog

### v0.01
1. Dynamic file naming based on number of split parts
2. Size allocation to parts for the given part count
3. Enabled SHA512 hashing by default for all the parts
4. CLI shows block names, block sizes and hash values
5. Capable of upto 999 parts - Going beyond is crazy

### v0.02 [Current]
1. Uses `colorama` for some funky CLI
2. Ledgers with block names, block sizes and hash values
3. Ledger reading and display for auditing purposes
4. Block collection health checkup for missing or corrupted files
5. Joining of files when health checkup returns positive
6. Uses `os` for ledger and block deletion from system
7. Automatic removal of ledger and blocks when joining complete
