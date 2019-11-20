from linepy import *
import json,codecs,sys
tkn = json.load(codecs.open("tokens.json","r","utf-8"))
print("歡迎使用蘿莉喵帳號管理系統2.0\nToken或帳密可直接輸入後按確定即會儲存\n輸入check可以登入檢測您的倉庫中token或帳密是否能用，系統將自動刪除無效資料\n輸入clear將清理您的倉庫\n輸入url可透過網址登入獲取token並儲存\n輸入ok系統將自動關閉\n\n請務必於網路良好處執行...\n")
bot = []
while 1:
    a = input("請輸入帳密 or Token : ")
    if a.lower() == 'check':
        for x in tkn["tokens"]:
            if type(x) == str:
                try:
                    bot.append( LINE(x))
                    print('ok')
                except:
                    tkn["tokens"].remove(x)
                    print('error')
            elif type(x) == list:
                try:
                    bot.append( LINE(x[0],x[1]))
                    print('ok')
                except:
                    tkn["tokens"].remove(x)
                    print('error')
            json.dump(tkn, codecs.open('tokens.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False) 
    elif a.lower() == 'url':
        try:
            bot.append( LINE() )
            tkn["tokens"].append(bot[-1].authToken)
            json.dump(tkn, codecs.open('tokens.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False) 
            print('ok')
        except:
            print('error')
    elif a.lower() == 'clear':
        tkn["tokens"].clear()
        json.dump(tkn, codecs.open('tokens.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False) 
    elif a.lower() == 'ok':
        sys.exit()
    elif '@' in a.lower():
        b = input("請輸入密碼 :")
        try:
            bot.append( LINE(a,b))
            tkn["tokens"].append([a,b])
            json.dump(tkn, codecs.open('tokens.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False) 
        except:
            print("無效帳密")
    else:
        try:
            bot.append( LINE(a))
            tkn["tokens"].append(str(a))
            json.dump(tkn, codecs.open('tokens.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False) 
        except:
            print("無效Token")
            

