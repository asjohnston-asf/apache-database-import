create schema api;

create table api.requests
(
  id bigint primary key,
  host varchar(100),
  path varchar(300),
  ip_address varchar(30),
  request_time timestamp,
  request_method varchar(10),
  user_agent varchar(500),
  response_size bigint,
  response_code bigint
);

create table api.request_parm (
  request_id bigint,
  parm_name varchar(500),
  parm_value varchar(500)
);

create index request_id on api.request_parm(request_id);
