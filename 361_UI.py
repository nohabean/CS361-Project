import ctypes
import fractions
import sys

import zmq
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QLabel, QHBoxLayout, QPushButton, QDialog, \
    QDialogButtonBox, QLineEdit, QComboBox, QMessageBox, QMainWindow
from PySide6.QtCore import Qt, QSize


global current_layout
global tab_widget
global conversion_layouts_map


def dark_title_bar(window):
    """
    https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
    """
    set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
    hwnd = int(window.winId())
    value = 2
    value = ctypes.c_int(value)
    set_window_attribute(hwnd, 20, ctypes.byref(value), 4)


def conversions_button_layout():
    # Create button layout for the conversions tab
    adc_buttons_layout_conversions = QHBoxLayout()

    add_button_conversions = QPushButton()
    add_button_conversions.setIcon(QIcon("add_new_button.png"))
    add_button_conversions.setIconSize(QSize(200, 40))
    add_button_conversions.setToolTip("<span style='color: white; font-size: 13px;'>Add a new entry to convert</span>")
    add_button_conversions.clicked.connect(lambda checked, btn=add_button_conversions: add_new_conversion(btn))
    adc_buttons_layout_conversions.addWidget(add_button_conversions)

    delete_button_conversions = QPushButton()
    delete_button_conversions.setIcon(QIcon("delete_all_button.png"))
    delete_button_conversions.setIconSize(QSize(200, 40))
    delete_button_conversions.setToolTip(
        "<span style='color: white; font-size: 13px;'>Deletes all current entries</span>")
    delete_button_conversions.clicked.connect(delete_all_conversions)
    adc_buttons_layout_conversions.addWidget(delete_button_conversions)

    clear_button_conversions = QPushButton()
    clear_button_conversions.setIcon(QIcon("clear_all_button.png"))
    clear_button_conversions.setIconSize(QSize(200, 40))
    clear_button_conversions.setToolTip(
        "<span style='color: white; font-size: 13px;'>Clears all data from the entry fields</span>")
    clear_button_conversions.clicked.connect(clear_all_conversions)
    adc_buttons_layout_conversions.addWidget(clear_button_conversions)

    cs_buttons_layout_conversions = QHBoxLayout()

    calculate_button_conversions = QPushButton()
    calculate_button_conversions.setIcon(QIcon("calculate_button.png"))
    calculate_button_conversions.setIconSize(QSize(320, 40))
    calculate_button_conversions.clicked.connect(convert_units)
    calculate_button_conversions.setToolTip("With valid input, convert measurements")
    cs_buttons_layout_conversions.addWidget(calculate_button_conversions)

    save_button_conversions = QPushButton()
    save_button_conversions.setIcon(QIcon("save_button.png"))
    save_button_conversions.setIconSize(QSize(320, 40))
    save_button_conversions.setToolTip("Export measurement conversion results")
    cs_buttons_layout_conversions.addWidget(save_button_conversions)

    # Create the first tab for Conversions
    conversions_tab = QWidget()
    conversions_layout = QVBoxLayout(conversions_tab)
    conversions_label = QLabel("Convert measurements by entering valid inputs (1/2, 0.5, 1 1/2, 1.5, etc.)")
    conversions_label_2 = QLabel("and selecting the units you want to convert from and to, then click Calculate.")
    conversions_label.setStyleSheet(
        "color: white; font-family: Inter; font-weight: bold; font-size: 16px; text-align: center; line-height: 2; margin-top: 5px; letter-spacing: 1px; word-spacing: 1px;")
    conversions_label_2.setStyleSheet(
        "color: white; font-family: Inter; font-weight: bold; font-size: 16px; text-align: center; line-height: 2; margin-top: 5px; margin-bottom: 10px; letter-spacing: 1px; word-spacing: 1px; ")
    conversions_label.setAlignment(Qt.AlignCenter)  # Align the label horizontally to the center
    conversions_label_2.setAlignment(Qt.AlignCenter)
    conversions_layout.addWidget(conversions_label)
    conversions_layout.addWidget(conversions_label_2)

    conversions_layout.addLayout(adc_buttons_layout_conversions)
    conversions_layout.addStretch(1)
    conversions_layout.addLayout(cs_buttons_layout_conversions)

    global current_layout
    current_layout= conversions_layout

    tab_widget.addTab(conversions_tab, "CONVERSIONS")


