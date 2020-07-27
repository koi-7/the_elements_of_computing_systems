#!/usr/bin/python3
# coding: utf-8

import re
import Code as cd


A_COMMAND = 0
C_COMMAND = 1
L_COMMAND = 2

symbol_pattern = r'[a-zA-z_.$0-9]+'
dest_pattern = r'(A?M?D?)'
comp_pattern = r'([AMD]?[\+\-\!&\|]?[01AMD]?)'
jump_pattern = r'(J?[EGLNM]?[TQEP]?)'

a_pattern = r'@[0-9]+'
c_pattern = dest_pattern + r'=?' + comp_pattern + r';?' + jump_pattern
l_pattern = r'\(' + symbol_pattern + r'\)'


class Parser:
    def __init__(self, filename):
        '''
        入力ファイル / ストリームを開きパースを行う準備をする
        in:  str
        out: void
        '''
        self.command = ''
        self.f = open(filename, 'rt')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.f.close()


    def hasMoreCommands(self):
        '''
        入力にまだコマンドが存在するか？
        in:  void
        out: bool
        '''
        if self.command == '':
            return False
        else:
            return True

    def advance(self):
        '''
        入力から次のコマンドを読み、それを現在のコマンドにする
        in:  void
        out: void
        '''

        # self.command = self.f.readline()

        #while self.command:
        #    if re.match(r'^\n$|^/{2}', self.command):
        #        self.command = self.f.readline()
        #    else:
        #        self.command = self.command.strip()
        #        break

        for line in self.f:
            print(line, end='')
            if re.match(r'^\n$|^//', line):
                continue
            else:
                self.command = line
                break

    def commandType(self):
        '''
        現コマンドの種類を返す
        in:  void
        out: A_COMMAND, C_COMMAND, L_COMMAND
        '''
        if re.match(a_pattern, self.command):
            return A_COMMAND
        elif re.match(c_pattern, self.command):
            return C_COMMAND
        elif re.match(l_pattern, self.command):
            return L_COMMAND

    def symbol(self):
        '''
        現コマンドのシンボルもしくは10進数の数値を返す
        in:  void
        out: str
        '''
        pass

    def dest(self):
        '''
        現 C 命令の dest ニーモニックを返す
        in:  void
        out: str
        '''
        pass

    def comp(self):
        '''
        現 C 命令の comp ニーモニックを返す
        in:  void
        out: str
        '''
        pass

    def jump(self):
        '''
        現 C 命令の jump ニーモニックを返す
        in:  void
        out: str
        '''
        pass
