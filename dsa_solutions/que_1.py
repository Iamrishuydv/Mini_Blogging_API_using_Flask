'''
Question 1: Majority Element
Given an array nums of size n, return the majority element.
The majority element is the element that appears more than ⌊n / 2⌋ times.
You may assume that the majority element always exists in the array.
'''

def majority_element(nums):
    element_count = 0
    candidate = None

    for n in nums:
        if element_count == 0:
            candidate = n
        if n == candidate:
            element_count += 1
        else: 
            element_count -= 1

    return candidate



nums = [2, 2, 1, 1, 1, 2, 2]
print("Majority Element:", majority_element(nums))
