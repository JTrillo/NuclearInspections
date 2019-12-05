from plotly.subplots import make_subplots
import plotly.graph_objs as go

NUM_TUBES = [500, 1000, 1500]
FILE_SIZES = [250, 500] #KB

def totalAcquisition(threeOrgsFileSizeFixed, fiveOrgsFileSizeFixed, threeOrgsNumTubesFixed, fiveOrgsNumTubesFixed):
    fig = make_subplots(rows=1, cols=2, shared_yaxes=True)

    fig.add_trace(go.Scatter(x=NUM_TUBES, y=threeOrgsFileSizeFixed, mode="lines", name="3 Orgs net (file size fixed)"), row=1, col=1)
    fig.add_trace(go.Scatter(x=NUM_TUBES, y=fiveOrgsFileSizeFixed, mode="lines", name="5 Orgs net (file size fixed)", line=dict(dash='dash')), row=1, col=1)
    fig.update_xaxes(title_text="Number of tubes", row=1, col=1, range=[500, 1500], tick0=500, dtick=250)
    fig.update_yaxes(title_text="Total elapsed time (s)", row=1, col=1)

    fig.add_trace(go.Scatter(x=FILE_SIZES, y=threeOrgsNumTubesFixed, mode="lines", name="3 Orgs net (file size fixed)"), row=1, col=2)
    fig.add_trace(go.Scatter(x=FILE_SIZES, y=fiveOrgsNumTubesFixed, mode="lines", name="5 Orgs net (file size fixed)", line=dict(dash='dash')), row=1, col=2)
    fig.update_xaxes(title_text="Raw data file size (KB)", row=1, col=2, range=[250, 500])

    fig.layout.update(showlegend=False, width=1000)

    config = {'toImageButtonOptions': {
        'filename': f'totalAcq',
    }}
    fig.show(config=config)

def avgAutoAnalysis(threeOrgsFileSizeFixed, fiveOrgsFileSizeFixed, threeOrgsNumTubesFixed, fiveOrgsNumTubesFixed):
    fig = make_subplots(rows=1, cols=2, shared_yaxes=True)
    
    fig.add_trace(go.Scatter(x=NUM_TUBES, y=threeOrgsFileSizeFixed, mode="lines", name="3 Orgs net (file size fixed)"), row=1, col=1)
    fig.add_trace(go.Scatter(x=NUM_TUBES, y=fiveOrgsFileSizeFixed, mode="lines", name="5 Orgs net (file size fixed)", line=dict(dash='dash')), row=1, col=1)
    fig.update_xaxes(title_text="Number of tubes", row=1, col=1, range=[500, 1500], tick0=500, dtick=250)
    fig.update_yaxes(title_text="Average response time (s)", row=1, col=1)

    fig.add_trace(go.Scatter(x=FILE_SIZES, y=threeOrgsNumTubesFixed, mode="lines", name="3 Orgs net (file size fixed)"), row=1, col=2)
    fig.add_trace(go.Scatter(x=FILE_SIZES, y=fiveOrgsNumTubesFixed, mode="lines", name="5 Orgs net (file size fixed)", line=dict(dash='dash')), row=1, col=2)
    fig.update_xaxes(title_text="Raw data file size (KB)", row=1, col=2, range=[250, 500])

    fig.layout.update(showlegend=False, width=1000)

    config = {'toImageButtonOptions': {
        'filename': f'avgAuto',
    }}
    fig.show(config=config)

def totalAutoAnalysis(threeOrgsFileSizeFixed, fiveOrgsFileSizeFixed, threeOrgsNumTubesFixed, fiveOrgsNumTubesFixed):
    fig = make_subplots(rows=1, cols=2, shared_yaxes=True)
    
    fig.add_trace(go.Scatter(x=NUM_TUBES, y=threeOrgsFileSizeFixed, mode="lines", name="3 Orgs net (file size fixed)"), row=1, col=1)
    fig.add_trace(go.Scatter(x=NUM_TUBES, y=fiveOrgsFileSizeFixed, mode="lines", name="5 Orgs net (file size fixed)", line=dict(dash='dash')), row=1, col=1)
    fig.update_xaxes(title_text="Number of tubes", row=1, col=1, range=[500, 1500], tick0=500, dtick=250)
    fig.update_yaxes(title_text="Total elapsed time (s)", row=1, col=1)

    fig.add_trace(go.Scatter(x=FILE_SIZES, y=threeOrgsNumTubesFixed, mode="lines", name="3 Orgs net (file size fixed)"), row=1, col=2)
    fig.add_trace(go.Scatter(x=FILE_SIZES, y=fiveOrgsNumTubesFixed, mode="lines", name="5 Orgs net (file size fixed)", line=dict(dash='dash')), row=1, col=2)
    fig.update_xaxes(title_text="Raw data file size (KB)", row=1, col=2, range=[250, 500])

    fig.layout.update(showlegend=False, width=1000)

    config = {'toImageButtonOptions': {
        'filename': f'totalAuto',
    }}
    fig.show(config=config)

