"""개발 환경에서 Streamlit 패키지가 없는 경우에만 쓰는 기초 UI 코드 경로 확인.

본 테스트는 실제 Streamlit의 위젯·브라우저 호환성이나 AppTest 검증을 대체하지 않습니다.
기본 위젯값에서 Python 코드가 예외 없이 계산 로직을 통과하는지만 확인합니다.
"""
from pathlib import Path
import contextlib
import runpy
import sys
from types import SimpleNamespace

ROOT=Path(__file__).resolve().parents[1]

class StopRun(Exception):pass

class State(dict):
    def __getattr__(self,key):
        if key in self:return self[key]
        raise AttributeError(key)
    def __setattr__(self,key,val):self[key]=val

class Page:
    def __init__(self,func,**kwargs):self.func=func
    def run(self):self.func()

class MockStreamlit:
    def __init__(self):
        self.session_state=State();self.query_params={};self.sidebar=self
    def __enter__(self):return self
    def __exit__(self,*args):return False
    def __getattr__(self,name):
        if name in ('cache_data','cache_resource'):
            return lambda function=None,**opts: function if function is not None else (lambda f:f)
        if name in ('title','header','subheader','write','caption','info','warning','error','success','metric','dataframe','plotly_chart','pyplot','json','markdown','bar_chart','download_button','set_page_config'):
            if name=='plotly_chart':return lambda *args,**kwargs:SimpleNamespace(selection=SimpleNamespace(points=[]))
            return lambda *args,**kwargs:None
        if name in ('form','expander','container'):
            return lambda *args,**kwargs:self
        if name in ('columns','tabs'):
            return lambda arg,*args,**kwargs:[self for _ in range(arg if isinstance(arg,int) else len(arg))]
        if name=='selectbox':
            return lambda label,options,index=0,**kwargs:list(options)[index]
        if name=='multiselect':
            def multi(label,options,default=None,key=None,**kwargs):
                if key in self.session_state:return self.session_state[key]
                result=list(default) if default is not None else []
                if key:self.session_state[key]=result
                return result
            return multi
        if name=='date_input':return lambda *args,**kwargs:kwargs.get('value', args[1] if len(args)>1 else None)
        if name=='slider':return lambda label,*args,**kwargs:kwargs.get('value',args[2] if len(args)>=3 else args[0])
        if name in ('text_input',):return lambda label,value='',**kwargs:value
        if name=='button':return lambda *args,**kwargs:False
        if name=='form_submit_button':return lambda *args,**kwargs:False
        if name=='file_uploader':return lambda *args,**kwargs:None
        if name=='data_editor':return lambda data,*args,**kwargs:data.copy()
        if name=='stop':return lambda:(_ for _ in ()).throw(StopRun())
        if name=='Page':return lambda function,**kwargs:Page(function,**kwargs)
        if name=='navigation':return lambda pages,**kwargs:pages[0]
        raise AttributeError(f'MockStreamlit does not implement {name}')

def smoke():
    paths=sorted((ROOT/'examples').glob('[0-9][0-9]_*.py'))
    paths+=sorted((ROOT/'solutions'/'practice').glob('[0-9][0-9]_*.py'))
    paths+=sorted((ROOT/'solutions').glob('mini_*/solution.py'))
    paths+=sorted((ROOT/'solutions').glob('advanced_*/reference_solution.py'))
    assert len(paths)==48,len(paths)
    ok=[]
    old=sys.modules.get('streamlit')
    try:
        for path in paths:
            sys.modules['streamlit']=MockStreamlit()
            try:runpy.run_path(str(path),run_name='__main__')
            except StopRun:pass
            except Exception as exc:
                raise RuntimeError(f'Fail: {path.relative_to(ROOT)}: {exc}') from exc
            ok.append(path.relative_to(ROOT))
    finally:
        if old is None:sys.modules.pop('streamlit',None)
        else:sys.modules['streamlit']=old
    print(f'Mock UI Python-flow smoke: {len(ok)} files completed (not actual Streamlit runtime).')

if __name__=='__main__':smoke()
