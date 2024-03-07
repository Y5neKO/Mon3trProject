"""  
@Time: 2024/3/6 10:05 
@Auth: Y5neKO
@File: banner.py 
@IDE: PyCharm 
"""
from core.color import color

version = "0.1"
author = "Y5neKO"

banner = '''\033[1;31;40m
       LLf                                            ,11,      
       LLLLLL,                                     i11111,      
       LLLLLLLLLt                              .111111111,      
       LLLLLLLLLLLLL,                       i111111111111.      
       iLLLLLLLLLLLLLLLt                .1111111111111111       
           LLLLLLLLLLLLLLLL.         ;111111111111111;          
              1LLLLLLLLLLLLLLL1  .1111111111111111              
                 .LLLLLLLLLLLLLL11111111111111;                 
       LLf           tLLLLLLLLLL11111111111.          .11.      
       LLLLLL,          :LLLLLLL1111111i           ;11111.      
       LLLLLLLL             fLLL1111,            :1111111.      
       LLLLLLLL                :1                :1111111.      
       LLLLLLLL      tLt                .11      :1111111.      
       LLLLLLLL      tLLLLL.         ;11111      :1111111.      
       LLLLLLLL      tLLLLLLLL1  .111111111      :1111111.      
       LLLLLLLL      tLLLLLLLLLL11111111111      :1111111.      
       LLLLLLLL      tLLLLLLLLLL11111111111      :1111111.      
       LLLLLLLL      tLLLLLLLLLL11111111111      :1111111.      
       LLLLLLLL      tLLLLLLLLLL11111111111      :1111111,      
       LLLLLLLLLLf   tLLLLLLL, L1: 11111111   ,1111111111.      
       LLLLLLLLLLLLLLtLLLLLLL,     1111111111111111111111,      
        ,LLLLLLLLLLLLLLLLLLLL,     11111111111111111111i        
            fLLLLLLLLLLLLLLLL,     11111111111111111,           
               :LLLLLLLLLLLLL,     11111111111111               
                   LLLLLLLLLL,     1111111111:                  
                      iLLLLLL,     1111111         \033[0m Mon3tr Webshell Management Client \033[1;31;40m
                          LLL,     111:\033[0m             v{} by {} :)
'''.format(color(version, "green"), color(author, "yellow"))
