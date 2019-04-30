# Determines what percent of security numbers "look" non-random.
# Does this by brute force, so if you try long length numbers, it will take a while. Nothing clever going on.

import sys
from collections import defaultdict

# Current checks implemented for "non-randomness" are in this horrible hash from name of check to definition
checks = {}

# Is the number a palindrome. Uses some weird python syntax for reversing string.
def palindrome(s):
  return s == s[::-1]
checks["Palindrome"] = palindrome

# * Unique numbers <= length / 2 rounded down (so for 6-digit numbers, only 3 unique numbers)
def unique_nums(s):
  target_length = len(s) / 2
  unique_nums = set()
  for c in s:
    unique_nums.add(c)
  return len(unique_nums) <= target_length
checks["Unique Numbers"] = unique_nums

# * One number three times in a row (does this have too much overlap with previous check?)
def three_in_a_row(s):
  check_letter = "X"
  letter_count = 0
  for c in s:
    if check_letter == c:
      letter_count += 1
      if letter_count == 3:
        return True
    else:
      check_letter = c
      letter_count = 1
  return False
checks["Three in a Row"] = three_in_a_row

# Ascending and descending sequence each use this thing which checks for a sequence of max(length / 2, 3) or longer.
# This check requires that the numbers be actual numbers.
def sequence(s):
  current_num = -2
  letter_count = 0
  for c in s:
    if int(c) == current_num + 1:
      letter_count += 1
    else:
      letter_count = 1
    current_num = int(c)
    if letter_count == max(len(s) / 2, 3):
      return True
  return False
checks["Ascending Sequence"] = sequence

def reverse_sequence(s):
  return sequence(s[::-1])
checks["Descending Sequence"] = reverse_sequence

# Because security numbers can start with 0, need this
def zero_pad(i, length):
  s = str(i)
  while len(s) < length:
    s = "0" + s
  return s


length = 6
if len(sys.argv) > 1:
  length = int(sys.argv[1])
  print "Using length " + sys.argv[1]
else:
  print "Default length is 6. Call with an argument for other lengths"

total_nums = 0
# Count of how many numbers matched N checkx
match_counts = defaultdict(int)
# Count of how many numbers matched each check
check_counts = defaultdict(int)

# Go through each number up to the size and check it.
for x in range(10**length):
  total_nums += 1
  s = zero_pad(x, length)
  matches = 0
  for name, check in checks.iteritems():
    if check(s):
      matches += 1
      check_counts[name] += 1
  match_counts[matches] += 1

# Now, print some stats
print "Checked %d numbers" % (total_nums)
print ""
for i in range(len(match_counts.keys())):
  print "%d Matches: %d (%.2f%%)" % (i, match_counts[i], 100.0*match_counts[i]/total_nums)
print ""
for name, count in check_counts.iteritems():
  print "%s Matches: %d (%.2f%%)" % (name, check_counts[name], 100.0*check_counts[name]/total_nums)
  
