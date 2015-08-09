import sys
#Global flag to initiate OR distribution after first pass
do_dis=0
#Process the given file line by line and call Convert function
def Process():
    global do_dis
    with open('sentences.txt', 'r') as f:
    #with open(sys.argv[2], 'r') as f:
        no_of_lines=-1
        output = open("sentences_CNF.txt",'w+')
        for line in f:
            if (no_of_lines==0) :
                #print "Done Processing given number of lines as per firstline"
                break
            if no_of_lines==-1 :
                no_of_lines=int(line)+1
            else:
                try:
                    do_dis=0
                    inter=Convert2CNF(eval(line))
                    #print "i=",inter
                    #Distribute OR after all other reductions
                    do_dis=1
                    #output.write(str(inter)+'\n')
                    op=Convert2CNF(eval(inter))
                    #print op
                    output.write(str(op)+'\n')
                except:
                    output.write(str(line)+'\n')
            no_of_lines-=1
        
#Recursive function to reduce the expressions
#Expected input is of type list
def Convert2CNF(line):
    sentence = line
    if sentence[0]=="implies":
        sentence = reduce_implies(sentence[1],sentence[2])
    elif sentence[0]=="not":
        sentence = reduce_not(sentence[1])
    elif sentence[0]=="iff":
        sentence = reduce_iff(sentence[1],sentence[2])
    elif sentence[0]=="and":
        sentence = reduce_and(sentence[1],sentence[2])
    elif sentence[0]=="or":
        #print "calling or for sen=",sentence
        sentence = reduce_or(sentence[1],sentence[2])
        #print "after_or=",sentence
    else:
        return "'"+str(sentence)+"'"
    return str(sentence)

#Reduce and and call Convert if it is nested
def reduce_and(firstpart,secondpart):
    firstpart=Convert2CNF((firstpart))
    secondpart=Convert2CNF((secondpart))
    #Handle same literal
    if(firstpart==secondpart):
        return firstpart
    if type(eval(firstpart))!=type(""):
        firstpart=eval(firstpart)
        if firstpart[0]=="and":
                firstpart=(Convert2CNF(firstpart[1]))+","+(Convert2CNF(firstpart[2]))
    if type(eval(secondpart))!=type(""):
        secondpart=eval(secondpart)
        if secondpart[0]=="and":
                secondpart=(Convert2CNF(secondpart[1]))+","+(Convert2CNF(secondpart[2]))
   
    and_ret="['and',"+str(firstpart)+","+str(secondpart)+"]"
    return and_ret

#Reduce OR , also has logic for dirtibution of OR when do_dis flag is set
#dis_flag tells if distribution happened
def reduce_or(firstpart,secondpart):
    #print "in ordo_dis=",do_dis
    dis_flag=0
    firstpart=Convert2CNF((firstpart))
    secondpart=Convert2CNF((secondpart))
    if(firstpart==secondpart):
        return firstpart
    org_firstpart=firstpart
    if type(eval(firstpart))!=type(""):
        firstpart=eval(firstpart)
        
        if do_dis==1:
            if firstpart[0]=="or":
               firstpart=(Convert2CNF(firstpart[1]))+","+(Convert2CNF(firstpart[2]))
            if firstpart[0]=="and":
                    dis_flag=1
                    #Logic to distribute or over and
                    if type(eval(secondpart))!=type(""):
                        secondpart1=eval(secondpart)
                        if secondpart1[0]=="or":
                            if firstpart[1]==secondpart1[2]:
                                return "['and',['or',"+Convert2CNF(firstpart[1])+","+Convert2CNF(secondpart1[1])+"],['or',"+Convert2CNF(firstpart[2])+","+Convert2CNF(secondpart1[1])+","+Convert2CNF(secondpart1[2])+"]]"  
                            if firstpart[1]==secondpart1[1]:
                                return "['and',['or',"+Convert2CNF(firstpart[1])+","+Convert2CNF(secondpart1[2])+"],['or',"+Convert2CNF(firstpart[2])+","+Convert2CNF(secondpart1[1])+","+Convert2CNF(secondpart1[2])+"]]"  
                            if firstpart[2]==secondpart1[2]:
                                return "['and',['or',"+Convert2CNF(firstpart[1])+","+Convert2CNF(secondpart1[1])+","+Convert2CNF(secondpart1[2])+"],['or',"+Convert2CNF(secondpart1[1])+","+Convert2CNF(secondpart1[2])+"]]"
                            if firstpart[2]==secondpart1[1]:
                                return "['and',['or',"+Convert2CNF(firstpart[1])+","+Convert2CNF(secondpart1[1])+","+Convert2CNF(secondpart1[2])+"],['or',"+Convert2CNF(secondpart1[1])+","+Convert2CNF(secondpart1[2])+"]]"
                            
                            else:
                                return "['and',['or',"+Convert2CNF(firstpart[1])+","+Convert2CNF(secondpart1[1])+","+Convert2CNF(secondpart1[2])+"],['or',"+Convert2CNF(firstpart[2])+","+Convert2CNF(secondpart1[1])+","+Convert2CNF(secondpart1[2])+"]]"
                        else:    
                            firstpart="['or',"+Convert2CNF(firstpart[1])+","+Convert2CNF(secondpart1[1])+"],['or',"+Convert2CNF(firstpart[2])+","+Convert2CNF(secondpart1[1])+"]"
                    else:
                        firstpart="['or',"+Convert2CNF(firstpart[1])+","+str(secondpart)+"],['or',"+Convert2CNF(firstpart[2])+","+str(secondpart)+"]" 
        
    if type(eval(secondpart))!=type(""):
        secondpart=eval(secondpart)
        
        
        if do_dis==1:
            if secondpart[0]=="or":
                secondpart=(Convert2CNF(secondpart[1]))+","+(Convert2CNF(secondpart[2]))
            if secondpart[0]=="and":
                    dis_flag=1
                    if type(eval(org_firstpart))!=type(""):
                        firstpart1=eval(org_firstpart)
                        secondpart="['or',"+Convert2CNF(firstpart1[1])+","+Convert2CNF(secondpart[2])+"],['or',"+Convert2CNF(firstpart1[2])+","+Convert2CNF(secondpart[2])+"]"
                    else:
                        secondpart="['or',"+str(firstpart)+","+Convert2CNF(secondpart[2])+"],['or',"+str(firstpart)+","+Convert2CNF(secondpart[2])+"]"
        
    if(dis_flag):
        return "['and',"+str(firstpart)+","+str(secondpart)+"]"
    else:
        or_ret="['or',"+str(firstpart)+","+str(secondpart)+"]"    
    return or_ret

#Reduce implies recursively  
def reduce_implies(firstpart,secondpart):
    #print "In implies",firstpart
    #print "in implies sec",secondpart
    firstpart=Convert2CNF((firstpart))
    secondpart=Convert2CNF((secondpart))
    firstpart_convert=eval("['not',"+firstpart+"]")
    #We might have to reduce the firstpart further
    firstpart_convert=Convert2CNF(firstpart_convert)
    implies_ret="['or',"+firstpart_convert+","+secondpart+"]"
    #print "impl ret=",implies_ret
    #return Convert2CNF(eval(implies_ret))
    return ((implies_ret))

#Reduce not and also has Demorgan's logic 
def reduce_not(firstpart):
        #print "in not fp=",type(firstpart)
        firstpart=Convert2CNF(firstpart)
        firstpart=eval(firstpart)
        #print "in not",firstpart
        #De-Morgan's reduction
        if firstpart[0]=="and":
            firstpart="['or',"+str(reduce_not(eval(Convert2CNF(firstpart[1]))))+","+str(reduce_not(eval(Convert2CNF(firstpart[2]))))+"]"
            return Convert2CNF(eval(firstpart))
        if firstpart[0]=="or":
            firstpart="['and',"+reduce_not(eval(Convert2CNF(firstpart[1])))+","+reduce_not(eval(Convert2CNF(firstpart[2])))+"]"
            #print "in or",firstpart
            return Convert2CNF(eval(firstpart))
        if firstpart[0]=="not":
            firstpart=Convert2CNF(firstpart[1])
            #print firstpart
            return (firstpart)
        
        not_ret="['not','"+firstpart+"']"
        return not_ret
#Reduce iff recursively 
def reduce_iff(firstpart,secondpart):
    #print "in iff"
    firstpart=Convert2CNF((firstpart))
    secondpart=Convert2CNF((secondpart))
    iff_ret="['and',"+reduce_implies(eval(firstpart),eval(secondpart))+","+reduce_implies(eval(secondpart),eval(firstpart))+"]"
    #print iff_ret
    return (iff_ret)

#Main function to initiate file processing  
if __name__=="__main__":
    Process()
    
