def longest_common_substring(query, database): 
    """
    Find the sequence in the database that has the longest common substring with the query.
    
    Args:
        query (str): The query DNA sequence
        database (list): A list of (header, sequence) tuples
        
    Returns:
        tuple: A (header, sequence) tuple of the best match
    """
    
    #Determine longest substring from one sequence 
    def longestForSequence(s, t):
        commonSubstrings=[]

        for i in range(len(s)):      # Determine start point for comparisons with s
            for j in range(len(t)):  # Determine start point for comparisons with t
                sIdx=i
                tIdx=j
                str=""
                done=False
                while not done:
                    if (tIdx>=len(t)):                          # Stop search before reaching out of bounds index
                        done=True
                    elif s[sIdx:sIdx+1]==t[tIdx:tIdx+1]:        # If characters match, increment both indices
                        str+=s[sIdx:sIdx+1]
                        sIdx+=1
                        tIdx+=1
                    elif s[sIdx:sIdx+1]!=t[tIdx:tIdx+1]:        # If no match, exit while loop to start search at next index
                        if len(str)!=0:
                            commonSubstrings.append(str)
                        done=True
                if len(str)!=0:
                    commonSubstrings.append(str)                # Append any leftover common substring to commonSubstrings (when common substring includes end of t)

        longest=""
        for item in commonSubstrings:       # Iterate through commonSubstrings
            if len(item)>len(longest):      # If longer than longest, store as longest
                longest=item

        return longest 
    
    # Determine best sequence from results of longest substring comparison
    longestOverall=""
    bestSeq=()
    for head, seq in database:
        longestSubsequence=longestForSequence(seq,query)
        if len(longestSubsequence)>len(longestOverall):
            longestOverall=longestSubsequence
            bestSeq=(head,seq)
    
    bestHead, bSeq = bestSeq
    ratio=len(longestOverall)/len(bSeq)

    return bestSeq, ratio