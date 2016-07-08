create table asfadm.request (
  id integer,
  host VARCHAR2(100),
  path VARCHAR2(300),
  ip_address VARCHAR2(30),
  request_time DATE,
  request_method VARCHAR2(10),
  user_agent VARCHAR2(500),
  response_size INTEGER,
  response_code INTEGER,
  constraint pk_request primary key (id)
);

create table asfadm.request_parm (
  id INTEGER,
  parm_name VARCHAR2(500),
  parm_value VARCHAR2(500)
);

create index request_parm_id_idx on asfadm.request_parm(id);
create public synonym request for asfadm.request;
create public synonym request_parm for asfadm.request_parm;
