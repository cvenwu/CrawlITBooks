from wxpy import *
bot = Bot()

friend = ensure_one(bot.search('SoBooks电子书')[0])
friend.send('验证码')


@bot.register(friend)
def forward_boss_message(msg):
    print(msg.raw)
    # if msg.member == friend:
        # msg.forward(bot.file_helper, prefix='老板发言')

# 堵塞线程
embed()