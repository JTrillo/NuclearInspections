import plotly.graph_objs as go

NUM_TUBES = [500, 1000, 1500]
FILENAME_END = '_fileSizeFixed'

def avgAcquisition(fileSize, threeOrgs, fiveOrgs):
    # Number of tubes
    n = NUM_TUBES

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=n, y=threeOrgs, mode="lines", name="3 Orgs net"))
    fig.add_trace(go.Scatter(x=n, y=fiveOrgs, mode="lines", name="5 Orgs net"))
    fig.layout = go.Layout(
        barmode='group',
        title=f"Executing transaction \'AddAcquisition\' with different number of tubes ({fileSize})",
        xaxis=dict(title=dict(text="Number of tubes")),
        yaxis=dict(title=dict(text="Average response time (s)"))
    )
    fig.update_xaxes(range=[500, 1500])
    fig.update_yaxes(range=[1.0, 4.0])

    config = {'toImageButtonOptions': {
        'filename': f'avgAcq{FILENAME_END}',
    }}
    fig.show(config=config)

def totalAcquisition(fileSize, threeOrgs, fiveOrgs):
    # Number of tubes
    n = NUM_TUBES

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=n, y=threeOrgs, mode="lines", name="3 Orgs net"))
    fig.add_trace(go.Scatter(x=n, y=fiveOrgs, mode="lines", name="5 Orgs net"))
    fig.layout = go.Layout(
        barmode='group',
        title=f"Elapsed time adding one acquisition per tube, with different number of tubes ({fileSize})",
        xaxis=dict(title=dict(text="Number of tubes")),
        yaxis=dict(title=dict(text="Total elapsed time (s)"))
    )
    fig.update_xaxes(range=[500, 1500])
    #fig.update_yaxes(range=[1.0, 4.0])
    
    config = {'toImageButtonOptions': {
        'filename': f'totalAcq{FILENAME_END}',
    }}
    fig.show(config=config)

def avgAutoAnalysis(fileSize, threeOrgs, fiveOrgs):
    # Number of tubes
    n = NUM_TUBES

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=n, y=threeOrgs, mode="lines", name="3 Orgs net"))
    fig.add_trace(go.Scatter(x=n, y=fiveOrgs, mode="lines", name="5 Orgs net"))
    fig.layout = go.Layout(
        barmode='group',
        title=f"Executing transaction \'AddAutomaticAnalysis\' with different number of tubes ({fileSize})",
        xaxis=dict(title=dict(text="Number of tubes")),
        yaxis=dict(title=dict(text="Average response time (s)"))
    )
    fig.update_xaxes(range=[500, 1500])
    fig.update_yaxes(range=[10.0, 17.0])
    
    config = {'toImageButtonOptions': {
        'filename': f'avgAuto{FILENAME_END}',
    }}
    fig.show(config=config)

def totalAutoAnalysis(fileSize, threeOrgs, fiveOrgs):
    # Number of tubes
    n = NUM_TUBES

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=n, y=threeOrgs, mode="lines", name="3 Orgs net"))
    fig.add_trace(go.Scatter(x=n, y=fiveOrgs, mode="lines", name="5 Orgs net"))
    fig.layout = go.Layout(
        barmode='group',
        title=f"Elapsed time adding one automatic analysis per acquisition, with different number of tubes ({fileSize})",
        xaxis=dict(title=dict(text="Number of tubes")),
        yaxis=dict(title=dict(text="Total elapsed time (s)"))
    )
    fig.update_xaxes(range=[500, 1500])
    #fig.update_yaxes(range=[13.0, 16.0])
    
    config = {'toImageButtonOptions': {
        'filename': f'totalAuto{FILENAME_END}',
    }}
    fig.show(config=config)

def avgAnalysis(fileSize, threeOrgs10, threeOrgs20, fiveOrgs10, fiveOrgs20):
    # Number of tubes
    n = NUM_TUBES

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=n, y=threeOrgs10, mode="lines", name="3 Orgs net (10 analysts per role)"))
    fig.add_trace(go.Scatter(x=n, y=threeOrgs20, mode="lines", name="3 Orgs net (20 analysts per role)"))
    fig.add_trace(go.Scatter(x=n, y=fiveOrgs10, mode="lines", name="5 Orgs net (10 analysts per role)"))
    fig.add_trace(go.Scatter(x=n, y=fiveOrgs20, mode="lines", name="5 Orgs net (20 analysts per role)"))
    fig.layout = go.Layout(
        barmode='group',
        title=f'Executing transaction \'AddAnalysis\' with different number of tubes and different number of analysts ({fileSize})',
        xaxis=dict(title=dict(text="Number of tubes")),
        yaxis=dict(title=dict(text="Average response time (s)"))
    )
    fig.update_xaxes(range=[500, 1500])
    fig.update_yaxes(range=[1.0, 4.0])
    
    config = {'toImageButtonOptions': {
        'filename': f'avgAnalysis{FILENAME_END}',
    }}
    fig.show(config=config)

