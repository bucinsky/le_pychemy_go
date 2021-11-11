##################################################################################################
# le_pychemy_go
# 
# STU FCHPT SLOVAKIA
# Lukas Bucinsky 
#
# 2021 Nov. 11 
#
##################################################################################################
# open a txt file and return its content
def open_read_file(filename):
    
    iname=filename
    try:
        ifile = open(iname, 'r')
    except IOError:
        print("Error, file cannot be open: "+iname)
    
    content=ifile.readlines()

    ifile.close()

    return content

######################################################################
# write a data file
# here we add a new line to the content,
# e.g. if you use content.append then this should be your choice
def write_data_file(fname,data): 
    try:
        datfile = open(fname, 'w')
    except IOError:
        print("Error: data file cannot be open.")
    
    # we will write the data into separate lines
    for line in data: 
        datfile.write(str(line)+"\n")

    datfile.close()
    return 0 

######################################################################
# write content to a file 
# if you read data and you do not need to add the newline tag 
# then choose this way 
def write_content_file(namew,content):
    try:
        fnamew = open(namew, 'w')
    except IOError:
        print("Error, file cannot be open: "+namew)
    
    for i,line in enumerate(content):
    #    fnamew.write(line+"\n")
        fnamew.write(line)

    fnamew.close()

    return 0

######################################################################
# print content on a screen
def print_content(contenti):
    
    for i,line in enumerate(contenti):
    #    fnamew.write(line+"\n")
        print(line,end="")

    return 0

#######################################################################
def main():
    print("This is a py file for file manipulations.")

#######################################################################
# to run main in this py file
if __name__ == "__main__":
   main()

