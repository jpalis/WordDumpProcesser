import urllib
import urllib.request
import re
import sys
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# Last Updated : 12/16/2020
#
# USAGE:  python parse.py [SINGLE COLUMN WORD DUMP LIST] [OUTPUT TEXT FILE] [ACCURACY: 0.00 - 1.00]
# 		  * Accuracy matches what percentage match of past test questions
# 		  * 0.8 would match test questions that 80% of the words are on this word dump

print("\nInitializing Parser ...\n")

BASE_DIR = "https://www2.ucsc.edu/courses/cse112-wm/:/Old-Exams/"

# Add additional midterm/ final exams as they are added in the future
TESTS = [

    # finals

    "cmps112-2018q1-final.tt",
    "cmps112-2018q2-final.tt",
    "cmps112-2018q4-final.tt",
    "cmps112-2019q1-final.tt",
    "cse112-2020q1-final.tt",
    "cse112-2020q4-final.tt",
    

    # midterms
    "cmps112-2018q1-midterm.tt",
    "cmps112-2018q2-midterm.tt",
    "cmps112-2018q4-midterm.tt",
    "cmps112-2019q1-midterm.tt",
    "cse112-2020q1-midterm.tt",
    "cse112-2020q4-final.tt",
    "cse112-2021q1-midterm.tt"
]

# read in data from word list
inp = open(sys.argv[1], "r")
wordlist = inp.readlines()
inp.close()

# write output to output file, create if not exists
output = open(sys.argv[2], "w+")
accuracy = float(sys.argv[3])

print("ACCURACY RATE    : " + str(accuracy))
print("TARGET DIRECTORY : " + BASE_DIR)
print("INPUT FILE       : " + str(sys.argv[1]) + '\n')

# Process word dump list
for i in range(len(wordlist)):
    wordlist[i] = wordlist[i].strip()

output.write('\n\n' + "ACCURACY RATE : " + str(accuracy) + '\n')

# Process prior exam text templates
for TEST in TESTS:  # for each exam.tt file

    URL = BASE_DIR + TEST
    print("    processing " + TEST)

    # extract html
    f = urllib.request.urlopen(URL)
    txt = f.read()
    txt = txt.decode("ISO-8859-1")

    # split decoded html into multiple choice questions and free response
    free_response = txt.split("Multiple choice")[0]
    multiple_choice = txt.split("Multiple choice")[1:]

    if len(free_response) > 0 or len(multiple_choice) > 0:
        output.write("| Matched questions from " + TEST + "\n")

    # reformat decoded html into lines labeled by their question number
    fr = re.compile(r"\n *[0-9]+\.").split("".join(free_response))[1:]

    # append each multiple choice line to string array mc
    mc = []
    for val in multiple_choice:
        mc.append(re.compile(r"\n *[0-9]+\.").split("".join(val))[1:])

    # fr = recopiled html string for each free_response question
    index = 1

    # process free response questions
    for elem in fr:
        num_matched, num_tot = 0, 0

        # split character array from exam.tt file, for each line, for each file
        temp = str(elem).strip().split()

        # process text into alphanumerics
        for t in temp:

            # temp = array of strings from exam.tt file
            # t = single word from exam.tt file word array

            tmp = t.strip().strip(".").strip('\\').strip("\'").strip("\\").strip(";").strip(".").strip(
                ",").strip("(").strip(")").split('\\n')[0].strip(";").strip(".").strip(":").strip('\'')

            if tmp.isalpha() or tmp.isdigit():
                if tmp in wordlist:
                    num_matched += 1
                    num_tot += 1
                else:
                    num_tot += 1
            else:
                pass

        if num_tot == 0:
            index += 1
            continue

        if((num_matched/num_tot) >= accuracy):
            output.write("[FREE RESPONSE] Q" + str(index) + " | " + " ACCURACY : " + "{:.2f}".format(num_matched/num_tot) + ' :' + '\n\n' +
                         (len(str(index)) + 2) * " " + str(elem) + '\n\n\n')
        index += 1

    # process multiple choice questions
    for part, each in enumerate(mc):
        index = 1

        for elem in each:

            num_matched = 0
            num_tot = 0
            temp = str(elem).strip().split()

            for tmp in temp:
                tmp = tmp.strip()
                if tmp.isalpha() or tmp.isdigit():
                    if tmp in wordlist:
                        num_matched += 1
                    num_tot += 1

            if num_tot == 0:
                index += 1
                continue
            if((num_matched/num_tot) >= accuracy):
                output.write("[MULTIPLE CHOICE] Q" + str(index) + " | PART : " + str(part + 1) + " | ACCURACY : " + "{:.2f}".format(num_matched/num_tot) + ' :' + '\n\n' +
                             (len(str(len(each))) + 1) * " " + str(elem) + '\n\n')
            index += 1

output.close()
print("\nTerminating Parser ...")
