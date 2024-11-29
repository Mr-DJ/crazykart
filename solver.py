import socket
import time

def get_messages(num_messages=3):
    s = socket.socket()
    s.connect(('localhost', 18739))
    messages = []
    
    try:
        for _ in range(num_messages):
            data = s.recv(1024).decode().strip()
            if data:
                messages.append(data)
            time.sleep(2)
    finally:
        s.close()
    
    return messages

def simulate_lfsr(length):
    # Recreate the same LFSR used by server
    state = [1, 0, 1, 0]  # Known initial state
    keystream = []
    
    for _ in range(length):
        # Same feedback function as server
        feedback = (state[0] ^ state[1] ^ state[2]) & 1
        state = state[1:] + [feedback]
        keystream.append(feedback)
    
    return keystream

def decrypt_message(message, keystream):
    message = message.rstrip('\n')  # Remove newline before decryption
    return ''.join(chr(ord(char) ^ k) for char, k in zip(message, keystream))


def main():
    print("Collecting encrypted messages...")
    messages = get_messages()
    
    print("\nDecrypting messages...")
    for i, encrypted in enumerate(messages):
        # Generate same keystream as server
        keystream = simulate_lfsr(len(encrypted))
        decrypted = decrypt_message(encrypted, keystream)
        print(f"Message {i}: {decrypted}")

if __name__ == "__main__":
    main()
