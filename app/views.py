from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post,Category
from .forms import PostForm,CategoryForm
from django.views.generic import TemplateView,ListView,DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
import pandas as pd
import io
import japanize_matplotlib
import base64
import matplotlib.pyplot as plt
import seaborn as sns
from prophet import Prophet


def make_dataframe(data):
    if len(data) == 0:
        return pd.DataFrame()
    else:
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        df["category_name"] = df["category_id"].apply(lambda category_id: Category.objects.get(id=category_id).name if pd.notna(category_id) else np.nan)
        df["month"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m")
        return df
   

def day_sum_graph(df):
    date = df.groupby("date")[["price"]].sum().reset_index()
    plt.figure(figsize = (10,6))
    sns.barplot(
        x = "date",
        y = "price",
        data = date
    )
    plt.title("日別支出_合計グラフ")
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return img_str

def day_mean_graph(df):
    date = df.groupby("date")[["price"]].mean().reset_index()
    plt.figure(figsize = (10,6))
    sns.barplot(
        x = "date",
        y = "price",
        data = date
    )
    plt.title("日別支出_平均グラフ")
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return img_str


def month_sum_graph(df):
    month = df.groupby("month")[["price"]].sum().reset_index()
    plt.figure(figsize = (10,6))
    sns.barplot(
        x = "month",
        y = "price",
        data = month,
        color="orange"
    )
    plt.title("月別支出_合計グラフ")
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return img_str

def month_mean_graph(df):
    month = df.groupby("month")[["price"]].mean().reset_index()
    plt.figure(figsize = (10,6))
    sns.barplot(
        x = "month",
        y = "price",
        data = month,
        color="orange"
    )
    plt.title("月別支出_平均グラフ")
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return img_str


def category_mean_pie_graph(df):
    cg = df.groupby("category_name")[["price"]].mean().reset_index()
    plt.figure(figsize=(6, 6))
    plt.pie(
        cg["price"],
        labels = cg["category_name"],
        )
    plt.title("カテゴリ別支出_平均")
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return img_str 

def category_sum_pie_graph(df):
    cg = df.groupby("category_name")[["price"]].sum().reset_index()
    plt.figure(figsize=(6, 6))
    plt.pie(
        cg["price"],
        labels = cg["category_name"],
        )
    plt.title("カテゴリ別支出_合計")
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return img_str 


def predict_sum_df(data):
    df = pd.DataFrame(data)
    if df.empty:
        return df
    df["date"] = pd.to_datetime(df["date"])
    df = df.groupby("date")["price"].sum().reset_index()
    df.columns = ["ds", "y"]
    return df

def predict_mean_df(data):
    df = pd.DataFrame(data)
    if df.empty:
        return df
    df["date"] = pd.to_datetime(df["date"])
    df = df.groupby("date")["price"].mean().reset_index()
    df.columns = ["ds", "y"]
    return df


def future_predict(df):
    model = Prophet(
        seasonality_mode='multiplicative',
    )
    model.add_seasonality(name='weekly', period=7, fourier_order=3)
    model.fit(df)
    if len(df) <= 10:
        future = model.make_future_dataframe(periods=5,freq="D")
        forecast = model.predict(future)
        forecast = forecast[["ds","yhat"]]
        return forecast
    elif 10 < len(df) <= 30:
        future = model.make_future_dataframe(periods=15,freq="D")
        forecast = model.predict(future)
        forecast = forecast[["ds","yhat"]]
        return forecast
    else:
        future = model.make_future_dataframe(periods=30,freq="D")
        forecast = model.predict(future)
        forecast = forecast[["ds","yhat"]]
        return forecast



def predict_graph(forecast,x,y,title):
    plt.figure(figsize=(10,6))
    sns.lineplot(
        x = x,
        y = y,
        data = forecast
    )
    plt.title(f"AI予測_日別支出{title}")
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return img_str 




class Home(TemplateView):
    template_name = "home.html"

class List(LoginRequiredMixin,ListView):
    model = Post
    template_name = "list.html"
    context_object_name = "objects"

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by('-date')
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        data = Post.objects.filter(user=self.request.user).values()
        df = make_dataframe(data)

        if df.empty: 
            context["day_sum_graph"] = None
            context["month_sum_graph"] = None
            context["day_mean_graph"] = None
            context["month_mean_graph"] = None
            context["category_mean_pie_graph"] = None
            context["category_sum_pie_graph"] = None

        else:
            dsg = day_sum_graph(df)
            context["day_sum_graph"] = dsg
            msg = month_sum_graph(df)
            context["month_sum_graph"] = msg
            dmg = day_mean_graph(df)
            context["day_mean_graph"] = dmg
            mmg = month_mean_graph(df)
            context["month_mean_graph"] = mmg
            cmpg = category_mean_pie_graph(df)
            context["category_mean_pie_graph"] = cmpg
            cspg = category_sum_pie_graph(df)
            context["category_sum_pie_graph"] = cspg
        return context
    

class Detail(LoginRequiredMixin,DetailView):
    model = Post
    template_name = "detail.html"

class Create(LoginRequiredMixin,CreateView):
    model = Post
    form_class = PostForm
    template_name = "create.html"
    success_url = reverse_lazy("list")

    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)

class Update(LoginRequiredMixin,UpdateView):
    model = Post
    form_class = PostForm
    template_name = "update.html"
    success_url = reverse_lazy("list")


class Delete(LoginRequiredMixin,DeleteView):
    model = Post
    template_name = "delete.html"
    success_url = reverse_lazy("list")


class Cate_Create(LoginRequiredMixin,CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "cate_create.html"
    success_url = reverse_lazy("create")

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class Predict(LoginRequiredMixin,ListView):
    model = Post
    template_name = "predict.html"
    
    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by('-date')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        data = Post.objects.filter(user=self.request.user).values()
        sum_df = predict_sum_df(data)
        mean_df = predict_mean_df(data)

        if len(sum_df) >= 5:
            sum_forecast = future_predict(sum_df)
            mean_forecast = future_predict(mean_df)
            sum_forecast.columns = ["日付","日別支出_合計"]
            mean_forecast.columns = ["日付","日別支出_平均"]
            sum_df.columns = ["日付","実際の支出_合計"]
            mean_df.columns = ["日付","実際の支出_平均"]
            sum_forecast = sum_df.merge(sum_forecast,how = "right",on = "日付")
            mean_forecast = mean_df.merge(mean_forecast,how = "right",on = "日付")
            forecast = sum_forecast.merge(mean_forecast,how = "left",on = "日付")
            context["forecast"] = forecast.to_dict(orient="records")
            context["predict_sum_graph"] = predict_graph(forecast,"日付","日別支出_合計","合計")
            context["predict_mean_graph"] = predict_graph(forecast,"日付","日別支出_平均","平均")
        else:
            context["sum_forecast"] = None
            context["mean_forecast"] = None
        return context