def calculate_recipes_button_layout():
    # Create button layout for the calculator tab
    adc_buttons_layout_calculator = QHBoxLayout()

    add_button_calculator = QPushButton()
    add_button_calculator.setIcon(QIcon("add_new_button.png"))
    add_button_calculator.setIconSize(QSize(200, 40))
    add_button_calculator.setToolTip(
        "<span style='color: white; font-size: 13px;'>Add a new entry for calculations</span>")
    add_button_calculator.clicked.connect(lambda checked, btn=add_button_calculator: add_new_recipe_calculation(btn))
    adc_buttons_layout_calculator.addWidget(add_button_calculator)

    delete_button_calculator = QPushButton()
    delete_button_calculator.setIcon(QIcon("delete_all_button.png"))
    delete_button_calculator.setIconSize(QSize(200, 40))
    delete_button_calculator.setToolTip(
        "<span style='color: white; font-size: 13px;'>Deletes all current entries</span>")
    delete_button_calculator.clicked.connect(delete_all_conversions)
    adc_buttons_layout_calculator.addWidget(delete_button_calculator)

    clear_button_calculator = QPushButton()
    clear_button_calculator.setIcon(QIcon("clear_all_button.png"))
    clear_button_calculator.setIconSize(QSize(200, 40))
    clear_button_calculator.setToolTip(
        "<span style='color: white; font-size: 13px;'>Clears all data from the entry fields</span>")
    clear_button_calculator.clicked.connect(clear_all_conversions)
    adc_buttons_layout_calculator.addWidget(clear_button_calculator)

    cs_buttons_layout_calculator = QHBoxLayout()

    calculate_button_calculator = QPushButton()
    calculate_button_calculator.setIcon(QIcon("calculate_button.png"))
    calculate_button_calculator.setIconSize(QSize(320, 40))
    calculate_button_calculator.setToolTip("With valid input, calculate modified measurements")
    cs_buttons_layout_calculator.addWidget(calculate_button_calculator)

    save_button_calculator = QPushButton()
    save_button_calculator.setIcon(QIcon("save_button.png"))
    save_button_calculator.setIconSize(QSize(320, 40))
    save_button_calculator.setToolTip("Export recipe calculation results")
    cs_buttons_layout_calculator.addWidget(save_button_calculator)

    # ------------------------------------------------------------------------------------------------------------------

    # Create the second tab for Calculator
    calculator_tab = QWidget()
    calculator_layout = QVBoxLayout(calculator_tab)
    calculator_label_1 = QLabel("To calculate a recipe adjustment, first enter the name of the item from the recipe,")
    calculator_label_2 = QLabel("the measurement from the recipe, and select the units of the measurement.")
    calculator_label_3 = QLabel("to either multiple or divide the measurement and enter an increment.")
    calculator_label_4 = QLabel("Calculate to calculate all recipe calculations and results will output below.")
    calculator_label_1.setStyleSheet(
        "color: white; font-family: Inter; font-weight: bold; font-size: 16px; text-align: center; line-height: 2; margin-top: 5px; letter-spacing: 1px; word-spacing: 1px;")
    calculator_label_1.setAlignment(Qt.AlignCenter)  # Align the label horizontally to the center
    calculator_layout.addWidget(calculator_label_1)
    calculator_label_2.setStyleSheet(
        "color: white; font-family: Inter; font-weight: bold; font-size: 16px; text-align: center; line-height: 2; margin-top: 5px; letter-spacing: 1px; word-spacing: 1px;")
    calculator_label_2.setAlignment(Qt.AlignCenter)  # Align the label horizontally to the center
    calculator_layout.addWidget(calculator_label_2)
    calculator_label_3.setStyleSheet(
        "color: white; font-family: Inter; font-weight: bold; font-size: 16px; text-align: center; line-height: 2; margin-top: 5px; letter-spacing: 1px; word-spacing: 1px;")
    calculator_label_3.setAlignment(Qt.AlignCenter)  # Align the label horizontally to the center
    calculator_layout.addWidget(calculator_label_3)
    calculator_label_4.setStyleSheet(
        "color: white; font-family: Inter; font-weight: bold; font-size: 16px; text-align: center; line-height: 2; margin-top: 5px; margin-bottom: 10px; letter-spacing: 1px; word-spacing: 1px;")
    calculator_label_4.setAlignment(Qt.AlignCenter)  # Align the label horizontally to the center
    calculator_layout.addWidget(calculator_label_4)

    calculator_layout.addLayout(adc_buttons_layout_calculator)
    calculator_layout.addStretch(1)
    calculator_layout.addLayout(cs_buttons_layout_calculator)

    global current_layout
    current_layout = calculator_layout

    tab_widget.addTab(calculator_tab, "RECIPE CALCULATOR")


