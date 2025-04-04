def load_fasta(filename):
    sequences = []

    with open(filename, 'r') as file:
        raw_content = file.readlines()
        
        header = ""
        sequence = ""

        for line in raw_content:
            line = line.strip()
            
            # Check if the line is a header (starts with '>')
            if line.startswith('>'):
                # If there's a sequence collected, save the previous one
                if sequence:
                    sequences.append((header, sequence))
                # Start a new sequence
                header = line[1:].strip()  # Remove the '>'
                sequence = ""
            else:
                sequence += line.strip().upper()  # Append the sequence in uppercase

        # Append the last sequence
        if sequence:
            sequences.append((header, sequence))

    return sequences
