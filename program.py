import re
import math

def discretize(given_value, limit, mn):    
    if(mn <= given_value and given_value <= limit):
        return 1
    else:
        return 2


hypothesis_space = 2**57
conjunctive_concepts = 3**57

print("Number of hypothesis space is: {}".format(hypothesis_space))
print("Number of conjunctive concepts is: {}".format(conjunctive_concepts))


average = [0] * 57
instances = [0] * 57 #number of instances without 0
st_dev = [0] * 57
minimum = [None] * 57
maximum = [None] * 57    
file_read = open("spambase.DOCUMENTATION", "r")

spam_count = 0
file_read = open("spambase.data", "r")
for line in file_read:
    data_row = line.split(",")    
    spam_flag = int(data_row[57])
    if(spam_flag == 1):
        spam_count += 1
file_read.close()

spam_of_80_percent = int (spam_count * 0.8)
#print ("{} {}".format(spam_count, spam_of_80_percent))

first_instance_flag = 1
spam_line_counter = 0
file_read = open("spambase.data", "r")
for line in file_read:    
    data_row = line.split(",")    
    spam_flag = int(data_row[57])
        
    if(first_instance_flag == 1 and spam_line_counter < spam_of_80_percent):
        if(first_instance_flag == 1):
            open_flag = 0
            for i in range(0, 57):
                minimum[i] = float(data_row[i])
                maximum[i] = float(data_row[i])
                
        spam_line_counter += 1
        for i in range(0, 57):
            if(float(data_row[i]) > 0):
                average[i] += float(data_row[i])
                instances[i] += 1
            
            if(float(data_row[i]) < minimum[i]):
                minimum[i] = float(data_row[i])
                
            if(float(data_row[i]) > maximum[i]):
                maximum[i] = float(data_row[i])
file_read.close()

#print("\nAverages:\n")                
for i in range(0, 57):
    average[i] = average[i] / instances[i]
    #print("{}\t{}".format(instances[i], average[i]))
    
    
spam_line_counter = 0
file_read = open("spambase.data", "r")
for line in file_read:    
    data_row = line.split(",")    
    spam_flag = int(data_row[57])
        
    if(spam_flag == 1 and spam_line_counter < spam_of_80_percent):
        spam_line_counter += 1
        for i in range(0, 57):
            if(float(data_row[i]) > 0):
                st_dev[i] += (average[i] - float(data_row[i])) ** 2
file_read.close()

#print("\nNo of insstances (without 0s), Average, Standard deviation, min and max:\n")
for i in range(0, 57):
    if(instances[i] > 1):
        st_dev[i] = st_dev[i] / (instances[i] - 1)
        st_dev[i] = math. sqrt(st_dev[i])
    #print("{}\t{}\t{}\t{}\t{}".format(instances[i], average[i], st_dev[i], minimum[i], maximum[i]))

#print("\nNo of insstances (without 0s), Average, Standard deviation, min, max and criteria value:\n")
counter = 0
values_limit = [None] * 57
temp_values = [None] * 57
values_flag = [None] * 57 # 1 for selected concepts and 0 for the opposite
for i in range(0, 57):
    values_limit[i] = average[i] + (3 * st_dev[i])
    

file_read = open("spambase.data", "r")    
first_instance_flag = 1
spam_line_counter = 0
testing_spam_count = 0
testing_spam_detected = 0

# Algorithm 4.1: Least general generalization
for line in file_read:    
    data_row = line.split(",")    
    spam_flag = int(data_row[57])
        
    if(spam_flag == 1):
        
        #For the first time it will take all the values from the first row
        if(first_instance_flag == 1):
            first_instance_flag = 0
            for i in range (0, 57):
                temp_values[i] = discretize(float(data_row[i]), values_limit[i], minimum[i])
                values_flag[i] = 1
                
            spam_line_counter += 1    
            continue
        
        #Algorithm 4.2: find least general conjunctive generalisation of two conjunctions
        #This algorithm will be used for first 80 percent
        if(spam_line_counter < spam_of_80_percent):
            for i in range (0, 57):
                if(values_flag[i] == 1 and temp_values[i] != discretize(float(data_row[i]), values_limit[i], minimum[i])):
                    values_flag[i] = 0           
        
        spam_line_counter += 1
file_read.close()

print("\nThe concepts are as following:")
#print(values_flag)
#print(temp_values)

file_read = open("spambase.names", "r")
line_counter = 0
concepts_counter = 0
for line_names in file_read:    
    if(line_counter >= 33 and line_counter < 90):
        #print(line_names)        
        array_position = line_counter - 33
        if(values_flag[array_position] == 1):
            concepts_counter += 1
            temp_name = temp_line = re.sub(' +', ' ',line_names.strip()).split(" ")
            print("\t{}".format(temp_name[0].replace(':', '')))
        
    line_counter += 1
file_read.close()

print("Number of concepts found: {}\n".format(concepts_counter))


file_read = open("spambase.data", "r")    
spam_line_counter = 0
spam_count = 0
spam_detected = 0


for line in file_read:    
    data_row = line.split(",")    
    spam_flag = int(data_row[57])    
    
    if(spam_flag == 1):
        spam_line_counter += 1
        if(spam_line_counter > spam_of_80_percent):            
            detection_flag = 1
            spam_count += 1
            for i in range (0, 57):
                if(values_flag[i] == 1 and discretize(float(data_row[i]), values_limit[i], minimum[i]) != temp_values[i]):
                    detection_flag = 0
                    break
            if(detection_flag == 1):
                spam_detected += 1

file_read.close()

percentage = ( spam_detected / spam_count ) * 100
print("\nSpam detected: {}".format(spam_detected))
print("Total number of spams: {}".format(spam_count))
print("Seccess rate of spam detection rate: {}".format(percentage))

spam_count = 0
spam_detected = 0
not_spam_detected = 0
not_spam_count = 0


file_read = open("spambase.data", "r")  
for line in file_read:
    data_row = line.split(",")
    spam_flag = int(data_row[57])
    if(spam_flag == 1):
        detection_flag = 1
        spam_count += 1
        for i in range (0, 57):
            if(values_flag[i] == 1 and discretize(float(data_row[i]), values_limit[i], minimum[i]) != temp_values[i]):
                detection_flag = 0
                break
        if(detection_flag == 1):
            spam_detected += 1
    
    elif(spam_flag == 0):
        not_spam_count += 1
        
        detection_flag = 0
        for i in range (0, 57):
            if(values_flag[i] == 1 and discretize(float(data_row[i]), values_limit[i], minimum[i]) != temp_values[i]):
                detection_flag = 1
                break
        
        if(detection_flag == 1):
            not_spam_detected += 1

file_read.close()

percentage = ( (spam_detected + not_spam_detected) / (spam_count + not_spam_count) ) * 100
print("\nOverall success rate for the whole dataset: {}".format(percentage))