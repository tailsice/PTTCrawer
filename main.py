#!/usr/bin/python3.5

import sys
import json
import getpass
import codecs
from PTTLibrary import PTT

def showPost(Post):
    PTTBot.Log('文章代碼: ' + Post.getID())
    PTTBot.Log('作者: ' + Post.getAuthor())
    PTTBot.Log('標題: ' + Post.getTitle())
    PTTBot.Log('時間: ' + Post.getDate())
    PTTBot.Log('價錢: ' + str(Post.getMoney()))
    PTTBot.Log('IP: ' + Post.getIP())
    PTTBot.Log('網址: ' + Post.getWebUrl())

    PTTBot.Log('內文:\n' + Post.getContent())

    PushCount = 0
    BooCount = 0
    ArrowCount = 0

    for Push in Post.getPushList():
        PushType = Push.getType()

        if PushType == PTT.PushType.Push:
            PushCount += 1
        elif PushType == PTT.PushType.Boo:
            BooCount += 1
        elif PushType == PTT.PushType.Arrow:
            ArrowCount += 1
        
        Author = Push.getAuthor()
        Content = Push.getContent()
        # IP = Push.getIP()
        PTTBot.Log('推文: ' + Author + ': ' + Content)
        
    PTTBot.Log('共有 ' + str(PushCount) + ' 推 ' + str(BooCount) + ' 噓 ' + str(ArrowCount) + ' 箭頭')

def PostHandler(Post):
    
    with codecs.open("CrawlBoardResult.txt", "a", "utf-8") as ResultFile:
        ResultFile.write('P幣: ' + str(Post.getMoney()) + ' ' + Post.getTitle() + '\n')

try:
    with open('Account.txt') as AccountFile:
        Account = json.load(AccountFile)
        ID = Account['ID']
        Password = Account['Password']
except FileNotFoundError:
    ID = input('請輸入帳號: ')
    Password = getpass.getpass('請輸入密碼: ')

# 如果不想在登入的時候踢掉其他登入，你可以這樣使用
PTTBot = PTT.Library(kickOtherLogin=False)
# 登入
ErrCode = PTTBot.login(ID, Password)
# 使用錯誤碼，判斷登入是否成功
if ErrCode != PTT.ErrorCode.Success:
    PTTBot.Log('登入失敗')
    sys.exit()

#CrawPost = 100
CrawPost = 1

EnableSearchCondition = False
inputSearchType = PTT.PostSearchType.Keyword
inputSearch = '[公告]'

if EnableSearchCondition:
    ErrCode, NewestIndex = PTTBot.getNewestIndex(Board='Hsinchu', SearchType=inputSearchType, Search=inputSearch)
else:
    ErrCode, NewestIndex = PTTBot.getNewestIndex(Board='Hsinchu')

if ErrCode == PTT.ErrorCode.Success:
    PTTBot.Log('取得 ' + 'Hsinchu' + ' 板最新文章編號成功: ' + str(NewestIndex))
else:
    PTTBot.Log('取得 ' + 'Hsinchu' + ' 板最新文章編號失敗')
    sys.exit()

# MaxMultiLogin             多重登入數量
# SearchType                搜尋種類
# Search                    搜尋條件

if EnableSearchCondition:
    ErrCode, SuccessCount, DeleteCount = PTTBot.crawlBoard('Hsinchu', PostHandler, StartIndex=NewestIndex - CrawPost + 1, EndIndex=NewestIndex, SearchType=inputSearchType, Search=inputSearch)
else:
    ErrCode, SuccessCount, DeleteCount = PTTBot.crawlBoard('Hsinchu', PostHandler, StartIndex=NewestIndex - CrawPost + 1, EndIndex=NewestIndex)

if ErrCode == PTT.ErrorCode.Success:
    PTTBot.Log('爬行成功共 ' + str(SuccessCount) + ' 篇文章 共有 ' + str(DeleteCount) + ' 篇文章被刪除')

# 登出
PTTBot.logout()
