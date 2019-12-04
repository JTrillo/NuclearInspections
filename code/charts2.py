import plotly.graph_objs as go

FILE_SIZES = [250, 500] #KB
FILENAME_END = '_numTubesFixed'

def avgAcquisition(numTubes, threeOrgs, fiveOrgs):
    # Sizes list
    n = FILE_SIZES

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=n, y=threeOrgs, mode="lines", name="3 Orgs net"))
    fig.add_trace(go.Scatter(x=n, y=fiveOrgs, mode="lines", name="5 Orgs net"))
    fig.layout = go.Layout(
        barmode='group',
        title=f"Executing transaction \'AddAcquisition\' with different raw data file sizes ({numTubes} tubes)",
        xaxis=dict(title=dict(text="Raw data file size (KB)")),
        yaxis=dict(title=dict(text="Average response time (s)"))
    )
    fig.update_xaxes(range=[250, 500])
    fig.update_yaxes(range=[1.0, 4.0])
    
    config = {'toImageButtonOptions': {
        'filename': f'avgAcq{FILENAME_END}',
    }}
    fig.show(config=config)

def totalAcquisition(numTubes, threeOrgs, fiveOrgs):
    # Sizes list
    n = FILE_SIZES

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=n, y=threeOrgs, mode="lines", name="3 Orgs net"))
    fig.add_trace(go.Scatter(x=n, y=fiveOrgs, mode="lines", name="5 Orgs net"))
    fig.layout = go.Layout(
        barmode='group',
        title=f"Elapsed time adding one acquisition per tube, with different raw data file sizes ({numTubes} tubes)",
        xaxis=dict(title=dict(text="Raw data file size (KB)")),
        yaxis=dict(title=dict(text="Total elapsed time (s)"))
    )
    fig.update_xaxes(range=[250, 500])
    #fig.update_yaxes(range=[1.0, 4.0])
    
    config = {'toImageButtonOptions': {
        'filename': f'totalAcq{FILENAME_END}',
    }}
    fig.show(config=config)

def avgAutoAnalysis(numTubes, threeOrgs, fiveOrgs):
    # Sizes list
    n = FILE_SIZES

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=n, y=threeOrgs, mode="lines", name="3 Orgs net"))
    fig.add_trace(go.Scatter(x=n, y=fiveOrgs, mode="lines", name="5 Orgs net"))
    fig.layout = go.Layout(
        barmode='group',
        title=f"Executing transaction \'AddAutomaticAnalysis\' with different raw data file sizes ({numTubes} tubes)",
        xaxis=dict(title=dict(text="Raw data file size (KB)")),
        yaxis=dict(title=dict(text="Average response time (s)"))
    )
    fig.update_xaxes(range=[250, 500])
    #fig.update_yaxes(range=[1.0, 4.0])
    
    config = {'toImageButtonOptions': {
        'filename': f'avgAuto{FILENAME_END}',
    }}
    fig.show(config=config)

def totalAutoAnalysis(numTubes, threeOrgs, fiveOrgs):
    # Sizes list
    n = FILE_SIZES

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=n, y=threeOrgs, mode="lines", name="3 Orgs net"))
    fig.add_trace(go.Scatter(x=n, y=fiveOrgs, mode="lines", name="5 Orgs net"))
    fig.layout = go.Layout(
        barmode='group',
        title=f"Elapsed time adding one automatic analysis per acquisition, with different raw data file sizes ({numTubes} tubes)",
        xaxis=dict(title=dict(text="Raw data file size (KB)")),
        yaxis=dict(title=dict(text="Total elapsed time (s)"))
    )
    fig.update_xaxes(range=[250, 500])
    #fig.update_yaxes(range=[1.0, 4.0])
    
    config = {'toImageButtonOptions': {
        'filename': f'totalAuto{FILENAME_END}',
    }}
    fig.show(config=config)

def avgAnalysis(numTubes, threeOrgs10, threeOrgs20, fiveOrgs10, fiveOrgs20):
    # Sizes list
    n = FILE_SIZES

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=n, y=threeOrgs10, mode="lines", name="3 Orgs net (10 analysts per role)"))
    fig.add_trace(go.Scatter(x=n, y=threeOrgs20, mode="lines", name="3 Orgs net (20 analysts per role)"))
    fig.add_trace(go.Scatter(x=n, y=fiveOrgs10, mode="lines", name="5 Orgs net (10 analysts per role)"))
    fig.add_trace(go.Scatter(x=n, y=fiveOrgs20, mode="lines", name="5 Orgs net (20 analysts per role)"))
    fig.layout = go.Layout(
        barmode='group',
        title=f"Executing transaction \'AddAnalysis\' with different raw data file sizes and different number of analysts ({numTubes} tubes)",
        xaxis=dict(title=dict(text="Raw data file size (KB)")),
        yaxis=dict(title=dict(text="Average response time (s)"))
    )
    fig.update_xaxes(range=[250, 500])
    fig.update_yaxes(range=[1.0, 4.0])
    
    config = {'toImageButtonOptions': {
        'filename': f'avgAnalysis{FILENAME_END}',
    }}
    fig.show(config=config)