def main():
    """

    """
    # ------------------------------------------------------------------------------------------------------------------
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Recipe Converter and Calculator")
    window.setFixedSize(1000, 700)

    # Set black background and black window border
    window.setStyleSheet("background-color: black; border: none;")
    dark_title_bar(window)

    # Set custom icon for the title bar
    app_icon = QIcon("main_window_icon.ico")
    window.setWindowIcon(app_icon)

    # Create the main layout
    layout = QVBoxLayout(window)
    layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

    # Initialize the dictionary to store sender buttons and their layouts
    global conversion_layouts_map
    conversion_layouts_map = {}

    global tab_widget

    # Create the tab widget
    tab_widget = QTabWidget()

    # Connect the currentChanged signal to update_current_layout function
    tab_widget.currentChanged.connect(update_current_layout)

    # Customize the appearance of the tab bar
    tab_widget.tabBar().setStyleSheet("""QTabBar::tab:selected { border-left: 1px solid black; border-right: 1px 
    solid black; background-color: #00FF19; color: black; font-weight: bold; font-family: Inter; font-size: 18px; 
    width: 498px; height: 40px; letter-spacing: 1px; word-spacing: 1px; } QTabBar::tab:!selected { border-left: 1px solid black; border-right: 1px solid 
    black; background-color: #B5B5B5; color: black; font-weight: bold; font-family: Inter; font-size: 18px; width: 
    498px; height: 40px; letter-spacing: 1px; word-spacing: 1px; } QTabBar::tab { margin: 0; } """)

    global current_layout

    # ------------------------------------------------------------------------------------------------------------------

    conversions_button_layout()
    calculate_recipes_button_layout()

    # ------------------------------------------------------------------------------------------------------------------

    # Set the tab widget border to none
    tab_widget.setStyleSheet("QTabWidget { border: none; background-color: black; }")
    tab_widget.update()

    # Add the tab widget to the layout
    layout.addWidget(tab_widget)

    window.show()
    sys.exit(app.exec())


def update_current_layout(index):
    global current_layout
    current_layout = tab_widget.widget(index).layout()


