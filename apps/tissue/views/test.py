
from dash import html, dcc, dash_table
import dash


app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
server = app.server

app.layout = html.Div([
html.Div([
html.H3("Card header", className="card-header"),
html.Div([
html.H5("Special title treatment", className="card-title"),
html.H6("SSupport card subtitle", className="card-subtitle text-muted"),
], className="card-body")
], className="card mb-3")
])

# <div class="card mb-3">
#   <h3 class="card-header">Card header</h3>
#   <div class="card-body">
#     <h5 class="card-title">Special title treatment</h5>
#     <h6 class="card-subtitle text-muted">Support card subtitle</h6>
#   </div>
#   <svg xmlns="http://www.w3.org/2000/svg" class="d-block user-select-none" width="100%" height="200" aria-label="Placeholder: Image cap" focusable="false" role="img" preserveAspectRatio="xMidYMid slice" viewBox="0 0 318 180" style="font-size:1.125rem;text-anchor:middle">
#     <rect width="100%" height="100%" fill="#868e96"></rect>
#     <text x="50%" y="50%" fill="#dee2e6" dy=".3em">Image cap</text>
#   </svg>
#   <div class="card-body">
#     <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
#   </div>
#   <ul class="list-group list-group-flush">
#     <li class="list-group-item">Cras justo odio</li>
#     <li class="list-group-item">Dapibus ac facilisis in</li>
#     <li class="list-group-item">Vestibulum at eros</li>
#   </ul>
#   <div class="card-body">
#     <a href="#" class="card-link">Card link</a>
#     <a href="#" class="card-link">Another link</a>
#   </div>
#   <div class="card-footer text-muted">
#     2 days ago
#   </div>
# </div>
# <div class="card">
#   <div class="card-body">
#     <h4 class="card-title">Card title</h4>
#     <h6 class="card-subtitle mb-2 text-muted">Card subtitle</h6>
#     <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
#     <a href="#" class="card-link">Card link</a>
#     <a href="#" class="card-link">Another link</a>
#   </div>
# </div>


# if __name__ == '__main__':
#     app.run_server(port=3000, debug=True)
