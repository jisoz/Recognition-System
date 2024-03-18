# def count_words(sentence):
#     word_count = {}
#     words = sentence.split()
#     for word in words:
#         if word in word_count:
#             word_count[word] += 1
#         else:
#             word_count[word] = 1
#     return word_count

# # Test the function
# input_sentence = "This is a test sentence. This sentence is a test."
# word_counts = count_words(input_sentence)
# print("Word Counts:", word_counts)









# def count_vowels(input_string):
#     vowels = "aeiouAEIOU"
#     vowel_count = 0
#     for char in input_string:
#         if char in vowels:
#             vowel_count += 1
#     return vowel_count

# # Test the function
# text = "Hello, how are you?"  # Change this to test different strings
# result = count_vowels(text)
# print("Number of vowels:", result)



# def is_palindrome(input_string):
#     return input_string == input_string[::-1]


# text = "radar"  # Change this to test different strings
# if is_palindrome(text):
#     print(text, "is a palindrome")
# else:
#     print(text, "is not a palindrome")




# def count_occurrences(lst, element):
#     return lst.count(element)

# # Test the function
# numbers = [1, 2, 2, 3, 2, 4, 5, 2]
# element_to_count = 2
# occurrences = count_occurrences(numbers, element_to_count)
# print(f"{element_to_count} occurs {occurrences} times in the list.")













# def square_numbers(lst):
#     return [num ** 2 for num in lst]

# # Test the function
# numbers = [1, 2, 3, 4, 5]
# squared_list = square_numbers(numbers)
# print(f"Squared list: {squared_list}")




# def unique_elements(lst):
#     unique_list = []
#     for item in lst:
#         if item not in unique_list:
#             unique_list.append(item)
#     return unique_list

# # Test the function
# numbers = [1, 2, 2, 3, 3, 4, 4, 5]
# unique_list = unique_elements(numbers)
# print(f"Unique elements in the list: {unique_list}")