def show_confirmation_dialog(icon, title, message):
    dialog = QDialog()
    dialog.setWindowTitle(title)
    dark_title_bar(dialog)
    dialog.setWindowIcon(QIcon(icon))
    dialog.setStyleSheet("background-color: #00FF19; border: none; color: black;")

    # Create vertical layout for dialog content
    layout = QVBoxLayout(dialog)
    label = QLabel(message)
    label.setStyleSheet("font-weight: bold; font-family: Inter; font-size: 16px; margin-bottom: 8px;")
    layout.addWidget(label)

    # Create horizontal layout for buttons
    button_layout = QHBoxLayout()
    button_layout.addStretch()  # Add stretchable space to the left
    button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    button_box.setStyleSheet(
        "background-color: black; color: white; font-weight: bold; font-family: Inter; font-size: 16px; width: 80px; height: 30px;")
    button_layout.addWidget(button_box)
    button_layout.addStretch()  # Add stretchable space to the right

    # Add horizontal layout to the vertical layout
    layout.addLayout(button_layout)

    def on_accepted():
        dialog.accept()

    def on_rejected():
        dialog.reject()

    button_box.accepted.connect(on_accepted)
    button_box.rejected.connect(on_rejected)

    return dialog.exec() == QDialog.Accepted


# ----------------------------------------------------------------------------------------------------------------------


def add_new_conversion(sender_button):
    global current_layout
    print("Add New Conversion clicked")

    # Create widgets
    delete_button = QPushButton()
    delete_button.setIcon(QIcon("delete_entry_button.png"))
    delete_button.setIconSize(QSize(50, 50))
    delete_button.setToolTip("<span style='color: white; font-size: 13px;'>Delete this entry</span>")
    delete_button.clicked.connect(lambda checked, btn=delete_button: delete_entry(btn))

    input_box = QLineEdit()
    input_box.setStyleSheet("background-color: black; color: white; border: 2px solid white; border-radius: 5px; height: 40px; width: 100px; font-weight: bold; font-size: 14px; font-family: Inter; padding-left: 10px;")
    input_box.setPlaceholderText("1/2, 0.5, 1 1/2, 3/2, ...")
    input_box.setToolTip("<span style='color: white; font-size: 13px;'>Enter a valid measurement</span>")
    input_box.textChanged.connect(lambda text: input_box.setStyleSheet(
        "background-color: black; color: white; border: 2px solid red; border-radius: 5px; height: 40px; width: 100px; font-weight: bold; font-size: 14px; font-family: Inter; padding-left: 10px;" if not validate_input(text) else "background-color: black; color: white; border: 2px solid white; border-radius: 5px; height: 40px; width: 100px; font-weight: bold; font-size: 14px; font-family: Inter; padding-left: 10px;"))

    input_unit_dropdown = QComboBox()
    input_unit_dropdown.addItems(["cups", "tbsp", "tsp"])
    input_unit_dropdown.setStyleSheet("background-color: white; color: black; height: 40px; width: 55px; font-size: 16px; font-family: Inter; font-weight: bold; ")
    input_unit_dropdown.setCurrentIndex(-1)
    input_unit_dropdown.setPlaceholderText("units")
    input_unit_dropdown.setToolTip("<span style='color: black; font-size: 13px;'>Select measurement units</span>")

    equal_label = QLabel("=")
    equal_label.setStyleSheet("color: white; font-family: Inter; font-size: 20px; font-weight: bold;")

    result_box = QLineEdit()
    result_box.setReadOnly(True)
    result_box.setStyleSheet("background-color: black; color: white; border: 2px solid white; border-radius: 5px; height: 40px; width: 100px; font-weight: bold; font-size: 14px; font-family: Inter; padding-left: 10px;")
    result_box.setPlaceholderText("results...")

    output_unit_dropdown = QComboBox()
    output_unit_dropdown.addItems(["cups", "tbsp", "tsp"])
    output_unit_dropdown.setStyleSheet(
        "background-color: white; color: black; height: 40px; width: 55px; font-size: 16px; font-family: Inter; font-weight: bold; ")
    output_unit_dropdown.setCurrentIndex(-1)
    output_unit_dropdown.setPlaceholderText("units")
    output_unit_dropdown.setToolTip("<span style='color: black; font-size: 13px;'>Select measurement units</span>")


    swap_button = QPushButton()
    swap_button.setIcon(QIcon("swap_button.png"))
    swap_button.setIconSize(QSize(40, 40))
    swap_button.setToolTip("<span style='color: white; font-size: 13px;'>Swap this entry's units</span>")
    swap_button.clicked.connect(lambda checked, btn=swap_button: swap_units(btn))

    # Create layout for the widgets
    new_conversion_layout = QHBoxLayout()
    new_conversion_layout.setProperty("isConversionLayout", True)  # Set property to identify conversion layouts
    new_conversion_layout.addWidget(delete_button)
    new_conversion_layout.addWidget(input_box)
    new_conversion_layout.addWidget(input_unit_dropdown)
    new_conversion_layout.addWidget(equal_label)
    new_conversion_layout.addWidget(result_box)
    new_conversion_layout.addWidget(output_unit_dropdown)
    new_conversion_layout.addWidget(swap_button)

    # Store the sender button and its corresponding layout in the dictionary
    conversion_layouts_map[delete_button] = new_conversion_layout

    # Find the layout of the current tab and add the new layout
    current_tab_index = tab_widget.currentIndex()
    current_tab_widget = tab_widget.widget(current_tab_index)
    current_tab_layout = current_tab_widget.layout()

    # Insert the new conversion layout at the beginning
    current_tab_layout.insertLayout(3, new_conversion_layout)

    # Update the current tab layout
    current_tab_layout.update()


