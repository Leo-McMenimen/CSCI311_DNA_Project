def edit_distance(query, database):
    """
    Computes the edit distance between the query sequence and all sequences in the database.
    Returns the sequence with the smallest edit distance to the query.
    
    Args:
        query (str): The query DNA sequence
        database (list): A list of (header, sequence) tuples
        
    Returns:
        tuple: A (header, sequence) tuple of the best match
    """
    def min_operations(s1, s2):
        m, n = len(s1), len(s2)
        # Create a 2D 
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i  # Cost of deletions
        for j in range(n + 1):
            dp[0][j] = j  # Cost of insertions
            #fill this by the operation
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]  # No operation needed if characters are the same
                else:
                    dp[i][j] = min(
                        dp[i - 1][j] + 1,  # Deletion
                        dp[i][j - 1] + 1,  # Insertion
                        dp[i - 1][j - 1] + 1  # Substitution
                    )
        return dp[m][n]
    
    # This is for my testing
    min_dist = float('inf')
    best_match = None
    
    for header, sequence in database:
        distance = min_operations(query, sequence)
        if distance < min_dist:
            min_dist = distance
            best_match = (header, sequence)
    return best_match 