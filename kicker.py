# -*- coding: utf-8 -*-
from linepy import *
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, pytz, six, ast, urllib, urllib.parse, timeit, _thread
botStart = time.time()
set = {
    "bot1" : [],
    "bots1" : []
}
tkn = json.load(codecs.open("tokens.json","r","utf-8"))
botnum = tkn["botnum"]
if botnum > len(tkn["tokens"]):
    print("所供應的token不足")
    sys.exit()
if type(tkn["tokens"][0]) == str:
    cl = LINE(tkn["tokens"][0]) 
elif type(tkn["tokens"][0]) == list:
    cl = LINE(tkn["tokens"][0][0],tkn["tokens"][0][1]) 
print('主機登入成功 ' + cl.profile.displayName)
b=0
for a in range(botnum-2):
    if type(tkn["tokens"][b+1]) == str:
        set["bot1"].append(LINE(tkn["tokens"][b+1]))
    elif type(tkn["tokens"][b+1]) == list:
        set["bot1"].append(LINE(tkn["tokens"][b+1][0],tkn["tokens"][b+1][1])) 
    b+=1
    print('ok')
if type(tkn["tokens"][botnum-1]) == str:
    js = LINE(tkn["tokens"][botnum-1]) 
elif type(tkn["tokens"][botnum-1]) == list:
    js = LINE(tkn["tokens"][botnum-1][0],tkn["tokens"][botnum-1][1]) 
print('JS保護登入成功\n登入所花時間為'+str(format_timespan(time.time() - botStart)))
Add = []
if tkn["kicker"] != []:
    for token in tkn["kicker"]:
        try:
            Add.append( LINE(token) )
        except:
            tkn["kicker"].remove(token)
clMID = cl.profile.mid
set["bots1"].append(clMID) 
c = 0
for a in range(botnum - 2):
    set["bots1"].append(set["bot1"][c].profile.mid) 
    c+=1
jsMID = js.profile.mid

Kickermid = []
if Add != []:
    for x in Add:
        Kickermid.append(x.profile.mid)

list = []
for x in set["bot1"]:
    list.append(x.profile.mid)

Botmid = {}
Botmid[clMID] = cl
for x in set["bot1"]:
    Botmid[x.profile.mid]=x

Kicker = {}
Kicker[clMID] = set["bot1"]
Kicker[jsMID] = set["bot1"]
for x in set["bot1"]:
    Kicker[x.profile.mid] = set["bot1"][set["bot1"].index(x)+1:]+set["bot1"][:set["bot1"].index(x)]

oepoll = OEPoll(cl)

ban = json.load(codecs.open("ban.json","r","utf-8"))
gp = json.load(codecs.open("group.json","r","utf-8"))
admin = json.load(codecs.open("admin.json","r","utf-8"))
settings = json.load(codecs.open("temp.json","r","utf-8"))
user = json.load(codecs.open("user.json","r","utf-8"))
owners = json.load(codecs.open("owners.json","r","utf-8"))
wc = json.load(codecs.open("wel.json","r","utf-8"))
black = json.load(codecs.open("black.json","r","utf-8"))
bot1 = json.load(codecs.open("bot.json","r","utf-8"))
#==============================================================================#
def restartBot():
    print ("[ 提醒 ] 機器重啟中")
    backupData()
    python = sys.executable
    os.execl(python, python, *sys.argv)
