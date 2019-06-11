from googletrans import Translator
import json
import requests

translator = Translator()


def google_translate(en):
    return translator.translate(en, 'zh-cn').text


def youdao_translate(text):
    # youdao dic api
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    key = {
        'type': "AUTO",
        'i': text,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "true"
    }
    response = requests.post(url, data=key)
    if response.status_code == 200:
        result = json.loads(response.text)
        return result['translateResult'][0][0]['tgt']
    else:
        return None


if __name__ == '__main__':
    english = 'hello'
    chinese = google_translate(english)
    print(google_translate(english))
    print(youdao_translate(english))