def add_new_recipe_calculation(sender_button):
    global current_layout
    print("Add New Conversion clicked")

    # Create widgets
    delete_button = QPushButton()
    delete_button.setIcon(QIcon("delete_entry_button.png"))
    delete_button.setIconSize(QSize(50, 50))
    delete_button.setToolTip("<span style='color: white; font-size: 13px;'>Delete this entry</span>")
    delete_button.clicked.connect(lambda checked, btn=delete_button: delete_entry(btn))

    item_name_input_box = QLineEdit()
    item_name_input_box.setStyleSheet("background-color: black; color: white; border: 2px solid white; border-radius: 5px; height: 40px; width: 100px; font-weight: bold; font-size: 14px; font-family: Inter; padding-left: 10px;")
    item_name_input_box.setPlaceholderText("milk, butter, flour, cheese, ...")
    item_name_input_box.setToolTip("<span style='color: white; font-size: 13px;'>Enter a valid measurement</span>")
    item_name_input_box.textChanged.connect(lambda text: item_name_input_box.setStyleSheet(
        "background-color: black; color: white; border: 2px solid red; border-radius: 5px; height: 40px; width: 100px; font-weight: bold; font-size: 14px; font-family: Inter; padding-left: 10px;" if not validate_input(text) else "background-color: black; color: white; border: 2px solid white; border-radius: 5px; height: 40px; width: 100px; font-weight: bold; font-size: 14px; font-family: Inter; padding-left: 10px;"))

    measurement_input_box = QLineEdit()
    measurement_input_box.setStyleSheet(
        "background-color: black; color: white; border: 2px solid white; border-radius: 5px; height: 40px; width: 50px; font-weight: bold; font-size: 14px; font-family: Inter; padding-left: 10px;")
    measurement_input_box.setPlaceholderText("1/2, 0.5, 1 1/2, 3/2, ...")
    measurement_input_box.setToolTip("<span style='color: white; font-size: 13px;'>Enter a valid measurement</span>")
    measurement_input_box.textChanged.connect(lambda text: measurement_input_box.setStyleSheet(
        "background-color: black; color: white; border: 2px solid red; border-radius: 5px; height: 40px; width: 50px; font-weight: bold; font-size: 14px; font-family: Inter; padding-left: 10px;" if not validate_input(
            text) else "background-color: black; color: white; border: 2px solid white; border-radius: 5px; height: 40px; width: 100px; font-weight: bold; font-size: 14px; font-family: Inter; padding-left: 10px;"))

    measurement_input_unit_dropdown = QComboBox()
    measurement_input_unit_dropdown.addItems(["cups", "tbsp", "tsp"])
    measurement_input_unit_dropdown.setStyleSheet("background-color: white; color: black; height: 40px; width: 55px; font-size: 16px; font-family: Inter; font-weight: bold; ")
    measurement_input_unit_dropdown.setCurrentIndex(-1)
    measurement_input_unit_dropdown.setPlaceholderText("units")
    measurement_input_unit_dropdown.setToolTip("<span style='color: black; font-size: 13px;'>Select measurement units</span>")

    #calc_function_switch =

    calc_factor_input = QLineEdit()
    calc_factor_input.setStyleSheet(
        "background-color: black; color: white; border: 2px solid white; border-radius: 5px; height: 40px; width: 50px; font-weight: bold; font-size: 14px; font-family: Inter; padding-left: 10px;")
    calc_factor_input.setPlaceholderText("2, 3, 4, ...")
    calc_factor_input.setToolTip("<span style='color: white; font-size: 13px;'>Enter a valid measurement</span>")
    calc_factor_input.textChanged.connect(lambda text: calc_factor_input.setStyleSheet(
        "background-color: black; color: white; border: 2px solid red; border-radius: 5px; height: 40px; width: 50px; font-weight: bold; font-size: 14px; font-family: Inter; padding-left: 10px;" if not validate_factor_input(
            text) else "background-color: black; color: white; border: 2px solid white; border-radius: 5px; height: 40px; width: 100px; font-weight: bold; font-size: 14px; font-family: Inter; padding-left: 10px;"))

    equal_label = QLabel("=")
    equal_label.setStyleSheet("color: white; font-family: Inter; font-size: 20px; font-weight: bold;")

    calc_result_box = QLineEdit()
    calc_result_box.setReadOnly(True)
    calc_result_box.setStyleSheet(
        "background-color: black; color: white; border: 2px solid white; border-radius: 5px; height: 40px; width: 100px; font-weight: bold; font-size: 14px; font-family: Inter; padding-left: 10px;")
    calc_result_box.setPlaceholderText("results...")

    # Create layout for the widgets
    new_recipe_calculator_layout = QHBoxLayout()
    new_recipe_calculator_layout.setProperty("isConversionLayout", True)  # Set property to identify conversion layouts
    new_recipe_calculator_layout.addWidget(delete_button)
    new_recipe_calculator_layout.addWidget(item_name_input_box)
    new_recipe_calculator_layout.addWidget(measurement_input_box)
    new_recipe_calculator_layout.addWidget(measurement_input_unit_dropdown)
    #new_recipe_calculator_layout.addWidget(calc_function)
    new_recipe_calculator_layout.addWidget(calc_factor_input)
    new_recipe_calculator_layout.addWidget(equal_label)
    new_recipe_calculator_layout.addWidget(calc_result_box)

    # Store the sender button and its corresponding layout in the dictionary
    conversion_layouts_map[delete_button] = new_recipe_calculator_layout

    # Find the layout of the current tab and add the new layout
    current_tab_index = tab_widget.currentIndex()
    current_tab_widget = tab_widget.widget(current_tab_index)
    current_tab_layout = current_tab_widget.layout()

    # Insert the new conversion layout at the beginning
    current_tab_layout.insertLayout(5, new_recipe_calculator_layout)

    # Update the current tab layout
    current_tab_layout.update()


