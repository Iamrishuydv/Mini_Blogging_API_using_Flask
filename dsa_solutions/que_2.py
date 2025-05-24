"""
 Question 2: Longest Consecutive Sequence
Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence.

You must write an algorithm that runs in O(n) time.
"""

def longest_consecutive(n):
    num_set = set(n)
    longest_cons = 0

    for num in num_set:
        if num - 1 not in num_set:
            current = num
            streaks = 1

            while current + 1 in num_set:
                current += 1
                streaks += 1

            longest_cons = max(longest_cons, streaks)

    return longest_cons

n = [100, 4, 200, 1, 3, 2]
print(longest_consecutive(n))