def avgAnalysis(threeOrgs10FileSizeFixed, threeOrgs20FileSizeFixed, fiveOrgs10FileSizeFixed, fiveOrgs20FileSizeFixed, threeOrgs10NumTubesFixed, threeOrgs20NumTubesFixed, fiveOrgs10NumTubesFixed, fiveOrgs20NumTubesFixed):
    fig = make_subplots(rows=1, cols=2, shared_yaxes=True)
    
    fig.add_trace(go.Scatter(x=NUM_TUBES, y=threeOrgs10FileSizeFixed, mode="lines", name="3 Orgs net 10 analysts per role (file size fixed)"), row=1, col=1)
    fig.add_trace(go.Scatter(x=NUM_TUBES, y=threeOrgs20FileSizeFixed, mode="lines", name="3 Orgs net 20 analysts per role (file size fixed)", line=dict(dash='dash')), row=1, col=1)
    fig.add_trace(go.Scatter(x=NUM_TUBES, y=fiveOrgs10FileSizeFixed, mode="lines", name="5 Orgs net 10 analysts per role (file size fixed)", line=dict(dash='dot')), row=1, col=1)
    fig.add_trace(go.Scatter(x=NUM_TUBES, y=fiveOrgs20FileSizeFixed, mode="lines+markers", name="5 Orgs net 20 analysts per role (file size fixed)"), row=1, col=1)
    fig.update_xaxes(title_text="Number of tubes", row=1, col=1, range=[500, 1500], tick0=500, dtick=250)
    fig.update_yaxes(title_text="Average response time (s)", row=1, col=1)

    fig.add_trace(go.Scatter(x=FILE_SIZES, y=threeOrgs10NumTubesFixed, mode="lines", name="3 Orgs net 10 analysts per role (file size fixed)"), row=1, col=2)
    fig.add_trace(go.Scatter(x=FILE_SIZES, y=threeOrgs20NumTubesFixed, mode="lines", name="3 Orgs net 20 analysts per role (file size fixed)", line=dict(dash='dash')), row=1, col=2)
    fig.add_trace(go.Scatter(x=FILE_SIZES, y=fiveOrgs10NumTubesFixed, mode="lines", name="5 Orgs net 10 analysts per role (file size fixed)", line=dict(dash='dot')), row=1, col=2)
    fig.add_trace(go.Scatter(x=FILE_SIZES, y=fiveOrgs20NumTubesFixed, mode="lines+markers", name="5 Orgs net 20 analysts per role (file size fixed)"), row=1, col=2)
    fig.update_xaxes(title_text="Raw data file size (KB)", row=1, col=2, range=[250, 500])

    fig.layout.update(showlegend=False, width=1000)

    config = {'toImageButtonOptions': {
        'filename': f'avgAnalysis',
    }}
    fig.show(config=config)

def totalAnalysis(threeOrgs10FileSizeFixed, threeOrgs20FileSizeFixed, fiveOrgs10FileSizeFixed, fiveOrgs20FileSizeFixed, threeOrgs10NumTubesFixed, threeOrgs20NumTubesFixed, fiveOrgs10NumTubesFixed, fiveOrgs20NumTubesFixed):
    fig = make_subplots(rows=1, cols=2, shared_yaxes=True)
    
    fig.add_trace(go.Scatter(x=NUM_TUBES, y=threeOrgs10FileSizeFixed, mode="lines", name="3 Orgs net 10 analysts per role (file size fixed)"), row=1, col=1)
    fig.add_trace(go.Scatter(x=NUM_TUBES, y=threeOrgs20FileSizeFixed, mode="lines", name="3 Orgs net 20 analysts per role (file size fixed)", line=dict(dash='dash')), row=1, col=1)
    fig.add_trace(go.Scatter(x=NUM_TUBES, y=fiveOrgs10FileSizeFixed, mode="lines", name="5 Orgs net 10 analysts per role (file size fixed)", line=dict(dash='dot')), row=1, col=1)
    fig.add_trace(go.Scatter(x=NUM_TUBES, y=fiveOrgs20FileSizeFixed, mode="lines+markers", name="5 Orgs net 20 analysts per role (file size fixed)"), row=1, col=1)
    fig.update_xaxes(title_text="Number of tubes", row=1, col=1, range=[500, 1500], tick0=500, dtick=250)
    fig.update_yaxes(title_text="Total elapsed time (s)", row=1, col=1)

    fig.add_trace(go.Scatter(x=FILE_SIZES, y=threeOrgs10NumTubesFixed, mode="lines", name="3 Orgs net 10 analysts per role (file size fixed)"), row=1, col=2)
    fig.add_trace(go.Scatter(x=FILE_SIZES, y=threeOrgs20NumTubesFixed, mode="lines", name="3 Orgs net 20 analysts per role (file size fixed)", line=dict(dash='dash')), row=1, col=2)
    fig.add_trace(go.Scatter(x=FILE_SIZES, y=fiveOrgs10NumTubesFixed, mode="lines", name="5 Orgs net 10 analysts per role (file size fixed)", line=dict(dash='dot')), row=1, col=2)
    fig.add_trace(go.Scatter(x=FILE_SIZES, y=fiveOrgs20NumTubesFixed, mode="lines+markers", name="5 Orgs net 20 analysts per role (file size fixed)"), row=1, col=2)
    fig.update_xaxes(title_text="Raw data file size (KB)", row=1, col=2, range=[250, 500])

    fig.layout.update(showlegend=False, width=1000)

    config = {'toImageButtonOptions': {
        'filename': f'totalAnalysis',
    }}
    fig.show(config=config)