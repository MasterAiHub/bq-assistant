# Encryption Specification

## Algorithm

BQ Assistant uses **AES-256-GCM** (Advanced Encryption Standard with Galois/Counter Mode) for all data encryption. This provides both confidentiality and authenticity.

## Key Management

- **Master Key**: A high-entropy master key is stored in environment variables.
- **Key Derivation**: We use PBKDF2 with SHA-512 to derive encryption keys from the master key and a unique salt.
- **Salt**: A unique salt is used for each deployment to prevent rainbow table attacks.

## Implementation Details

The encryption logic is implemented in `backend/security/encryption.py` using the `cryptography` library.

### Encrypted Data Format

Encrypted data is stored as a base64-encoded string containing the initialization vector (IV), the ciphertext, and the authentication tag.
