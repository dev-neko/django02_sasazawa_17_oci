'''
https://qiita.com/haessal/items/abaef7ee4fdbd3b218f5
ここの記事を参考にして、プロジェクトをクローンするごとに SECRET_KEY を生成する形にした
'''

from django.core.management.utils import get_random_secret_key

secret_key = get_random_secret_key()
text = 'SECRET_KEY=\'{0}\''.format(secret_key)
print(text)