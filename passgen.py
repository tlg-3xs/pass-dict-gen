#!/usr/bin/python3
import sys, argparse, datetime, signal

def arg_parser():
    parser = argparse.ArgumentParser(description="Creates a custom password wordlist from a set of keywords and phrases.")
    parser.add_argument('-i','--input',dest='input', type=argparse.FileType('r'), default=sys.stdin, nargs='?', help='Input file for keywords. If not specified defaults to stdin.')
    parser.add_argument('-o','--output', dest='output', type=argparse.FileType('w'), default=sys.stdout, nargs='?', help='Output file. If not specified defaults to stdout.')
    parser.add_argument('-y','--year', dest='year', type=int, action='append', default=[], const=datetime.datetime.now().year, nargs='?', help='Year for making combinations. Can be specified multiple times. If it\'s specified without value defaults to actual year.')
    parser.add_argument('--all', action='store_true', help='Makes all posible combinations. -y value can be specified normally (by default assumes -y).')
    parser.add_argument('-d','--dollar', dest='dollar', action='store_true', help='Replaces s and S with $.')
    parser.add_argument('-at', dest='at', action='store_true', help='Replaces a and A with @.')
    parser.add_argument('-l','--l337','--l33t', dest='l337', action='store_true', help='Replaces letters with numbers.')
    parser.add_argument('-q','--quiet',dest='quiet',action='store_true', help='Suppresses the message requesting input from stdin. Use it when the input is provided by another program.')
    parser.add_argument('-min','--minimum',dest='min',action='store', type=int, default=1, help='Minimum length of password. Default=1')
    parser.add_argument('-max','--maximum',dest='max',action='store', type=int, default=200, help='Maximum length of password. Default=200')
    return parser.parse_args()

def main(args):
    try:
        result=set()
        if args.all: #check if --all flag has been set
            args.year.append(datetime.datetime.now().year) #add the current year to the list
        args.year=list(set(args.year)) #remove duplicates if there's any
        if args.input == sys.stdin and not args.quiet:
            print("Insert input, one per line. Finish with a newline plus ctrl+c:", file=sys.stderr)
        try:
            for lines in args.input: #read from choosen input
                words = lines.strip().split()
                if words: #check for avoid empty lines
                    for i in range(len(words)):
                        w = words.pop(0)
                        words.append(w.capitalize())
                    w = ''.join(words)
                    result.add(w)
                    result.add(w.lower())
                    if len(words) > 1: #check if it's a single word or a sentence
                        result.add('_'.join(words))
                        result.add('_'.join(words).lower())
                    if args.l337 or args.all: #check if l337 or --all flags has been set
                        result.update(f_l337(w,args))
                    else:
                        total=set()
                        if args.dollar: #check if dollar flag has been set
                            for x in result:
                                if x.find('s')!=-1 or x.find('S')!=-1:
                                    total.add(x.replace('s','$').replace('S','$'))
                        if args.at: #check if at flag has been set
                            for x in result:
                                if x.find('a')!=-1 or x.find('A')!=-1:
                                    total.add(x.replace('a','@').replace('A','@'))
                        result.update(total)
        except KeyboardInterrupt: #allows the use of Ctrl+C as EOF
            pass
        total=set()
        for x in result:
            total.update(base(x,len(words)))
        result.update(total)
        for x in result:
            if args.min <= len(x) and args.max >= len(x):
                print(x,file=args.output)
    except KeyboardInterrupt:
        print("Catched SIGINT. Exiting...")
        if args.input != sys.stdin:
            args.input.close()
        if args.output != sys.stdout:
            args.output.close()
        sys.exit(0)


def base(w, length):
    result=year_signs(w)
    result.update(year_signs(w.lower()))
    result.update(year_signs(w.upper()))
    if length > 1: #w was a single word originally, it comes capitalized in first place. This is a check for avoid duplicates.
        result.update(year_signs(w.capitalize()))
    if hasVowel(w):
        result.update(year_signs(upperVowel(w)))
        if w.capitalize() != year_signs(upperVowel(w).swapcase()):
            result.update(year_signs(upperVowel(w).swapcase()))
    return result

def hasVowel(word): #simple function that returns if a word has a vowel.
    return word.find('a')!=-1 or word.find('A')!=-1 or word.find('e')!=-1 or word.find('E')!=-1 or word.find('i')!= -1 or word.find('I')!=-1 or word.find('o')!=-1 or word.find('O')!=-1 or word.find('u')!=-1 or word.find('U')!=-1

def upperVowel(word): #returns the word with all vowels uppercased
    return word.lower().replace('a','A').replace('e','E').replace('i','I').replace('o','O').replace('u','U')

