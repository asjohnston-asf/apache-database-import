import psycopg2
import re
from urlparse import urlparse
from urlparse import parse_qs
from sys import argv
from os import environ

apache_host = 'api.daac.asf.alaska.edu'
LOG_FILE = argv[1]
ii = int(argv[2])

DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_NAME = 'postgres'
DB_HOST = os.environ['DB_HOST']

connection_string = 'dbname={0} user={1} password={2} host={3}'.format(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST)
db = psycopg2.connect(connection_string)

cur = db.cursor()

regex = '([(\d\.)]+) - \S* \[(\S*?) \S*?\] "(\S*) ?(\S*) ?\S*?" (\d+) (\S*?) ".*?" "(.*?)".*'

with open(LOG_FILE, 'r') as input:
  while True:
    line = input.readline()
    if not line:
      break

    try:
      ii = ii + 1
      result = re.match(regex, line)
      if not result:
        print(ii)
        print(line)
        continue
      (ip, time, method, url, response_code, response_size, user_agent) = result.groups()
      o = urlparse(url)
      if response_size == '-':
        response_size = None

      cur.execute("insert into api.requests values (%s, %s, %s, %s, to_timestamp(%s, 'DD/Mon/YYYY:HH24:MI:SS'), %s, %s, %s, %s)",
        (ii, apache_host, o.path[:299], ip, time, method, user_agent, response_size, response_code))

      params = parse_qs(o.query)
      for param_name in params:
        for param_value in params[param_name]:
          cur.execute ("insert into api.request_parm (request_id, parm_name, parm_value) values (%s, %s, %s)",
                             (ii, param_name, param_value[:499]))
      if not (ii%10000):
        print(ii)
    except Exception as e:
      print(ii)
      print(line)
      print(e)
      raise e

db.commit()