def delete_all_conversions():
    print("Delete All Conversions clicked")
    confirmation_result = show_confirmation_dialog("trash_icon.ico", "Delete All Conversions", "Are you sure you want to delete all conversions?")
    if confirmation_result:
        print("Delete All Conversions confirmed")
        # Perform deletion operation here
        current_tab_index = tab_widget.currentIndex()
        current_tab_widget = tab_widget.widget(current_tab_index)
        current_tab_layout = current_tab_widget.layout()

        # Find and remove all conversion layouts
        for i in reversed(range(current_tab_layout.count())):
            layout = current_tab_layout.itemAt(i).layout()
            if layout and layout.property("isConversionLayout"):
                # Disconnect signals associated with delete buttons
                disconnect_delete_signals(layout)

                # Remove the layout containing conversion widgets
                while layout.count():
                    # Remove each widget in the layout
                    widget = layout.takeAt(0).widget()
                    if widget:
                        widget.deleteLater()
                layout.deleteLater()

        # Clear the conversion_layouts_map
        conversion_layouts_map.clear()
    else:
        print("Delete All Conversions cancelled")


def disconnect_delete_signals(layout):
    for i in range(layout.count()):
        item = layout.itemAt(i)
        if item:
            widget = item.widget()
            if widget:
                delete_button = widget.findChild(QPushButton)
                if delete_button:
                    delete_button.clicked.disconnect()


