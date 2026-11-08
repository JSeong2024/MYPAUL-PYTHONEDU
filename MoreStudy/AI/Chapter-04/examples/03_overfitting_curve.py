"""모델 복잡도와 CV 오차를 비교한다. 테스트 데이터는 모델 선택에 사용하지 않는다."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]

def run(df):
    X=df[["input_x"]].to_numpy()
    y=df.target_y.to_numpy()
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.25,random_state=42)
    cv=KFold(n_splits=5,shuffle=True,random_state=42)
    degrees=[1,3,5,9,14,24]
    cv_rmse=[]
    for d in degrees:
        estimator=make_pipeline(PolynomialFeatures(d,include_bias=False),StandardScaler(),Ridge(alpha=.01))
        scores=cross_val_score(estimator,X_train,y_train,cv=cv,scoring="neg_mean_squared_error")
        cv_rmse.append(float(np.sqrt(-scores).mean()))
    selected=degrees[int(np.argmin(cv_rmse))]
    fitted=make_pipeline(PolynomialFeatures(selected,include_bias=False),StandardScaler(),Ridge(alpha=.01))
    fitted.fit(X_train,y_train)
    test_rmse=float(np.sqrt(((y_test-fitted.predict(X_test))**2).mean()))
    return degrees,cv_rmse,selected,test_rmse


def plot(degrees,errors,output=ROOT/"outputs/example_03_overfitting_curve.png"):
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    fig,ax=plt.subplots(figsize=(7.2,4.2))
    ax.plot(degrees,errors,marker="o")
    ax.set(xlabel="Polynomial degree",ylabel="Mean CV RMSE",title="Model complexity and validation error")
    fig.tight_layout();fig.savefig(output,dpi=150);plt.close(fig)
    return output


def main():
    result=run(pd.read_csv(ROOT/"data/curve_measurements.csv"))
    for degree,score in zip(result[0],result[1]):print(f"Degree {degree:2d}: CV RMSE {score:.3f}")
    print(f"Selected degree={result[2]}, held-out test RMSE={result[3]:.3f}")
    print("Saved:",plot(result[0],result[1]))

if __name__=="__main__":main()
