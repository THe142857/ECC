import matplotlib.pyplot as plt
import numpy as np

a_curve = -2.0
b_curve = 3.0

Px1_str = "2.0_top"
Px2_str = "4.0_top"

coeff_curve = [1, 0, a_curve, b_curve]
x_val_min_curve = min(np.roots(coeff_curve).real[abs(np.roots(coeff_curve).imag) < 1e-5])
x_val_max_curve = 500.0


def find_other_point_x(x1, x2, m, b):       # finds other intersection point x
    for point_x in find_linear_curve_roots(m, b):
        if abs(point_x - x1) < 0.001 or abs(point_x - x2) < 0.001:
            pass
        else:
            try:
                return point_x
            except NameError:
                raise NameError('Only two intersections!!??!?')


def top_curve_find_y(x, a_c, b_c):
    try:
        return (x ** 3 + a_c * x + b_c) ** (1/2.0)
    except Exception:
        pass


def bottom_curve_find_y(x, a_c, b_c):
    try:
        return - (x ** 3 + a_c * x + b_c) ** (1/2.0)
    except Exception:
        pass


def str_x_to_num_x(p_str):
    underscore_idx = p_str.find("_")
    return float(p_str[:underscore_idx])


def str_x_find_num_y(p_str):
    px = str_x_to_num_x(p_str)
    if "top" in p_str:
        return top_curve_find_y(px, a_curve, b_curve)
    else:
        return bottom_curve_find_y(px, a_curve, b_curve)


def find_slope(x1, x2, y1, y2):
    return (y2 - y1) / (x2 - x1)


def find_b(x1, x2, y1, y2):
    m = find_slope(x1, x2, y1, y2)
    return y1 - m * x1


def linear_find_y(x, slope, y_int):
    return slope * x + y_int


def find_linear_curve_roots(linear_m, linear_b):
    coeff_linear_curve = [1, -linear_m ** 2, a_curve - 2 * linear_m * linear_b,
                          b_curve - linear_b ** 2]
    return np.roots(coeff_linear_curve)


Px1 = str_x_to_num_x(Px1_str)
Px2 = str_x_to_num_x(Px2_str)
Py1 = str_x_find_num_y(Px1_str)
Py2 = str_x_find_num_y(Px2_str)
m_linear = find_slope(Px1, Px2, Py1, Py2)
b_linear = find_b(Px1, Px2, Py1, Py2)

x_min_frame = -2.0
x_max_frame = 30.0
y_min_frame = -30.0
y_max_frame = 30.0


def color_other_point(x1, x2, m, b):
    x_other = find_other_point_x(x1, x2, m, b)
    y_other = linear_find_y(x_other, m, b)
    plt.plot(x_other, y_other, color="orange", marker="o")


def find_discriminant(a, b):
    return -16 * (4 * a ** 3 + 27 * b ** 2)


def point_str_flip(p_str):
    if "top" in p_str:
        return p_str.replace("top", "bottom")
    else:
        return p_str.replace("bottom", "top")


def plot_line_intersections(x1_str, x2_str):
    x1_num = str_x_to_num_x(x1_str)
    x2_num = str_x_to_num_x(x2_str)
    y1_num = str_x_find_num_y(x1_str)
    y2_num = str_x_find_num_y(x2_str)

    m = find_slope(x1_num, x2_num, y1_num, y2_num)
    b = find_b(x1_num, x2_num, y1_num, y2_num)

    roots_x = find_linear_curve_roots(m, b)
    x_begin = min(roots_x)
    x_end = max(roots_x)
    x = np.arange(x_begin, x_end, 0.001)
    y = linear_find_y(x, m, b)

    plt.plot(x, y, color="black")    # linear line
    color_other_point(x1_num, x2_num, m, b)     # intersections


def draw_legend():
    ax.annotate("Red=Original Point",
                xy=(.63, .975), xycoords="axes fraction",
                horizontalalignment='left', verticalalignment='top',
                fontsize=10, color="red")
    ax.annotate("Green=Reflection(Second Point)",
                xy=(.53, .925), xycoords="axes fraction",
                horizontalalignment='left', verticalalignment='top',
                fontsize=10, color="green")
    ax.annotate("Orange=other intersection",
                xy=(.58, .875), xycoords="axes fraction",
                horizontalalignment='left', verticalalignment='top',
                fontsize=10, color="orange")


def draw_basics():
    ax.clear()

    curve_top = plt.plot(x_curve, y_curve_top)  # draws top portion
    plt.setp(curve_top, color='b', linewidth=2.0)

    curve_bottom = plt.plot(x_curve, y_curve_bottom)  # draws bottom portion
    plt.setp(curve_bottom, color='b', linewidth=2.0)

    plt.xlim(x_min_frame, x_max_frame)
    plt.ylim(y_min_frame, y_max_frame)

    plt.annotate("Click to Proceed",
                 xy=(.01, .975), xycoords="figure fraction",
                 horizontalalignment='left', verticalalignment='top',
                 fontsize=20)

    draw_legend()



click_counter = 0
fig, ax = plt.subplots()


def onclick(event):
    global click_counter
    global Px2
    global Py2
    global m_linear
    global b_linear

    plt.ion()

    if click_counter % 2 == 0:
        draw_basics()

        reflect_point_x = find_other_point_x(Px1, Px2, m_linear, b_linear)
        reflect_point_y = - linear_find_y(reflect_point_x, m_linear, b_linear)
        plt.plot(reflect_point_x, reflect_point_y, color="green", marker="o")   # reflection pt
        plt.plot(Px1, Py1, "ro")    # original pt

    else:
        reflect_point_x = find_other_point_x(Px1, Px2, m_linear, b_linear)
        reflect_point_y = - linear_find_y(reflect_point_x, m_linear, b_linear)
        if reflect_point_y >= 0:
            reflect_point_x_str = str(reflect_point_x) + "_top"
        else:
            reflect_point_x_str = str(reflect_point_x) + "_bottom"

        plot_line_intersections(Px1_str, reflect_point_x_str)

        Px2 = reflect_point_x       # sets reflection point as new point 2
        Py2 = reflect_point_y
        m_linear = find_slope(Px1, Px2, Py1, Py2)
        b_linear = find_b(Px1, Px2, Py1, Py2)

    click_counter += 1
    plt.ioff()


cid = fig.canvas.mpl_connect('button_press_event', onclick)


x_curve = np.arange(x_val_min_curve, x_val_max_curve, 0.001)
y_curve_top = top_curve_find_y(x_curve, a_curve, b_curve)
y_curve_bottom = bottom_curve_find_y(x_curve, a_curve, b_curve)

draw_basics()
plt.plot(Px1, Py1, color="red", marker="o")
plt.plot(Px2, Py2, color="green", marker="o")
plot_line_intersections(Px1_str, Px2_str)


if find_discriminant(a_curve, b_curve) != 0:
    plt.show()
else:
    print("Discriminant = 0 ERROR!!")

