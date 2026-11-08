"""Advanced 02: segment purchase participation, correct population denominators."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import pandas as pd
from core.utils import arguments,load,numeric,save,figure_start,finish,iso_day

def extras(p):
 p.add_argument('--start',default='2026-10-01');p.add_argument('--end',default='2026-10-28')
def run():
 args=arguments('Customer Behavior Analysis','advanced_02_customer_behavior',extras)
 customers=load(args.data/'customers.csv',['customer_id','segment','joined_on'])
 if customers.customer_id.duplicated().any():raise ValueError('duplicate customer reference')
 orders=load(args.data/'orders.csv',['order_id','customer_id','ordered_on','amount_krw','status'])
 orders['amount_krw']=numeric(orders.amount_krw)
 bad=orders.order_id.duplicated(keep=False)|~orders.customer_id.isin(customers.customer_id)|orders.amount_krw.isna()|orders.amount_krw.lt(0)|~orders.status.isin(['paid','refunded'])|pd.to_datetime(orders.ordered_on,errors='coerce').isna()
 audit=orders.loc[bad,['order_id','customer_id']].copy();audit['reason']='invalid_order';save(audit,args.output/'audit.csv')
 orders=orders.loc[~bad];orders=iso_day(orders.rename(columns={'ordered_on':'local_date'}),start=args.start,end=args.end)
 paid=orders[orders.status.eq('paid')]
 buyers=paid.groupby('customer_id',as_index=False).agg(spend_krw=('amount_krw','sum'),paid_orders=('order_id','size')).merge(customers,on='customer_id',how='left')
 base=customers.groupby('segment',as_index=False).agg(registered_customers=('customer_id','nunique'))
 sub=buyers.groupby('segment',as_index=False).agg(buyers=('customer_id','nunique'),revenue_krw=('spend_krw','sum'),paid_orders=('paid_orders','sum'))
 summary=base.merge(sub,on='segment',how='left').fillna(0)
 summary['participation_pct']=100*summary.buyers/summary.registered_customers
 summary['revenue_per_buyer_krw']=summary.revenue_krw/summary.buyers.replace(0,float('nan'))
 save(summary,args.output/'segment_summary.csv')
 fig,ax=figure_start();ax.bar(summary.segment,summary.participation_pct);ax.set_ylim(0,100)
 ax.set_ylabel('Registered customers who paid (%)');ax.set_xlabel('Segment');ax.set_title('Purchase participation by registered segment')
 finish(fig,args.output/'dashboard.png');print(f'PASS advanced_02: {len(paid)} paid orders')
if __name__=='__main__':run()
