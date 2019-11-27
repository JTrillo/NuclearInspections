import plotly.graph_objs as go

NUM_TUBES = [500, 1000, 1500]

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
    fig.show()

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
    fig.show()

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
    fig.show()

def totalAutoAnalysis(fileSize, threeOrgs, fiveOrgs):
    # Number of tubes
    n = NUM_TUBES

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=n, y=threeOrgs, mode="lines", name="3 Orgs net"))
    fig.add_trace(go.Scatter(x=n, y=fiveOrgs, mode="lines", name="5 Orgs net"))
    fig.layout = go.Layout(
        barmode='group',
        title=f"Elapsed tiem adding one automatic analysis per acquisition, with different number of tubes ({fileSize})",
        xaxis=dict(title=dict(text="Number of tubes")),
        yaxis=dict(title=dict(text="Total elapsed time (s)"))
    )
    fig.update_xaxes(range=[500, 1500])
    #fig.update_yaxes(range=[13.0, 16.0])
    fig.show()

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
    fig.show()

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
        title=f'Elapsed time adding one analysis per acquisition by primary and secondary analysts, with different number of tubes and different number of analysts ({fileSize})',
        xaxis=dict(title=dict(text="Number of tubes")),
        yaxis=dict(title=dict(text="Average response time (s)"))
    )
    fig.update_xaxes(range=[500, 1500])
    #fig.update_yaxes(range=[1.0, 4.0])
    fig.show()

#def avgResolution(fileSize, threeOrgs10, threeOrgs20, fiveOrgs10, fiveOrgs20):
def avgResolution(fileSize, threeOrgs10, threeOrgs20):
    # Number of tubes
    n = NUM_TUBES

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=n, y=threeOrgs10, mode="lines", name="3 Orgs net (10 advanced analysts)"))
    fig.add_trace(go.Scatter(x=n, y=threeOrgs20, mode="lines", name="3 Orgs net (20 advanced analysts)"))
    #fig.add_trace(go.Scatter(x=n, y=fiveOrgs10, mode="lines", name="5 Orgs net (10 advanced analysts)"))
    #fig.add_trace(go.Scatter(x=n, y=fiveOrgs20, mode="lines", name="5 Orgs net (20 advanced analysts)"))
    fig.layout = go.Layout(
        barmode='group',
        title=f'Executing transaction \'AddAnalysis\' with different number of tubes and different number of advanced analysts ({fileSize})',
        xaxis=dict(title=dict(text="Number of tubes")),
        yaxis=dict(title=dict(text="Average response time (s)"))
    )
    fig.update_xaxes(range=[500, 1500])
    fig.update_yaxes(range=[1.0, 4.0])
    fig.show()

#def totalResolution(fileSize, threeOrgs10, threeOrgs20, fiveOrgs10, fiveOrgs20):
def totalResolution(fileSize, threeOrgs10, threeOrgs20):
    # Number of tubes
    n = NUM_TUBES

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=n, y=threeOrgs10, mode="lines", name="3 Orgs net (10 advanced analysts)"))
    fig.add_trace(go.Scatter(x=n, y=threeOrgs20, mode="lines", name="3 Orgs net (20 advanced analysts)"))
    #fig.add_trace(go.Scatter(x=n, y=fiveOrgs10, mode="lines", name="5 Orgs net (10 advanced analysts)"))
    #fig.add_trace(go.Scatter(x=n, y=fiveOrgs20, mode="lines", name="5 Orgs net (20 advanced analysts)"))
    fig.layout = go.Layout(
        barmode='group',
        title=f'Elapsed time adding one analysis per acquisition by advanced analysts, with different number of tubes and different number of analysts ({fileSize})',
        xaxis=dict(title=dict(text="Number of tubes")),
        yaxis=dict(title=dict(text="Average response time (s)"))
    )
    fig.update_xaxes(range=[500, 1500])
    #fig.update_yaxes(range=[1.0, 4.0])
    fig.show()