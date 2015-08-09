import sys

#Process the given file line by line and call DPLL function
def Process():
    with open('CNF_satisfiability.txt', 'r') as f:
    #with open(sys.argv[2], 'r') as f:
        no_of_lines=-1
        output = open("satisfiability_CNF.txt",'w+')
        i=0
        for line in f:
            if (no_of_lines==0) :
                ##print "Done Processing given number of lines as per firstline"
                break
            if no_of_lines==-1 :
                no_of_lines=int(line)+1
            else:
                try:
                    op=DPLL(eval(line))
                    #BuildModel()
                    print i
                    print op
                    i+=1
                    output.write(str(op)+'\n')
                except:
                    output.write('["false"]'+'\n')
            no_of_lines-=1

def DPLL(sentence):
    ##print sentence
    clauses=[]
    model=[]
    no_of_clauses=0
    symbols=set()
    if len(sentence)==0:
        return '["false"]'
    for i in sentence:
        if type(i)==type("") and str(i)=="and":
            pass
        else:
            if i is not list and i=="or" or i=="not":
                clauses.append(sentence)
                no_of_clauses+=1
                break
            else:
                clauses.append(i)
                no_of_clauses+=1
    #print "all clauses=",clauses
    #print "no. of clauses=",no_of_clauses
    symbols=Symbol(clauses)
    #print "sumbols=",symbols
    while(not canistop(model,symbols,clauses)):
        find_pure_symbols(clauses,symbols,model)
        if(isemptyclause(clauses)):
            return '["false"]'
        if len(clauses)!=0:
            clauses=find_unit_clauses(clauses,model)
        #print "model=",model
        #print "final clauses=",clauses
        #print "program can exit=",canistop(model,symbols,clauses)
        if(isemptyclause(clauses)):
            return '["false"]'
        for parent in clauses:
            for child in parent:
                if type(child) is list:
                    temp_c=list(clauses)
                    temp_c.append(child[1])
                    temp_m=list(model)
                    if(call_rest(temp_c,temp_m,symbols)==0):
                        temp_c=list(clauses)
                        temp_c.append("['not',"+child[1]+"]")
                        if(call_rest(temp_c,temp_m,symbols)==0):
                            return '["false"]'
                        else:
                            return BuildModel(temp_m)
                    else:
                        return BuildModel(temp_m)
                if type(child) is str and child!="and" and child!="or":
                    temp_c=list(clauses)
                    temp_c.append(child)
                    temp_m=list(model)
                    if(call_rest(temp_c,temp_m,symbols)==0):
                        temp_c=list(clauses)
                        temp_c.append("['not',"+child+"]")
                        if(call_rest(temp_c,temp_m,symbols)==0):
                            return '["false"]'
                        else:
                            return BuildModel(temp_m)
                    else:
                        return BuildModel(temp_m)
  
    return BuildModel(model)

def call_rest(clauses,model,symbols):
    while(not canistop(model,symbols,clauses)):
        find_pure_symbols(clauses,symbols,model)
        if(isemptyclause(clauses)):
            return 0
        if len(clauses)!=0:
            clauses=find_unit_clauses(clauses,model)
        if(isemptyclause(clauses)):
            return 0
    return 1

def BuildModel(model):
    output=[]
    #temp_model=
    output.append("true")
    for m in model:
        if type(m) is list:
            output.append(m[1]+"=false")
        else:
            output.append(m+"=true")
    return output

def Symbol(clauses):
    symbol=set()
    for parent in clauses:
        if type(parent) is list:
            for child in parent:
                if child!="or" and child!="not":
                    if type(child) is list:
                        symbol.add(str(child[1]))
                    else:
                        symbol.add(str(child))
        elif parent!="or" and parent!="not":
             symbol.add((parent))
    return symbol

#returns true if no more processing is required i.e. when model contains all symbols
def canistop(model,symbols,clauses):
    model_symbols=set()
    remaining_symbols=set()
    model_symbols=Symbol(model)
    remaining_symbols=symbols.difference(model_symbols)
    ##print "rem symbols=",remaining_symbols
    if(len(remaining_symbols)==0 and len(clauses)==0):
        return 1
    else:
        return 0
        
def isemptyclause(clauses):
    for i in clauses:
        if type(i) is list and len(i)==0:
            return 1
        else:
            return 0

