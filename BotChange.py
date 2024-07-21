# import threading
import Error
# import wx
from zhipuai import ZhipuAI, APIConnectionError
# import openai
# import httpx

# from bot import bot_factory
# from bridge.bridge import Bridge
from log import logger


def botChange(content, question):
    # 检查字符串的最后两个字符是否是 "{}"
    if question[-2:] == "{}":
        # 如果是，将它们替换为 "?"
        question = question[:-2] + "?"
    if question.find('{') != -1 and question.find('}') - question.find("{") != 1:
        cur = question.find('{') + 1
        sub_string = ""
        # logger.info(question)
        while question[cur] != '}':
            sub_string += question[cur]
            cur += 1
        question = question.replace("{" + sub_string + "}", "？？？")
        # logger.info(sub_string)
        question = question.lstrip(" ")
        new_content = ("以下是部分markdown截取笔记：" + content + "其中，问题是" + "“" +
                       question + "”，" + "目标答案a是：" + sub_string + "。" +
                       "问题格式一般是“是什么”“是怎样”其中的一种。请你理解问题的上下文后，请将该问题以更完整的形式问出来，看如何问这个问题能够得到目标答案a, 问题中不要出现答案相关内容。请直接给出问题，不要回复其他内容")
    else:
        question = question.lstrip(" ")
        new_content = ("以下是部分markdown截取笔记：" + content + "其中，问题是" + "“" +
                       question + "”。" +
                       "请你理解上下文，上文是问题的提问范围或对应知识点，下文是问题的答案。需要你将该问题以更完整的形式问出来,问题中不要出现答案相关内容。请直接给出问题，不要回复其他内容")

    """
    此为智谱清言API调用代码。在使用时，将api_key和model切换成你的api以及对应model即可。推荐使用GLM-4，更加智能，对笔记的理解准确度更高
    """
    client = ZhipuAI(api_key="21*************************************Pt")
    try:
        completion = client.chat.completions.create(
            # model="glm-3-turbo",  # 填写需要调用的模型名称
            model="glm-4",
            messages=[
                {"role": "user", "content": new_content},
            ],
        )
    except APIConnectionError:
        raise Error.InitializationError("我连接不到你的网络")
    """
    以上为智谱清言调用代码。如需更换大模型，将上面代码替换，并将message设置为：
    messages=[
                {"role": "user", "content": new_content},
            ],
    """

    if completion.choices[0].message.content.find('：') != -1:
        return completion.choices[0].message.content[completion.choices[0].message.content.index('：') + 1:]
    return completion.choices[0].message.content

    # bot = bot_factory.create_bot(Bridge().btype['chat'])
    # session_id = 20021010
    # bot_prompt = "你是一个出题机器人，接收到消息后只需要针对内容提问即可"
    # session = bot.sessions.build_session(session_id, bot_prompt)
    # session.add_query(new_content)
    # logger.info(new_content)
    # result = bot.reply_text(session)
    # prompt = result['content']
    # return prompt
