SmartQQBot - AzurLane插件
=========

## 注意: 本分支只针对azurlane插件开展

## 依赖
+ `PIL` or `Pillow`
+ `six` and `requests`
+ `bottle` （可选）

## 快速开始
+ 安装Python \> 2.6 / Python \>= 3(tested on 3.4)
+ `python setup.py develop`
+ `pip install bottle`
+ `python run.py --no-gui --http`
+ 访问`your_host_addr:8888`,扫码登录
+ 控制台不再输出登录确认的log的时候就登录成功了
+ 首次登陆过后, 以后的登陆会尝试使用保存的cookie进行自动登录（失败后会自动弹出二维码进行二维码登陆）


## 特性

+ 二维码登录（支持本地扫码和浏览器扫码)


### 基础功能
注: 插件默认启用了basic、weather和manager, 如需其他功能请自行配置开启

+ 舰娘查询(azurlane[shhip]), 响应群聊`(船|老婆|舰娘) XXX`, 回复wiki中该舰娘基本属性
+ 复读功能(basic[repeat]), 检测到群聊中***连续两个***回复内容相同, 将自动复读该内容1次。



## 已知问题
+ 由于WebQQ协议的限制, 机器人回复消息有可能会被屏蔽, 暂时还没有较好的解决方案。

## ChangeLog
+ 2018.10.23 azurlane插件


## RoadMap

+ 装备/天梯一图流

## Basic&Thanks
+ [SmartQQBot--Yinzo](https://github.com/Yinzo/SmartQQBot)




