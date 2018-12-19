
MONTH_LIST as (
  select (rownum + MIN)/12 || TO_CHAR((rownum + MIN)%12,'00')
  from ALL
  where rownum < xx
),
ADD as (
  select * from L
  union
  select kensa_no, taisho_mei, month 
  from keikaku_mst, month_list
  where not exists (select 1 from L where kensa_no = kensa_no and taisho_mei = taisyo_mei and month = month)
),
ruikei as (
  select *
    sum(xx) over (partition by xxx order by xxx, xxx) as x,
  from add
)

