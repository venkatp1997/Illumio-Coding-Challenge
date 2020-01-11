'''
Class for IP Address objects.
Defines comparators for easy comparison.
Defining the equal, not equal and less than comparison functions
is enough to do all types of comparisons.
'''
class IP:
    '''
    Defining the address instance attribute.
    '''
    def __init__(self, address):
        self.address = address
    
    '''
    Function for performing equal comparison.
    Split by '.' and check if all indices are equal.
    '''
    def __eq__(self, other):
        L1 = [int(x) for x in self.address.split(".")]
        L2 = [int(x) for x in other.address.split(".")]

        return ((L1[0] == L2[0]) and (L1[1] == L2[1]) and (L1[2] == L2[2]) and (L1[3] == L2[3]))

    '''
    Function for performing not equal comparison.
    Split by '.' and check if at least one index is not equal.
    '''
    def __ne__(self, other):
        L1 = [int(x) for x in self.address.split(".")]
        L2 = [int(x) for x in other.address.split(".")]

        return ((L1[0] != L2[0]) or (L1[1] != L2[1]) or (L1[2] != L2[2]) or (L1[3] != L2[3]))
    
    '''
    Function for performing less than comparison.
    Split by '.' and check fields from most significant to less significant.
    '''
    def __lt__(self, other):
        L1 = [int(x) for x in self.address.split(".")]
        L2 = [int(x) for x in other.address.split(".")]

        if(L1[0] == L2[0]):
            if(L1[1] == L2[1]):
                if(L1[2] == L2[2]):
                    if(L1[3] == L2[3]):
                        return False
                    else:
                        return (L1[3] < L2[3])
                else:
                    return (L1[2] < L2[2])
            else:
                return (L1[1] < L2[1])
        else:
            return (L1[0] < L2[0])

