import time
import openai
import telebot

# устанавливаем ключ API от OpenAI
openai.api_key = "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"

# создаем экземпляр бота для Telegram
bot = telebot.TeleBot("6062518191:AAHrZtGWo9ev3gE8G6Kp7IOVGsDtpTirDEs")

# функция для генерации комплиментов
def generate_compliment():
    prompt = "Напиши комплимент для девушки на русском языке. Используй от 200 до 300 символов. Учитывай время суток - московское."
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=100,
        n=1,
        stop=None,
        timeout=30,
    )
    compliment = response.choices[0].text.strip()
    return compliment

# функция для отправки комплимента
def send_compliment(chat_id):
    compliment = generate_compliment()
    bot.send_message(chat_id, compliment)

# функция для отправки комплиментов каждые 2 часа
def start_compliment_sender(chat_id):
    while True:
        try:
            # Проверяем текущее время
            now = time.localtime()
            hour = now.tm_hour
            # Отправляем комплимент только если время между 11 и 23 часами по мск
            if hour >= 11 and hour < 23:
                send_compliment(chat_id)
            time.sleep(7200)
        except Exception as e:
            print(e)
            time.sleep(60)

# обработчик команды start
@bot.message_handler(commands=["start"])
def handle_start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Привет. Владик очень переживает, что ты слишком долго будешь сидеть без комплиментов, поэтому он сделал меня. Я, типа купидон или что-то в этом духе. Кстати, есть вероятность, что никакого бота нет, а Владик просто стесняется слишком часто отправлять комплименты, поэтому сделал вид, что это типа бот. Кто знает...)")
    start_compliment_sender(chat_id)

# запускаем бота
bot.polling(none_stop=True)
