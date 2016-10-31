
# blueprint FSA class
class FSA:
    def __init__(self, num_states = 0):
        self.num_states = num_states
        self.transitions = {}
        self.final_states = set()
        
    """ TODO: Add methods for adding transitions, setting final states, looking up next
    state in the state transitions table, checking whether or not a state is a final 
    (accepting) state. 
    """
    
    def add_transition(self, s, currentState, newState):
        self.transitions[(s, currentState)] = newState
           
    def set_final_state(self, final):
        self.final_states.add(final)
    
    def lookup(self, current, s):  
        if (s, current) in self.transitions:
            return self.transitions[(s, current)]
        else:
            return None
    
    def is_final(self, state):
        return state in self.final_states
        
# recognizes an input string such as '12' or '11' or '1993' 
# takes in a single FSA        
def DRecognize(input_str, fsa):

    """ TODO: Implement D-RECOGNIZE from SLP Figure 2.12, return true or false based on 
    whether or not the fsa object accepts or rejects the input string.
    """
    index = 0
    currentState = "0"
    
    while True:
        if index == len(input_str):
            if fsa.is_final(currentState):
                return True
            else:
                return False      
        elif not fsa.lookup(currentState, input_str[index]):
            return False
        else:
            currentState = fsa.lookup(currentState, input_str[index])
            index += 1
            
# recognizes an input string such as '12/11/1993'
# takes in a list of FSAs: MM, seps, DD...I assume the appropriate order
def DRecognizeMulti(input_str, fsa_list): 
    """ TODO: Extend D-RECOGNIZE such that it inputs a list of FSA instead of a single 
    one. This algorithm should accept/reject input strings such as 12/31/2000 based on 
    whether or not the string is in the language defined by the FSA that is the 
    concatenation of the input list of FSA.

    """
    # use recrusion!
    
    index = 0
    currentState = "0"
    
    while True:
        
        if index == len(input_str):
            if fsa_list[0].is_final(currentState):
                return True
            else:
                return False
                
        elif fsa_list[0].is_final(currentState):
            if len(fsa_list) > 1:
                # keep looking
                return DRecognizeMulti(input_str[index:], fsa_list[1:])
            else:
                return False
                
        elif not fsa_list[0].lookup(currentState, input_str[index]):
            return False
            
        else:
            currentState = fsa_list[0].lookup(currentState, input_str[index])
            index += 1
   
""" Below are some test cases. Include the output of this in your write-up and provide 
explanations. 
"""


# define variables,
# call FSA class here

months = FSA(4) 

months.add_transition("0", "0", "1")
months.add_transition("1", "0" ,"2")

num = [str(n) for n in [1,2,3,4,5,6,7,8,9]]
map(lambda n: months.add_transition(n, "1", "3"),num)

months.add_transition("0", "2", "3")
months.add_transition("1", "2", "3")
months.add_transition("2", "2", "3")


months.set_final_state("3")

days = FSA(5)

days.add_transition("0", "0", "1")
days.add_transition("1", "0", "2")
days.add_transition("2", "0", "2")
days.add_transition("3", "0", "3")

num = [str(n) for n in [1,2,3,4,5,6,7,8,9]]
map(lambda n: days.add_transition(n, "1", "4"),num)

num = [str(n) for n in [0,1,2,3,4,5,6,7,8,9]]
map(lambda n: days.add_transition(n, "2", "4"),num)

days.add_transition("0", "3", "4")
days.add_transition("1", "3", "4")

days.set_final_state("4")

years = FSA(6)

years.add_transition("1", "0", "1")
years.add_transition("2", "0", "2")

years.add_transition("9", "1", "3")
years.add_transition("0", "2", "3")


num = [str(n) for n in [0,1,2,3,4,5,6,7,8,9]]
map(lambda n: years.add_transition(n, "3", "4"),num)

num = [str(n) for n in [0,1,2,3,4,5,6,7,8,9]]
map(lambda n: years.add_transition(n, "4", "5"),num)

years.set_final_state("5")

seps = FSA(2)

seps.add_transition("/", "0", "1")
seps.add_transition(" ", "0", "1")
seps.add_transition("-", "0", "1")

seps.set_final_state("1")

print ("Testing Months Example...")
print ("DRecognize(12, months)  ", DRecognize("12", months))
print ("DRecognize(13, months)  ", DRecognize("13", months))
print()


def Test(months, days, years, seps):
    #print "\nTest Months FSA"
    for input in ["", "00", "01", "1", "09", "9", "10", "11", "12", "13", "123"]:
        print ("'%s'\t%s" %(input, DRecognizeMulti(input, [months])))
    #print "\nTest Days FSA"
    for input in ["", "00", "01", "09", "9", "10", "11", "21", "31", "32", "123"]:
        print ("'%s'\t%s" %(input, DRecognizeMulti(input, [days])))
    #print "\nTest Years FSA"
    for input in ["", "1899", "1900", "1901", "1999", "2000", "2001", "2099", "2100"]:
        print( "'%s'\t%s" %(input, DRecognizeMulti(input, [years])))
    #print "\nTest Separators FSA"
    for input in ["", ",", " ", "-", "/", "//", ":"]:
        print ("'%s'\t%s" %(input, DRecognizeMulti(input, [seps])))
   # print "\nTest Date Expressions FSA"
    for input in ["", "12 31 2000", "12/31/2000", "12-31-2000", "12:31:2000", 
                  "00-31-2000", "12-00-2000", "12-31-0000", 
                  "12-32-1987", "13-31-1987", "12-31-2150"]:
        print( "'%s'\t%s" %(input, 
                           DRecognizeMulti(input, [months, seps, days, seps, years])))

Test(months, days, years, seps)






