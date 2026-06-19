import os
import shutil
from backend.security.encryption import SecureEncryption

def backup_encrypted():
    print("Starting encrypted backup...")
    
    # Initialize encryption
    encryptor = SecureEncryption()
    
    # Mock data to backup
    data_to_backup = "Sensitive database contents"
    
    # Encrypt data
    encrypted_data = encryptor.encrypt_data(data_to_backup)
    
    # Save to backup file
    with open("backups/encrypted_backup.dat", "w") as f:
        f.write(encrypted_data)
        
    print("[SUCCESS] Encrypted backup saved to backups/encrypted_backup.dat")

if __name__ == "__main__":
    if not os.path.exists("backups"):
        os.makedirs("backups")
    backup_encrypted()
