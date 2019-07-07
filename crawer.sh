#!/bin/bash
DIR="/home/icl/PTT"
FILE_1="CrawlBoardResult-1.txt"
MD5_1="md5_1"
FILE_2="CrawlBoardResult-2.txt"
MD5_2="md5_2"
FILE_3="CrawlBoardResult-3.txt"
MD5_3="md5_3"
URL="Webhook link"
cd $DIR

#if [ -e $FILE ]; then
#  rm -rf $FILE
#fi

# Gossiping
MD5=$(md5sum $FILE_1 | awk '{print $1}')
OLD_MD5=$(cat $MD5_1)

if [ "$MD5" != "$OLD_MD5" ]; then
  echo "Update MD5"
  echo $MD5 > $MD5_1
  cat $FILE | grep "發錢"
  if [ "$?" == "0" ]; then
    curl -X POST --data-urlencode "payload={\"channel\": \"@tails\", \"username\": \"webhookbot\", \"text\": \"This is has new posted for money on Gossiping board.\", \"icon_emoji\": \":ghost:\"}" "$URL"
  fi
fi

rm -rf $FILE_1

# PokemonGO
MD5=$(md5sum $FILE_2 | awk '{print $1}')
OLD_MD5=$(cat $MD5_2)

if [ "$MD5" != "$OLD_MD5" ]; then
  echo "Update MD5"
  echo $MD5 > $MD5_2
  cat $FILE | grep "發錢"
  if [ "$?" == "0" ]; then
    curl -X POST --data-urlencode "payload={\"channel\": \"@tails\", \"username\": \"webhookbot\", \"text\": \"This is has new posted for money on PokemonGO board.\", \"icon_emoji\": \":ghost:\"}" "$URL"
  fi
fi

rm -rf $FILE_2

# Hsinchu
MD5=$(md5sum $FILE_3 | awk '{print $1}')
OLD_MD5=$(cat $MD5_3)

if [ "$MD5" != "$OLD_MD5" ]; then
  echo "Update MD5"
  echo $MD5 > $MD5_3
  cat $FILE | grep "贈送"
  if [ "$?" == "0" ]; then
    curl -X POST --data-urlencode "payload={\"channel\": \"@tails\", \"username\": \"webhookbot\", \"text\": \"This is has new posted for gift on HsinChu board.\", \"icon_emoji\": \":ghost:\"}" "$URL"
  fi
fi

rm -rf $FILE_3
