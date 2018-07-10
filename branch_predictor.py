import csv
import sys

print("Select your branch prediction algorithms");
print("1 . predictor_1_bit");
print("2 . predictor_2_bit");
print("3. predictor_2_2");
print("4. Custom predictor");
print("\n\n")


selector = sys.argv[1]
fileName = sys.argv[2]

# common function variables

branch_total = 0;
unique_branch_count = 0;
correct_predictions = 0;
incorrect_predictions=0;
misprediction_rate=0;
entry_table = {};          #keeping the count of unique branches

# 1 bit branch predictor ===============================================================================================
def predictor_1_bit():
    global branch_total;
    global correct_predictions;
    global incorrect_predictions;
    prediction_table = {};  # A dictionary to hold entries
    for i in range(0, 8192):
        index_bin = str(bin(i))[2:];  # storing binary values of the 8192 entries.
        zeros_count = 13 - len(index_bin);  # number of prefix seros to be added
        key = zeros_count * "0" + index_bin;
        prediction_table[key] = 0;  # predicts as not taken

    read = csv.reader(open(fileName));  # Reading the traces files.
    line = next(read);
    while line:
        branch_total += 1;
        address_decimal = int(line[0]);  # address_decimal = complete address of the branch in decimal

        if address_decimal not in entry_table.keys():  # checking for the unique branches
            entry_table[address_decimal] = 0;

        suffix_binary = str(bin(address_decimal))[-13:];  # The last 13 bits of the branch address
        taken = int(line[1])  # The real branch status. 0=not taken, 1=taken
        if taken == prediction_table[suffix_binary]:
            correct_predictions += 1;
        else:
            incorrect_predictions += 1;
            prediction_table[
                suffix_binary] = taken;  # if the prediction is wrong, replace is it with the new prediction
        try:
            line = next(read);
        except StopIteration:
            print("File Reading Complete!")
            break;

# 2 bit branch predictor =====================================================================================================

def predictor_2_bit():
    global branch_total;
    global correct_predictions;
    global incorrect_predictions;
    prediction_table = {};  # A dictionary to hold entries
    for i in range(0, 4096):
        index_bin = str(bin(i))[2:];  # storing binary values of the 8192 entries.
        zeros_count = 12 - len(index_bin);  # number of prefix seros to be added
        key = zeros_count * "0" + index_bin;
        prediction_table[key] = '00';  # predicts as not taken

    read = csv.reader(open(fileName));  # Reading the traces files.
    line = next(read);
    while line:
        branch_total += 1;
        address_decimal = int(line[0]);  # address_decimal = complete address of the branch in decimal

        if address_decimal not in entry_table.keys():  # checking for the unique branches
            entry_table[address_decimal] = 0;

        suffix_binary = str(bin(address_decimal))[-12:];  # The last 12 bits of the branch address
        taken = int(line[1])  # The real branch status. 0=not taken, 1=taken
        prediction = prediction_table[suffix_binary];  # the two bit state value of the branch predictor

        if prediction == "00":  # prediction as not taken
            if taken == 0:
                correct_predictions += 1;
            else:
                incorrect_predictions += 1;
                prediction_table[suffix_binary] = "01";
        elif prediction == "01":  # predict as not taken
            if taken == 0:
                correct_predictions += 1;
                prediction_table[suffix_binary] = "00";
            else:
                incorrect_predictions += 1;
                prediction_table[suffix_binary] = "11";
        elif prediction == "11":  # predict as taken
            if taken == 0:
                incorrect_predictions += 1;
                prediction_table[suffix_binary] = "10";
            else:
                correct_predictions += 1;
        else:  # predict as taken
            if taken == 0:
                incorrect_predictions += 1;
                prediction_table[suffix_binary] = "00";
            else:
                correct_predictions += 1;
                prediction_table[suffix_binary] = "11"

        try:
            line = next(read);
        except StopIteration:
            print("File Reading Complete!")
            break;