def totalAnalysis(fileSize, threeOrgs10, threeOrgs20, fiveOrgs10, fiveOrgs20):
    # Number of tubes
    n = NUM_TUBES

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=n, y=threeOrgs10, mode="lines", name="3 Orgs net (10 analysts per role)"))
    fig.add_trace(go.Scatter(x=n, y=threeOrgs20, mode="lines", name="3 Orgs net (20 analysts per role)"))
    fig.add_trace(go.Scatter(x=n, y=fiveOrgs10, mode="lines", name="5 Orgs net (10 analysts per role)"))
    fig.add_trace(go.Scatter(x=n, y=fiveOrgs20, mode="lines", name="5 Orgs net (20 analysts per role)"))
    fig.layout = go.Layout(
        barmode='group',
        title=f'Elapsed time adding one analysis per acquisition by primary and secondary analysts, <br> with different number of tubes and different number of analysts ({fileSize})',
        xaxis=dict(title=dict(text="Number of tubes")),
        yaxis=dict(title=dict(text="Average response time (s)"))
    )
    fig.update_xaxes(range=[500, 1500])
    #fig.update_yaxes(range=[1.0, 4.0])
    
    config = {'toImageButtonOptions': {
        'filename': f'totalAnalysis{FILENAME_END}',
    }}
    fig.show(config=config)

def avgResolution(fileSize, threeOrgs10, threeOrgs20, fiveOrgs10, fiveOrgs20):
    # Number of tubes
    n = NUM_TUBES

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=n, y=threeOrgs10, mode="lines", name="3 Orgs net (10 advanced analysts)"))
    fig.add_trace(go.Scatter(x=n, y=threeOrgs20, mode="lines", name="3 Orgs net (20 advanced analysts)"))
    fig.add_trace(go.Scatter(x=n, y=fiveOrgs10, mode="lines", name="5 Orgs net (10 advanced analysts)"))
    fig.add_trace(go.Scatter(x=n, y=fiveOrgs20, mode="lines", name="5 Orgs net (20 advanced analysts)"))
    fig.layout = go.Layout(
        barmode='group',
        title=f'Executing transaction \'AddAnalysis\' with different number of tubes <br> and different number of advanced analysts ({fileSize})',
        xaxis=dict(title=dict(text="Number of tubes")),
        yaxis=dict(title=dict(text="Average response time (s)"))
    )
    fig.update_xaxes(range=[500, 1500])
    fig.update_yaxes(range=[1.0, 4.0])
    
    config = {'toImageButtonOptions': {
        'filename': f'avgRes{FILENAME_END}',
    }}
    fig.show(config=config)

def totalResolution(fileSize, threeOrgs10, threeOrgs20, fiveOrgs10, fiveOrgs20):
    # Number of tubes
    n = NUM_TUBES

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=n, y=threeOrgs10, mode="lines", name="3 Orgs net (10 advanced analysts)"))
    fig.add_trace(go.Scatter(x=n, y=threeOrgs20, mode="lines", name="3 Orgs net (20 advanced analysts)"))
    fig.add_trace(go.Scatter(x=n, y=fiveOrgs10, mode="lines", name="5 Orgs net (10 advanced analysts)"))
    fig.add_trace(go.Scatter(x=n, y=fiveOrgs20, mode="lines", name="5 Orgs net (20 advanced analysts)"))
    fig.layout = go.Layout(
        barmode='group',
        title=f'Elapsed time adding one analysis per acquisition by advanced analysts, <br> with different number of tubes and different number of analysts ({fileSize})',
        xaxis=dict(title=dict(text="Number of tubes")),
        yaxis=dict(title=dict(text="Average response time (s)"))
    )
    fig.update_xaxes(range=[500, 1500])
    #fig.update_yaxes(range=[1.0, 4.0])
    
    config = {'toImageButtonOptions': {
        'filename': f'totalRes{FILENAME_END}',
    }}
    fig.show(config=config)