def clear_all_conversions():
    print("Clear All Conversions clicked")
    confirmation_result = show_confirmation_dialog("clear_icon.ico", "Clear All Conversions", "Are you sure you want to clear all conversions?")
    if confirmation_result:
        print("Clear All Conversions confirmed")
        # Perform clear operation here
        # Iterate through all conversion layouts
        for layout in conversion_layouts_map.values():
            input_box = layout.itemAt(1).widget()
            input_box.clear()

            result_box = layout.itemAt(4).widget()
            result_box.clear()

            input_unit_dropdown = layout.itemAt(2).widget()
            input_unit_dropdown.setCurrentIndex(-1)  # Set the dropdown to default (empty)

            output_unit_dropdown = layout.itemAt(5).widget()
            output_unit_dropdown.setCurrentIndex(-1)  # Set the dropdown to default (empty)
    else:
        print("Clear All Conversions cancelled")


def delete_entry(sender_button):
    print("Delete Entry clicked")
    confirmation_result = show_confirmation_dialog("trash_icon.ico", "Delete Entry",
                                                   "Are you sure you want to delete this entry?")
    if confirmation_result:
        # Get the layout associated with the sender button
        layout = conversion_layouts_map.get(sender_button)

        # Check if the layout exists
        if layout:
            # Disconnect signals associated with delete buttons
            disconnect_delete_signals(layout)

            # Remove the layout from the conversion_layouts_map dictionary
            del conversion_layouts_map[sender_button]

            # Find the layout of the parent tab widget
            current_tab_index = tab_widget.currentIndex()
            current_tab_widget = tab_widget.widget(current_tab_index)
            current_tab_layout = current_tab_widget.layout()

            # Find and remove the layout containing the delete button and associated widgets
            for i in reversed(range(current_tab_layout.count())):
                layout_item = current_tab_layout.itemAt(i)
                if layout_item and layout_item.layout() == layout:
                    while layout.count():
                        widget = layout.takeAt(0).widget()
                        if widget:
                            widget.deleteLater()
                    layout.deleteLater()
                    break
        else:
            print("Sender button is None")
    else:
        print("Delete Entry cancelled")


def swap_units(sender_button):
    # Get the layout associated with the sender button
    layout = conversion_layouts_map.get(sender_button)

    # Check if the layout exists
    if layout:
        # Extract input unit from input unit dropdown
        input_unit_dropdown = layout.itemAt(2).widget()
        input_unit_index = input_unit_dropdown.currentIndex()

        # Extract output unit from output unit dropdown
        output_unit_dropdown = layout.itemAt(5).widget()
        output_unit_index = output_unit_dropdown.currentIndex()

        # Swap the input and output units
        input_unit_dropdown.setCurrentIndex(output_unit_index)
        output_unit_dropdown.setCurrentIndex(input_unit_index)

        # Update the GUI
        input_unit_dropdown.update()
        output_unit_dropdown.update()

        # Optionally, you can also update the conversion calculation here if needed
    else:
        print("Layout not found for sender button")


# ----------------------------------------------------------------------------------------------------------------------


