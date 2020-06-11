from plotly.subplots import make_subplots
import plotly.graph_objs as go

NUM_TUBES = [500, 1000, 1500]
FILE_SIZES = [250, 500] #KB
FONT = dict(size=14)
LEGEND_FONT=dict(size=16)
BLUE_LINE = dict(color='#1f77b4') #royalblue
RED_LINE = dict(color='#ef553b', dash='dash')
GREEN_LINE=dict(color='#00cc96', dash='dot')
PURPLE_LINE=dict(color='#9467bd', dash='dashdot')

def totalAcquisition(threeOrgsFileSizeFixed, fiveOrgsFileSizeFixed, threeOrgsNumTubesFixed, fiveOrgsNumTubesFixed):
    fig = make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing= 0.05)

    fig.add_trace(go.Scatter(x=NUM_TUBES, y=threeOrgsFileSizeFixed, mode="lines", name="3-PN", line=BLUE_LINE), row=1, col=1)
    fig.add_trace(go.Scatter(x=NUM_TUBES, y=fiveOrgsFileSizeFixed, mode="lines", name="5-PN", line=RED_LINE), row=1, col=1)
    fig.update_xaxes(title_text="Number of tubes (file size 250 KB)", row=1, col=1, range=[500, 1500], tick0=500, dtick=250)
    fig.update_yaxes(title_text="Total elapsed time (s)", row=1, col=1)

    fig.add_trace(go.Scatter(x=FILE_SIZES, y=threeOrgsNumTubesFixed, mode="lines", name="3-PN", line=BLUE_LINE, showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x=FILE_SIZES, y=fiveOrgsNumTubesFixed, mode="lines", name="5-PN", line=RED_LINE, showlegend=False), row=1, col=2)
    fig.update_xaxes(title_text="Raw data file size (KB, 500 tubes)", row=1, col=2, range=[250, 500])

    #fig.layout.update(legend=dict(y=1.15, orientation="h", font=LEGEND_FONT), width=810)
    fig.layout.update(legend=dict(y=1.15, orientation="h", font=LEGEND_FONT), width=810, annotations=[
        dict(
            x=0, y=-0.3, showarrow=False, text="<b>a)</b> Varying number of tubes. File size is fixed", xref="paper", yref="paper", font=FONT
        ), dict(
            x=1, y=-0.3, showarrow=False, text="<b>b)</b> Varying file size. Number of tubes is fixed", xref="paper", yref="paper", font=FONT
        )
    ])

    config = {'toImageButtonOptions': {
        'filename': f'totalAcq',
    }}
    fig.show(config=config)

def avgAutoAnalysis(threeOrgsFileSizeFixed, fiveOrgsFileSizeFixed, threeOrgsNumTubesFixed, fiveOrgsNumTubesFixed):
    fig = make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing= 0.05)
    
    fig.add_trace(go.Scatter(x=NUM_TUBES, y=threeOrgsFileSizeFixed, mode="lines", name="3-PN", line=BLUE_LINE), row=1, col=1)
    fig.add_trace(go.Scatter(x=NUM_TUBES, y=fiveOrgsFileSizeFixed, mode="lines", name="5-PN", line=RED_LINE), row=1, col=1)
    fig.update_xaxes(title_text="Number of tubes (file size 250 KB)", row=1, col=1, range=[500, 1500], tick0=500, dtick=250)
    fig.update_yaxes(title_text="Average response time (s)", row=1, col=1)

    fig.add_trace(go.Scatter(x=FILE_SIZES, y=threeOrgsNumTubesFixed, mode="lines", name="3-PN", line=BLUE_LINE, showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x=FILE_SIZES, y=fiveOrgsNumTubesFixed, mode="lines", name="5-PN", line=RED_LINE, showlegend=False), row=1, col=2)
    fig.update_xaxes(title_text="Raw data file size (KB, 500 tubes)", row=1, col=2, range=[250, 500])

    #fig.layout.update(legend=dict(y=1.15, orientation="h", font=LEGEND_FONT), width=810)
    fig.layout.update(legend=dict(y=1.15, orientation="h", font=LEGEND_FONT), width=810, annotations=[
        dict(
            x=0, y=-0.3, showarrow=False, text="<b>a)</b> Varying number of tubes. File size is fixed", xref="paper", yref="paper", font=FONT
        ), dict(
            x=1, y=-0.3, showarrow=False, text="<b>b)</b> Varying file size. Number of tubes is fixed", xref="paper", yref="paper", font=FONT
        )
    ])

    config = {'toImageButtonOptions': {
        'filename': f'avgAuto',
    }}
    fig.show(config=config)

