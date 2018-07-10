#class BranchHistoryTable:
import csv

branch_total = 0;
unique_branch_count = 0;
correct_predictions = 0;
incorrect_predictions=0;
misprediction_rate=0;

prediction_table = {};   #A dictionary to hold entries
entry_table = {};          #keeping the count of unique branches

for i in range(0,8192):
    index_bin = str(bin(i))[2:];      #storing binary values of the 8192 entries.
    zeros_count = 13-len(index_bin);    #number of prefix seros to be added
    key = zeros_count*"0" + index_bin;
    prediction_table[key] = 0;       #predicts as not taken


read = csv.reader(open("ray.csv"));              #Reading the traces files.
line = next(read);
while line:
    branch_total+=1;
    address_decimal = int(line[0]);                     # address_decimal = complete address of the branch in decimal

    if address_decimal not in entry_table.keys():       #checking for the unique branches
        entry_table[address_decimal] =0;

    suffix_binary = str(bin(address_decimal))[-13:];      #The last 13 bits of the branch address
    taken = int(line[1])                                        #The real branch status. 0=not taken, 1=taken
    if taken == prediction_table[suffix_binary]:
        correct_predictions +=1;
    else:
        incorrect_predictions+=1;
        prediction_table[suffix_binary] = taken;        #if the prediction is wrong, replace is it with the new prediction
    try:
        line=next(read);
    except StopIteration:
        print("File Reading Complete!")
        break;

unique_branch_count = len(entry_table);
misprediction_rate = incorrect_predictions / branch_total;

print();
print("Total Number of branches = ",branch_total);
print("Number of Unique branches = ",unique_branch_count);
print("Number of correct predictions = ",correct_predictions)
print("Number of incorrect predictions = ",incorrect_predictions);
print("misprediction rate = ",misprediction_rate)