def find_unit_clauses(clauses,model):
    
    unit_clauses=[]
    temp_clauses=list(clauses)
    no_deleted=0
    for i,parent in enumerate(clauses):
        
        if type(parent) is list:
            if parent[0]=="not":
                if parent[1] not in unit_clauses:
                    unit_clauses.append(parent)
                    
                    del temp_clauses[i-no_deleted]
                    no_deleted+=1
                
                
        else:
            unit_clauses.append(parent)
            
            del temp_clauses[i-no_deleted]
            no_deleted+=1
    clauses=temp_clauses
    for unit in unit_clauses:
        if type(unit) is list:
            if unit[0]=="not":
                cur_sym=unit[1]
                for i,parent in enumerate(clauses):
                    if type(parent) is  list:
                        for j,child in enumerate(parent):
                            if type(child) is str and child!="or":
                                if cur_sym==child:
                                    del temp_clauses[i][j]
                                    
        elif type(unit) is str and unit!="or":
            cur_sym=unit
            for i,parent in enumerate(clauses):
                 if type(parent) is  list:
                      if parent[0]=="not" and parent[1]==cur_sym:
                          del temp_clauses[i][0]
                          del temp_clauses[i][0]
                          
                      for j,child in enumerate(parent):
                          if type(child) is list and child[0]=="not":
                               if cur_sym==child[1]:
                                #p=list(parent)
                                ###print "p=",parent
                                del temp_clauses[i][j]
                            
                          
    #clauses=[]
    #clauses=temp_clauses
    ##print "Clauses=",clauses    
              
    ##print "Unit clauses=",unit_clauses
    
    ##print "Remaining Clauses=",temp_clauses
    for i,parent in enumerate(temp_clauses):
        if type(parent) is list and len(parent)<3:
                for j,child in enumerate(parent):
                    if type(child) is str and child=='or':
                        del temp_clauses[i][j]
    ##print "Remaining Clauses later=",temp_clauses
    for p in unit_clauses:
        flag=0
        for m in model:
            if type(p) is list and type(m) is list:
                if p[1]==m[1]:
                    flag=1
            if type(p) is str and type(m) is str:
                if p==m:
                    flag=1
            if type(p) is list and type(m) is str:
                if p[1]==m:
                    flag=1
            if type(p) is str and type(m) is list:
                if p==m[1]:
                    flag=1
        if(flag==0):
            model.append(p)
                 
    return temp_clauses

def find_pure_symbols(clauses,symbols,model):
    pure_symbols=[]
    
    for cur_sym in symbols:
        sym_count=0
        pure_sym=0
        pure_sym_not=0
        
        
        ###print "cur_sym=",cur_sym
        for i,parent in enumerate(clauses):
            ###print "parent=",parent
            if type(parent) is list:
               if(parent[0]=="not" and cur_sym==parent[1]):
                            ###print "in parent list"
                            pure_sym_not+=1
                            continue
               for j,child in enumerate(parent):
                   ###print "child=",child
                   if type(child) is list :
                        if(cur_sym==child[1]):
                            ##print "in child list"
                            pure_sym_not+=1
                            
                   else:
                        if(cur_sym==child):
                            ##print "in child str"
                            pure_sym+=1
            elif parent!="or" and parent!="not":
                if(cur_sym==parent):
                    pure_sym+=1
            ##print "cur_sym=",cur_sym
            ##print "pure_sym count=",pure_sym_not,pure_sym
        if(pure_sym>=1 and pure_sym_not>=1):
            ##print "cur_sym=",cur_sym
            ##print "not a pure symbol"
            pass
        else:
            ##print "cur_sym=",cur_sym
            if(pure_sym_not==0):
                ##print "it is a pure symbol"
                #cur=[]
                #cur.append(cur_sym)
                pure_symbols.append(cur_sym)
            else:
                ##print "not of it is a pure symbol"
                cur=[]
                cur.append("not")
                cur.append(cur_sym)
                pure_symbols.append(cur)
    #print "pure_symbols=",pure_symbols
    temp_clauses=(clauses)
    #print "clauses=",clauses
    no_deleted=0
    for p in pure_symbols:
        ##print "p=",p
        for i,parent in enumerate(clauses):
            ##print "parent=",parent
            if len(temp_clauses)==0:
                    break
            
            if type(parent) is list:
               ##print "in here1",type(p)
               if type(p) is list:
                   ##print "in here2"
                   if(parent[0]=="not" and p[1]==parent[1]):
                            ##print "in here"
                            del temp_clauses[i-no_deleted]
                            #no_deleted+=1
                            continue
               for j,child in enumerate(parent):
                  
                   if type(child) is list :
                        if type(p) is list:
                            if(p[1]==child[1]):
                                del temp_clauses[i-no_deleted]
                                #no_deleted+=1
                                continue
                        
                   else:
                        if(p==child):
                            del temp_clauses[i-no_deleted]
                            #no_deleted+=1
                            continue
            elif parent!="or" and parent!="not":
                if(p==parent):
                    del temp_clauses[i-no_deleted]
                    #no_deleted+=1
                    continue
    #print "Remaining clauses are=",temp_clauses
    #print "pure clauses=",clauses
    clauses=temp_clauses
    
    
    #print "pure sym=",pure_symbols
    
    for p in pure_symbols:
        flag=0
        for m in model:
            if type(p) is list and type(m) is list:
                if p[1]==m[1]:
                    flag=1
            if type(p) is str and type(m) is str:
                if p==m:
                    flag=1
            if type(p) is list and type(m) is str:
                if p[1]==m:
                    flag=1
            if type(p) is str and type(m) is list:
                if p==m[1]:
                    flag=1
        if(flag==0):
            model.append(p)
        
                
                
    
                 
        
    return 

#Main function to initiate file processing  
if __name__=="__main__":
    Process()


    
    