def totalAutoAnalysis(threeOrgsFileSizeFixed, fiveOrgsFileSizeFixed, threeOrgsNumTubesFixed, fiveOrgsNumTubesFixed):
    fig = make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing= 0.05)
    
    fig.add_trace(go.Scatter(x=NUM_TUBES, y=threeOrgsFileSizeFixed, mode="lines", name="3-PN", line=BLUE_LINE), row=1, col=1)
    fig.add_trace(go.Scatter(x=NUM_TUBES, y=fiveOrgsFileSizeFixed, mode="lines", name="5-PN", line=RED_LINE), row=1, col=1)
    fig.update_xaxes(title_text="Number of tubes (file size 250 KB)", row=1, col=1, range=[500, 1500], tick0=500, dtick=250)
    fig.update_yaxes(title_text="Total elapsed time (s)", row=1, col=1)

    fig.add_trace(go.Scatter(x=FILE_SIZES, y=threeOrgsNumTubesFixed, mode="lines", name="3-PN", line=BLUE_LINE, showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x=FILE_SIZES, y=fiveOrgsNumTubesFixed, mode="lines", name="5-PN", line=RED_LINE, showlegend=False), row=1, col=2)
    fig.update_xaxes(title_text="Raw data file size (KB, 500 tubes)", row=1, col=2, range=[250, 500])

    #fig.layout.update(legend=dict(y=1.15, orientation="h", font=LEGEND_FONT), width=810)
    fig.layout.update(legend=dict(y=1.15, orientation="h", font=LEGEND_FONT), width=810, annotations=[
        dict(
            x=0, y=-0.3, showarrow=False, text="<b>a)</b> Varying number of tubes. File size is fixed", xref="paper", yref="paper", font=FONT
        ), dict(
            x=1, y=-0.3, showarrow=False, text="<b>b)</b> Varying file size. Number of tubes is fixed", xref="paper", yref="paper", font=FONT
        )
    ])

    config = {'toImageButtonOptions': {
        'filename': f'totalAuto',
    }}
    fig.show(config=config)

def avgAnalysis(threeOrgs10FileSizeFixed, threeOrgs20FileSizeFixed, fiveOrgs10FileSizeFixed, fiveOrgs20FileSizeFixed, threeOrgs10NumTubesFixed, threeOrgs20NumTubesFixed, fiveOrgs10NumTubesFixed, fiveOrgs20NumTubesFixed):
    fig = make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing= 0.05)
    
    fig.add_trace(go.Scatter(x=NUM_TUBES, y=threeOrgs10FileSizeFixed, mode="lines", name="3-PN, 10 analysts per role", line=BLUE_LINE), row=1, col=1)
    fig.add_trace(go.Scatter(x=NUM_TUBES, y=threeOrgs20FileSizeFixed, mode="lines", name="3-PN, 20 analysts per role", line=GREEN_LINE), row=1, col=1)
    fig.add_trace(go.Scatter(x=NUM_TUBES, y=fiveOrgs10FileSizeFixed, mode="lines", name="5-PN, 10 analysts per role", line=RED_LINE), row=1, col=1)
    fig.add_trace(go.Scatter(x=NUM_TUBES, y=fiveOrgs20FileSizeFixed, mode="lines", name="5-PN, 20 analysts per role", line=PURPLE_LINE), row=1, col=1)
    fig.update_xaxes(title_text="Number of tubes (file size 250 KB)", row=1, col=1, range=[500, 1500], tick0=500, dtick=250)
    fig.update_yaxes(title_text="Average response time (s)", row=1, col=1)

    fig.add_trace(go.Scatter(x=FILE_SIZES, y=threeOrgs10NumTubesFixed, mode="lines", name="3-PN, 10 analysts per role", line=BLUE_LINE, showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x=FILE_SIZES, y=threeOrgs20NumTubesFixed, mode="lines", name="3-PN, 20 analysts per role", line=GREEN_LINE, showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x=FILE_SIZES, y=fiveOrgs10NumTubesFixed, mode="lines", name="5-PN, 10 analysts per role", line=RED_LINE, showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x=FILE_SIZES, y=fiveOrgs20NumTubesFixed, mode="lines", name="5-PN, 20 analysts per role", line=PURPLE_LINE, showlegend=False), row=1, col=2)
    fig.update_xaxes(title_text="Raw data file size (KB, 500 tubes)", row=1, col=2, range=[250, 500])

    #fig.layout.update(legend=dict(y=1.25, orientation="h", font=LEGEND_FONT), width=810)
    fig.layout.update(legend=dict(y=1.25, orientation="h", font=LEGEND_FONT), width=810, annotations=[
        dict(
            x=0, y=-0.3, showarrow=False, text="<b>a)</b> Varying number of tubes. File size is fixed", xref="paper", yref="paper", font=FONT
        ), dict(
            x=1, y=-0.3, showarrow=False, text="<b>b)</b> Varying file size. Number of tubes is fixed", xref="paper", yref="paper", font=FONT
        )
    ])

    config = {'toImageButtonOptions': {
        'filename': f'avgAnalysis',
    }}
    fig.show(config=config)

