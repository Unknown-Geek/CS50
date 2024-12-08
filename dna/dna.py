import csv
import sys


def main():
    db_list = []
    n = len(sys.argv)
    if n != 3:
        print('Usage: python program.py DATABASE.csv SEQUENCE.txt')
        return 1
    db = sys.argv[1]
    txt = sys.argv[2]

    # Read database file into a variable
    with open(db, 'r') as f_db:
        reader = csv.reader(f_db)
        db_list = list(reader)

    # Read DNA sequence file into a variable
    with open(txt, 'r') as f_txt:
        txt_contents = f_txt.read().strip()

    len1 = len(db_list)
    len2 = len(db_list[0])
    for i in range(1, len1):
        count = 0
        for j in range(1, len2):
            if int(longest_match(txt_contents, db_list[0][j])) == int(db_list[i][j]):
                count += 1
        if count == len2 - 1:
            print(db_list[i][0])
            return

    print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
