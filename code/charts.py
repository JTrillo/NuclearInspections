import plotly.graph_objs as go


def avgAnalysis(threeOrgs, fiveOrgs):
    try:
        if len(threeOrgs) != 6 or len(fiveOrgs) != 6:
            print("Both lists must contain 6 numbers")
        else:
            # Number analysts
            n = [1, 2, 5, 10, 25, 50]

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=n, y=threeOrgs, mode="lines", name="3 Orgs net"))
            fig.add_trace(go.Scatter(x=n, y=fiveOrgs, mode="lines", name="5 Orgs net"))
            fig.layout = go.Layout(
                barmode='group',
                title='Executing transaction \'AddAnalysis\' with different number of analysts',
                xaxis=dict(title=dict(text="Number of analysts working at same time")),
                yaxis=dict(title=dict(text="Average response time (s)"))
            )
            fig.show()
    except TypeError:
        print("Both arguments must be lists containing 6 numbers")

def avgGetAcquisitions(threeOrgs, fiveOrgs):
    try:
        if len(threeOrgs) != 6 or len(fiveOrgs) != 6:
            print("Both lists must contain 6 numbers")
        else:
            # Number analysts
            n = [1, 2, 5, 10, 25, 50]

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=n, y=threeOrgs, mode="lines", name="3 Orgs net"))
            fig.add_trace(go.Scatter(x=n, y=fiveOrgs, mode="lines", name="5 Orgs net"))
            fig.layout = go.Layout(
                barmode='group',
                title='Retrieving acquisition data with different number of analysts',
                xaxis=dict(title=dict(text="Number of analysts working at same time")),
                yaxis=dict(title=dict(text="Average response time (s)"))
            )
            fig.show()
    except TypeError:
        print("Both arguments must be lists containing 6 numbers")

def avgGetAnalyses(threeOrgs, fiveOrgs):
    try:
        if len(threeOrgs) != 6 or len(fiveOrgs) != 6:
            print("Both lists must contain 6 numbers")
        else:
            # Number analysts
            n = [1, 2, 5, 10, 25, 50]

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=n, y=threeOrgs, mode="lines", name="3 Orgs net"))
            fig.add_trace(go.Scatter(x=n, y=fiveOrgs, mode="lines", name="5 Orgs net"))
            fig.layout = go.Layout(
                barmode='group',
                title='Retrieving previous analyses data with different number of advanced analysts',
                xaxis=dict(title=dict(text="Number of advanced analysts working at same time")),
                yaxis=dict(title=dict(text="Average response time (s)"))
            )
            fig.show()
    except TypeError:
        print("Both arguments must be lists containing 6 numbers")