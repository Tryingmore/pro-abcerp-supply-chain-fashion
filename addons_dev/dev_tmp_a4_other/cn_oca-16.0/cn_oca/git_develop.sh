#!/bin/sh
echo "欢迎参与 CN_OCA!";
echo "===================";
echo "请输入开发分支名称:";
read branch_name;
git checkout 16.0 > /dev/null 2>&1
git branch -v > /dev/null 2>&1
git checkout -b "feature/${branch_name}" > /dev/null 2>&1
echo "创建分支: ${branch_name}"
echo "请将要开发的模块从OCA拷到当前目录下. "
