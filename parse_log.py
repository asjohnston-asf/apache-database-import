import cx_Oracle
import re
from urlparse import urlparse
from urlparse import parse_qs

DB_USER = ''
DB_PASSWORD = ''
DB_SID = ''
LOG_FILE = ''
HOST = ''

db = cx_Oracle.connect(DB_USER, DB_PASSWORD, DB_SID)

cur = db.cursor()

ii = 0
regex = '([(\d\.)]+) - \S* \[(\S*?) \S*?\] "(\S*) ?(\S*) ?\S*?" (\d+) (\S*?) ".*?" "(.*?)".*'

with open(LOG_FILE, 'r') as input:
    while True:
        line = input.readline()
        if not line:
            break
        ii = ii + 1
        print(str(ii) + ': ' + line)
        (ip, time, method, url, response_code, response_size, user_agent) = re.match(regex, line).groups()
        o = urlparse(url)
        if response_size == '-':
            response_size = None

        cur.execute("insert into asfadm.request values (:1, :2, :3, :4, TO_DATE(:5, 'DD/Mon/YYYY:HH24:MI:SS'), :6, :7, :8, :9)",
            (ii, HOST, o.path[:299], ip, time, method, user_agent, response_size, response_code))

        params = parse_qs(o.query)
        for param_name in params:
            for param_value in params[param_name]:
                cur.execute ("insert into asfadm.request_parm values (:1, :2, :3)",
                             (ii, param_name, param_value[:499]))

db.commit()
