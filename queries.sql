SELECT count(EAN)
FROM retail
left join shop on EAN=Reference_id


SELECT count(Reference_id)
FROM shop
where expiry_date  <= date '2021-10-20'