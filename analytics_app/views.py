from django.http import HttpResponse
from django.shortcuts import render
from .forms import AnalyticsForm
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def download_chart(request):
    image_data = request.session.get('chart_image')
    if image_data:
        raw_image = base64.b64decode(image_data)
        response = HttpResponse(raw_image, content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="chart.png"'
        return response
    else:
        return HttpResponse("No chart to download.", status=404)


# Helper to safely parse float values from URL
def safe_float(value, default=0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default

# Chart generator
def generate_bar_chart(months, values, colors, width, gap, chart_width, chart_height):
    fig, ax = plt.subplots(figsize=(chart_width, chart_height))

    # Define fixed frame centers
    left_center = 0.25
    right_center = 0.75
    bar_positions = [left_center, right_center]

    # Draw bars
    bars = ax.bar(bar_positions, values, color=colors, width=width)

    # Vertical frame lines (left, middle, right)
    ax.axvline(x=0.0, color='black', linewidth=0.5, alpha=0.2)
    ax.axvline(x=0.5, color='black', linewidth=0.5, alpha=0.2)
    ax.axvline(x=1.0, color='black', linewidth=0.5, alpha=0.2)

    # Horizontal base line
    ax.hlines(y=0, xmin=0.0, xmax=1.0, color='black', linewidth=1, alpha=0.4)

    # Add labels above bars
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 4,  # ← controls margin above bar
            f'{height}',
            ha='center',
            va='bottom',
            fontsize=14,       # ← font size
            color='gray',     # ← font color
            alpha=0.8,         # ← transparency
            fontweight='normal'  # ← optional: bold/normal
        )


    # Clean chart styling
    ax.set_xlim(-0.1, 1.1)
    
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(
        months,
        fontsize=14,
        color='gray',
        alpha=0.8,
        fontweight='normal'
    )

    
    ax.set_yticklabels([])
    ax.spines[['top', 'left', 'right', 'bottom']].set_visible(False)
    ax.tick_params(axis='y', length=0)
    ax.tick_params(axis='x', length=0 , pad=10)

    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png', dpi=300)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    return base64.b64encode(image_png).decode('utf-8'), image_png  # return both



# View handler
def analytics_view(request):
    if request.method == 'POST':
        form = AnalyticsForm(request.POST)
        if form.is_valid():
            data = {
                'months': [form.cleaned_data['month1'], form.cleaned_data['month2']],
                'values': [form.cleaned_data['value1'], form.cleaned_data['value2']],
                'colors': ['#4040f1', '#4040f1'],  # RGB(64, 64, 241) as hex
                'width': 0.1,
                'chart_width': 11.1,
                'chart_height': 6.2,
            }

            gap = 0.2  # Manual spacing between bars and center

            graphic, raw_image = generate_bar_chart(
                months=data['months'],
                values=data['values'],
                colors=data['colors'],
                width=data['width'],
                gap=gap,
                chart_width=data['chart_width'],
                chart_height=data['chart_height']
            )
            
            request.session['chart_image'] = base64.b64encode(raw_image).decode('utf-8')  # store in session

            return render(request, 'analytics/results.html', {
                'graphic': graphic,
                'data': data
            })
    else:
        # Load from query params and safely cast
        form = AnalyticsForm(initial={
            'month1': request.GET.get('month1', 'Ocak'),
            'value1': safe_float(request.GET.get('value1', 100)),
            'color1': request.GET.get('color1', '#1f77b4'),
            'month2': request.GET.get('month2', 'Şubat'),
            'value2': safe_float(request.GET.get('value2', 150)),
            'color2': request.GET.get('color2', '#ff7f0e'),
            'bar_width': safe_float(request.GET.get('bar_width'), 0.7),
            'chart_width': safe_float(request.GET.get('chart_width'), 4.0),
            'chart_height': safe_float(request.GET.get('chart_height'), 6.0),
        })

    return render(request, 'analytics/index.html', {'form': form})