def totalAnalysis(numTubes, threeOrgs10, threeOrgs20, fiveOrgs10, fiveOrgs20):
    # Sizes list
    n = FILE_SIZES

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=n, y=threeOrgs10, mode="lines", name="3 Orgs net (10 analysts per role)"))
    fig.add_trace(go.Scatter(x=n, y=threeOrgs20, mode="lines", name="3 Orgs net (20 analysts per role)"))
    fig.add_trace(go.Scatter(x=n, y=fiveOrgs10, mode="lines", name="5 Orgs net (10 analysts per role)"))
    fig.add_trace(go.Scatter(x=n, y=fiveOrgs20, mode="lines", name="5 Orgs net (20 analysts per role)"))
    fig.layout = go.Layout(
        barmode='group',
        title=f"Elapsed time adding one analysis per acquisition by primary and secondary analysts, <br> with different raw data file sizes and different number of analysts ({numTubes} tubes)",
        xaxis=dict(title=dict(text="Raw data file size (KB)")),
        yaxis=dict(title=dict(text="Total elapsed time (s)"))
    )
    fig.update_xaxes(range=[250, 500])
    #fig.update_yaxes(range=[1.0, 4.0])
    
    config = {'toImageButtonOptions': {
        'filename': f'totalAnalysis{FILENAME_END}',
    }}
    fig.show(config=config)

def avgResolution(numTubes, threeOrgs10, threeOrgs20, fiveOrgs10, fiveOrgs20):
    # Sizes list
    n = FILE_SIZES

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=n, y=threeOrgs10, mode="lines", name="3 Orgs net (10 advanced analysts)"))
    fig.add_trace(go.Scatter(x=n, y=threeOrgs20, mode="lines", name="3 Orgs net (20 advanced analysts)"))
    fig.add_trace(go.Scatter(x=n, y=fiveOrgs10, mode="lines", name="5 Orgs net (10 advanced analysts)"))
    fig.add_trace(go.Scatter(x=n, y=fiveOrgs20, mode="lines", name="5 Orgs net (20 advanced analysts)"))
    fig.layout = go.Layout(
        barmode='group',
        title=f"Executing transaction \'AddAnalysis\' with different raw data file sizes <br> and different number of advanced analysts ({numTubes} tubes)",
        xaxis=dict(title=dict(text="Raw data file size (KB)")),
        yaxis=dict(title=dict(text="Average response time (s)"))
    )
    fig.update_xaxes(range=[250, 500])
    fig.update_yaxes(range=[1.0, 4.0])
    
    config = {'toImageButtonOptions': {
        'filename': f'avgRes{FILENAME_END}',
    }}
    fig.show(config=config)

def totalResolution(numTubes, threeOrgs10, threeOrgs20, fiveOrgs10, fiveOrgs20):
    # Sizes list
    n = FILE_SIZES

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=n, y=threeOrgs10, mode="lines", name="3 Orgs net (10 advanced analysts)"))
    fig.add_trace(go.Scatter(x=n, y=threeOrgs20, mode="lines", name="3 Orgs net (20 advanced analysts)"))
    fig.add_trace(go.Scatter(x=n, y=fiveOrgs10, mode="lines", name="5 Orgs net (10 advanced analysts)"))
    fig.add_trace(go.Scatter(x=n, y=fiveOrgs20, mode="lines", name="5 Orgs net (20 advanced analysts)"))
    fig.layout = go.Layout(
        barmode='group',
        title=f"Elapsed time adding one analysis per acquisition by advanced analysts, <br> with different raw data file sizes and different number of analysts ({numTubes} tubes)",
        xaxis=dict(title=dict(text="Raw data file size (KB)")),
        yaxis=dict(title=dict(text="Total elapsed time (s)"))
    )
    fig.update_xaxes(range=[250, 500])
    #fig.update_yaxes(range=[1.0, 4.0])
    
    config = {'toImageButtonOptions': {
        'filename': f'totalRes{FILENAME_END}',
    }}
    fig.show(config=config)