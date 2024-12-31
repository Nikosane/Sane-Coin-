import random
import hashlib

def load_words(filename):
    """Load words from a file and return a list of words."""
    with open(filename, 'r') as file:
        words = file.read().splitlines()  # Assuming words are one per line
    return words

def select_words_from_list(words, num=5):
    """Select a random set of words from the list."""
    return random.sample(words, num)

def prompt_user_for_word_selection(words):
    """Prompt the user to select a word from the provided list."""
    print("Here are your 5 words to choose from:")
    for i, word in enumerate(words, 1):
        print(f"{i}. {word}")
    
    while True:
        selection = input("Do you want to select a word from the list? (y/n): ").strip().lower()
        if selection == 'y':
            selected_word = input("Please enter the word you have selected: ").strip().lower()  # Convert to lowercase
            # Compare the selected word in lowercase for case-insensitivity
            if selected_word in [word.lower() for word in words]:  # Convert words to lowercase for comparison
                # Get the exact word from the list (case-sensitive)
                for word in words:
                    if word.lower() == selected_word:
                        return word
            else:
                print("Invalid word selected. Please select a word from the list.")
        elif selection == 'n':
            print("You chose to skip. A new set of words will be provided.")
            return None
        else:
            print("Invalid input. Please enter 'y' to select or 'n' to skip.")

def split_words_into_chunks(words, chunk_size=100):
    """Split the words into chunks of `chunk_size` words each."""
    random.shuffle(words)  # Shuffle the words to ensure random chunks
    chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
    return chunks  # Return all chunks

def generate_keys(num_keys=3):
    """Generate `num_keys` random keys."""
    keys = []
    for _ in range(num_keys):
        key = hashlib.sha256(str(random.randint(0, 10000)).encode()).hexdigest()[:16]  # Generate 16-character keys
        keys.append(key)
    return keys

def encrypt_chunk(chunk, key):
    """Encrypt a chunk using a simple XOR encryption (for illustration)."""
    encrypted = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(chunk))
    return encrypted

def start_game(words):
    """Start the game logic where the user selects a word and continues."""
    while True:
        selected_words = select_words_from_list(words)
        desired_word = prompt_user_for_word_selection(selected_words)
        
        if desired_word:
            print(f"The desired word for this round is: {desired_word}")
            break
        else:
            print("Let's try again with a new set of words.\n")
    
    # Now, process the words into chunks
    chunks = split_words_into_chunks(words)
    
    # Generate 3 keys for encryption
    keys = generate_keys()
    print(f"Your 3 public keys are: {keys}")
    
    # Private key for the program (not shared with user)
    program_key = "defaultprivatekey"  # This is the private key for encryption that won't be shared
    
    # Encrypt the chunks: First 3 chunks with public keys, remaining with private key
    encrypted_chunks = []
    encrypted_chunk_info = []

    # Encrypt first 3 chunks with public keys
    for i in range(min(3, len(chunks))):  # Ensure we don't go out of bounds
        encrypted_chunks.append(encrypt_chunk(' '.join(chunks[i]), keys[i]))
        encrypted_chunk_info.append("public")  # Mark the encryption method as "public"
    
    # Encrypt the remaining chunks with the private program key
    for i in range(3, len(chunks)):
        encrypted_chunks.append(encrypt_chunk(' '.join(chunks[i]), program_key))
        encrypted_chunk_info.append("private")  # Mark the encryption method as "private"
    
    # Shuffle the encrypted chunks and their associated information
    encrypted_chunks_with_info = list(zip(encrypted_chunks, encrypted_chunk_info))
    random.shuffle(encrypted_chunks_with_info)
    
    # Display the list of chunks without showing the actual encrypted content
    print("\nEncrypted Chunks (You can choose from these, but not the actual content):")
    for i, (_, encryption_method) in enumerate(encrypted_chunks_with_info):
        print(f"Encrypted chunk {i + 1}: is encrypted with the secret key")

    # Now, the user selects 3 chunks to proceed with the game
    print("\nSelect 3 chunks to proceed with:")
    selected_chunks = []
    while len(selected_chunks) < 3:
        try:
            selection = int(input(f"Enter the number of chunk to select (1-{len(encrypted_chunks)}): "))
            if selection < 1 or selection > len(encrypted_chunks):
                print(f"Please enter a number between 1 and {len(encrypted_chunks)}.")
            elif selection not in selected_chunks:
                selected_chunks.append(selection)
            else:
                print("You have already selected this chunk.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Once the user selects 3 chunks, proceed with the next step
    print(f"\nYou have selected the following chunks: {selected_chunks}")
    print("You can proceed with the game now.")
    
    # Next steps of the game could go here (based on your game design)

# Example usage (assuming words.txt exists)
if __name__ == "__main__":
    words = load_words("words.txt")  # Make sure to provide the correct path to the words file
    start_game(words)
