#!/usr/bin/python

#import needed classes
import random, sys, argparse

#notes:
#action="store_true" paired with default=False guarantees that the value of an option will be a bool
#self.lines is a list
#error when I put -e flag because it takes all arguments and doesn't stop. But it still expects an argument for filename

#arg.var is a list whenever the flag is set in CLI
#arg.var is nonempty whenever the flag is set and there is an argument to it

class shuf:
    #constructor
    #this object will by the end of construction have a list called lines that contains the lines that the user wishes to permute
    def __init__(self, filename = None):
        #if the filename is given, then we ignore all behavior related to stdin
        if filename != None:
            f = open (filename, 'r')
            self.lines = f.readlines()
            f.close()
        #if the filename is not given, then either we are reading from stdin or there are arguments with -e 
    #member functions
    def chooseline(self):
        return random.choice(self.lines)
    def printlines(self):
        for line in self.lines:
            print( line[:-1])
    def shuflines(self):
        random.shuffle(self.lines)
    def printnlines(self, n):
        for line in self.lines[0:n]:
            print (line[:-1])

def main():
    #version_msg = "%prog 2.0"
    #usage_msg = """%prog [OPTION]... FILE Output random permutations from FILE."""
    #create the parser
    parser = argparse.ArgumentParser(#version=version_msg, usage=usage_msg
    )
    #add positional argument (nonoptional)
    parser.add_argument("filename", nargs="*")
    #add echo optional argument; logical; default=false;
    parser.add_argument("-e", "--echo", action="store", default=None, help="treat each ARG as an input line", nargs="*")
    #add headcount optional argument
    parser.add_argument("-n", "--head-count", dest="headcount", action="store", default=None, nargs="*", help="output at most COUNT lines")
    #add repeat optional argument
    parser.add_argument("-r", "--repeat", action="store", nargs="*", default=None, help="output lines can be repeated")
    

    
    #references
    input_list = list()
    args = parser.parse_args()
    echo = args.echo
    filename = args.filename
    headcount = args.headcount
    repeat = args.repeat

    '''    
    #test: print out type of each object, and print their value
    print( "args' type: " + str(type(args)))
    if args:
        print( args)
    print( "echo's type: " + str(type(echo)))
    if echo:
        print( "echo exists with element(s):")
        for element in echo:
            print( element)
    print( "filename's type: " + str(type(filename)))
    if filename:
        print( "filename exists with filename(s):")
        for element in filename:
            print( element)
    print( "headcount's type: " + str(type(headcount)))
    if headcount:
        print( "headcount exists with value(s):")
        for element in headcount:
            print element
    print "repeat's type: " + str(type(repeat))
    if repeat:
        print "repeat exists with value(s):"
        for element in repeat:
            print element
    '''

            

    #For all cases, if echo is a list, then echo behavior will occur
    #Echo itself doesn't need to contain any values, but as long as flag -e is set, echo behavior will occur

    #if echo flag set, then permute and print all CLI arguments
    if type(echo) is list:
        '''
        print "args.echo is type list and each arg in args has value:"
        
        #test
        for arg in vars(args):
            print arg, getattr(args, arg)
            print "end"
        '''
        #if a flag is set, then add all of its arguments (if any) to input_list
        if type(echo) is list:    
            for element in echo:
                input_list.append(element)
        if type(filename) is list:
            for element in filename:
                input_list.append(element)
        if type(headcount) is list:
            for element in headcount[1:]:
                input_list.append(element)
        if type(repeat) is list:
            for element in repeat:
                input_list.append(element)
        '''
        print "Since the echo flag is set, we will be permuting these lines:"
        print input_list
        for element in input_list:
            print element
        '''
        #permute the elements in input_list
        random.shuffle(input_list)

        '''
        print "The result is: "
        '''
        #if echo, headcount flag is set
        if type(headcount) is list:
            #if headcount's first arg is a valid number
            try:
                #the actual headcount
                count = int(headcount[0])
                #offset
                
                count_index = count - 1               
                if count == 0:
                    sys.exit(1)
                if count < 0:
                    sys.stderr.write("shuf: invalid line count: '" + str(count) + "'\n")
                    sys.exit(1)
                '''
                print "The number of lines that will be displayed per permutation is: " + str(count)
                '''
            except Exception as e:
                #print 'type is:', e.__class__.__name__
                #print_exc()
                sys.stderr.write("shuf: invalid line count: \n" + str(count))
                sys.exit(1)
                
            #if echo, headcount, repeat flag is set
            if type(repeat) is list:
                while(True):
                    for i in input_list[0:count]:
                        print( i)
                    random.shuffle(input_list)
            #if only echo, headcount
            else:
                for i in input_list[0:count]:
                    print( i)

                    
        #if headcount flag not set
        else:
            #if only echo and repeat
            if type(repeat) is list:
                while(True):
                    for i in input_list:
                        print( i)
                    random.shuffle(input_list)
            #if only echo
            else:
                for i in input_list:
                    print (i)
                
       
            





                    
                
    #echo flag is not set; wish to use the shuf class to handle file object
    else:
        #retrieve a valid file
        try:
            file = None
            operands = 0
                        
            #if the flag is set and they contain arguments
            if type(filename) is list and len(filename) > 0:
                #if stdin is triggered
                if filename[0] == "-":
                    file = sys.stdin.readline()[:-1]
                    #print ("The file given by stdin is: " + file)
                else:
                    file = filename[0]
                    #print ("The file given by positional arg is: " + file)
                
            elif type(headcount) is list and len(headcount) > 1:
                file = headcount[1]
                
            elif type(repeat) is list and len(repeat) > 0:
                file = repeat[0]
                
            else:
                #no arguments; read from stdin
                file = sys.stdin.readline()
        except:
            sys.stderr.write("invalid FILENAME")
            exit(1)

        #create the shuf object to handle the file
        try:
            input_file = shuf(file)
        except:
            print ("shuf: " + file + ": No such file or directory")
            exit(1)
        #randomly permute lines
        input_file.shuflines()

        #check for too many operands
        if type(filename) is list:
            operands += len(filename)
        if type(headcount) is list:
            operands += len(headcount)
        if type(repeat) is list:
            operands += len(repeat)
        #print "The number of operands given were: " + str(operands)
        if operands > 2:
            print ("shuf: extra operand")
            exit(1)

            
        

        '''
        #test
        print str(file) + " is the file to be permuted with original lines: "
        input_file.printlines()
        print ("And it has the permuted lines:")
        input_file.shuflines()
        input_file.printlines()
        '''



        
        
        #echo not set, headcount set
        if type(headcount) is list:
            #if headcount's first arg is a valid number
            try:
                #the actual headcount
                count = int(headcount[0])
                #offset
                
                count_index = count - 1               
                if count == 0:
                    sys.exit(1)
                if count < 0:
                    sys.stderr.write("shuf: invalid line count: '" + str(count) + "'\n")
                    sys.exit(1)
                
                #print "The number of lines that will be displayed per permutation is: " + str(count)
            except Exception as e:
                #print 'type is:', e.__class__.__name__
                #print_exc()
                sys.stderr.write("shuf: invalid line count: \n" + str(count))
                sys.exit(1)
            


            
            #only headcount and repeat set
            if type(repeat) is list:
                while (True):
                    input_file.printnlines(count)
                    input_file.shuflines()                                
            #only headcount set
            else:
                input_file.printnlines(count)

                
        #headcount not set
        else:            
            #only repeat is set
            if type(repeat) is list:
                while(True):
                    input_file.printlines()
            #no flag is set
            else:
                input_file.printlines()
        
                        
    
    

    
if __name__ == "__main__":
    main()


 
