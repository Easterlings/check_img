import os
# 获取 .env 文件的绝对路径
abs_env_path = os.path.abspath('.env')
# 加载环境变量
if os.path.exists(abs_env_path):
    with open(abs_env_path, 'r') as env_file:
        for line in env_file:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                os.environ[key] = value
else:
    raise Exception(f".env file not exists")


DATABASE = {
    "host" : "127.0.0.1",
    "user" : "root",
    "password" : "123456",
    "database" : "check_img",
}

# 数据库
if os.environ.get('DB_HOST'):
    DATABASE = {
        "host" : os.environ.get('DB_HOST'),
        "user" : os.environ.get('DB_USERNAME'),
        "password" : os.environ.get('DB_PASSWORD'),
        "database" : os.environ.get('DB_DATABASE'),
    }
