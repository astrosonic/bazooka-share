# protexon v0.03
Node-based shared network protocol emphasizing on security and decentralization

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

### v0.03 [Oncoming]
1. Switched default accent from GREEN to CYAN
2. Fragment capacity increased to 9999 blocks - Going beyond is stupid
3. Fixed issue when block count greater than byte size was accepted
4. Fixed issue when block count equal to 100 was not accepted
5. Fixed issue when requested file for splitting was not found
6. Fixed issue when requested ledger for joining was not found
7. Refactored code for optimised calculation
8. Added percentage progress display for joining/splitting
