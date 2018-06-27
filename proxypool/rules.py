PATH='/root/Code/spiders/proxypool/'
PLACE=open(PATH+'place.txt', 'r').read().split('\n')

TASKS={
    "xici": {
        "host": "http://www.xicidaili.com/",
        "resource": ["http://www.xicidaili.com/nn/%d"%(x) for x in range(1, 6)]+
                    ["http://www.xicidaili.com/nt/%d"%(x) for x in range(1, 6)]+
                    ["http://www.xicidaili.com/wn/%d"%(x) for x in range(1, 6)]+
                    ["http://www.xicidaili.com/wt/%d"%(x) for x in range(1, 6)],
        "parser_type": "page",
        "parse_rule":{
            "prefix": "//tr",
            "start_pos": 1,
            "end_pos": None,
            "detail": "td/text()",
            "ip_pos": 0,
            "port_pos": 1,
            "protocal_pos": 4,
        },
        "interval": 15,
    },
    "free_proxy_list": {
	"host": "https://free-proxy-list.net/",
        "resource": ["https://free-proxy-list.net/"],
        "parser_type": "page",
        "parse_rule":{
            "prefix": "//tbody/tr",
            "start_pos": 0,
            "end_pos": None,
            "detail": "td/text()",
            "ip_pos": 0,
            "port_pos": 1,
            "protocal_pos": None,
        },
	"interval": 10,
    },
    "kuai": {
        "host": "https://www.kuaidaili.com/",
        "resource": ["https://www.kuaidaili.com/free/inha/%d"%(x) for x in range(1, 9)]+
                    ["https://www.kuaidaili.com/free/intr/%d"%(x) for x in range(1, 9)],
        "parser_type": "page",
        "parse_rule": {
            "prefix": "//tr",
            "start_pos": 1,
            "end_pos": None,
            "detail": "td/text()",
            "ip_pos": 0,
            "port_pos": 1,
            "protocal_pos": 3,
        },
        "interval": 15,
    },
    "data5u": {
        "host": "http://www.data5u.com/",
        "resource": ["http://www.data5u.com/free/index.shtml",
                    "http://www.data5u.com/free/gngn/index.shtml",
                    "http://www.data5u.com/free/gnpt/index.shtml",
                    "http://www.data5u.com/free/gwgn/index.shtml",
                    "http://www.data5u.com/free/gwpt/index.shtml"]+
                    ["http://www.data5u.com/free/area/%s/index.html"%(x) for x in PLACE if x],
        "parser_type": "page",
        "parse_rule": {
            "prefix": "//ul[@class='l2']",
            "start_pos": 0,
            "end_pos": None,
            "detail": "span/li/.//text()",
            "ip_pos": 0,
            "port_pos": 1,
            "protocal_pos": 3,
        },
        "interval": 15,
    }
}

VALIDATE_RULES={
    'baidu': {
        'urls': ['http://www.baidu.com'],
        'check_sign': ['Baidu'],
    },
    'zhihu': {
        'urls': ['https://www.zhihu.com'],
        'check_sign': ['知乎'],
    },
}

# TASK_ITEMS=[
#     {"name":"xici", "url":"http://www.xicidaili.com/nn/1"},
# ]

THRESHOLD_SPEED=1

DB_HOST='localhost'
DB_PORT=6379
DB_ID=1

DB_TASK_QUEUE_NAME="ProxyPool:TASK_QUEUE"
DB_RAW_IPPOOL_NAME="ProxyPool:RAW_IPPOOL"
DB_IPPOOL_NAME="ProxyPool:IPPOOL"

DB_SPLIT_SYMBOL=','
