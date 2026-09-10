import io
import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from config import C_HDR, TITLE, TAIWAN_TZ
from datetime import datetime

matplotlib.use("Agg")

def render_schedule_figure(start_dt, dates, emp_id, emp_name, cells, unit_label, badge_title="Producer"):
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    
    ax.text(0.05, 0.9, f"{TITLE} - {unit_label}", fontsize=16, fontweight="bold")
    ax.text(0.05, 0.82, f"CREW: {emp_name} ({emp_id})", fontsize=12)
    
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf
