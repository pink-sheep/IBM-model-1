import re
##en_file = open("toy.en")
##de_file = open("toy.de")

##en_file = open("de-en.tiny.en")
##de_file = open("de-en.tiny.de")

tab_file = open("tab.txt", "w")
align_file = open("align.txt", "w")

# punctuation
punctuation = [",",".","?","!","%","(",")","'",";",":",'"', "-"]

# english stats
e_sents = []
e_words = set()
for line in en_file:
    temp0 = []
    spline0 = line.split()
    clean0 = [x for x in spline0 if x not in punctuation]
    for each in clean0:
        temp0.append(each)
        e_words.add(each)
    e_sents.append(temp0)

# german stats
f_sents = []
f_words = set()
for line in de_file:
    temp1 = []
    spline1 = line.split()
    clean1 = [x for x in spline1 if x not in punctuation]
    for each in clean1:
        temp1.append(each)
        f_words.add(each)
    f_sents.append(temp1)

# sentence pairs
pairs = []
for i in range (0, len(e_sents)):
    pairs.append((e_sents[i], f_sents[i]))

# IBM model 1
def IBM_model():
# unform initialisation
    global e_words
    global e_sents
    global f_words
    global f_sents
    global pairs
    t = {}
    for e in e_words:
        for f in f_words:
            t [(e,f)] = 1.0/(len(e_words) * len(f_words))
    t2 ={}
    # do until converge
    conv = 1
    while (conv!=0):
        # set count(e,f) to 0
        count = {}
        for e in e_words:
            for f in f_words:
                count[(e,f)] = 0.0
        #set total(f) to 0
        total = {}
        for f in f_words:
            total[f] = 0.0
        # for all sentence pairs
        for each in pairs:
            (e_s, f_s) = each
            #for all words in e_s
            total_s = {}
            for e in e_s:
                total_s[e]=0.0
                # for all words in f_s
                for f in f_s:
                    total_s[e] = total_s[e] + t[(e,f)]
            #for all words in e_s
            for e in e_s:
                #for all words in f_s
                for f in f_s:
                    count[(e,f)] = count[(e,f)] + (t[(e,f)]/total_s[e])
                    total[f] =  total[f] + (t[(e,f)]/total_s[e])
        # for all f
        for f in f_words:
            #for all e
            for e in e_words:
                t2[(e,f)] = count[(e,f)]/total[f]

        diff = []
        for key in t2:
            d = abs(t.get(key) - t2.get(key))
            diff.append(d)

        check = [x for x in diff if x > 0.001]


        if (check == []) :
            conv = 0
        else:
            t.update(t2)
    return t


# A table containing the word translation probabilities that were learned
def table(dic):
    global tab_file
    freq_list = [(key, val) for key, val in dic.items()]
    freq_list.sort()
    tab_file.write("The word translation probabilities that were learned\n\n")  
    for item in freq_list:
        if (item[1] != 0.0):
            line = item[0][0] + "\t\t" + item[0][1] + "\t\t" + str(item[1]) + "\n"
            tab_file.write(line)  
    tab_file.close()

# Word Best Alignment
def align(pairs, dic):
    global align_file
    align_file.write("The most probable word alignment \n\n")
    for pair in pairs:
        (e_sent, f_sent) = pair
        order = []
        f_sent2 = []
        for e in e_sent:
            prob = 0.0
            for f in f_sent:
                p_ef = dic.get((e,f))
                if (p_ef > prob):
                    prob = p_ef
                    e_loc = e_sent.index(e) 
                    f_loc = f_sent.index(f)
            line = str(e_loc+1) + " -> " + str(f_loc+1) 
            order.append(line)
            f_sent2.insert(f_loc, f_sent[f_loc])
            f_sent[f_loc] = ""
        esent = " ".join(e_sent)
        fsent = " ".join(f_sent2)
        order2 = "; ".join(order)
        align_file.write(esent + "\n")
        align_file.write(fsent + "\n")
        align_file.write(order2+ "\n\n")
        
    align_file.close()
                    
if __name__ == "__main__":
    t = IBM_model()
    table(t)
    align(pairs, t)
    
    

    
    

    
       
    


            
    
    

        

