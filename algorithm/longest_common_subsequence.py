def longest_common_subsequence(query, database):
    """
    Find the sequence in the database with the longest common subsequence with the query.
    
    Args:
        query (str): The query DNA sequence
        database (list): A list of (header, sequence) tuples
        
    Returns:
        tuple: A (header, sequence) tuple of the best match
    """
    def get_lcs_len(s1, s2):
        """compute the length of the longest common subsequence."""
        rows = len(s1)
        cols = len(s2)
        # Create a table to store the LCS lengths
        dp = [[0] * (cols + 1) for _ in range(rows + 1)]
        # Fill the dp table
        for i in range(1, rows + 1):
            for j in range(1, cols + 1):
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])   
        return dp[rows][cols]
    #this is just to check with my testing file
    best_seq = None
    len_max = 0
    for head, seq in database:
        len_current = get_lcs_len(query, seq)
        if len_current > len_max:
            len_max = len_current
            best_seq = (head, seq)
    return best_seq