def year_signs(w1): #returns a set with combinations of the word and the signs and, if specified, the year(s)
    result=set()
    result.update(signs(w1,1)) #combines the word and signs after it
    result.update(signs(w1,2)) #combines the word and signs before it
    if args.year:
        result.update(year(w1,1)) #combines the word and year(s) after it
        result.update(year(w1,2)) #combines the word and year(s) before it
        for x in year(w1,1):
            result.update(signs(x,1)) #combination of word+year+sign
            result.update(signs(x,2)) #combination of sign+word+year
        for x in signs(w1,1):
            result.update(year(x,1)) #combination of word+sign+year
            result.update(year(x,2)) #combination of year+word+sign
        for x in year(w1,2):
            result.update(signs(x,2)) #combination of sign+year+word
        for x in signs(w1,2):
            result.update(year(x,2)) #combination of year+sign+word
    return result

def year(word,mode): #returns a set with combinations of the word and the year(s)
    total=set()
    for y in args.year:
        if mode == 1:
            total.add(word+str(y)) #combination of word+year with 4 digits
            total.add(word+str(y)[::-1]) #combination of word + reversed year
            total.add(word+str(y)[2:])  #combination of word+year with 2 digits
            total.add(word+str(y)[2:][::-1]) #combination of word + reversed year with 2 digits
        else:
            total.add(str(y)+word) #combination of year+word with 4 digits
            total.add(str(y)[::-1]+word) #combination of reversed year with 4 digits + word
            total.add(str(y)[2:]+word) #combination of year with 2 digits + word
            total.add(str(y)[2:][::-1]+word) #combination of reversed year with 2 digits + word
    return total

def signs(word,mode): #returns a set with combinations of the word and signs
    signs_list=['*','#','\'','?','¡','¿','!','\\','|','º','ª','\"','@','·','$','~','%','&','/','(',')','=','^','[',']','{','}','+','<','>','_','-',';',',','.']
    result=set()
    for x in signs_list:
        if mode == 1:
            result.add(word+x) #combination of word+sign
        else:
            result.add(x+word) #combination of sign+word
    return result

def l337_a(word): #returns the word with a vowel replaced with 4
    if word is not None:
            return word.replace("a","4").replace("A","4")
    return None

def l337_e(word): #returns the word with e vowel replaced with 3
    if word is not None:
            return word.replace("e","3").replace("E","3")
    return None

def l337_i(word): #returns the word with i vowel replaced with 1
    if word is not None:
            return word.replace("i","1").replace("I","1")
    return None

def l337_o(word): #returns the word with o vowel replaced with 0
    if word is not None:
            return word.replace("o","0").replace("O","0")
    return None

def l337_s(word): #returns the word with s letter replaced with 5
    if word is not None:
            return word.replace("s","5").replace("S","5")
    return None

def l337_t(word): #returns the word with t letter replaced with 7
    if word is not None:
            return word.replace("t","7").replace("T","7")
    return None

def dollar(word): #returns the word with s letter replaced with $
    if word is not None and (word.find('s')!=-1 or word.find('S')!=-1):
            return word.replace("s","$").replace("S","$")
    return None

def at(word): #returns the word with a vowel replaced with @
    if word is not None and (word.find('a') != -1 or word.find('A') != -1):
        return word.replace("a","@").replace("A","@")
    else:
        return None

def f_l337(word,args): #returns a set with combinations of the word in a l337 fashion
    l337_list=[]
    if word.find('a') != -1 or word.find('A') != -1:
        l337_list.append(l337_a)
        if args.at or args.all:
            l337_list.append(at)
    if word.find('e') != -1 or word.find('E') != -1:
        l337_list.append(l337_e)
    if word.find('i') != -1 or word.find('I') != -1:
        l337_list.append(l337_i)
    if word.find('o') != -1 or word.find('O') != -1:
        l337_list.append(l337_o)
    if word.find('s') != -1 or word.find('S') != -1:
        l337_list.append(l337_s)
        if args.dollar or args.all:
            l337_list.append(dollar)
    if word.find('t') != -1 or word.find('T') != -1:
        l337_list.append(l337_t)
    return fr_l337(word,l337_list,0)

def fr_l337(w,l_list,j): #recursive function for making combinations of l337 functions of the word
    total=set()
    for i in range(j,len(l_list)):
        word=l_list[i](w)
        if word is not None:
            total.add(word)
            total.update(fr_l337(word,l_list,j+1))
    return total

if __name__ == "__main__":
    args = arg_parser()
    main(args)
