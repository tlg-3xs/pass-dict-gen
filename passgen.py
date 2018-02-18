#!/usr/bin/python3
import sys, argparse, datetime
#Just for testing
def arg_parser():
    parser = argparse.ArgumentParser(description="Creates a custom password wordlist from a set of keywords and phrases.")
    parser.add_argument('-i','--input',dest='input', type=argparse.FileType('r'), default=sys.stdin, nargs='?', help='Input file for keywords. If not specified defaults to stdin.')
    parser.add_argument('-o','--output', dest='output', type=argparse.FileType('w'), default=sys.stdout, nargs='?', help='Output file. If not specified defaults to stdout.')
    parser.add_argument('-y','--year', dest='year', type=int, action='append', default=[], const=datetime.datetime.now().year, nargs='?', help='Year for making combinations. Can be specified multiple times. If it\'s specified without value defaults to actual year.')
    parser.add_argument('--all', action='store_true', help='Makes all posible combinations. -y value can be specified normally (by default assumes -y).')
    parser.add_argument('-d','--dollar', dest='dollar', action='store_true', help='Replaces s and S with $.')
    parser.add_argument('-at', dest='at', action='store_true', help='Replaces a and A with @.')
    parser.add_argument('-l','--l337','--l33t', dest='l337', action='store_true', help='Replaces letters with numbers.')
    return parser.parse_args()

def main(args):
    result=[]
    if args.all:
        args.year.append(datetime.datetime.now().year)
    args.year=list(set(args.year))
    for lines in args.input:
        words = lines.strip().split()
        for i in range(len(words)):
            w = words.pop(0)
            words.append(w.capitalize())
        w = ''.join(words)
        result.append(w)
        if len(words) > 1:
            result.append('_'.join(words))
        if args.l337 or args.all:
            result=result+f_l337(w,args)
        else:
            total=[]
            if args.dollar:
                for x in result:
                    if x.find('s')!=-1 or x.find('S')!=-1:
                        total.append(x.replace('s','$').replace('S','$'))
            if args.at:
                for x in result:
                    if x.find('a')!=-1 or x.find('A')!=-1:
                        total.append(x.replace('a','@').replace('A','@'))
            result=result+total
    total=[]
    for x in result:
        total=total+base(x,len(words))
    result=list(set(result+total)) #temporary fix for removing duplicates.
    for x in result:
        print(x,file=args.output)

def base(w, length):
    result=year_signs(w)
    result+=year_signs(w.lower())
    if not w.isupper():
        result+=year_signs(w.upper())
    if length > 1: #w was a single word originally, it comes capitalized in first place. This is a check for avoid duplicates.
        result+=year_signs(w.capitalize())
    if hasVocal(w):
        result+=year_signs(upperVocal(w))
        if w.capitalize() != year_signs(upperVocal(w).swapcase()):
            result+=year_signs(upperVocal(w).swapcase())
    return result

def hasVocal(word):
    return word.find('a')!=-1 or word.find('A')!=-1 or word.find('e')!=-1 or word.find('E')!=-1 or word.find('i')!= -1 or word.find('I')!=-1 or word.find('o')!=-1 or word.find('O')!=-1 or word.find('u')!=-1 or word.find('U')!=-1

def upperVocal(word):
    return word.lower().replace('a','A').replace('e','E').replace('i','I').replace('o','O').replace('u','U')

def year_signs(w1):
    result=[]
    result += signs(w1,1)
    result += signs(w1,2)
    if args.year:
        result += year(w1,1)
        result += year(w1,2)
        for x in year(w1,1):
            result += signs(x,1)
            result += signs(x,2)
        for x in signs(w1,1):
            result += year(x,1)
            result += year(x,2)
        for x in year(w1,2):
            result += signs(x,2)
        for x in signs(w1,2):
            result += year(x,2)
    return result

def year(word,mode):
    total=[]
    for y in args.year:
        if mode == 1:
            total.append(word+str(y))
            total.append(word+str(y)[::-1])
            total.append(word+str(y)[2:])
            total.append(word+str(y)[2:][::-1])
        else:
            total.append(str(y)+word)
            total.append(str(y)[::-1]+word)
            total.append(str(y)[2:]+word)
            total.append(str(y)[2:][::-1]+word)
    return total

def signs(word,mode):
    signs_list=['*','#','\'','?','¡','¿','!','\\','|','º','ª','\"','@','·','$','~','%','&','/','(',')','=','^','[',']','{','}','+','<','>','_','-',';',',','.']
    result=[]
    for x in signs_list:
        if mode == 1:
            result.append(word+x)
        else:
            result.append(x+word)
    return result

def l337_a(word):
    if word is not None:
            return word.replace("a","4").replace("A","4")
    return None

def l337_e(word):
    if word is not None:
            return word.replace("e","3").replace("E","3")
    return None

def l337_i(word):
    if word is not None:
            return word.replace("i","1").replace("I","1")
    return None

def l337_o(word):
    if word is not None:
            return word.replace("o","0").replace("O","0")
    return None

def l337_s(word):
    if word is not None:
            return word.replace("s","5").replace("S","5")
    return None

def l337_t(word):
    if word is not None:
            return word.replace("t","7").replace("T","7")
    return None

def dollar(word):
    if word is not None and (word.find('s')!=-1 or word.find('S')!=-1):
            return word.replace("s","$").replace("S","$")
    return None

def at(word):
    if word is not None and (word.find('a') != -1 or word.find('A') != -1):
        return word.replace("a","@").replace("A","@")
    else:
        return None

def f_l337(word,args):
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

def fr_l337(w,l_list,j):
    total=[]
    for i in range(j,len(l_list)):
        word=l_list[i](w)
        if word is not None:
            total.append(word)
            total+=fr_l337(word,l_list,j+1)
    return total

if __name__ == "__main__":
    args = arg_parser()
    main(args)
