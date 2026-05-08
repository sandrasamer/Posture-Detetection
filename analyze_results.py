"""Analyze posture detection session logs.

Run after using main.py:
    python analyze_results.py

This creates report-ready charts and a text summary in the results folder.
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt


LOG_DIR = Path(__file__).with_name("logs")
RESULTS_DIR = Path(__file__).with_name("results")


def find_latest_log():
    logs = sorted(LOG_DIR.glob("session_*.csv"))

    if not logs:
        raise FileNotFoundError(
            "No logs found. Run main.py first, then close it to save a session log."
        )

    return logs[-1]


def read_log(filename):
    rows = []

    with filename.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row["score"] = float(row.get("score") or 0)
            rows.append(row)

    return rows


def save_score_plot(rows):
    scores = [row["score"] for row in rows]
    x_values = list(range(1, len(scores) + 1))

    plt.figure(figsize=(10, 5))
    plt.plot(x_values, scores, linewidth=2, color="#176b87")
    plt.axhline(80, linestyle="--", color="#32cd32", label="Correct threshold")
    plt.axhline(55, linestyle="--", color="#e6c81e", label="Warning threshold")
    plt.ylim(0, 105)
    plt.xlabel("Logged sample")
    plt.ylabel("Posture score")
    plt.title("Posture Score Over Time")
    plt.legend()
    plt.grid(True, alpha=0.3)

    output = RESULTS_DIR / "score_over_time.png"
    plt.savefig(output, dpi=160, bbox_inches="tight")
    plt.close()

    return output


def save_risk_plot(rows):
    counts = Counter(row.get("risk_level", "Unknown") for row in rows)

    labels = ["Low", "Medium", "High", "Unknown"]
    values = [counts.get(label, 0) for label in labels]

    plt.figure(figsize=(7, 5))
    plt.bar(labels, values, color=["#32cd32", "#e6c81e", "#f03c3c", "#777777"])
    plt.xlabel("Risk level")
    plt.ylabel("Number of logged samples")
    plt.title("Risk Level Distribution")
    plt.grid(axis="y", alpha=0.3)

    output = RESULTS_DIR / "risk_distribution.png"
    plt.savefig(output, dpi=160, bbox_inches="tight")
    plt.close()

    return output


def write_summary(rows, log_file):
    scores = [row["score"] for row in rows]
    statuses = Counter(row.get("status", "UNKNOWN") for row in rows)
    risks = Counter(row.get("risk_level", "Unknown") for row in rows)
    modes = Counter(row.get("mode", "unknown") for row in rows)

    average_score = sum(scores) / len(scores)
    minimum_score = min(scores)
    maximum_score = max(scores)

    warning_or_bad = sum(
        1 for row in rows if row.get("status") in ("WARNING", "INCORRECT")
    )

    summary = RESULTS_DIR / "summary.txt"

    with summary.open("w", encoding="utf-8") as file:
        file.write("Posture Detection Results Summary\n")
        file.write("=================================\n\n")

        file.write(f"Log file analyzed: {log_file.name}\n")
        file.write(f"Total logged samples: {len(rows)}\n")
        file.write(f"Average score: {average_score:.2f}%\n")
        file.write(f"Minimum score: {minimum_score:.2f}%\n")
        file.write(f"Maximum score: {maximum_score:.2f}%\n")
        file.write(f"Warning/incorrect samples: {warning_or_bad}\n\n")

        file.write("Status counts:\n")
        for status, count in statuses.items():
            file.write(f"- {status}: {count}\n")

        file.write("\nRisk level counts:\n")
        for risk, count in risks.items():
            file.write(f"- {risk}: {count}\n")

        file.write("\nImage-processing modes used:\n")
        for mode, count in modes.items():
            file.write(f"- {mode}: {count}\n")

        file.write("\nInterpretation:\n")
        file.write(
            "Higher scores indicate better posture alignment. Low scores usually "
            "correspond to forward head posture, neck bending, trunk leaning, or "
            "shoulder imbalance. The generated plots can be used as supporting "
            "analysis in the project report.\n"
        )

    return summary


def main():
    RESULTS_DIR.mkdir(exist_ok=True)

    log_file = find_latest_log()
    rows = read_log(log_file)

    if not rows:
        raise RuntimeError(
            "The latest log file is empty. Run main.py for a longer session."
        )

    score_plot = save_score_plot(rows)
    risk_plot = save_risk_plot(rows)
    summary = write_summary(rows, log_file)

    print(f"Analyzed: {log_file}")
    print(f"Saved: {score_plot}")
    print(f"Saved: {risk_plot}")
    print(f"Saved: {summary}")


if __name__ == "__main__":
    main()
