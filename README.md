
# 免责声明
<span style="color:red;">**该脚本打卡会强制修改为在校状态，非在校同学切勿使用！！！**</span>

郑重声明：本人只是使用该脚本测试微信通知功能，不承担一切责任【仅用于学习交流请大家遵守防疫政策】。任何个人使用本脚本一律视为自行承担全部责任！

验证码辅助识别为图鉴api
图鉴识别仅为残障人士以及有需要的个人和企业提供图像识别和图像识别分类服务
http://www.kuaishibie.cn/news/2b2c1b3bb7104c66bdd7ba421eaa4506.html

**该脚本打卡会强制修改为在校状态，非在校同学切勿使用！！！**

以下大部分为原作者的内容
# Daily_Fudan
> 一键平安复旦小脚本
> 

> 无用的前情提要：https://zhuanlan.zhihu.com/p/136340395
>


---

## 💭声明
【仅用于学习交流请大家遵守防疫政策】


> 🔺 此脚本原理是拉取你上一次提交的信息，然后再次上传。所以跟你前一天信息一样，如果你需要修改，请停止此脚本运行，并手动提交。
> 

> 🛑 由于本人水平零蛋， 此脚本能跑起来属实意外，本人怀着探讨的目的上传到网络平台交流，并未授权任何人，造成的一切后果概不负责。


这个人很懒，此Readme文档直接拿[genshin-impact-helper](https://github.com/y1ndan/genshin-impact-helper)
改的

## 📐部署

- 项目地址：[github/daily_fudan_actions](https://github.com/Limour-dev/daily_fudan_actions)
- 点击右上角`Fork`到自己的账号下

![fork](https://i.loli.net/2020/10/28/qpXowZmIWeEUyrJ.png)

- 将仓库默认分支设置为 main 分支


### 3. 添加 账号密码 至 Secrets

- 回到项目页面，依次点击`Settings`-->`Secrets`-->`New secret`

![new-secret.png](https://i.loli.net/2020/10/28/sxTuBFtRvzSgUaA.png)

- 建立名为`FUDAN`的 secret，值为`学号`+`(空格)`+`密码`，最后点击`Add secret`
- secret名字必须为`FUDAN`！
- secret名字必须为`FUDAN`！
- secret名字必须为`FUDAN`！
- 如果要开启成功填写的通知，在 http://iyuu.cn/ 申请token 然后在密码后面+ `(空格)`+`token`
- `学号`+`(空格)`+`密码`+ `(空格)`+`token`
- 如果要开启验证码识别，在 http://www.kuaishibie.cn/ 注册账号并充值
  然后在token后面 + `(空格)`+`uname` + `(空格)`+`pwd`
- `学号`+`(空格)`+`密码`+ `(空格)`+`token`+`(空格)`+`uname` + `(空格)`+`pwd`

### 4. 启用 Actions

> Actions 默认为关闭状态，Fork 之后需要手动执行一次，若成功运行其才会激活。

返回项目主页面，点击上方的`Actions`，再点击左侧的`Daily Fudan`，再点击`Run workflow`
    
![run](https://i.loli.net/2020/10/28/5ylvgdYf9BDMqAH.png)

</details>

至此，部署完毕。

## 🔍结果

当你完成上述流程，可以在`Actions`页面点击`Daily Fudan`-->`build`-->`Run sign`查看结果。

<details>
<summary>查看结果</summary>

### 签到成功

如果成功，会输出类似`成功`的信息：


### 签到失败

如果失败，会输出类似`啥`的信息：


同时你会收到一封来自GitHub、标题为`Run failed: Daily Fudan - master`的邮件。

</details>







