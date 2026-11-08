"""Mini 02: Regression Baseline과 실제 예측 모델 비교."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split, KFold, cross_validate
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from common import ROOT, ETA_FEATURES, load_delivery


def metrics(y_true, predicted):
    mse=float(mean_squared_error(y_true,predicted))
    return {"mae":float(mean_absolute_error(y_true,predicted)),
            "mse":mse, "rmse":float(np.sqrt(mse)),
            "r2":float(r2_score(y_true,predicted))}


def evaluate(df):
    X,y=df[ETA_FEATURES].to_numpy(),df.actual_minutes.to_numpy()
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,random_state=42)
    dummy=DummyRegressor(strategy="median").fit(Xtr,ytr)
    model=make_pipeline(StandardScaler(),Ridge(alpha=3.0)).fit(Xtr,ytr)
    baseline=metrics(yte,dummy.predict(Xte))
    pred=model.predict(Xte)
    fitted=metrics(yte,pred)
    cv=KFold(n_splits=5,shuffle=True,random_state=42)
    scores=cross_validate(make_pipeline(StandardScaler(),Ridge(alpha=3.0)),Xtr,ytr,
                          cv=cv,scoring={"mae":"neg_mean_absolute_error","r2":"r2"})
    return {"baseline":baseline,"model":fitted,"actual":yte,"predicted":pred,
            "cv_mae":-scores["test_mae"],"cv_r2":scores["test_r2"]}


def plot_result(r,output=ROOT / "outputs/mini_02_eta_regression.png"):
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    fig,axs=plt.subplots(1,2,figsize=(10,4))
    axs[0].scatter(r["actual"],r["predicted"],alpha=.65,s=18)
    bounds=[min(r["actual"].min(),r["predicted"].min()),max(r["actual"].max(),r["predicted"].max())]
    axs[0].plot(bounds,bounds,linestyle="--",color="gray")
    axs[0].set(xlabel="Actual minutes",ylabel="Predicted minutes",title="Delivery time prediction")
    residual=r["actual"]-r["predicted"]
    axs[1].scatter(r["predicted"],residual,alpha=.65,s=18)
    axs[1].axhline(0,color="gray",linestyle="--")
    axs[1].set(xlabel="Predicted minutes",ylabel="Residual (actual - predicted)",title="Residual check")
    fig.tight_layout();fig.savefig(output,dpi=150);plt.close(fig)
    return output


def main():
    r=evaluate(load_delivery())
    print("Median baseline:",r["baseline"])
    print("Ridge:",r["model"])
    print(f"Train CV MAE: {r['cv_mae'].mean():.3f} ± {r['cv_mae'].std():.3f}")
    print("Saved:",plot_result(r))

if __name__=="__main__":main()
