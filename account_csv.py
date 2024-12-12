import os
import django
import pandas as pd


# Thêm thư mục chứa ứng dụng Django vào sys.path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "datn.settings")
django.setup()
from accounts.models import Account, UserProfile
import names
import random


def random_phone_generator():
    first = str(random.randint(100, 999))
    second = str(random.randint(1, 888)).zfill(3)

    last = (str(random.randint(1, 9998)).zfill(4))
    while last in ['1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888']:
        last = (str(random.randint(1, 9998)).zfill(4))

    return '{}-{}-{}'.format(first, second, last)


df = pd.read_csv(r'customers.csv')
df2 = df.drop_duplicates()

for index, row in df2.iterrows():
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    phone_number = random_phone_generator()  # Sử dụng hàm tạo số điện thoại ngẫu nhiên
    email = row[0] + '@gmail.com'
    password = row[0]
    username = email.split('@')[0]
    customer_id = row[0]

    try:
        user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username,
                                           password=password)
        user.phone_number = phone_number
        user.save()
    except Exception as e:
        print('Lỗi:', e)
        continue

    profile = UserProfile()
    profile.user_id = user.id
    profile.profile_picture = 'default/default-user.png'
    profile.save()
    print(index)
