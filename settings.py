def load_words(pos_dic, pos_ans):
    dictionary_f = open(pos_dic, "r");
    answer_f = open(pos_ans, "r");
    
    dictionary = [];
    answer = [];
    for w in dictionary_f:
        dictionary.append(w);
    for w in answer_f:
        answer.append(w);
    dictionary_f.close();
    answer_f.close();
    dictionary.sort();
    answer.sort();
    return dictionary, answer;

def init():
    global dictionary
    global answer
    dictionary, answer = load_words("dictionary.txt", "answer.txt");
    