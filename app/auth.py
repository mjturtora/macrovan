import keyring
import getpass
import sys

SERVICE_ID = "MacroVan"
USER_CONFIG_KEY = "current_username"

def _prompt_for_username():
    user = input("Enter web username: ").strip()
    if not user:
        print("Error: Username cannot be empty.")
        sys.exit(1)
    keyring.set_password(SERVICE_ID, USER_CONFIG_KEY, user)
    return user

def _prompt_for_password(user):
    pwd = getpass.getpass(f"Enter password for {user}: ")
    if not pwd:
        print("Error: Password cannot be empty.")
        sys.exit(1)
    keyring.set_password(SERVICE_ID, user, pwd)
    return pwd

def handle_auth():
    is_reset = "--reset" in sys.argv
    current_user = keyring.get_password(SERVICE_ID, USER_CONFIG_KEY)

    if current_user:
        print(f"[*] Active User: {current_user}")
    else:
        print("[!] No user configured.")

    if is_reset:
        print(f"\n--- {SERVICE_ID} Reset Menu ---")
        print(f"Current User: {current_user or 'None'}")
        choice = input("Update (U)sername, (P)assword, or (B)oth? [U/P/B]: ").strip().lower()
        
        if choice == 'u':
            current_user = _prompt_for_username()
        elif choice == 'p':
            if not current_user: current_user = _prompt_for_username()
            _prompt_for_password(current_user)
        elif choice == 'b':
            current_user = _prompt_for_username()
            _prompt_for_password(current_user)
        else:
            print("Invalid choice. No changes made.")
        
        print("\nReset complete. Please run without --reset to start.")
        sys.exit(0)

    # Normal Flow: Ensure we have both
    if not current_user:
        current_user = _prompt_for_username()
        
    current_pwd = keyring.get_password(SERVICE_ID, current_user)
    if not current_pwd:
        current_pwd = _prompt_for_password(current_user)
        
    return current_user, current_pwd

# --- THE "LAZY BRIDGE" ---
username, password = handle_auth()
