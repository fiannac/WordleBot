import random as rand
import settings
global dictionary
global answer


def binary_search(vect, elem, begin, end):
    if(begin > end):
        return -1;
    p = int((begin+end)/2);
    if(vect[p] == elem):
            return p;
    elif(begin == end):
        return -1;
    elif(vect[p]>elem):
        return binary_search(vect, elem, begin, p-1);
    return binary_search(vect, elem, p+1, end);
    
def search_word(dic, word):
    return binary_search(dic, word + '\n', 0, len(dic)-1) != -1;


def cmp_words(word, ans, white_char, grey_char, yellow_char, green_char):
    #0 gray, 1 yellow, 2 green
    res = [0,0,0,0,0];
    occ = [0,0,0,0,0];
    
    for n,c in zip(range(5),word):
        if c == ans[n]:
            occ[n] = 1;
            res[n] = 2;
            
    for n,c in zip(range(5),word):
        for i in range(5):
            if occ[i] == 0 and c == ans[i] and res[n]==0:
                occ[i] = 1;
                res[n] = 1;
    
    for n,c in zip(range(5),word):
        if res[n] == 0:
            if c in white_char: white_char.remove(c);
            if c not in grey_char: grey_char.append(c);
        elif res[n] == 1:
            if c in white_char: white_char.remove(c);
            if c not in yellow_char and c not in green_char: yellow_char.append(c);
        elif res[n] == 2:
            if c in white_char: white_char.remove(c);
            if c in grey_char: grey_char.remove(c);
            if c in yellow_char: yellow_char.remove(c);
            if c not in green_char: green_char.append(c);
            
    return res;

def rand_word():
    sol = rand.choice(settings.answer);
    return sol;
