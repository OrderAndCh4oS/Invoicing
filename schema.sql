create table billable_item
(
  id          integer
    primary key
  autoincrement,
  title       text not null,
  description text,
  invoice_id  int  not null,
  qty         real not null,
  rate        real not null
);

create table company
(
  id      INTEGER
    primary key
  autoincrement,
  name    text not null,
  address text
);

create table client
(
  id        integer
    primary key
  autoincrement,
  fullname  text not null,
  email     text,
  telephone text,
  company_id
    constraint clients_companies_id_fk
    references company
      on delete cascade
);

create table invoice
(
  id             integer
    primary key
  autoincrement,
  client_id      int  not null
    constraint invoices_clients_id_fk
    references client
      on delete cascade,
  created_at     text not null,
  reference_code text
);

create unique index invoices_reference_code_uindex
  on invoice (reference_code);

CREATE TRIGGER insert_invoice_reference_code
  after insert
  on invoice
begin
  update invoice
  set reference_code = printf('I-%d', id + 999)
  where id = new.id;
end;

create table project
(
  id             integer
    primary key
  autoincrement,
  created_at     text not null,
  client_id      int  not null
    constraint projects_clients_id_fk
    references clients (id)
      on delete set null,
  reference_code text,
  title          text
);

create unique index projects_reference_code_uindex
  on project (reference_code);

CREATE TRIGGER insert_project_reference_code
  after insert
  on project
begin
  update project
  set reference_code = printf('P-%d', id + 999)
  where id = new.id;
end;

create table staff
(
  id         integer
    primary key
  autoincrement,
  first_name text not null,
  last_name  text not null,
  job_title  int  not null,
  rate       real not null
);

create table status
(
  id     integer
    primary key
  autoincrement,
  title  text not null,
  colour text not null
);

create table job
(
  id             integer
    primary key
                      autoincrement,
  description    text,
  status_id      int  not null
    constraint jobs_status_id_fk
    references status
      on delete set null,
  assigned_to    int
    constraint jobs_staff_id_fk
    references staff
      on delete set null,
  created_at     text,
  deadline       text,
  estimated_time real not null,
  actual_time    real default 0,
  billable_time  real default 0,
  project_id     int
    constraint jobs_projects_id_fk
    references project
      on delete set null,
  invoice_id     int
    constraint jobs_invoices_id_fk
    references invoice
      on delete set null,
  completed      int  default 0,
  title          text,
  reference_code text
);

CREATE TRIGGER insert_job_reference_code
  after insert
  on job
begin
  update job
  set reference_code = printf('J-%d', id + 999)
  where id = new.id;
end;