def totalAnalysis(threeOrgs10FileSizeFixed, threeOrgs20FileSizeFixed, fiveOrgs10FileSizeFixed, fiveOrgs20FileSizeFixed, threeOrgs10NumTubesFixed, threeOrgs20NumTubesFixed, fiveOrgs10NumTubesFixed, fiveOrgs20NumTubesFixed):
    fig = make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing= 0.05)
    
    fig.add_trace(go.Scatter(x=NUM_TUBES, y=threeOrgs10FileSizeFixed, mode="lines", name="3-PN, 10 analysts per role", line=BLUE_LINE), row=1, col=1)
    fig.add_trace(go.Scatter(x=NUM_TUBES, y=threeOrgs20FileSizeFixed, mode="lines", name="3-PN, 20 analysts per role", line=GREEN_LINE), row=1, col=1)
    fig.add_trace(go.Scatter(x=NUM_TUBES, y=fiveOrgs10FileSizeFixed, mode="lines", name="5-PN, 10 analysts per role", line=RED_LINE), row=1, col=1)
    fig.add_trace(go.Scatter(x=NUM_TUBES, y=fiveOrgs20FileSizeFixed, mode="lines", name="5-PN, 20 analysts per role", line=PURPLE_LINE), row=1, col=1)
    fig.update_xaxes(title_text="Number of tubes (file size 250 KB)", row=1, col=1, range=[500, 1500], tick0=500, dtick=250)
    fig.update_yaxes(title_text="Total elapsed time (s)", row=1, col=1)

    fig.add_trace(go.Scatter(x=FILE_SIZES, y=threeOrgs10NumTubesFixed, mode="lines", name="3-PN, 10 analysts per role", line=BLUE_LINE, showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x=FILE_SIZES, y=threeOrgs20NumTubesFixed, mode="lines", name="3-PN, 20 analysts per role", line=GREEN_LINE, showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x=FILE_SIZES, y=fiveOrgs10NumTubesFixed, mode="lines", name="5-PN, 10 analysts per role", line=RED_LINE, showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x=FILE_SIZES, y=fiveOrgs20NumTubesFixed, mode="lines", name="5-PN, 20 analysts per role", line=PURPLE_LINE, showlegend=False), row=1, col=2)
    fig.update_xaxes(title_text="Raw data file size (KB, 500 tubes)", row=1, col=2, range=[250, 500])

    #fig.layout.update(legend=dict(y=1.25, orientation="h", font=LEGEND_FONT), width=810)
    fig.layout.update(legend=dict(y=1.25, orientation="h", font=LEGEND_FONT), width=810, annotations=[
        dict(
            x=0, y=-0.3, showarrow=False, text="<b>a)</b> Varying number of tubes. File size is fixed", xref="paper", yref="paper", font=FONT
        ), dict(
            x=1, y=-0.3, showarrow=False, text="<b>b)</b> Varying file size. Number of tubes is fixed", xref="paper", yref="paper", font=FONT
        )
    ])

    config = {'toImageButtonOptions': {
        'filename': f'totalAnalysis',
    }}
    fig.show(config=config)