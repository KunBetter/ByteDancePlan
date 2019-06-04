from googletrans import Translator

translator = Translator()


def googleTranslate(english):
    return translator.translate(english, 'zh-cn').text


if __name__ == '__main__':
    english = 'hello'
    chinese = googleTranslate(english)
    print(chinese)
