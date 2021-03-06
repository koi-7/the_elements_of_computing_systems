#!/usr/bin/python3
# coding: utf-8

import re
import Code as cd


A_COMMAND = 0
C_COMMAND = 1
L_COMMAND = 2

a_pattern = r'@([a-zA-z_.$0-9]+)'
l_pattern = r'\(([a-zA-z_.$0-9]+)\)'


class Parser:
    def __init__(self, filename):
        """
        入力ファイル / ストリームを開きパースを行う準備をする
        str -> void
        """
        self.command = ''
        self.f = open(filename, 'rt')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.f.close()


    def hasMoreCommands(self):
        """
        入力にまだコマンドが存在するか？
        void -> bool
        """
        while True:
            line = self.f.readline()
            if line == '':
                return False
            elif re.match(r'^\n$|^/{2}', line):
                continue
            else:
                self.command = line
                return True

    def advance(self):
        """
        入力から次のコマンドを読み、それを現在のコマンドにする
        void -> void
        """
        line = self.command                   ## '  dest=comp;jump    // comment\n'
        line = self.command.replace(' ', '')  ## 'dest=comp;jump//comment\n'
        line_list = line.split('//')
        self.command = line_list[0].strip()  ## コメントの有無に関係なく先頭要素

    def commandType(self):
        """
        現コマンドの種類を返す
        void -> A_COMMAND | C_COMMAND | L_COMMAND
        """
        if re.match(a_pattern, self.command):
            return A_COMMAND
        elif re.match(l_pattern, self.command):
            return L_COMMAND
        else:
            return C_COMMAND

    def symbol(self):
        """
        現コマンドのシンボルもしくは10進数の数値を返す
        void -> str
        """
        if self.commandType() == A_COMMAND:    ## @Xxx
            pattern = a_pattern
        elif self.commandType() == L_COMMAND:  ## (Xxx)
            pattern = l_pattern

        m = re.match(pattern, self.command)
        return m.group(1)

    def dest(self):
        """
        現 C 命令の dest ニーモニックを返す
        void -> str
        """
        m = self.command.split('=')
        if len(m) == 1:
            return ''
        else:
            return m[0]

    def comp(self):
        """
        現 C 命令の comp ニーモニックを返す
        void -> str
        """
        m1 = self.command.split('=')
        if len(m1) == 1:
            m2 = m1[0].split(';')
        else:
            m2 = m1[1].split(';')
        return m2[0]

    def jump(self):
        """
        現 C 命令の jump ニーモニックを返す
        void -> str
        """
        m = self.command.split(';')
        if len(m) == 1:
            return ''
        else:
            return m[1]
