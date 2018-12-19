
```

L as (
),
MONTH_LIST_SEQ as (
  select level n from dual connect by level <= MONTHS_BETWEEN(TO_DATE(@@@END@@@, 'YYYYMM'), TO_DATE(@@@START@@@, 'YYYYMM')) + 1
),
MONTH_LIST as (
  select TO_CHAR(add_months( TO_DATE(@@@START@@@, 'YYYYMM'), n-1), 'YYYYMM') MON,
  from MONTH_LIST_SEQ
),
L2 as ( -- 指定期間内の全月のレコードを追加
  select * from L
  union
  select K.kensa_no, K.taisho_mei, P.hinsyu, M.month, 0, 0, 0
  FROM keikaku_mst K
  INNER JOIN MONTH_LIST M
  LEFT OUTER JOIN xxx P on xx = xx
  where not exists (select 1 from L where kensa_no = kensa_no and taisho_mei = taisyo_mei and month = month)
),
L3 as ( -- 累計値を追加
  select *
    sum(xx) over (partition by xxx order by xxx, xxx) as x,
  from L2
)

```
