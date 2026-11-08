"""Mini 02: completed order revenue (not canceled order quantity)."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from core.utils import arguments,load,numeric,save,figure_start,finish

def run():
    args=arguments('Retail Sales Report','mini_02_retail_report')
    df=load(args.data/'orders.csv',['order_id','date','category','quantity','unit_price_krw','status'])
    if df.order_id.duplicated().any():raise ValueError('duplicate order_id')
    df['quantity']=numeric(df.quantity);df['unit_price_krw']=numeric(df.unit_price_krw)
    if df[['quantity','unit_price_krw']].isna().any().any() or (df[['quantity','unit_price_krw']]<0).any().any():raise ValueError('invalid amount')
    paid=df[df.status.eq('completed')].copy();paid['revenue_krw']=paid.quantity*paid.unit_price_krw
    summary=paid.groupby('category',as_index=False).agg(orders=('order_id','nunique'),revenue_krw=('revenue_krw','sum'))
    summary=summary.sort_values('revenue_krw',ascending=False)
    save(summary,args.output/'category_revenue.csv')
    fig,ax=figure_start();ax.bar(summary.category,summary.revenue_krw)
    ax.set_ylabel('Revenue (KRW)');ax.set_xlabel('Category');ax.set_title('Completed sales by category')
    finish(fig,args.output/'report.png');print(f'PASS mini_02: {len(paid)} completed orders')
if __name__=='__main__':run()