# 2,2 branch predictor ==================================================================================================
def predictor_2_2():
    global branch_total;
    prediction_table_00 = {};  # A dictionary to hold entries
    for i in range(0, 1024):
        index_bin = str(bin(i))[2:];  # storing binary values of the 1024 entries.
        zeros_count = 10 - len(index_bin);  # number of prefix seros to be added
        key = zeros_count * "0" + index_bin;
        prediction_table_00[key] = '00';  # predicts as not taken

    prediction_table_01 = prediction_table_00.copy();  # prediction tables referenced by 01
    prediction_table_11 = prediction_table_00.copy();
    prediction_table_10 = prediction_table_00.copy();

    def transition_function(prediction_table, suffix_binary, taken):

        prediction = prediction_table[suffix_binary];  # the two bit state value of the branch predictor
        global incorrect_predictions;
        global correct_predictions;
        if prediction == "00":  # prediction as not taken
            if taken == 0:
                correct_predictions += 1;
            else:
                incorrect_predictions += 1;
                prediction_table[suffix_binary] = "01";
        elif prediction == "01":  # predict as not taken
            if taken == 0:
                correct_predictions += 1;
                prediction_table[suffix_binary] = "00";
            else:
                incorrect_predictions += 1;
                prediction_table[suffix_binary] = "11";
        elif prediction == "11":  # predict as taken
            if taken == 0:
                incorrect_predictions += 1;
                prediction_table[suffix_binary] = "10";
            else:
                correct_predictions += 1;
        else:  # predict as taken
            if taken == 0:
                incorrect_predictions += 1;
                prediction_table[suffix_binary] = "00";
            else:
                correct_predictions += 1;
                prediction_table[suffix_binary] = "11"

    read = csv.reader(open(fileName));  # Reading the traces files.
    line = next(read);

    reference = "00";  # the reference number of the first reference table

    while line:
        branch_total += 1;
        address_decimal = int(line[0]);  # address_decimal = complete address of the branch in decimal

        if address_decimal not in entry_table.keys():  # checking for the unique branches
            entry_table[address_decimal] = 0;

        suffix_binary = str(bin(address_decimal))[-10:];  # The last 10 bits of the branch address

        taken = int(line[1])  # The real branch status. 0=not taken, 1=taken

        if reference == "00":
            prediction_table = prediction_table_00;
        elif reference == "01":
            prediction_table = prediction_table_01;
        elif reference == "11":
            prediction_table = prediction_table_11;
        else:
            prediction_table = prediction_table_10;

        transition_function(prediction_table, suffix_binary, taken);

        reference += str(taken);
        reference = reference[1:];
        try:
            line = next(read);
        except StopIteration:
            print("File Reading Complete!")
            break;


#Custom Branch predictor ===============================================================================================
def predictor_custom():
    global branch_total;
    prediction_table_000 = {};  # A dictionary to hold entries
    for i in range(0, 1024):
        index_bin = str(bin(i))[2:];  # storing binary values of the 8192 entries.
        zeros_count = 10 - len(index_bin);  # number of prefix seros to be added
        key = zeros_count * "0" + index_bin;
        prediction_table_000[key] = '00';  # predicts as not taken

    prediction_table_001 = prediction_table_000.copy();  # prediction tables referenced by 01
    prediction_table_010 = prediction_table_000.copy();
    prediction_table_011 = prediction_table_000.copy();
    prediction_table_100 = prediction_table_000.copy();
    prediction_table_101 = prediction_table_000.copy();
    prediction_table_110 = prediction_table_000.copy();
    prediction_table_111 = prediction_table_000.copy();

    def transition_function(prediction_table, suffix_binary, taken):

        prediction = prediction_table[suffix_binary];  # the two bit state value of the branch predictor
        global incorrect_predictions
        global correct_predictions;
        if prediction == "00":  # prediction as not taken
            if taken == 0:
                correct_predictions += 1;
            else:
                incorrect_predictions += 1;
                prediction_table[suffix_binary] = "01";
        elif prediction == "01":  # predict as not taken
            if taken == 0:
                correct_predictions += 1;
                prediction_table[suffix_binary] = "00";
            else:
                incorrect_predictions += 1;
                prediction_table[suffix_binary] = "11";
        elif prediction == "11":  # predict as taken
            if taken == 0:
                incorrect_predictions += 1;
                prediction_table[suffix_binary] = "10";
            else:
                correct_predictions += 1;
        else:  # predict as taken
            if taken == 0:
                incorrect_predictions += 1;
                prediction_table[suffix_binary] = "00";
            else:
                correct_predictions += 1;
                prediction_table[suffix_binary] = "11"

    read = csv.reader(open("12queens.csv"));  # Reading the traces files.
    line = next(read);

    reference = "000";  # the reference number of the first reference table

    while line:
        branch_total += 1;
        address_decimal = int(line[0]);  # address_decimal = complete address of the branch in decimal

        if address_decimal not in entry_table.keys():  # checking for the unique branches
            entry_table[address_decimal] = 0;

        suffix_binary = str(bin(address_decimal))[-10:];  # The last 13 bits of the branch address

        taken = int(line[1])  # The real branch status. 0=not taken, 1=taken

        if reference == "000":
            prediction_table = prediction_table_000;
        elif reference == "001":
            prediction_table = prediction_table_001;
        elif reference == "010":
            prediction_table = prediction_table_010;
        elif reference == "011":
            prediction_table = prediction_table_011;
        elif reference == "100":
            prediction_table = prediction_table_100;
        elif reference == "101":
            prediction_table = prediction_table_101;
        elif reference == "110":
            prediction_table = prediction_table_110;
        else:
            prediction_table = prediction_table_111;

        transition_function(prediction_table, suffix_binary, taken);

        reference += str(taken);
        reference = reference[1:];
        try:
            line = next(read);
        except StopIteration:
            print("File Reading Complete!")
            break;


if selector == "1":
    predictor_1_bit();
elif selector == "2":
    predictor_2_bit();
elif selector == "3":
    predictor_2_2();
elif selector == "4":
    predictor_custom();
else:
    print("Incorrect Function");

unique_branch_count = len(entry_table);
misprediction_rate = incorrect_predictions / float(branch_total);

print();
print("Total Number of branches = ",branch_total);
print("Number of Unique branches = ",unique_branch_count);
print("Number of correct predictions = ",correct_predictions)
print("Number of incorrect predictions = ",incorrect_predictions);
print("misprediction rate = ",misprediction_rate)

