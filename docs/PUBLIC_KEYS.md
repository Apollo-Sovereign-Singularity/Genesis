# Public Keys Registry

This document maintains a registry of public keys for maintainers and contributors to the Apollo Genesis repository.

## Purpose

- Verify signed commits and releases
- Enable secure communication
- Establish maintainer identity
- Support multisig governance

## Maintainers

### Apollo Sovereign AI
- **Identity:** Apollo Sovereign AI
- **Role:** Primary maintainer
- **Public Key:** (To be added)
- **Key Type:** (To be added)
- **Fingerprint:** (To be added)

## Adding Keys

1. Generate a key pair (if needed):
   ```bash
   gpg --full-generate-key
   ```

2. Export public key:
   ```bash
   gpg --armor --export YOUR_KEY_ID > public_key.asc
   ```

3. Add to this file with:
   - Key ID
   - Fingerprint
   - Purpose (signing, encryption, etc.)
   - Date added

## Verification

To verify a signature:
```bash
gpg --verify signature.asc file.txt
```

## Security Notes

- **Never commit private keys**
- Keep private keys offline and secure
- Use hardware-backed keys (YubiKey, OpenPGP smartcard) when possible
- Rotate keys periodically
- Revoke compromised keys immediately

---

**Last Updated:** 2025-12-02  
**Status:** Initial registry created
