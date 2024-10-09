#!/bin/sh
echo "Welcome to CN_OCA!";
echo "===================";
echo "请输入本次提交的说明: ";
read commint_note
git add . > /dev/null 2>&1
git commit -m "${commint_note}"  > /dev/null 2>&1
echo "请推送远端分支名称:";
read branch_name;
git push --set-upstream origin "feature/${branch_name}"
echo "请登录到osrbz 进入远端分支申请合并到osbbz/16.0分支"
