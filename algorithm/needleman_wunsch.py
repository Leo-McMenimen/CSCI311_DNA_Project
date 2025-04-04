def needleman_wunsch(query, database):
    """
    Implement the Needleman-Wunsch algorithm.
    
    Args:
        query (str): The query DNA sequence
        database (list): A list of (header, sequence) tuples
        
    Returns:
        tuple: A (header, sequence) tuple of the best match
    """
    def align_seqs(s1, s2, match=1, mismatch=-1, gap=-1):
        """
        input with 2 sequeces and retrun the allignment scores
        """
        rows = len(s1)
        cols = len(s2)
        dp = [[0 for _ in range(cols + 1)] for _ in range(rows + 1)]
        # Initialize first row and column with gap penalties
        for i in range(rows + 1):
            dp[i][0] = gap * i
        for j in range(cols + 1):
            dp[0][j] = gap * j
        # Fill the scoring matrix
        for i in range(1, rows + 1):
            for j in range(1, cols + 1):
                diag = dp[i-1][j-1] + (match if s1[i-1] == s2[j-1] else mismatch)
                up = dp[i-1][j] + gap
                left = dp[i][j-1] + gap
                dp[i][j] = max(diag, up, left)  
        # Return alignment score (bottom-right cell)
        return dp[rows][cols]
    
    best_seq = None
    max_score = float('-inf')
    for head, seq in database:
        curr_score = align_seqs(query, seq)
        if curr_score > max_score:
            max_score = curr_score
            best_seq = (head, seq)
    return best_seq 