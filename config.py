from urllib import parse

# vCenter 的的认证配置
VC_CONFIG_MAP = {
    "DC1-vCenter": {
        "host": "10.10.10.1",
        "user": "query",
        "pwd": "password",
    },
    "DC2-vCenter": {
        "host": "10.10.10.3",
        "user": "query",
        "pwd": "password",
    },
}

REPORT_DB_DSN = "mysql+pymysql://user:{!s}@10.10.10.3:3306/db?charset=utf8".format(parse.unquote_plus("passw@rd"))
