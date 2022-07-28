from statistics import mean

with open('example.star', 'r') as f:
    starfile = list(f)

dataframe = {}

# loop over our list of lines
for line in starfile:
    # remove the '\n' character at the end of each line
    line = line.rstrip()

    # skip blank lines --- remember '' is False
    if not line:
        continue
    
    # create a couple bool variables to make it easier to keep track
    # of what's going on. Not strictly necessary, but neater.
    is_table_name = 'data_' in line
    is_table_start = line == 'loop_'
    is_column_name = line[0] == '_'

    # for this example, we know there's only one table. If you were
    # being thorough, you could create the dictionary here instead
    # of before the loop.
    if is_table_name or is_table_start:
        continue

    if is_column_name:
        # remove the comment at the end of the line by splitting
        # on whitespace and keeping only the first element. Again,
        # you don't need to do this. If you skip this step you just
        # end up including RELION's column number comments.
        line = line.split()[0]

        # remove "_rln" by slicing the string
        line = line[4:]

        # create an key/value pair with an empty list to add to
        dataframe[line] = []
    else:
        # get the column names. we do this here since we know that all
        # the columns are defined before the data.
        colnames = list(dataframe.keys())

        # split the line on whitespace by default. gives us a list of the
        # entries as strings
        line = line.split()

        # loop over the integers from 0 to the number of entries - 1
        for i in range(len(line)):
            # add the i-th entry to the i-th column
            dataframe[colnames[i]].append(line[i])

# first I'll write a function to convert a list of strings
# into a list of numbers, since we'll be doing that a lot
def convert_to_numbers(string_column):
    numbers = []
    for entry in string_column:
        numbers.append(float(entry))

    return numbers

# for each column we care about:
for colname in ['AngleRot', 'AngleTilt', 'AnglePsi']:
    # make a list of numbers
    numbers = convert_to_numbers(dataframe[colname])
    # print their average
    print('Mean for ', colname, ': ', mean(numbers), sep = '')

for colname in ['CoordinateX', 'CoordinateY']:
    # if you don't know what convert_to_numbers is, check my solution
    # for the mean of AngleRot, AngleTilt, and AnglePsi
    numbers = convert_to_numbers(dataframe[colname])
    print('Min for ', colname, ': ', min(numbers), sep = '')
    print('Max for ', colname, ': ', max(numbers), sep = '')
    
# challenge questions

# convert the strings to numbers
#
# I defined convert_to_numbers() when writing
# my solution for the AngleRot, AngleTilt, AnglePsi question
dataframe['AngleRot'] = convert_to_numbers(dataframe['AngleRot'])

# for each integer i from 0 to the length of AngleRot - 1
for i in range(len(dataframe['AngleRot'])):
    # add 180 to the i-th particle, modulo 360, and store that value in position i
    dataframe['AngleRot'][i] = (dataframe['AngleRot'][i] + 180) % 360


def write_star(filename, table_name, table):
    with open(filename, 'w') as f:
        f.write('data_')
        f.write(table_name)
        f.write('\n\nloop_\n')
        for colname in table.keys():
            f.write('_rln' + colname + '\n')
        
        # colname is still stored from the loop,
        # so we can use that to access whatever
        # the last column happens to be
        #
        # for each integer from 0 to the length of the column - 1:
        for i in range(len(table[colname])):
            # make a new empty list
            row = []

            # for each column name
            for colname in table.keys():
                # add the i-th element of the column to the list as a string
                row.append(str(dataframe[colname][i]))

            # once we've looped over each column, combine the list
            # of strings into a single string separated by spaces.
            # you should google string.join() for syntax!
            #
            # you could of course do this with a for loop too :)

            row = ' '.join(row)

            # write our new row to the file
            f.write(row)
            # and finally, write a newline for the next row
            f.write('\n')

write_star('rotated.star', 'particles', dataframe)