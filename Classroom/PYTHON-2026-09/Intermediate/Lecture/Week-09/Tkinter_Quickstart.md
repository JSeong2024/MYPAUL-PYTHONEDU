# Tkinter 기초 · 버튼으로 표 채우기

**실습 목표** — 버튼을 클릭하면 함수가 실행되고, 준비한 데이터가 표에 표시되도록 만듭니다. 자동화 교안의 준비물 신청 집계 결과를 예시 데이터로 사용합니다.

## 알아둘 개념

| 코드 | 역할 |
|---|---|
| `tk.Tk()` | 기본 창을 만듭니다. |
| `ttk.Button(..., command=show_summary)` | 버튼을 누를 때 실행할 함수를 등록합니다. |
| `ttk.Treeview(..., show="headings")` | 열 제목이 있는 표를 만듭니다. |
| `table.insert("", "end", values=row)` | 표의 마지막에 행 하나를 추가합니다. |
| `root.mainloop()` | 버튼 클릭이나 창 닫기 같은 입력을 기다립니다. |

버튼을 눌렀을 때 호출할 함수는 `command=show_summary`처럼 전달합니다. `command=show_summary()`로 쓰면 버튼을 만드는 순간 함수가 호출되고, 그 반환값이 `command`에 전달됩니다.

## 실습 · 준비물 집계 결과 표시

Windows 터미널에서 `py -m tkinter`를 실행해 작은 창이 열리는지 확인합니다. 아래 코드를 `supplies_viewer.py`로 저장하고 `py supplies_viewer.py`로 실행합니다.

```python
import tkinter as tk
from tkinter import ttk


SAMPLE_ROWS = [
    ("지우개", 1),
    ("연필", 3),
    ("자", 1),
]


def show_summary():
    for item in table.get_children():
        table.delete(item)

    for row in SAMPLE_ROWS:
        table.insert("", "end", values=row)

    status.config(text=f"품목 {len(SAMPLE_ROWS)}종")


root = tk.Tk()
root.title("준비물 집계")

ttk.Button(root, text="집계 결과 표시", command=show_summary).pack(padx=12, pady=8)

table = ttk.Treeview(root, columns=("item", "count"), show="headings", height=6)
table.heading("item", text="품목")
table.heading("count", text="신청 건수")
table.column("item", width=160)
table.column("count", width=90, anchor="e")
table.pack(fill="both", expand=True, padx=12)

status = ttk.Label(root, text="버튼을 눌러 집계 결과를 확인하세요.")
status.pack(anchor="w", padx=12, pady=8)

root.mainloop()
```

`SAMPLE_ROWS`에서 행마다 두 값을 꺼내 표에 넣습니다. 콜백 안에서 이전 행을 먼저 비우므로, 버튼을 여러 번 눌러도 행이 중복되지 않습니다. 상태에 표시되는 **3종**은 품목의 종류 수입니다. 신청 건수를 합하면 5건입니다.

### 확인하기

1. 앱 시작 직후에는 표가 비어 있는지 확인합니다.
2. 버튼을 눌러 지우개, 연필, 자가 각각 한 행에 표시되는지 확인합니다.
3. 버튼을 한 번 더 눌러도 여전히 세 행인지 확인합니다.
4. `SAMPLE_ROWS`에 `("공책", 2)`를 추가한 뒤 다시 실행합니다. 새 행이 나타나고 품목 수가 바뀌는지 확인합니다.

## 파일 관리자 프로젝트에 적용하기

먼저 학생이 작성한 파일 관리 함수의 반환값을 터미널에서 확인합니다. 그다음 화면에 어떤 열이 필요한지 정하고, 버튼을 눌렀을 때 함수의 결과를 표에 전달합니다. 폴더 선택창을 연결하고 싶다면 `filedialog.askdirectory()`를 찾아보세요. **선택을 취소한 경우 이전 화면을 어떻게 유지할지**도 함께 설계합니다.

## 참고

- [Python 공식 문서 · Tkinter](https://docs.python.org/3.13/library/tkinter.html)
- [Python 공식 문서 · Treeview](https://docs.python.org/3.13/library/tkinter.ttk.html#treeview)
- [Python 공식 문서 · 폴더 선택 대화상자](https://docs.python.org/3.13/library/dialog.html#tkinter.filedialog.askdirectory)
