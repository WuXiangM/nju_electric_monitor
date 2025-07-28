import pandas as pd
from flask import Flask, render_template_string
import os
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__)

CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'electricity_data.csv')

TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-cn">
<head>
    <meta charset="UTF-8">
    <title>南京大学电费监控面板</title>
    <style>
        body { font-family: 'Segoe UI', '微软雅黑', Arial, sans-serif; margin: 0; background: linear-gradient(120deg, #0f2027, #2c5364 80%); min-height: 100vh; }
        .container { max-width: 950px; margin: 48px auto; background: rgba(20, 30, 48, 0.95); border-radius: 18px; box-shadow: 0 6px 32px #0ff2ff33; padding: 38px 44px; }
        h1 { text-align: center; color: #00eaff; margin-bottom: 12px; letter-spacing: 2px; text-shadow: 0 2px 8px #0ff2ff44; }
        .desc { text-align: center; color: #b2e6ff; margin-bottom: 32px; font-size: 1.1em; }
        table { border-collapse: collapse; width: 100%; margin: 36px 0 0 0; background: rgba(10, 20, 40, 0.95); border-radius: 10px; overflow: hidden; }
        th, td { border: 1px solid #1de9b6; padding: 12px 18px; text-align: center; color: #fff; }
        th { background: linear-gradient(90deg, #00eaff 60%, #1de9b6 100%); color: #fff; font-weight: bold; letter-spacing: 1px; }
        td { color: #fff; }
        caption { font-size: 1.25em; margin-bottom: 12px; font-weight: bold; color: #00eaff; }
        tr:nth-child(even) { background: rgba(0, 234, 255, 0.07); }
        tr:nth-child(odd) { background: rgba(29, 233, 182, 0.07); }
        .chart-block { text-align: center; margin: 36px 0 10px 0; }
        .chart-block iframe, .chart-block div { border-radius: 12px; box-shadow: 0 2px 18px #00eaff33; background: #fff; }
        .reload-btn {
            display: inline-block;
            margin: 0 0 18px 0;
            padding: 8px 22px;
            font-size: 1em;
            color: #00eaff;
            background: linear-gradient(90deg, #232526 0%, #1de9b6 100%);
            border: none;
            border-radius: 8px;
            box-shadow: 0 2px 8px #00eaff33;
            cursor: pointer;
            transition: background 0.2s, color 0.2s;
        }
        .reload-btn:hover {
            background: linear-gradient(90deg, #1de9b6 0%, #00eaff 100%);
            color: #232526;
        }
        @media (max-width: 800px) {
            .container { padding: 10px; }
            table, th, td { font-size: 13px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>南京大学电费监控面板</h1>
        <div class="desc">展示最近电费数据及变化趋势</div>
        <div class="chart-block">
            <button class="reload-btn" onclick="location.reload()">更新/重新加载</button>
            {{ plot_div|safe }}
        </div>
        <table>
            <caption>电费数据明细</caption>
            <tr>
                <th>时间</th>
                <th>剩余电量</th>
                <th>单位</th>
            </tr>
            {% for row in rows %}
            <tr>
                <td>{{ row['time'] }}</td>
                <td>{{ row['num'] }}</td>
                <td>{{ row['unit'] }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    df = pd.read_csv(CSV_PATH)
    df['time'] = pd.to_datetime(df['time'])
    df_sorted = df.sort_values('time')
    # 生成plotly曲线，科技感配色
    trace = go.Scatter(
        x=df_sorted['time'],
        y=df_sorted['num'],
        mode='lines+markers',
        marker=dict(color='#00eaff', size=9, line=dict(width=2, color='#1de9b6')),
        line=dict(width=3, color='#1de9b6'),
        hovertemplate='时间: %{x|%Y-%m-%d %H:%M:%S}<br>剩余电量: %{y} 度',
        name='剩余电量',
        text=None,
        showlegend=False
    )
    layout = go.Layout(
        title=dict(text='电费变化曲线', x=0.5, font=dict(family='Segoe UI,微软雅黑', size=20, color='#00eaff')),
        xaxis=dict(
            title='时间', 
            tickformat='%Y-%m-%d %H:%M', 
            tickangle=30, 
            showgrid=True, 
            gridcolor='rgba(29,233,182,0.15)', 
            gridwidth=1,
            griddash='dash',
            color='#b2e6ff', 
            tickfont=dict(color='#b2e6ff')
        ),
        yaxis=dict(
            title='剩余电量 (度)', 
            showgrid=True, 
            gridcolor='rgba(29,233,182,0.15)', 
            gridwidth=1,
            griddash='dash',
            color='#b2e6ff', 
            tickfont=dict(color='#b2e6ff')
        ),
        hovermode='x unified',
        plot_bgcolor='rgba(10,20,40,0.95)',
        paper_bgcolor='rgba(20,30,48,0.95)',
        margin=dict(l=60, r=30, t=60, b=60),
        font=dict(family='Segoe UI,微软雅黑', size=14, color='#b2e6ff')
    )
    fig = go.Figure(data=[trace], layout=layout)
    plot_div = pio.to_html(fig, full_html=False, include_plotlyjs='cdn', config={
        'displayModeBar': True,
        'scrollZoom': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['select2d', 'lasso2d', 'autoScale2d', 'resetScale2d', 'toggleSpikelines']
    })
    # 格式化时间为字符串用于表格展示
    df_sorted['time'] = df_sorted['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    rows = df_sorted.to_dict(orient="records")
    return render_template_string(TEMPLATE, rows=rows, plot_div=plot_div)

if __name__ == "__main__":
    app.run(debug=True)
