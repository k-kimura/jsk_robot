#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python2.7とpython3.xでは標準型の扱いが異なる
# python2.7 <type 'str'>, ,<type 'int'>
# python3.x <class 'str'>, <class 'int' >
# isinstanceを使用するとpython2.7の型はbytes型として認識されてしまう

if __name__ == "__main__":
    arg_list = ['', 'CaoProv.DENSO.VRC', 'localhost', '', 1]
    
    for arg in arg_list:
        
        if arg is None:
            print('None')

        elif isinstance(arg, (bytearray)):
            print('1 byte arg:{}, argtype{}'.format(arg, type(arg)))

        elif isinstance(arg, (bytes)):
            print('2 byte arg:{}, argtype{}'.format(arg, type(arg)))

        else:
            print('normal arg:{}, type arg:{}'.format(arg, type(arg)))