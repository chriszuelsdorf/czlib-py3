# create an object that gets fed a csv file, which you then read into, and 
#   can access fields given a key, as a string aka c.g("foo$bar")
#   would access the field bar from primary key foo.
class cscsv:
    '''Custom CSV Reader. Allows easy reference to column headers in R style.
        
    Inital Parameters:
    file: pass a freshly opened file object.
    unique_id_colname: pass a case-sensitive column name to use as a key-column
    '''
    def __init__(self, file, unique_id_colname):
        self.dictionary = {} # keys are objnames, values are dicts
        self.modeldict = {} # keys are colnames, values should be empty
        self.refs = {} # keys are positions, and values are colnames
        fl = True
        for line in file:
            if fl:
                # setup firstline
                fl = not fl
                # get the line
                t = line.strip().split(',')
                # loop all fields
                i = 0
                for e in t:
                    # add to the model dictionary
                    self.modeldict[e.upper()] = ""
                    # add to the helper list
                    self.refs[i] = e.upper()
                    i += 1
            else:
                if unique_id_colname not in self.modeldict.keys():
                    raise ValueError("Invalid unique_id_colname given.")
                t = line.strip().split(',') # get the linelist
                a = dict(self.modeldict) # create a copy of the model dictionary
                if len(t) != len(a.keys()):
                    raise ValueError("Length of line and length of colnames don't match. Check if your CSV contains extra commas (try importing to Excel, find-and-replacing all commas, and saving).")
                # now we are ready to read the line
                for i in range(len(t)):
                    colname = str(self.refs[i])
                    a[colname] = str(t[i])
                # now that the local dictionary is populated, we use the key to give it to the higher 
                #   power, unless the self.dictionary already has a key.
                if a[unique_id_colname] in self.dictionary:
                    print(line)
                    raise ValueError("The key already exists.")
                else:
                    self.dictionary[a[unique_id_colname]] = dict(a)

    # read file into memory, and setup as internal dictionary
    def get_dict(unique_id):
        '''Obtains a dictionary which mimics a row from the CSV.
        
        Param:
        unique_id: the value from the key-column assigned at creation.
        '''
        try:
            t = self.dictionary[unique_id]
            return t
        except KeyError:
            raise KeyError("No valid key for input {uid}".format(uid=unique_id))

    # get a specific entry, with dollarsign separator
    def get_dollar(inpstr):
        '''Obtains an entry from the CSV, in R fashion.
        
        Param:
        inpstr: should be unique_id$col_name.
        '''
        a = inpstr.split('$')
        if len(a) != 2:
            raise ValueError("Expected dollarsign-delimited input of length 2.")
        try:
            return self.dictionary[a[0]][a[1]]
        except KeyError:
            raise KeyError("No valid key combination for {inst}, returning empty string.".format(inst=inpstr))
    
    # get based on 2arg input
    def get_2arg(self, uid, colname):
        '''Obtains an entry from the CSV, via two arguments.
        
        Param:
        uid: the value from the primary-key-column assigned at creation.
        colname: the desired column id/header
        '''
        if uid not in self.dictionary:
            raise ValueError("No uid key in dictionary for {unid}.".format(unid=uid))
        try:
            return self.dictionary[uid][colname]
        except KeyError:
            raise KeyError("No colname key in dictionary for {cn}.".format(cn=colname))
