import os
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent
MPL_CONFIG_DIR = OUTPUT_DIR / ".mplconfig"
MPL_CONFIG_DIR.mkdir(exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CONFIG_DIR))

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams["font.sans-serif"] = ["Hiragino Sans GB", "Songti SC"]
    plt.rcParams["axes.unicode_minus"] = False
except ModuleNotFoundError:
    matplotlib = None
    plt = None


a = [3.20, 3.99, 4.64, 5.30, 5.97, 6.62, 7.28, 7.93, 8.59, 9.26] # V_H (mV)
b = [0.243, 0.302, 0.353, 0.402, 0.452, 0.502, 0.552, 0.601, 0.651, 0.701] # I_M (A)
c = [3.32, 3.96, 4.62, 5.29, 5.96, 6.61, 7.28, 7.93, 8.59, 9.25] # V_H (mV)
d = [2.50, 3.00, 3.50, 4.00, 4.50, 5.00, 5.50, 6.00, 6.50, 7.00] # I_S (mA)
e = [3.60, 4.47, 5.22, 5.95, 6.69, 7.43, 8.17, 8.90, 9.64, 10.38] # B (mT)
f = [1.22, 1.41, 1.64, 2.08, 3.66, 5.23, 5.85, 6.73, 7.00, 7.24,
     7.38, 7.40, 7.39, 7.36, 7.35, 7.23, 7.06, 6.85, 6.46, 5.69,
     4.32, 2.65, 1.98, 1.70, 1.45] # B (mT)
g = [0.0, 2.0, 4.0, 8.0, 16.0, 24.0, 32.0, 40.0, 48.0, 64.0,
     96.0, 128.0, 150.0, 172.0, 204.0, 236.0, 252.0, 260.0, 268.0, 276.0,
     284.0, 292.0, 296.0, 298.0, 300.0] # x (mm)

LINE_COLOR = "#1f77b4"
HALL_CURRENT_A = 0.005


def least_squares_fit(x_values, y_values):
    if len(x_values) != len(y_values):
        raise ValueError("x and y data must have the same length.")
    if not x_values:
        raise ValueError("x and y data must not be empty.")

    sample_count = len(x_values)
    x_mean = sum(x_values) / sample_count
    y_mean = sum(y_values) / sample_count
    sum_xy = sum(x * y for x, y in zip(x_values, y_values))
    sum_x_squared = sum(x * x for x in x_values)
    denominator = sum_x_squared - sample_count * x_mean * x_mean

    if denominator == 0:
        raise ValueError("Cannot fit a line when all x values are identical.")

    slope = (sum_xy - sample_count * x_mean * y_mean) / denominator
    intercept = y_mean - slope * x_mean
    return slope, intercept


def calculate_average_hall_coefficient(vh_values_mv, b_values_mt, current_a):
    if len(vh_values_mv) != len(b_values_mt):
        raise ValueError("V_H and B data must have the same length.")
    if not vh_values_mv:
        raise ValueError("V_H and B data must not be empty.")
    if current_a == 0:
        raise ValueError("Hall current must be non-zero.")
    if any(float(b_value_mt) == 0 for b_value_mt in b_values_mt):
        raise ValueError("Magnetic field data must be non-zero.")

    hall_coefficients = [
        (float(vh_value_mv) * 1e-3) / (current_a * float(b_value_mt) * 1e-3)
        for vh_value_mv, b_value_mt in zip(vh_values_mv, b_values_mt)
    ]
    return sum(hall_coefficients) / len(hall_coefficients), hall_coefficients


def plot_curve(x_values, y_values, xlabel, ylabel, legend_label, output_name):
    if plt is None:
        raise RuntimeError("matplotlib is required to generate plots.")

    figure, axis = plt.subplots(figsize=(6.4, 4.8))
    axis.plot(
        x_values,
        y_values,
        color=LINE_COLOR,
        marker="o",
        linewidth=1.8,
        label=legend_label,
    )
    axis.set_xlabel(xlabel)
    axis.set_ylabel(ylabel)
    axis.legend(loc="upper right")
    axis.grid(True, linestyle="--", alpha=0.4)
    figure.tight_layout()
    figure.savefig(OUTPUT_DIR / output_name, dpi=300, bbox_inches="tight")
    plt.close(figure)


def main():
    k1, intercept1 = least_squares_fit(b, a)
    k2, intercept2 = least_squares_fit(d, c)
    kh_average, kh_values = calculate_average_hall_coefficient(a, e, HALL_CURRENT_A)

    if plt is not None:
        plot_curve(
            b,
            a,
            r"$I_M\left(\mathrm{A}\right)$",
            r"$V_H\left(\mathrm{mV}\right)$",
            r"$V_H-I_M$ 曲线",
            "vh_im_curve.png",
        )
        plot_curve(
            d,
            c,
            r"$I_S\left(\mathrm{mA}\right)$",
            r"$V_H\left(\mathrm{mV}\right)$",
            r"$V_H-I_S$ 曲线",
            "vh_is_curve.png",
        )
        plot_curve(
            g,
            f,
            r"$x\left(\mathrm{mm}\right)$",
            r"$B\left(\mathrm{mT}\right)$",
            r"$B-X$ 曲线",
            "b_x_curve.png",
        )

    print(f"k1 = {k1:.6f}")
    print(f"intercept1 = {intercept1:.6f}")
    print(f"k2 = {k2:.6f}")
    print(f"intercept2 = {intercept2:.6f}")
    print(
        "K_H values from a/e = "
        + ", ".join(f"{value:.6f}" for value in kh_values)
        + " m^2/C"
    )
    print(f"Average K_H from a/e = {kh_average:.6f} m^2/C")
    print(
        r"LaTeX: \overline{K}_H = \frac{\sum\limits_{i = 1}^{10} "
        r"\frac{V_{H_i}}{I_S B_i}}{10} = "
        f"{kh_average:.4f}"
        r" \ \mathrm{m^2/C}"
    )
    if plt is not None:
        print(f"Saved: {OUTPUT_DIR / 'vh_im_curve.png'}")
        print(f"Saved: {OUTPUT_DIR / 'vh_is_curve.png'}")
        print(f"Saved: {OUTPUT_DIR / 'b_x_curve.png'}")
    else:
        print("Skipped plotting because matplotlib is not installed.")


if __name__ == "__main__":
    main()
