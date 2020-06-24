from  lexer_utils import *
def filter_source(s):#过滤注释
    result=''
    flag=False
    for i in s:
        if i==note_tail:
            flag=False
            continue
        if flag:
            continue
        if i == note_head:
            flag=True
            continue
        result+=i
    if flag:
        return False,error_note

    return True,result
def is_digit(x):
    for i in x:
        if '0'>i or i>'9':
            return False
    return True

def is_identifier(x):
    import re
    pattern = re.compile('[a-zA-Z]+[a-zA-Z0-9]*')#正则表达式匹配单词
    r = re.match(pattern, x)

    if r and r.span()[1] == len(x):
        return  True
    return  False
def judge_word(x,line):
    global  identifiers,consts
    if x in reserved_words:
        result=[reserved_words.index(x) + offset_reserved_word, placeholder]
    elif is_identifier(x):
        if x not  in identifiers:
            identifiers.append(x)
        result=[identifier_code,identifiers.index(x)]
    elif is_digit(x):
        if x not in consts:
            consts.append(x)
        result=[const_code, consts.index(x)]
    else:
        return False,(error_word+x+line_prompt+line)

    return True,result


def scanner(s):
    flag_string = False
    flag_double = False
    flag_end=False
    tokens = []
    temp = None
    buffer = ''
    line=1
    for i in s:
        if not flag_string:
            if not flag_double:
                if i in double_head:
                    if temp:
                        is_right,token=judge_word(temp,str(line))
                        if is_right:
                            tokens.append(token)
                        else:
                            return False,token+line_prompt+str(line)
                    temp = i
                    flag_double = True
                    continue
            else:
                if i == dictionary[temp]:
                    tokens.append([delimiter_double.index(temp + i) + offset_delimiter_double, placeholder])
                    temp = None
                    flag_double = False
                    continue
                elif temp in delimiter_single:
                    tokens.append([delimiter_single.index(temp) + offset_delimiter_single, placeholder])
                    temp = i
                    flag_double = False
                    continue
                else:
                    return False,error_delimeter_double.format(temp + dictionary[temp])+line_prompt+str(line)

            if i in delimiter_single:
                if temp:
                    is_right, token = judge_word(temp,str(line))
                    if is_right:
                        tokens.append(token)
                        temp=None
                    else:
                        return False, token
                if i != ' ' and i != '\t':#过滤掉空格和制表符
                    tokens.append([delimiter_single.index(i) + offset_delimiter_single, placeholder])
                    if i=='\n':
                        line+=1
                    if i==eof:
                        flag_end=True
                        break
                continue
        if i == string_end:
            if flag_string:
                flag_string = False
                if buffer not in consts:
                    consts.append(buffer)
                tokens.append([string_code, consts.index(buffer)])
                buffer = ''
            else:
                flag_string = True
            continue
        if flag_string:
            buffer += i
            continue
        if temp:
            temp += i
        else:
            temp = i
    if flag_end:
        return True,tokens
    return False,error_end

def translate(tokens):
    line=1
    infos=[]
    for i in tokens:
        code=i[0]
        content=i[1]
        if code == identifier_code:
            type = '标识符'
            value = identifiers[content]
        elif code == const_code:
            type = '常量'
            value = consts[content]
        elif code == string_code:
            type = '字符串'
            value = consts[content]
        elif offset_delimiter_single > code >= offset_delimiter_double:
            type = '双字符分界符'
            value = delimiter_double[code - offset_delimiter_double]
        elif code >= offset_reserved_word:
            type = "保留字"
            value = reserved_words[code - offset_reserved_word]
        elif code == delimiter_single.index(eof)+offset_delimiter_single:
            type='文件结束符'
            value=eof
        elif offset_delimiter_single <= code:
            type = '单字符分界符'
            value = delimiter_single[code - offset_delimiter_single]
        else:
            return False,error_translate
        infos.append([line,repr(value),type])
        if code==delimiter_single.index('\n')+offset_delimiter_single:
            line+=1
    return True,infos

def read_file(path):
    try:
        if '.' in path:
            type = path.split('.')[1]
            if type == 'txt':
                with  open(path, "r", encoding="UTF-8") as f:
                    data = f.read()
                    return True, data
            else:
                return False, error_path
        else:
            return False, error_path
    except IOError as err:
        return False, ("File Error:" + str(err))  # str()将异常转换为字符串
        # print(str(err))

def print_result(r,num_per_line):
    for i in range(len(r)):
        print(r[i],end='')
        if (i+1)%num_per_line==0:
            print('')
    print('')
def analyze(source_code):
    source_code = source_code + eof
    is_right, s = filter_source(source_code)
    if is_right:
        is_right, tokens = scanner(s)
        if is_right:
            is_right,infos = translate(tokens)
            if is_right:
                r = []
                for i in zip(tokens, infos):
                    r.append([i[1][0], i[1][1], i[1][2], i[0][0], i[0][1]])
                return True,r
            else:
                return  False,infos
        else:
            return False,tokens
    else:
        return False,s


placeholder=-1#保留字，分界符内容部分为-1
note_head='{'
note_tail='}'
eof='$'
delimiter_single=['+','-','*','/','<','>','=','(',')','[',']','.',';',' ',eof,'\n','\t',',']
delimiter_double =[':=','..']
double_head=[]
dictionary=dict()
for i in delimiter_double:#字典存储双字符分界符第一个字符和第二个字符的对应关系
    dictionary[i[0]]=i[1]
    double_head.append(i[0])
string_end='\''
reserved_words=["program","procedure","type","var","if","then","else","fi","while","do","endwh","begin","end","read","write","array","of","record","return","integer","char"]
identifier_code = 0
const_code = 1
string_code=2

offset_delimiter_double=3
offset_delimiter_single =  offset_delimiter_double+len(delimiter_double)
offset_reserved_word =  offset_delimiter_single+len(delimiter_single)
identifiers=[]
consts=[]

if __name__=="__main__":

    #-----input source code in console------
    # input eof to end input(In this case eof is $)
    source_code=''
    while True:
        a=input()

        flag=False
        for i in a:
            source_code+=i
            if i==eof:
                flag=True
                break
        if flag:
            break
        source_code+='\n'
    is_right=True
    # #-----input source code by file-----
    # is_right,source_code = read_file(r't.txt')
    if is_right:
        source_code = source_code + eof
        is_right,s=filter_source(source_code)
        if is_right:
            is_right,tokens=scanner(s)
            # ---check tokens ----
            if is_right:
                print("tokens:")
                print_result(tokens,5)
                print("after tranlation:")
                is_right,translated=translate(tokens)
                print_result(translated,5)
            else:
                print(tokens)
        else:
            print(s)
    else:
        print(source_code)