def backupData():
    try: 
        json.dump(ban, codecs.open('ban.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False) 
        json.dump(gp, codecs.open('group.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
        json.dump(settings,codecs.open('temp.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
        json.dump(tkn,codecs.open('tokens.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False) 
        json.dump(user,codecs.open('user.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
        json.dump(admin,codecs.open('admin.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
        json.dump(owners,codecs.open('owners.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
        json.dump(wc,codecs.open('wel.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
        json.dump(black,codecs.open('black.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)        
        json.dump(bot1,codecs.open('bot.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)   		
        return True
    except Exception as error:
        logError(error)
        return False
def ismid(mid):
    try:
        cl.getContact(mid)
        return True
    except:
        return False
def sendMessageWithMention(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@x '
        cl.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
        logError(error)
def sendMention(to, text="", mids=[]):
    arrData = ""
    arr = []
    mention = "@WangPing "
    if mids == []:
        raise Exception("Invalid mids")
    if "@!" in text:
        if text.count("@!") != len(mids):
            raise Exception("Invalid mid")
        texts = text.split("@!")
        textx = ""
        for mid in mids:
            textx += str(texts[mids.index(mid)])
            slen = len(textx)
            elen = len(textx) + 15
            arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
            arr.append(arrData)
            textx += mention
        textx += str(texts[len(mids)])
    else:
        textx = ""
        slen = len(textx)
        elen = len(textx) + 15
        arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mids[0]}
        arr.append(arrData)
        textx += mention + str(text)
    cl.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)        
def cek(mid):
    if mid  in (owners["owners"] + set["bots1"] + Kickermid + bot1["bot"]):
        return True
    else:
        return False
def killban(to):
    group = cl.getGroup(to)
    gMembMids = [contact.mid for contact in group.members]
    matched_list = []
    for tag in black["blacklist"]:
        matched_list+=filter(lambda str: str == tag, gMembMids)
    if matched_list == []:
        return True
    else:
        for jj in matched_list:
            random.choice(set["bot1"]).kickoutFromGroup(to,[jj])
        cl.sendMessage(to, "黑名單以踢除")
        return False
def help():
    key = '' if not settings['setKey']['status'] else settings['setKey']['key']
    with open('help.txt', 'r') as f:
        text = f.read()
    helpMsg = text.format(key=key.title())
    return helpMsg
def killtkban(to):
    group = cl.getGroup(to)
    gMembMids = [contact.mid for contact in group.members]
    matched_list = []
    for tag in black["tkbanlist"]:
        matched_list+=filter(lambda str: str == tag, gMembMids)
    if matched_list == []:
        return True
    else:
        for jj in matched_list:
            random.choice(set["bot1"]).kickoutFromGroup(to,[jj])
        cl.sendMessage(to, "永久黑名單以踢除")
        return False
def joinLink(x,to,on=False):
    G = cl.getGroup(to)
    if G.preventedJoinByTicket != on:
        G.preventedJoinByTicket = on
        x.updateGroup(G)
def logError(text):
    cl.log("[ ERROR ] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
def helpmessage():
    helpMessage = """
----------------------------
		 管理員權限 
----------群組功能----------
	save-儲存設定
    運行-機器運行時間
    @bye-機器退群
    contact:-mid偵測友資
    help-指令表
    bothelp-黑單設定指令表
    確認-查看群組設定
    wc-查看進群設定
----------權限查詢----------
	最高管理員-查看管理員
    黑單人數-查看黑單人數
    永黑人數-查看永黑人數
    禁言黑單-查看禁言黑單人數
    單群黑單-查看本群單群黑單
    群組管理員-查看群組群長
----------群組權限----------
	gradd @-標註增加正群長權限
    grdel @-移除單群最高權限
    gban @-標註增加單群黑單
    gbandel @-移除單群黑單
----------票卷查詢----------
	Mid-標註查mid
	mymid-直接獲取自己的mid
    gc mid-查看票卷
----------遊戲功能----------
    拉霸一次-拉霸機
----------其他功能----------
    購票-購票詳情	
----------群組設定----------
	JS 開啟/關閉-JS翻機特別防禦
	pro On/Off 所有保護
	op On/Off 踢人保護
	qp On/Off 網址保護
	@ip On/Off 邀請保護
    @name on/off 群名保護
    @jk on/off 進群踢保護
----------------------------	
"""
    return helpMessage
def helpmessagetag():
    helpMessageTag ="""
----------------------------
	作者權限者功能表
----------群組功能----------
	save-儲存設定
    運行-機器運行時間
    @bye-機器退群
    contact:-mid偵測友資
    help-指令表
    確認-查看群組設定
    wc-查看進群設定
----------群組權限----------	
    群組管理員-查看管理員
    最高管理員-查看最高權限者
    永黑人數-查看永黑人數
    黑單人數-查看黑單人數
    禁言黑單-查看禁言黑單人數
	單群黑單-查看單群黑單人數
----------權限增加----------
    gradd @-標註增加單群作者
    gdel @-移除單群作者
    ban-丟友資加入黑單
    unban-丟友資移除黑單
    talk-丟友資加入禁言黑單
    untalk-丟友資移除禁言黑單
	owners:mid-mid作者權限增加
    ownersdel-mid-mid移除作者權限
----------重啟功能----------	
	@rebot-重啟機器
----------遊戲指令----------		
	拉霸一次-拉霸機
----------票卷查詢----------	
	Mid-標註查mid
	mymid-直接獲取自己的mid
    gc mid-查看票卷
    ticket mid 數量-增加購買者的票卷
----------群組設定----------
	js開啟/關閉-JS翻機特別防禦
	pro on/off 所有保護
	@op on/off 踢人保護
	@qp on/off 網址保護
	@ip on/off 邀請保護
    @name on/off 群名保護
    @jk on/off 進群踢保護
----------------------------	
"""
    return helpMessageTag
def helpbot():
    helpBot = """✯ 王萍 ✯
機器的設定內容
≺ 機器設定 ≻
⊳  Mide網址 機器網址入群
⊳  Mode邀請 機器邀請入群
⊳  Mode追加 機器使用追加
≺ 追加設定 ≻
⊳ KickerAdd:(token) 登入追加
⊳ KickerDel:(mid) 追加清除
⊳ KickerList 查看所有追加
⊳ Kicker Test-追加測試
"""
    return helpBot
wait = {
    "ban" : False,
    "unban" : False,
    "botadd" : False,
    "autoLeave" : True,
    "botdel" : False,
    "ban" : False,
    "unban" : False,
    "tkban" : False,
    "tkunban" : False,
    "bban" : False,
    "unbban" : False,
    "talk" : False,
    "untalk" : False,
    "contact" : True,
    "add" : False,
    "del" : False,
    "clp" : False,
    "botp" : False,
    "bot" : False,
    "rapidFire" : {},
    "mid" : {},
    "game" :{}
}
myProfile = {
    "displayName": "",
    "statusMessage": "",
    "pictureStatus": ""
}

if clMID not in owners["owners"]:
    owners["owners"].append(clMID) 
def lineBot(op):
    try:
        if op.type == 0:
            return
        if op.type == 25 or op.type == 26:
            msg = op.message
            if msg.contentType == 13:
                if wait["ban"] == True:
                    if msg._from in owners["ownerss"]:
                        ls = msg.contentMetadata["mid"]
                        if ls not in black["blacklist"]:
                            black["blacklist"][ls] = ls
                            cl.sendMessage(msg.to, "已加入黑單")
                            wait["ban"] = False
                        else:
                            cl.sendMessage(msg.to, "此人已黑單")
                            wait["ban"] = False
                            backupData()
                elif wait["unban"] == True:
                    if msg._from in owners["ownerss"]:
                        try:
                            if msg.contentMetadata["mid"] not in black["blacklist"][msg.contentMetadata["mid"]]:
                                 cl.sendMessage(msg.to,"此目前沒在黑單")
                                 wait["unban"] = False
                                 backupData()
                            else:
                                del black["blacklist"][msg.contentMetadata["mid"]]
                                wait["unban"] = False
                                cl.sendMessage(msg.to,"成功刪除黑單")
                        except:cl.sendMessage(msg.to, "此人目前不在黑單")
        if op.type == 25 or op.type == 26:
            msg = op.message
            if msg.contentType == 13:
                if wait["bban"] == True:
                    if msg._from in owners["ownerss"]:
                        ls = msg.contentMetadata["mid"]
                        if ls not in black['tkbanlist']:
                            black['tkbanlist'][ls] = ls
                            cl.sendMessage(msg.to, "已加入永久黑單")
                            wait["bban"] = False
                        else:
                            cl.sendMessage(msg.to, "此人已永久黑單")
                            wait["bban"] = False
                            backupData()
                elif wait["unbban"] == True:
                    if msg._from in owners["ownerss"]:
                        try:
                            if msg.contentMetadata["mid"] not in black['tkbanlist'][msg.contentMetadata["mid"]]:
                                 cl.sendMessage(msg.to,"此目前沒在永久黑單")
                                 wait["unbban"] = False
                                 backupData()
                            else:
                                del black['tkbanlist'][msg.contentMetadata["mid"]]
                                wait["unbban"] = False
                                cl.sendMessage(msg.to,"成功刪除永久黑單")
                        except:cl.sendMessage(msg.to, "此人目前不在永久黑單")
        if op.type == 25 or op.type == 26:
            msg = op.message
            if msg.contentType == 13:
                if wait["talk"] == True:
                    if msg._from in owners["ownerss"]:
                        ls = msg.contentMetadata["mid"]
                        if ls not in black['Talklist']:
                            black['Talklist'][ls] = ls
                            cl.sendMessage(msg.to, "已加入禁言黑單")
                            wait["talk"] = False
                        else:
                            cl.sendMessage(msg.to, "此人已禁言黑單")
                            wait["talk"] = False
                            backupData()
                elif wait["untalk"] == True:
                    if msg._from in owners["ownerss"]:
                        try:
                            if msg.contentMetadata["mid"] not in black['Talklist'][msg.contentMetadata["mid"]]:
                                 cl.sendMessage(msg.to,"此目前沒在禁言黑單")
                                 wait["untalk"] = False
                                 backupData()
                            else:
                                del black['Talklist'][msg.contentMetadata["mid"]]
                                wait["untalk"] = False
                                cl.sendMessage(msg.to,"成功刪除禁言黑單")
                        except:cl.sendMessage(msg.to, "此人目前不在禁言黑單")
        if op.type == 25 or op.type == 26:
            msg = op.message
            if msg.contentType == 13:
                if wait["owner"] == True:
                    if msg._from in owners["ownerss"]:
                        ls = msg.contentMetadata["mid"]
                        if ls not in owners["ownerss"]:
                            owners["ownerss"][ls] = ls
                            cl.sendMessage(msg.to, "已加入最大權限")
                            wait["owner"] = False
                        else:
                            cl.sendMessage(msg.to, "此人已最大權限")
                            wait["owner"] = False
                            backupData()
                elif wait["unowner"] == True:
                    if msg._from in owners["ownerss"]:
                        try:
                            if msg.contentMetadata["mid"] not in owners["ownerss"][msg.contentMetadata["mid"]]:
                                 cl.sendMessage(msg.to,"此目前沒在最大權限")
                                 wait["unowner"] = False
                                 backupData()
                            else:
                                del owners["ownerss"][msg.contentMetadata["mid"]]
                                wait["unowner"] = False
                                cl.sendMessage(msg.to,"成功刪除最大權限")
                        except:cl.sendMessage(msg.to, "此人目前不在最大權限")
        if op.type == 11:
            if cek(op.param2) or (op.param1 in gp["gm"] and op.param2 in gp["gm"][op.param1]) or op.param2 in owners["ownerss"]:
                pass
            else:
                G = cl.getGroup(op.param1)
                if G.preventedJoinByTicket == False and op.param1 in settings["qrprotect"]:
                    G.preventedJoinByTicket = True
                    random.choice(set["bot1"]).updateGroup(G)
                    random.choice(set["bot1"]).kickoutFromGroup(op.param1,[op.param2])
                    random.choice(set["bot1"]).sendMessage(op.param1, "[警告]\n網址保護開啟中(#･∀･)\n此人更動網址!!!")
                    black["blacklist"][op.param2] = True
                    json.dump(black, codecs.open('black.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False) 
        if op.type == 11:
            if cek(op.param2) or (op.param1 in gp["gm"] and op.param2 in gp["gm"][op.param1]) or op.param2 in owners["ownerss"]:
                pass
            else:
                G = cl.getGroup(op.param1)
                if op.param1 in settings["name"]:
                    G.name = settings["name"][op.param1]
                    random.choice(set["bot1"]).updateGroup(G)
                    random.choice(set["bot1"]).kickoutFromGroup(op.param1,[op.param2])  
                    random.choice(set["bot1"]).sendMessage(op.param1, "[警告]\n群名保護開啟中(#･∀･)\n此人變更了群名!!!")
                    black["blacklist"][op.param2] = True
                    json.dump(black, codecs.open('black.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False) 
        if op.type == 17:
            if op.param2 in black["blacklist"]: 
                if settings["warmode"] == None:
                    joinLink(random.choice(set["bot1"]),op.param1)
                    Ticket = random.choice(set["bot1"]).reissueGroupTicket(op.param1)
                    b = random.choice(Add)
                    b.acceptGroupInvitationByTicket(op.param1,Ticket)
                    b.kickoutFromGroup(op.param1,[op.param2])
                    joinLink(b,op.param1,True)
                    b.leaveGroup(op.param1)
                else:
                    random.choice(set["bot1"]).kickoutFromGroup(op.param1,[op.param2])
                    joinLink(random.choice(set["bot1"]),op.param1,True)
        if op.type ==19:
            if cek(op.param2) or (op.param1 in gp["gm"] and op.param2 in gp["gm"][op.param1]) or op.param2 in owners["ownerss"]:
                pass
                
            elif settings["warmode"] != None and op.param1 in settings["protect"]:
                random.choice(set["bot1"]).sendMessage(op.param1, "[警告]\n踢人保護開啟中(#･∀･)\n此人踢出了成員!!!")
                black["blacklist"][op.param2] = True
                json.dump(black, codecs.open('black.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False) 
                for x in set["bot1"]:
                    try:
                        x.kickoutFromGroup(op.param1,[op.param2])
                    except:
                        continue
                    else:
                        break
            elif op.param3 not in set["bots1"] and op.param1 in settings["protect"] and settings["warmode"] == None:
                for x in set["bot1"]:
                    try:
                        joinLink(x,op.param1)
                        Ticket = x.reissueGroupTicket(op.param1)
                        b = random.choice(Add)
                        b.acceptGroupInvitationByTicket(op.param1,Ticket)
                        b.kickoutFromGroup(op.param1,[op.param2])
                        joinLink(b,op.param1,True)
                        b.leaveGroup(op.param1)
                    except:
                        continue
                    else:
                        break
            if op.param3 in owners["owners"] and op.param3 != clMID:
                random.choice(set["bot1"]).findAndAddContactsByMid(op.param3)
                random.choice(set["bot1"]).inviteIntoGroup(op.param1,[op.param3])
        if op.type ==19:
            if op.param3 in set["bots1"] and settings["warmode"] == True:
                for x in Kicker[op.param3]:
                    try:
                        joinLink(x,op.param1)
                        Ticket = x.reissueGroupTicket(op.param1)
                        Botmid[op.param3].acceptGroupInvitationByTicket(op.param1,Ticket)
                    except:
                        continue
                    else:
                        break
                else:
                    if op.param1 in settings["jspro"]:
                        try:
                            js.acceptGroupInvitation(op.param1)
                            js.kickoutFromGroup(op.param1,[op.param2])
                            joinLink(js,op.param1)
                            Ticket = js.reissueGroupTicket(op.param1)
                            cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                            for y in set["bot1"]:
                                y.acceptGroupInvitationByTicket(op.param1,Ticket)
                            js.leaveGroup(op.param1)
                        except:
                            pass
                try:
                    random.choice(set["bot1"]).cancelGroupInvitation(op.param1,[op.param2])
                    cl.reissueGroupTicket(op.param1)
                    joinLink(random.choice(set["bot1"]),op.param1,True)
                except:
                    pass
            elif op.param3 in set["bots1"] and settings["warmode"] == False: 
                for x in Kicker[op.param3]:
                    try:
                        x.findAndAddContactsByMid(op.param3)
                        x.inviteIntoGroup(op.param1,[op.param3])
                        Botmid[op.param3].acceptGroupInvitation(op.param1)
                    except:
                        continue
                    else:
                        break
                else:
                    if op.param1 in settings["jspro"]:
                        try:
                            js.acceptGroupInvitation(op.param1)
                            js.kickoutFromGroup(op.param1,[op.param2])
                            joinLink(js,op.param1)
                            Ticket = js.reissueGroupTicket(op.param1)
                            cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                            for y in set["bot1"]:
                                y.acceptGroupInvitationByTicket(op.param1,Ticket)
                            js.leaveGroup(op.param1)
                        except:
                            pass
                try:
                    random.choice(set["bot1"]).cancelGroupInvitation(op.param1,[op.param2])
                    cl.reissueGroupTicket(op.param1)
                    joinLink(x,op.param1,True)
                except:
                    pass
            elif op.param3 in set["bots1"] and settings["warmode"] == None:
                for x in Kicker[op.param3]:
                    try:
                        joinLink(x,op.param1)
                        Ticket = x.reissueGroupTicket(op.param1)
                        Botmid[op.param3].acceptGroupInvitationByTicket(op.param1,Ticket)
                        if cek(op.param2) or (op.param1 in gp["gm"] and op.param2 in gp["gm"][op.param1]):
                            pass
                        else:
                            b = random.choice(Add)
                            b.acceptGroupInvitationByTicket(op.param1,Ticket)
                            b.kickoutFromGroup(op.param1,[op.param2])
                            joinLink(b,op.param1,True)
                            b.cancelGroupInvitation(op.param1,[op.param2])
                            b.leaveGroup(op.param1)
                            black["blacklist"][op.param2] = True
                            json.dump(black, codecs.open('black.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False) 
                    except:
                        continue
                    else:
                        break
                else:
                    if op.param1 in settings["jspro"]:
                        try:
                            js.acceptGroupInvitation(op.param1)
                            js.kickoutFromGroup(op.param1,[op.param2])
                            joinLink(js,op.param1)
                            Ticket = js.reissueGroupTicket(op.param1)
                            cl.acceptGroupInvitationByTicket(op.param1,Ticket)
                            for y in set["bot1"]:
                                y.acceptGroupInvitationByTicket(op.param1,Ticket)
                            js.leaveGroup(op.param1)
                        except:
                            pass
        if op.type == 13:
            if op.param1 in settings["invprotect"]:
                if cek(op.param2) or (op.param1 in gp["gm"] and op.param2 in gp["gm"][op.param1]) or op.param2 in owners["ownerss"]:
                    pass
                else:
                    random.choice(set["bot1"]).kickoutFromGroup(op.param1,[op.param2])
                    try:
                        random.choice(set["bot1"]).cancelGroupInvitation(op.param1,[op.param3])
                    except:
                        random.choice(set["bot1"]).kickoutFromGroup(op.param1,[op.param3])
                    cl.sendMessage(op.param1, "[警告]\n邀請保護開啟中(#･∀･)\n此人亂邀請!")
                    black["blacklist"][op.param2] = True
                    json.dump(black, codecs.open('black.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False) 
        if op.type == 32:
            if op.param3 in set["bots1"]:
                if not cek(op.param2):
                    for x in Kicker[op.param3]:
                        try:
                            random.choice(set["bot1"]).kickoutFromGroup(op.param1,[op.param2])
                            black["blacklist"][op.param2] = True
                            json.dump(black, codecs.open('black.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False) 
                        except:
                            pass
                        else:
                            break
            elif op.param3 in [jsMID] + owners["owners"]:
                if op.param2 in owners["owners"] or op.param2 in set["bots1"]:
                    for x in set["bot1"]:
                        try:
                            x.findAndAddContactsByMid(op.param3)
                            x.inviteIntoGroup(op.param1,[op.param3])
                        except:
                            pass
                        else:
                            break
                else:
                    for x in Kicker[op.param3]:
                        try:
                            x.kickoutFromGroup(op.param1,[op.param2])
                            x.findAndAddContactsByMid(op.param3)
                            x.inviteIntoGroup(op.param1,[op.param3])
                            black["blacklist"][op.param2] = True
                            json.dump(black, codecs.open('black.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False) 
                        except:
                            pass
                        else:
                            break
        if op.type == 13:
            if op.param1 in settings["invprotect"]:
                if cek(op.param2) or (op.param1 in gp["gm"] and op.param2 in gp["gm"][op.param1]) or op.param2 in owners["ownerss"]:
                    pass
                else:
                    random.choice(set["bot1"]).kickoutFromGroup(op.param1,[op.param2])
                    try:
                        random.choice(set["bot1"]).cancelGroupInvitation(op.param1,[op.param3])
                    except:
                        random.choice(set["bot1"]).kickoutFromGroup(op.param1,[op.param3])
                    black["blacklist"][op.param2] = True
                    json.dump(black, codecs.open('black.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False) 
                    cl.sendMessage(op.param1, "[警告]\n邀請保護開啟中(#･∀･)\n此人亂邀請!\n已加入為黑名單中")
        if op.type == 32:
            if op.param3 in set["bots1"]:
                if not cek(op.param2) :
                    for x in Kicker[op.param3]:
                        try:
                            random.choice(set["bot1"]).kickoutFromGroup(op.param1,[op.param2])
                            black["blacklist"][op.param2] = True
                            json.dump(black, codecs.open('black.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                        except:
                            pass
                        else:
                            break
            elif op.param3 in [jsMID] + admin["admin"] + owners["ownerss"] + creator["creator"]:
                if op.param2 in owners["owners"] or op.param2 in set["bots1"]:
                    for x in set["bot1"]:
                        try:
                            x.findAndAddContactsByMid(op.param3)
                            x.inviteIntoGroup(op.param1,[op.param3])
                        except:
                            pass
                        else:
                            break
                else:
                    for x in Kicker[op.param3]:
                        try:
                            x.kickoutFromGroup(op.param1,[op.param2])
                            x.findAndAddContactsByMid(op.param3)
                            x.inviteIntoGroup(op.param1,[op.param3])
                        except:
                            pass
                        else:
                            break
        if op.type == 60:
            if op.param1 in settings["Autojoin"]:
                if op.param2 in owners["ownerss"] or (op.param1 in gp["gm"] and op.param2 in gp["gm"][op.param1]) or op.param2 in set["bots1"]:
                    try:
                        random.choice(set["bot1"]).sendMessage(op.param1, "[警告]\n由於你是權限者妳不會被踢")
                    except:
                        pass
                else:
                    random.choice(set["bot1"]).kickoutFromGroup(op.param1,[op.param2])
        if op.type == 26:
            msg = op.message
            if msg._from not in owners['ownerss']:
                if msg._from in black["Talklist"]:
                    try:
                        random.choice(set["bot1"]).kickoutFromGroup(msg.to, [msg._from])
                    except:
                        random.choice(set["bot1"]).kickoutFromGroup(msg.to, [msg._from])
                        try:
                            random.choice(set["bot1"]).kickoutFromGroup(msg.to, [msg._from])
                        except:
                            random.choice(set["bot1"]).kickoutFromGroup(msg.to, [msg._from])
        if op.type == 60:
            if op.param2 in owners['ownerss']:
                cl.sendMessage(op.param1, "[顯示]\n此人位於最高權限名單(๑•̀ㅂ•́)و✧")
            elif op.param2 in black['blacklist']:
                random.choice(set["bot1"]).sendMessage(op.param1, "[警告]\n此人位於黑名單中(つд⊂)ｴｰﾝ")        
                random.choice(set["bot1"]).kickoutFromGroup(op.param1,[op.param2])      
            elif op.param2 in black['tkbanlist']:
                random.choice(set["bot1"]).sendMessage(op.param1, "[警告]\n此人位於永久黑名單中(つд⊂)ｴｰﾝ")
                random.choice(set["bot1"]).kickoutFromGroup(op.param1,[op.param2])                 
        if op.type == 5:
            cl.findAndAddContactsByMid(op.param1)
            cl.sendMessage(op.param1, "你好 {} 謝謝你加我為好友(´・ω・｀)\n此機器為防翻機器人 1張票100元整\n有興趣可以私以下友資購買".format(str(cl.getContact(op.param1).displayName)))
            cl.sendContact(op.param1,'u5116c2105717b25bd4683e7d4ddefead')
            cl.sendContact(op.param1,'ub58bfb2df5c4cfd8db1b5c28555422e7')
        if op.type == 13:
            if clMID in op.param3:
                if op.param2 in set["bots1"]:
                    pass
                elif op.param2 == jsMID:
                    cl.acceptGroupInvitation(op.param1)	
                elif op.param2 in owners["ownerss"]:
                    cl.acceptGroupInvitation(op.param1)						
                    try:
                        G = cl.getGroup(op.param1)
                        GS = G.creator.mid
                        if op.param1 not in gp["gm"]:
                            gp["gm"][op.param1] = {}
                        cl.sendMessage(op.param1, "本群GM為:")
                        cl.sendContact(op.param1, GS)
                        gp["gm"][op.param1][GS] = GS
                        with open('group.json', 'w') as fp:
                            json.dump(gp, fp, sort_keys=True, indent=4)
                        cl.sendMessage(op.param1, "設置GM權限成功")
                        gid = cl.getGroupIdsJoined()
                        if op.param1 not in gid:
                            gp["gm"][op.param1] = {}
                        cl.sendMessage(op.param1,"gid建立完成")
                        cl.sendMessage(op.param1,"打上@join讓機器進來")
                        settings["inviteprotect"][G.id] = True
                        settings["qrprotect"][G.id] = True
                        settings["protect"][G.id] = True
                        backupData()
                    except:
                        cl.sendMessage(op.param1, "群長砍帳幫你設定群長")
                        if op.param1 not in gp["gm"]:
                            gp["gm"][op.param1] = {}
                        GSs = "uf5cea65de5804929ce44c168cb26addd"
                        gp["gm"][op.param1][GSs] = GSs
                        with open('group.json', 'w') as fp:
                            json.dump(gp, fp, sort_keys=True, indent=4)
                        cl.sendMessage(op.param1, "設置GM權限成功")
                        backupData()
                        gid = cl.getGroupIdsJoined()
                        if op.param1 not in gid:
                            gp["gm"][op.param1] = {}
                        cl.sendMessage(op.param1,"gid建立完成")
                        cl.sendMessage(op.param1,"打上@join讓機器進來")                        
                        backupData()
                elif op.param2 in user["user"]:
                    user["user"][op.param2] = user["user"][op.param2] -1
                    cl.acceptGroupInvitation(op.param1)
                    cl.sendMessage(op.param1,"防翻保護使用權購入")
                    cl.sendMessage(op.param1,"謝謝持有票卷者邀請\n剩餘票卷:{}張".format(str(user["user"][op.param2])))
                    cl.sendMessage(op.param1,"請打上@join讓機器進來謝謝")
                    try:
                        G = cl.getGroup(op.param1)
                        GS = G.creator.mid
                        if op.param1 not in gp["gm"]:
                            gp["gm"][op.param1] = {}
                        cl.sendMessage(op.param1, "本群GM為:")
                        cl.sendContact(op.param1, GS)
                        gp["gm"][op.param1][GS] = GS
                        with open('group.json', 'w') as fp:
                            json.dump(gp, fp, sort_keys=True, indent=4)
                        cl.sendMessage(op.param1, "設置GM權限成功")
                        gid = cl.getGroupIdsJoined()
                        if op.param1 not in gid:
                            gp["gm"][op.param1] = {}
                        cl.sendMessage(op.param1,"gid建立完成")
                        cl.sendMessage(op.param1,"打上@join讓機器進來")
                        settings["inviteprotect"][G.id] = True
                        settings["qrprotect"][G.id] = True
                        settings["protect"][G.id] = True
                        backupData()
                    except:
                        cl.sendMessage(op.param1, "群長砍帳幫你設定群長")
                        if op.param1 not in gp["gm"]:
                            gp["gm"][op.param1] = {}
                        GSs = "uf5cea65de5804929ce44c168cb26addd"
                        gp["gm"][op.param1][GSs] = GSs
                        with open('group.json', 'w') as fp:
                            json.dump(gp, fp, sort_keys=True, indent=4)
                        cl.sendMessage(op.param1, "設置GM權限成功")
                        backupData()
                        gid = cl.getGroupIdsJoined()
                        if op.param1 not in gid:
                            gp["gm"][op.param1] = {}
                        cl.sendMessage(op.param1,"gid建立完成")
                        cl.sendMessage(op.param1,"打上@join讓機器進來")
                        backupData()
                    cl.sendMessage(op.param1,"已設置此群群長為邀請者與創群者")
                    cl.sendMessage(op.param1,"如需購票可以私以下友資(๑•̀ㅂ•́)و✧")
                    cl.sendContact(op.param1, "uf5cea65de5804929ce44c168cb26addd")
                    if user["user"][op.param2] <= -1:
                        cl.acceptGroupInvitation(op.param1)
                        cl.sendMessage(op.param1,"你的票不夠啦ヾ(;ﾟ;Д;ﾟ;)ﾉﾞ")
                        cl.sendMessage(op.param1,"如需要票請找下面的友資")
                        cl.sendContact(op.param1, "uf5cea65de5804929ce44c168cb26addd")
                        time.sleep(1)
                        cl.leaveGroup(op.param1)
                    if user["user"][op.param2] == 0:
                        cl.acceptGroupInvitation(op.param1)
                        cl.sendMessage(op.param1,"你的票不夠啦ヾ(;ﾟ;Д;ﾟ;)ﾉﾞ")
                        cl.sendMessage(op.param1,"如需要票請找下面的友資")
                        cl.sendContact(op.param1, "uf5cea65de5804929ce44c168cb26addd")
                        time.sleep(1)
                        cl.leaveGroup(op.param1)
                else:
                    G = cl.getGroup(op.param1)
                    cl.acceptGroupInvitation(op.param1)
                    cl.sendMessage(op.param1,"你的票不夠啦(´；ω；｀)")
                    cl.sendMessage(op.param1,"如需購票可以私以下友資ﾞ")
                    cl.sendContact(op.param1, "uf5cea65de5804929ce44c168cb26addd")
                    time.sleep(1)
                    cl.leaveGroup(op.param1)
        if op.type == 24 or op.type == 21 or op.type ==22:
            Botmid[op.param3].leaveRoom(op.param1)  
        if op.type == 26 or op.type == 25:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 0:
                if text is None:
                    return
            if sender in sender:
                if ".kickall" in text.lower() or text.lower() == "kick on" or "kickall" in text.lower():
                    if sender not in owners["ownerss"] and sender not in 'u96612d4cfdf2e8a3c4991bbb8380ae1a':
                        pro = random.choice(set["bot1"])
                        pro.kickoutFromGroup(to,[sender])
                        cl.relatedMessage(to, "{} 嘗試使用翻群指令\n基於安全考量 暫時踢出".format(str(cl.getContact(sender).displayName)),op.message.id) 						
                elif msg.text.lower().startswith("mid "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        ret_ = ""
                        for ls in lists:
                            ret_ += "" + ls
                        cl.relatedMessage(msg.to, str(ret_),op.message.id)
                elif text.lower() == "/mt" and msg.toType == 2: cl.sendMessage(msg.to, text=cl.getContact(msg._from).displayName, contentMetadata={'previewUrl': 'http://dl.profile.line-cdn.net/' + cl.getContact(msg._from).pictureStatus, 'i-installUrl': 'line://nv/profilePopup/mid=' + msg._from, 'ORGCONTP': 'MUSIC', 'type': 'mt', 'subText': cl.getContact(msg._from).statusMessage, 'a-installUrl': 'http://google.com', 'a-packageName': 'jp.naver.line.music', 'playUrl': str(BeautifulSoup(requests.get("https://anonfile.com/sb3d8725nc").text, "html.parser").find("a", id="download-url")['href']), 'countryCode': 'TW', 'a-linkUri': 'line://nv/profilePopup/mid=' + msg._from, 'i-linkUri': 'line://nv/profilePopup/mid=' + msg._from, 'text': cl.getContact(msg._from).displayName, 'id': 'mt000000000a6b79f9','linkUri': 'line://nv/profilePopup/mid=' + msg._from}, contentType=19)
                elif text.lower() == 'wc':
                    if to in wc['wel']:
                        cl.sendMessage(to, wc['wel'][to])
                    else:
                        cl.sendMessage(to, "[提示]\n使用預設群組歡迎訊息中!!!")
                elif text.lower() == '@wc on':
                    if msg.toType ==2 :
                        try:
                            settings["welcomes"][to] = True
                            cl.sendMessage(to, "進群顯示開啟 ✔")
                            backupData()
                        except:
                            pass
                elif text.lower() == '@wc off':
                    if msg.toType ==2 :
                        try:
                            del settings["welcomes"][to]
                            cl.sendMessage(to, "進群顯示關閉 ✘")
                        except:
                            cl.sendMessage(to, "幹你娘 就沒開你是要關洨==")
                    backupData()
                elif text.lower() == 'tagall':
                    group = random.choice(set["bot1"]).getGroup(msg.to)
                    nama = [contact.mid for contact in group.members]
                    k = len(nama)//20
                    for a in range(k+1):
                        txt = u""
                        s=0
                        b=[]
                        for i in group.members[a*20 : (a+1)*20]:
                            b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
                            s += 7
                            txt += u'@Alin \n'
                        random.choice(set["bot1"]).sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
                elif text.lower() == '拉霸一次':
                    A = random.choice(["０","９","８","７","６","５","４","３","２","２","１"])
                    B = random.choice(["０","９","８","７","６","５","４","３","２","２","１"])
                    C = random.choice(["０","９","８","７","６","５","４","３","２","２","１"])
                    D = random.choice(["０","９","８","７","６","５","４","３","２","２","１"])
                    E = random.choice(["０","９","８","７","６","５","４","３","２","２","１"])
                    F = random.choice(["０","９","８","７","６","５","４","３","２","２","１"])
                    G = random.choice(["０","９","８","７","６","５","４","３","２","２","１"])
                    H = random.choice(["０","９","８","７","６","５","４","３","２","２","１"])
                    I = random.choice(["０","９","８","７","６","５","４","３","２","２","１"])
                    slot = "   拉霸機\n╔═╦═╦═╗\n║{}║{}║{}║\n║{}║{}║{}║\n║{}║{}║{}║\n╚═╩═╩═╝".format(A,B,C,D,E,F,G,H,I)
                    cl.relatedMessage(to,slot,op.message.id)
                    if A == D == G :
                        cl.relatedMessage(to,"恭喜~~",op.message.id)
                        return
                    if B == E == H:
                        cl.relatedMessage(to,"恭喜~~",op.message.id)
                        return
                    if C == F == I:
                        cl.relatedMessage(to,"恭喜~~",op.message.id)
                        return
                    if A == B == C:
                        cl.relatedMessage(to,"恭喜~~",op.message.id)
                        return
                    if D == E == F:
                        cl.relatedMessage(to,"恭喜~~",op.message.id)
                        return
                    if G == H == I:
                        cl.relatedMessage(to,"恭喜~~",op.message.id)
                        return
                    if A == E == I:
                        cl.relatedMessage(to,"恭喜~~",op.message.id)
                        return
                    if C == E == G:
                        cl.relatedMessage(to,"恭喜~~",op.message.id)
                        return
                    cl.relatedMessage(to,"可惜啦ww再試一次吧w",op.message.id)
                elif text.lower().startswith("say "):
                    x = text.split(' ')
                    if len(x) == 2:
                        cl.sendMessage(to,x[1])
                    elif len(x) == 3:
                        try:
                            c = int(x[2])
                            for c in range(c):
                                cl.sendMessage(to,x[1])
                        except:
                            cl.sendMessage(to,"無法正確執行此指令")
                elif msg.text.lower().startswith("tag "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    y = text[5:].replace(cl.getContact(inkey).displayName,"")
                    try:
                        c = int(y.replace(" ",""))
                        for c in range(c):
                            sendMessageWithMention(to, inkey)
                    except:
                        sendMessageWithMention(to, inkey)
                elif text.lower() == 'mymid':
                    cl.relatedMessage(to,"您的識別碼\n" +  sender,op.message.id)					
                elif text.lower() == 'sp':
                    start = time.time()
                    cl.relatedMessage(to, "測速中...",op.message.id)
                    elapsed_time = time.time() - start
                    cl.relatedMessage(to,format(str(elapsed_time)) + '秒',op.message.id)			
                elif text.lower() == 'speed':
                    start = time.time()
                    cl.relatedMessage(to, "測速中...",op.message.id)
                    elapsed_time = time.time() - start
                    cl.relatedMessage(to,format(str(elapsed_time)) + '秒',op.message.id)			
                elif text.lower() == '購票':			
                    cl.relatedMessage(to,"如需購票可以私以下友資\n機器票卷為 1群 1票\n被踢出請私訊作者",op.message.id)			
                    cl.sendContact(to, "uf5cea65de5804929ce44c168cb26addd")
                elif text.lower() == '群組管理員':
                    G = cl.getGroup(to)				
                    if G.id not in gp["gm"] or gp["gm"][G.id]==[]:
                        cl.relatedMessage(msg.to,"沒有群組管理員的樣子",op.message.id)
                    else:
                         try:
                             mc = "►[ 群管名單 ]◄"
                             for mi_d in gp["gm"][G.id]:
                                 mc += "\n▸ " +cl.getContact(mi_d).displayName
                             cl.relatedMessage(msg.to,mc + "\n►[ 已經幫您查詢 ]◄",op.message.id)
                         except:
                             pass
                elif text.lower() == '單群黑單':
                    G = cl.getGroup(to)
                    if G.id not in black["bbblacklist"] or black["bbblacklist"][G.id]==[]:
                        cl.relatedMessage(msg.to,"沒有單群黑單",op.message.id)
                    else:
                         try:
                             mc = "►[ 單群黑單名單 ]◄"
                             for mi_d in black["bbblacklist"][G.id]:
                                 mc += "\n▸ " +cl.getContact(mi_d).displayName
                             cl.relatedMessage(msg.to,mc + "\n►[ 已經幫您查詢 ]◄",op.message.id)
                         except:
                             pass
                elif text.lower() == 'help':
                    G = cl.getGroup(to)
                    if sender in owners["ownerss"]:
                        helpMessageTag = helpmessagetag()
                        cl.sendMessage(to, str(helpMessageTag))
                    elif sender in gp["gm"][to]:
                        helpMessage = helpmessage()
                        cl.sendMessage(to, str(helpMessage))
                    else:
                        cl.sendMessage(to, help())
                elif msg.text.lower().startswith("contact:"):
                    y = text[8:].split(' ')
                    for mid in y:
                        cl.sendContact(to,mid)
                elif text.lower() == '@確認':
                    G = cl.getGroup(to)
                    if G.invitee is None:
                        gPending = "0"
                    else:
                        gPending = str(len(G.invitee))
                    if G.preventedJoinByTicket == True:
                        gQr = "關閉"
                        gTicket = "沒有"
                    else:
                        gQr = "開啟"
                        gTicket = "https://line.me/R/ti/g/{}".format(str(cl.reissueGroupTicket(G.id)))
                    path = "http://dl.profile.line-cdn.net/" + G.pictureStatus
                    ret_ = "╔══[ 本機設定 ]"
                    if settings["warmode"] ==True: ret_+="\n╠ 機器入群模式 ※網址進入※"
                    elif settings["warmode"] ==False: ret_ += "\n╠ 機器入群模式 ※邀請進入※"
                    else: ret_ += "\n╠ 機器入群模式 ※追加踢人進群※"
                    ret_ += "\n╠══[ 單群設定 ]"
                    G = cl.getGroup(to)
                    ret_ += "\n╠ 群組名稱 : {}".format(str(G.name))
                    ret_ += "\n╠ 黑單人數 : {}".format(str(len(black["blacklist"])))
                    ret_ += "\n╠ 永黑人數 : {}".format(str(len(black["tkbanlist"])))
                    ret_ += "\n╠ 禁言黑單人數 : {}".format(str(len(black["Talklist"])))
                    ret_ += "\n╠ 最高權限人數 : {}".format(str(len(owners["ownerss"])))
                    if G.id in settings["protect"] : ret_+="\n╠ 踢人保護 ✅"
                    else: ret_ += "\n╠ 踢人保護 ❌"
                    if G.id in settings["qrprotect"] : ret_+="\n╠ 網址保護 ✅"
                    else: ret_ += "\n╠ 網址保護 ❌"
                    if G.id in settings["invprotect"] : ret_+="\n╠ 邀請保護 ✅"
                    else: ret_ += "\n╠ 邀請保護 ❌"
                    if G.id in settings["Autojoin"] : ret_+="\n╠ 進群踢保護 ✅"
                    else: ret_ += "\n╠ 進群踢保護 ❌"
                    if G.id in settings["name"] : ret_+="\n╠ 群名保護 ✅"
                    else: ret_ += "\n╠ 群名保護 ❌"
                    if G.id in settings["jspro"]: ret_+="\n╠ JS翻機保護(暫時停用) ✅"
                    else: ret_ += "\n╠ JS翻機保護(暫時停用) ❌"
                    ret_ += "\n╠ 版本號 <喵防2.0>\n╚[ 修改者 王萍 ]"
                    cl.sendMessage(to, str(ret_))
#=====查看權限單===================================================================================================================
                elif text.lower() == '最高管理員':
                    if owners["ownerss"] == {}:
                        cl.sendMessage(to, "沒有權限者")
                    else:
                        cl.sendMessage(to, "以下是最高權限者")
                        mc = "╔══[ owner List ]"
                        for mi_d in owners["ownerss"]:
                            mc += "\n╠" + cl.getContact(mi_d).displayName
                        cl.sendMessage(to, mc+"\n╚══[總共"+str(len(owners["ownerss"]))+ "個人有最高權限]")
                elif text.lower() == '黑單人數':
                    if black["blacklist"] == {}:
                        cl.sendMessage(to, "沒有黑單人員")
                    else:
                        cl.sendMessage(to, "以下是黑單人員")
                        no = 0
                        mc = "╔══[ black List ]"
                        for mi_d in black["blacklist"]:
                            no += 1
                            mc += "\n╠ {} | {} |".format(no,cl.getContact(mi_d).displayName)
                            mc += "\n╠" + cl.getContact(mi_d).mid
                        cl.sendMessage(to, mc+"\n╚══[總共"+str(len(black["blacklist"]))+ "個人有黑單]")
                elif text.lower() == '禁言黑單':
                    if black["Talklist"] == {}:
                        cl.sendMessage(to, "沒有禁言黑單人員")
                    else:
                        cl.sendMessage(to, "以下是禁言黑單人員")
                        mc = "╔══[  talk black List ]"
                        for mi_d in black["Talklist"]:
                            mc += "\n╠" + cl.getContact(mi_d).displayName
                        cl.sendMessage(to, mc+"\n╚══[總共"+str(len(black["Talklist"]))+ "個人有黑單]")
                elif text.lower() == '永黑人數':
                    if black["tkbanlist"] == {}:
                        cl.sendMessage(to, "沒有永黑人員")
                    else:
                        cl.sendMessage(to, "以下是永黑人員")
                        mc = "╔══[ bblack List ]"
                        for mi_d in black["tkbanlist"]:
                            mc += "\n╠" + cl.getContact(mi_d).displayName
                        cl.sendMessage(to, mc+"\n╚══[總共"+str(len(black["tkbanlist"]))+ "個人有永黑]")
#=====票===================================================================================================================
                elif text.lower().startswith("gc "):
                    x = text[3:]
                    if x in user["users"]:
                        cl.sendMessage(to,"還擁有{}張票".format(str(user["users"][x])))
                    elif x in owners["ownerss"]:
                        cl.sendMessage(to, "妳是最高權限妳是無限票卷")
                    else:
                        cl.sendMessage(to,"沒有票惹(´°̥̥̥̥ω°̥̥̥̥｀)請找下面的人購買票卷")
                        cl.sendContact(to,"uf5cea65de5804929ce44c168cb26addd")
#=====完===================================================================================================================
#=====作者權限===================================================================================================================
            if sender in owners["ownerss"] or sender in gp["gm"][to]:
                if text.lower() == 'mode網址':
                    settings["warmode"] = True
                    cl.relatedMessage(to, "設定成=>BOT網址邀回群",op.message.id)
                elif text.lower() == 'mode邀請':
                    settings["warmode"] = False
                    cl.relatedMessage(to,"設定成=>BOT邀請回群",op.message.id)
                elif text.lower() == 'mode追加':
                    settings["warmode"] = None
                    cl.relatedMessage(to,"追加機器幫助踢人",op.message.id)
                    if Add == []:
                        cl.relatedMessage(to,"你沒有 追加機器人 請使用==>KickerAdd:Token 來新增",op.message.id)	
                elif text.lower().startswith("kickeradd:"):
                    token = text.split(':',2)[1]
                    try:
                        Add.append( LINE(token) )
                        tkn["kicker"].append(str(token))
                        Kickermid.append(Add[-1].profile.mid)
                        cl.sendMessage(to,"success login to line")
                        json.dump(tkn,codecs.open('tokens.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                    except:
                        cl.sendMessage(to,"error")
                elif text.lower().startswith("kickerdel:"):
                    mi_d = text.split(':',2)[1]
                    for x in Add:
                        if x.profile.mid == mi_d:
                            Add.remove(x)
                            tkn["kicker"].remove(str(x.authToken))
                    cl.sendMessage(to,"OK")
                elif text.lower() =='kickerlist':
                    if Add == []:
                        cl.sendMessage(msg.to,"無追加保鏢!\n無保鏢時追加系統無法正常運作\n輸入kickeradd:帳號token以登入追加")
                    else:
                        mc = "[ Kicker List ]"
                        for x in Add:
                            mc += "\n↬ "+x.profile.displayName+"\n"+str(x.profile.mid)
                        cl.sendMessage(msg.to,mc + "\n[ Finish ]")
                elif text.lower() == 'pro on':
                    if msg.toType ==2:
                        try:
                            random.choice(set["bot1"]).sendMessage(to, "踢人保護開啟")
                            random.choice(set["bot1"]).sendMessage(to, "網址保護開啟")
                            random.choice(set["bot1"]).sendMessage(to, "邀請保護開啟")
                            settings["protect"][to] = True
                            settings["qrprotect"][to] = True
                            settings["invprotect"][to] = True
                        except:
                            cl.relatedMessage(to, "機器沒有全體進入此群組",op.message.id)
                elif text.lower() == 'pro off':
                    if msg.toType ==2:
                        G = cl.getGroup(msg.to)
                        try:
                            del settings["protect"][G.id]
                            random.choice(set["bot1"]).sendMessage(to, "踢人保護關閉")
                        except:
                            pass
                        try:
                            del settings["qrprotect"][G.id]
                            random.choice(set["bot1"]).sendMessage(to, "網址保護關閉")
                        except:
                            pass
                        try:
                            del settings["invprotect"][G.id]
                            random.choice(set["bot1"]).sendMessage(to, "邀請保護關閉")
                        except:
                            pass
                elif text.lower() == 'js開啟':
                    if msg.toType ==2 and to not in settings["jspro"]:
                        cl.sendMessage(to,"JS protect開啟")
                        cl.findAndAddContactsByMid(jsMID)
                        cl.inviteIntoGroup(to,[jsMID])
                        settings["jspro"][to] = True
                        json.dump(settings,codecs.open('temp.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                elif text.lower() == 'js關閉':
                    if msg.toType ==2 and to in settings["jspro"]:
                        cl.sendMessage(to,"JS protect off")
                        del settings["jspro"][to]
                        backupData()
                        group = cl.getGroup(to)
                        if group.invitee != None:
                            gMembMids = [contact.mid for contact in group.invitee]
                            if jsMID in gMembMids :
                                cl.cancelGroupInvitation(to,[jsMID])
                elif text.lower() == '@qp on':
                    if msg.toType ==2:
                        try:
                            random.choice(set["bot1"]).relatedMessage(to,"網址保護開啟",op.message.id)
                            settings["qrprotect"][to] = True
                            backupData()
                        except:
                            cl.relatedMessage(to, "機器沒有全體進入此群組",op.message.id)
                elif text.lower() == '@qp off':
                    if msg.toType ==2 :
                        try:
                            del settings["qrprotect"][to]
                            cl.sendMessage(to, "網址保護關閉")
                            backupData()
                        except:
                            cl.sendMessage(to, "要開請打 @qp on")
                elif text.lower() == '@jk on':
                    if msg.toType ==2:
                        try:
                            random.choice(set["bot1"]).relatedMessage(to,"進群踢保護開啟",op.message.id)
                            settings["Autojoin"][to] = True
                            backupData()
                        except:
                            cl.relatedMessage(to, "機器沒有全體進入此群組",op.message.id)
                elif text.lower() == '@jk off':
                    if msg.toType ==2 :
                        try:
                            del settings["Autojoin"][to]
                            cl.sendMessage(to, "進群踢保護關閉")
                            backupData()
                        except:
                            cl.sendMessage(to, "要開請打 @jk on")
                elif text.lower() == '@ip on':
                    if msg.toType ==2:
                        try:
                            random.choice(set["bot1"]).sendMessage(to,"邀請保護開啟")
                            settings["invprotect"][to] = True
                            backupData()
                        except:
                            cl.relatedMessage(to, "機器沒有全體進入此群組",op.message.id)
                elif text.lower() == '@ip off':
                    if msg.toType ==2 :
                        try:
                            del settings["invprotect"][to]
                            cl.sendMessage(to, "邀請保護關閉")
                            backupData()
                        except:
                            cl.sendMessage(to, "要開請打 @ip on")
                elif text.lower() == '@op on':
                    if msg.toType ==2:
                        try:
                            random.choice(set["bot1"]).sendMessage(to,"踢人保護開啟")
                            settings["protect"][to] = True
                            backupData()
                        except:
                            cl.relatedMessage(to, "機器沒有全體進入此群組",op.message.id)
                elif text.lower() == '@op off':
                    if msg.toType ==2 :
                        try:
                            del settings["protect"][to]
                            cl.sendMessage(to, "踢人保護關閉")
                            backupData()
                        except:
                            cl.sendMessage(to, "要開請打 @op on")
                elif text.lower() == '@name on':
                    if msg.toType ==2:
                        try:
                            random.choice(set["bot1"]).sendMessage(to,"群名保護開啟")
                            settings["name"][to] = cl.getGroup(to).name
                            backupData()
                        except:
                            cl.relatedMessage(to, "機器沒有全體進入此群組",op.message.id)
                elif text.lower() == '@name off':
                    if msg.toType ==2 :
                        try:
                            del settings["name"][to]
                            cl.sendMessage(to, "群名保護關閉")
                            backupData()
                        except:
                            cl.sendMessage(to, "要開請打 @name on")
                elif text.lower() == 'save':
                    backupData()
                    cl.sendMessage(to,'儲存設定成功!')
                elif text.lower() == '運行':
                    cl.sendMessage(to, "時間也許有點久長\n請自行注意機器有無出錯\n運行時間長達{}".format(str(format_timespan(time.time() - botStart))))
                elif text.lower() in ['@bye']:
                    try:
                        random.choice(set["bot1"]).getGroup(to)
                        cl.sendMessage(to,'Bye~Bye~QQ')
                        for x in set["bot1"]:
                            x.leaveGroup(msg.to)
                        group = cl.getGroup(msg.to)
                        if group.invitee != None:
                            gMembMids = [contact.mid for contact in group.invitee]
                            if jsMID in gMembMids :
                                cl.cancelGroupInvitation(to,[jsMID])
                    except:
                        pass
                    if to in settings["jspro"]:
                        del settings["jspro"][to]
                    if to in settings["protect"]:
                        del settings["protect"][to]
                    if to in settings["qrprotect"]:
                        del settings["qrprotect"][to]
                    if to in settings["invprotect"]:
                        del settings["invprotect"][to]
                    if to in settings["Autojoin"]:
                        del settings["Autojoin"][to]
                    cl.leaveGroup(msg.to)
                elif text.lower() in ['@join']:
                    G = cl.getGroup(to)
                    if sender in owners["ownerss"]:
                        joinLink(cl,to)
                        Ticket = cl.reissueGroupTicket(msg.to)
                        for y in set["bot1"]:
                            y.acceptGroupInvitationByTicket(msg.to,Ticket)
                        joinLink(cl,to,True)
                        settings["protect"][to] = True
                        settings["qrprotect"][to] = True
                        settings["invprotect"][to] = True
                        random.choice(set["bot1"]).sendMessage(to, "預設踢人保護開啟")
                        random.choice(set["bot1"]).sendMessage(to, "預設網址保護開啟")
                        random.choice(set["bot1"]).sendMessage(to, "預設邀請保護開啟")
                        cl.sendMessage(to,"自動幫你設定群長")
                        G = cl.getGroup(op.param1)
                        if op.param1 not in gp["gm"]:
                            gp["gm"][op.param1] = []
                        try:
                            if G.creator.mid not in gp["gm"][op.param1]:
                                gp["gm"][op.param1].append(G.creator.mid)
                        except:
                            if op.param2 not in gp["gm"][op.param1]:
                                gp["gm"][op.param1].append(op.param2)		
                elif text.lower() == 'me':
                    if msg.toType == 0:
                        cl.sendContact(to, sender)
                    else:
                        sendMessageWithMention(to, sender)
                        cl.sendContact(to,sender)
                elif text.lower() == 'bothelp':
                    helpBot = helpbot()
                    cl.sendMessage(to, str(helpBot))
                elif text.lower() == 'tagall':
                    group = cl.getGroup(msg.to)
                    nama = [contact.mid for contact in group.members]
                    k = len(nama)//20
                    for a in range(k+1):
                        txt = u""
                        s=0
                        b=[]
                        for i in group.members[a*20 : (a+1)*20]:
                            b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
                            s += 7
                            txt += u'@Alin \n'
                        random.choice(set["bot1"]).sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
#=====查看權限單===================================================================================================================
                elif text.lower() == 'ownerlist':
                    if owners["ownerss"] == {}:
                        cl.sendMessage(to, "沒有最高權限者")
                    else:
                        cl.sendMessage(to, "以下是最高權限者")
                        mc = "╔══[ owner List ]"
                        for mi_d in owners["ownerss"]:
                            mc += "\n╠" + cl.getContact(mi_d).displayName
                        cl.sendMessage(to, mc+"\n╚══[總共"+str(len(owners["ownerss"]))+ "個人有最高權限]")
                elif text.lower() == 'gmlist':
                    G = cl.getGroup(to)				
                    if G.id not in gp["gm"] or gp["gm"][G.id]==[]:
                        cl.relatedMessage(msg.to,"沒有群組管理員的樣子",op.message.id)
                    else:
                         try:
                             mc = "►[ 群管名單 ]◄"
                             for mi_d in gp["gm"][G.id]:
                                 mc += "\n▸ " +cl.getContact(mi_d).displayName
                             cl.relatedMessage(msg.to,mc + "\n►[ 已經幫您查詢 ]◄",op.message.id)
                         except:
                             pass
#=====增加權限===================================================================================================================
                elif msg.text.lower().startswith("gradd "): 
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            if to not in gp['gm']:
                                gp['gm'][to] = {}
                            if ls not in gp['gm'][to]:
                                gp['gm'][to][ls] = ls
                                with open('group.json', 'w') as fp:
                                    json.dump(gp, fp, sort_keys=True, indent=4)
                                    cl.sendMessage(to, "成功新增GM權限")
                                    cl.sendContact(to, ls)
                            else:
                                cl.sendMessage(to, "此人已擁有GM權限")
                elif msg.text.lower().startswith("gdel "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            if ls in gp['gm'][to][ls]:
                                try:
                                    del gp['gm'][to][ls]
                                    with open('group.json', 'w') as fp:
                                        json.dump(gp, fp, sort_keys=True, indent=4)
                                        cl.sendMessage(to, "成功刪除Group Master權限")
                                except:
                                    cl.sendMessage(to, "[ERROR]\n刪除Group Master權限失敗")
                            else:
                                cl.sendMessage(to, "[ERROR]\n此人並未擁有Group Master權限")
                elif msg.text.lower().startswith("bban "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                       names = re.findall(r'@(\w+)', text)
                       mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                       mentionees = mention['MENTIONEES']
                       lists = []
                       for mention in mentionees:
                           if mention["M"] not in lists:
                               lists.append(mention["M"])
                       for ls in lists:
                           if ls not in black['tkbanlist']:
                               black['tkbanlist'][ls] = True
                               with open('black.json', 'w') as fp:
                                   json.dump(settings, fp, sort_keys=True, indent=4)
                                   cl.sendMessage(to, "成功新增永黑")
                                   cl.sendMessage(to, "[提示]\n已成功加入永黑\nMID: " + ls)
                                   cl.sendContact(to, ls)
                           else:
                               cl.sendMessage(to, "此人已擁有永黑")
                elif msg.text.lower().startswith("unbban "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                       names = re.findall(r'@(\w+)', text)
                       mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                       mentionees = mention['MENTIONEES']
                       lists = []
                       for mention in mentionees:
                           if mention["M"] not in lists:
                               lists.append(mention["M"])
                       for ls in lists:
                           if ls in black['tkbanlist']:
                               del black['tkbanlist'][ls]
                               with open('black.json', 'w') as fp:
                                   json.dump(settings, fp, sort_keys=True, indent=4)
                                   cl.sendMessage(to, "成功移除永黑")
                                   cl.sendMessage(to, "[提示]\n已成功移除永黑\nMID: " + ls)
                                   cl.sendContact(to, ls)
                           else:
                               cl.sendMessage(to, "此人並未擁有永黑")
                elif msg.text.lower().startswith("ban "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                       names = re.findall(r'@(\w+)', text)
                       mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                       mentionees = mention['MENTIONEES']
                       lists = []
                       for mention in mentionees:
                           if mention["M"] not in lists:
                               lists.append(mention["M"])
                       for ls in lists:
                           if ls not in black['blacklist']:
                               black['blacklist'][ls] = True
                               with open('black.json', 'w') as fp:
                                   json.dump(settings, fp, sort_keys=True, indent=4)
                                   cl.sendMessage(to, "成功新增黑單")
                                   cl.sendMessage(to, "[提示]\n已成功加入黑單\nMID: " + ls)
                                   cl.sendContact(to, ls)
                           else:
                               cl.sendMessage(to, "此人已擁有黑單")
                elif msg.text.lower().startswith("unban "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                       names = re.findall(r'@(\w+)', text)
                       mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                       mentionees = mention['MENTIONEES']
                       lists = []
                       for mention in mentionees:
                           if mention["M"] not in lists:
                               lists.append(mention["M"])
                       for ls in lists:
                           if ls in black['blacklist']:
                               del black['blacklist'][ls]
                               with open('black.json', 'w') as fp:
                                   json.dump(settings, fp, sort_keys=True, indent=4)
                                   cl.sendMessage(to, "成功移除黑單")
                                   cl.sendMessage(to, "[提示]\n已成功移除黑單\nMID: " + ls)
                                   cl.sendContact(to, ls)
                           else:
                               cl.sendMessage(to, "此人並未擁有黑單")
                elif text.lower().startswith("gban "):
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    G = cl.getGroup(to)
                    if to not in black["bbblacklist"]:
                        black["bbblacklist"][to] =[]
                        for x in key["MENTIONEES"]:
                            black["bbblacklist"][to].append(x["M"])
                            with open('black.json', 'w') as fp:
                                json.dump(gp, fp, sort_keys=True, indent=4)
                                cl.sendMessage(to, "成功新增單群黑單")
                    else:
                        for x in key["MENTIONEES"]:
                            black["bbblacklist"][to].append(x["M"])
                        cl.sendMessage(to,"ok")
                elif text.lower().startswith("gbandel "):
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    G = cl.getGroup(to)
                    if to not in black["bbblacklist"]:
                        cl.sendMessage(to, "There is no group ban！")
                    else:
                        for x in key["MENTIONEES"]:
                            try:
                                black["bbblacklist"][to].remove(x["M"])
                                del black["bbblacklist"][to]
                                cl.sendMessage(to, "已刪除單群黑單！")
                            except:
                                cl.sendMessage(to,"你沒權限")
                        cl.sendMessage(to,"OK")
                elif msg.text.lower(). startswith("ban:"):
                    x = text.replace("ban:",'')
                    y = x.split(' ')
                    for mid in y:
                        black["blacklist"][mid] = True
                    cl.sendMessage(to, "已加入黑名單")
                elif msg.text.lower(). startswith("unban:"):
                    x = text.replace("unban:",'')
                    y = x.split(' ')
                    for mid in y:
                        del black["blacklist"][mid]
                    cl.sendMessage(to, "已移除黑名單")
                elif text.lower().startswith('admindel:'):
                    x = text.replace("admindel:",'')
                    y = x.split(' ')
                    for mid in y:
                        del pp["admin"][mid]
                    cl.sendMessage(to, "已成功移除管理員權限")
                    backupData()
                elif msg.text.lower(). startswith("bban "):
                    x = text.replace("bban ",'')
                    y = x.split(' ')
                    for mid in y:
                        black["tkbanlist"][mid] = True
                    cl.sendMessage(to, "已加入永黑")
                elif msg.text.lower(). startswith("unbban "):
                    x = text.replace("unbban ",'')
                    y = x.split(' ')
                    for mid in y:
                        del black["tkbanlist"][mid]
                    cl.sendMessage(to, "已移除永黑")
                elif msg.text.lower(). startswith("owners:"):
                    x = text.replace("owners:",'')
                    y = x.split(' ')
                    for mid in y:
                        owners["ownerss"][mid] = True
                    cl.sendMessage(to, "已加入最高權限")
                elif msg.text.lower(). startswith("ownersdel:"):
                    x = text.replace("ownersdel:",'')
                    y = x.split(' ')
                    for mid in y:
                        del owners["ownerss"][mid]
                    cl.sendMessage(to, "已移除最高權限")
#=====友資黑單===================================================================================================================
                elif text.lower() == 'ban':
                    cl.sendMessage(to, "請傳送友資加入黑名單")
                    wait["ban"] = True
                elif text.lower() == 'unban':
                    cl.sendMessage(to, "請傳送友資移除黑名單")
                    wait["unban"] = True
                elif text.lower() == 'bban':
                    cl.sendMessage(to, "請傳送友資加入永黑")
                    wait["bban"] = True
                elif text.lower() == 'unbban':
                    cl.sendMessage(to, "請傳送友資移除永黑")
                    wait["unbban"] = True
                elif text.lower() == 'talk':
                    cl.sendMessage(to, "請傳送友資加入禁言黑單")
                    wait["talk"] = True
                elif text.lower() == 'untalk':
                    cl.sendMessage(to, "請傳送友資移除禁言黑單")
                    wait["untalk"] = True
                elif text.lower() == 'owner':
                    cl.sendMessage(to, "請傳送友資加入最大權限")
                    wait["owner"] = True
                elif text.lower() == 'unowner':
                    cl.sendMessage(to, "請傳送友資移除最大權限")
                    wait["unowner"] = True
#=====清除黑單跟永黑===================================================================================================================
                elif text.lower() == 'clear ban':
                    for mi_d in black["blacklist"]:
                        black["blacklist"] = {}
                    cl.sendMessage(to, "已清空黑名單")
                    json.dump(black, codecs.open('black.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                elif text.lower() == 'clear bban':
                    for mi_d in black["tkbanlist"]:
                        black["tkbanlist"] = {}
                    cl.sendMessage(to, "已清空永黑")
                    json.dump(black, codecs.open('black.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                elif text.lower() == 'clear talk':
                    for mi_d in black["Talklist"]:
                        black["Talklist"] = {}
                    cl.sendMessage(to, "已清空禁言黑單")
                    json.dump(black, codecs.open('black.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
#=====票===================================================================================================================
                elif msg.text.lower().startswith("ticket "):
                    x = text.split(" ")
                    if len(x) ==2:
                        if x[1] not in user["user"]:                                                           
                            user["user"][x[1]] = 1
                            cl.sendMessage(to,"ok")
                        else:
                            user["user"][x[1]] +=1
                        cl.sendMessage(to,"ok")
                    elif len(x) ==3:
                        if x[1] not in user["user"]:
                            user["user"][x[1]] = int(x[2])
                            cl.sendMessage(to,"ok")
                        else:
                            user["user"][x[1]] +=int(x[2])
                        cl.sendMessage(to,"ok")
                        backupData()
                elif text.lower() == '@rebot':
                    cl.sendMessage(to, "重新啟動中...")
                    cl.sendMessage(to, "重啟成功")
                    restartBot()
                elif msg.text.lower().startswith("add_wc"):
                    list_ = msg.text.split("：")
                    if to not in wc['wel']:
                        try:
                            wc['wel'][to] = list_[1]
                            with open('wel.json', 'w') as fp:
                                json.dump(wc, fp, sort_keys=True, indent=4)
                                cl.sendMessage(to, "[提示]\n成功設置群組歡迎訊息\n歡迎訊息: " + list_[1])
                        except:
                            cl.sendMessage(to, "[提示]\n設置群組歡迎訊息失敗!!!")
                    else:
                        cl.sendMessage(to, "[提示]\n群組歡迎訊息已存在!!!")
                elif msg.text.lower().startswith("renew_wc"):
                    list_ = msg.text.split("：")
                    if to in wc['wel']:
                        try:
                            del wc['wel'][to]
                            wc['wel'][to] = list_[1]
                            with open('wel.json', 'w') as fp:
                                json.dump(wc, fp, sort_keys=True, indent=4)
                                cl.sendMessage(to, "[提示]\n成功更新群組歡迎訊息\n歡迎訊息: " + list_[1])
                        except:
                            cl.sendMessage(to, "[提示]\n更新群組歡迎訊息失敗!!!")
                    else:
                        cl.sendMessage(to, "[提示]\n你正在更新不存在的歡迎訊息!!!")
                elif text.lower() == ("del_wc"):
                    if to in wc['wel']:
                        try:
                            del wc['wel'][to]
                            with open('wel.json', 'w') as fp:
                                json.dump(wc, fp, sort_keys=True, indent=4)
                                cl.sendMessage(to, "[提示]\n成功刪除群組歡迎訊息")
                        except:
                            cl.sendMessage(to, "[提示]\n刪除群組歡迎訊息失敗!!!")
                    else:
                        cl.sendMessage(to, "[提示]\n你正在刪除不存在的歡迎訊息!!!")
            
    except Exception as error:
        logError(error)
print("系統開始執行~")
while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                #lineBot(op)
                oepoll.setRevision(op.revision)
                thread = threading.Thread(target=lineBot, args=(op,))
                thread.start()
    except Exception as e:
        logError(e)