def validate_input(input_text):
    """
    Validate if the input is a number, "/", ".", or " " and ensure no more than one occurrence.
    """
    valid_characters = "0123456789/. "

    # Check if the input starts with a space or "/"
    if input_text.startswith(" ") or input_text.startswith("/"):
        show_toast("Invalid Input", "Input cannot start with a space or '/'.")
        return False

    # Count the occurrences of "/", ",", and " "
    slash_count = input_text.count("/")
    comma_count = input_text.count(".")
    space_count = input_text.count(" ")

    # Check for dividing by zero
    if "/" in input_text and input_text.endswith("/0"):
        show_toast("Invalid Input", "Cannot divide by zero.")
        return False

    # Split the input into whole number and fraction parts
    parts = input_text.split(" ")
    if len(parts) == 2:
        whole_part, fraction_part = parts
        # If there's a "/" in the input, ensure it's at the end (fraction)
        if "/" in whole_part and not "/" in fraction_part:
            show_toast("Invalid Input", "Please enter a valid number or fraction.")
            return False
    else:
        whole_part = parts[0]
        fraction_part = ""

    # If any of these counts exceed 1, return False
    if slash_count > 1 or comma_count > 1 or space_count > 1 or (slash_count + comma_count > 1) or (comma_count + space_count > 1):
        show_toast("Invalid Input", "Exceeded allowed number of special characters. Please enter a valid number or fraction.")
        return False

    # Check each character in the input_text
    for char in input_text:
        # If the character is not in the valid characters, show a toast notification and return False
        if char not in valid_characters:
            show_toast("Invalid Input", "Please enter a valid number or fraction.")
            return False

    # If all characters are valid, return True
    return True


def validate_factor_input(input_text):
    """
    Validate if the input is a number.
    """
    valid_characters = "0123456789"

    # Check each character in the input_text
    for char in input_text:
        # If the character is not in the valid characters, show a toast notification and return False
        if char not in valid_characters:
            show_toast("Invalid Input", "Please enter a valid number.")
            return False

    # If all characters are valid, return True
    return True


def show_toast(title, message):
    """
    Show a toast notification.
    """
    toast = QMessageBox()
    toast.setWindowTitle(title)
    toast.setText(message)
    toast.setStyleSheet("background-color: #00FF19; border: none; color: black; font-family: Inter; font-size: 16px; font-weight: bold;")
    dark_title_bar(toast)
    toast.exec()


def convert_units():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    # Iterate through each conversion layout
    for layout in conversion_layouts_map.values():
        # Extract input value from input box
        input_box = layout.itemAt(1).widget()
        input_value_str = input_box.text()

        # Extract input unit from input unit dropdown
        input_unit_dropdown = layout.itemAt(2).widget()
        input_unit = input_unit_dropdown.currentText()

        # Extract output unit from output unit dropdown
        output_unit_dropdown = layout.itemAt(5).widget()
        output_unit = output_unit_dropdown.currentText()

        # Perform input validation
        if not validate_input(input_value_str):
            continue

        # Convert input value to float or fraction
        try:
            input_value = float(fractions.Fraction(input_value_str))
        except ValueError:
            show_toast("Invalid Input", "Please enter a valid number.")
            continue

        if input_unit == "" or output_unit == "":
            show_toast("Invalid Input", "Must select measurement units to convert.")
            continue

        if input_unit == output_unit:
            show_toast("Invalid Input", "Measurement units must not match.")
            continue

        # Send request to the conversion microservice
        request = {
            "value": input_value,
            "input_unit": input_unit,
            "output_unit": output_unit
        }
        socket.send_json(request)

        # Receive response from the microservice
        response = socket.recv_json()
        if response['status'] == 'success':
            result_value = response['data']
        else:
            show_toast("Conversion Error", response['message'])
            continue

        # Update result box with the converted value
        result_box = layout.itemAt(4).widget()
        result_box.setText(str(result_value))


def calculate_recipes():
    pass


if __name__ == "__main__":
    main()