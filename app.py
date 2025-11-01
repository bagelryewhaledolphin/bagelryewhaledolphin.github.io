import io
import base64
import random
from flask import Flask, render_template, request, Response
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def index():
    # Render the initial HTML page with the form
    return render_template('index.html')

@app.route('/generate-graph', methods=['POST'])
def generate_graph():
    # Get the user input from the form
    try:
        input_value = int(request.form['user_input_value'])
    except ValueError:
        return "Invalid input. Please enter an integer."

    # Generate the plot
    img_data = create_plot(input_value)

    # Return an HTML response that displays the image
    return f"""
    <h2>Generated Graph:</h2>
    <img src="data:image/png;base64,{img_data}" alt="Matplotlib Graph">
    <p><a href="/">Go Back</a></p>
    """

def create_plot(n_points):
    # This function generates a simple matplotlib plot and encodes it
    # in base64 so it can be embedded directly in the HTML.

    plt.figure(figsize=(6, 4))
    x = range(n_points)
    y = [random.randint(1, 100) for _ in range(n_points)]
    plt.plot(x, y)
    plt.xlabel('X Value')
    plt.ylabel('Y Value')
    plt.title(f'Random data for {n_points} points')
    plt.grid(True)

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Encode the image data in base64
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')

    return img_base64

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
