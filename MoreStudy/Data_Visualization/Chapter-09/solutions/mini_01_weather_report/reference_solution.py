"""Mini 01: one-station static weather report."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from core.utils import arguments,load,numeric,save,figure_start,finish

def run():
    args=arguments('Weather Visualization Report','mini_01_weather_report')
    df=load(args.data/'weather_daily.csv',['date','temperature_c','precipitation_mm'])
    if df.date.duplicated().any():raise ValueError('date must be unique')
    df['temperature_c']=numeric(df.temperature_c)
    df['precipitation_mm']=numeric(df.precipitation_mm)
    if df[['temperature_c','precipitation_mm']].isna().any().any() or df.precipitation_mm.lt(0).any():raise ValueError('invalid weather measurements')
    df=df.sort_values('date')
    save(df,args.output/'daily_summary.csv')
    fig,ax=figure_start()
    x=list(range(len(df)))
    ax.plot(x,df.temperature_c,marker='o',label='Temperature (°C)')
    ax.set_xlabel('Observation date (KST)'); ax.set_ylabel('Temperature (°C)')
    ax.set_xticks(x[::max(1,len(x)//7)],[df.date.iloc[i][5:] for i in x[::max(1,len(x)//7)]])
    ax2=ax.twinx();ax2.bar(x,df.precipitation_mm,alpha=.22,label='Rain (mm)');ax2.set_ylabel('Precipitation (mm)')
    ax.set_title('Daily weather: temperature and precipitation')
    finish(fig,args.output/'report.png')
    print(f'PASS mini_01: {len(df)} days')
if __name__=='__main__':run()
