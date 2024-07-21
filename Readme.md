# 背背——ai识别笔记抽查记忆软件，支持识别幕布、MindMaster、mindline、XMind等主流思维导图软件的txt、docx导出格式，支持识别markdown格式笔记



​														<u>软件制作不易，请大家多多支持！</u>



### 1.1 版本说明：

​	背背——2.1版本更新：

- 支持使用智谱清言GLM及chatGPT的API导入；
- 支持识别幕布、MindMaster、mindline、XMind等主流思维导图软件的txt、docx导出格式，支持识别markdown格式笔记（.md）
- 更新

### **1.1 软件功能概述**

“背背”是一款支持对**markdown和思维导图的导出笔记**进行ai分析、出题的软件，创新性地将思维导图和markdown的内容逻辑性与ai的强大理解能力相结合，达到用户随心所欲使用的流畅效用。

该软件结合大模型使用，真正实现ai理解笔记并随机抽查的功能，基于**抽查式背诵**，只需要在你的标记中标记出要背的内容，即可随时随机抽查笔记内容，实现科学、高效的记忆，简直是**零碎知识点烦恼者和背诵困难者**们的救星！

与普通ai大模型的知识库功能相比最大的优点，是可以定制化不同位置的笔记出题，能够随时在记笔记过程中标注自己认为重要的知识点，笔记记录后直接导入软件进行ai分析，ai会将所有标记点位置的相关知识点理解，转化为提问形式，且**保证答案一定为原笔记内容**。经过测试，在后端+ai大模型的结合下，精确出题正确率达到90%。以下是与大模型知识库（智谱清言GLM-4）对比之下的优势：

 

|                      | 智谱清言知识库                                               | 背背——ai笔记理解                                           |
| -------------------- | ------------------------------------------------------------ | ---------------------------------------------------------- |
| 功能                 | 理解用户文档，根据用户文档回答问题                           | Ai理解软件抽选文档，并严格按照格式出题                     |
| 出题方式             | 每次需主动打字要求，题目种类和知识点容易发散，以综合题目考察测试为主 | 一键点击出题，题目精确到笔记原文内容，以抽查式回忆笔记为主 |
| 是否可定位原笔记位置 | 人工智能黑箱操作，否                                         | 后端加持处理，直接回看出题原笔记                           |
| 便利性与准确性       | 需要用户频繁输入，出现问题随机                               | 按钮点击即可抽查，且确保每次提的问题都是自己标记的相关内容 |

 

综上所述，背背ai理解笔记软件专为结构逻辑型思维导图/markdown笔记开发。结合穿插式记忆+抽查式学习，真正做到ai赋能学习，让大量零碎知识点通过科学的方式印入脑海，让ai称为理解你的学习导师。

### **1.2 软件使用指南**

“背背”ai理解软件界面利用wxpython架构，使用zhiuai的大模型api实现ai读取和理解。

在使用源代码时，建议python版本升级到3.12。在pycharm终端的本项目文件夹下，使用“pip install -r requirements.txt”安装依赖：

![image-20240721134014412](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20240721134014412.png)

 

在您需要的导入笔记中，需要用大括号{}来标记我们认为重要且需要背下的知识点，这些标记可以在做笔记时同步标注，学习后将笔记内容直接导入软件，方便快捷。大括号的标记方法有两种格式：

①对该知识点的子内容标记，只需在笔记知识点内容加上“{}”即可。知识点可以是“优点”这种抽象的知识点标识，只需要保证整体笔记有逻辑即可。如下图（思维导图实示例）：



![image-20240720120116999](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20240720120116999.png)

 

②对该知识点的部分内容本身进行标记，利用“{”和“}”将对应的信息点括起来即可，如下图，ai将会将本知识点挖去答案，再转化表述进行出题，这对于学生记忆细致且重要的知识点非常有用。如下图：

 ![image-20240720120254321](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20240720120254321.png)

 

准备好笔记标注，即可将笔记导出成为待识别格式。利用主流思维导图软件的“导出”功能，导出成为docx或txt形式，最终格式要让思维导图变为文本大纲格式，以mindmaster和mindline举例如下：



<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20240720121938143.png" alt="image-20240720121938143" style="zoom: 50%;" />

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20240720122344321.png" alt="image-20240720122344321" style="zoom: 67%;" />

前往智谱ai开放平台（[智谱AI (zhipuai.cn)](https://www.zhipuai.cn/)），注册/登录后前往”api秘钥“，进入”账户充值“充值一定量金额获得api使用权（新用户有一个月100万token免费使用权，无需充值，可跳过此步）。充值后在”API keys“处复制api秘钥

（如果你有其他大模型的API和调用方法，可以直接在botChange下替换调用代码并使用）



![image-20240720121128233](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20240720121128233.png)



进入BotChange.py，将你的api秘钥填入api-key中：



![image-20240720121629369](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20240720121629369.png)



准备工作完成。接下来，在GUI_start页面运行，即可打开软件界面：

 

![img](file:///C:\Users\DELL\AppData\Local\Temp\ksohtml14684\wps12.jpg) ![img](file:///C:\Users\DELL\AppData\Local\Temp\ksohtml14684\wps13.jpg)

 

打开软件后，进入选择文件界面。我们点击打开文件，找到刚才我们导出的**文字大纲格式笔记**：



![img](file:///C:\Users\DELL\AppData\Local\Temp\ksohtml14684\wps14.jpg) 



导入笔记后注意，该笔记软件需要联网连接ai大模型，否则会出现警告字样：

 

![img](file:///C:\Users\DELL\AppData\Local\Temp\ksohtml14684\wps17.jpg) 

 

连接网络后，重新点击“确定”。等待ai返回数据后，进入主界面。如下图所示，主界面由文本框（显示ai提问文本）、显示上级内容按钮，答案按钮和换题按钮组成：

 

![img](file:///C:\Users\DELL\AppData\Local\Temp\ksohtml14684\wps18.jpg) 



用户可以点击“向上展开”，看到该问题在笔记中所属的更宽知识点范围以帮助唤醒记忆，支持多次点击逐步向上获取父级内容。



![image-20240718191037623](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20240718191037623.png)



若想不起该问题答案，点击“答案”按钮，对应答案会出现。答案内容可以继续展开的，会在内容后以“++”标注。点击标签即可继续展开答案的子内容：

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20240720122800718.png" alt="image-20240720122800718" style="zoom: 67%;" />



需要看题目在原文笔记出处，可以点击“显示笔记原出处”按钮，进入原笔记所在的位置，一键回顾原笔记内容：



<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20240720123047750.png" alt="image-20240720123047750" style="zoom:67%;" />



*作者寄语：*

欢迎大家共帮助同完善背背的功能，真正让ai助力成为我们随手可用的“第二大脑”！对软件有建议、有疑问，希望成为贡献者，可加入交流群：



<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20240721135040962.png" alt="image-20240721135040962" style="zoom: 33%;" />



接下来，本软件将持续不断地更新更多功能，也欢迎您参与成为贡献者。

觉得这款软件不错的，给我们打赏给我们多多支持！你们的支持就是我们探索的动力！

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20240721134240483.png" alt="image-20240721134240483" style="zoom: 33%;" />

![img](file:///C:\Users\DELL\AppData\Local\Temp\SGPicFaceTpBq\16676\01058027.jpg)