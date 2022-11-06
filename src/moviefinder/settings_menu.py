from moviefinder.user import User
from moviefinder.validators import EmailValidator
from moviefinder.validators import NameValidator
from moviefinder.validators import PasswordValidator
from moviefinder.validators import valid_services
from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class SettingsMenu(QtWidgets.QWidget):
    def __init__(self, user: User, main_window: QtWidgets.QMainWindow):
        super().__init__(main_window)
        self.user = user
        self.main_window = main_window
        self.layout = QtWidgets.QFormLayout(self)
        title_label = QtWidgets.QLabel("<h1>settings</h1>", self)
        title_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.layout.addRow(title_label)
        self.name_line_edit = QtWidgets.QLineEdit(self)
        self.name_line_edit.setValidator(NameValidator())
        self.layout.addRow("name:", self.name_line_edit)
        self.email_line_edit = QtWidgets.QLineEdit(self)
        self.email_line_edit.setValidator(EmailValidator())
        self.layout.addRow("email:", self.email_line_edit)
        self.password_line_edit = QtWidgets.QLineEdit(self)
        self.password_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_line_edit.setValidator(PasswordValidator())
        self.layout.addRow("new password:", self.password_line_edit)
        self.confirm_password_line_edit = QtWidgets.QLineEdit(self)
        self.confirm_password_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.layout.addRow("confirm new password:", self.confirm_password_line_edit)
        self.region_combo_box = QtWidgets.QComboBox(self)
        self.region_combo_box.addItem("United States")
        self.layout.addRow("region:", self.region_combo_box)
        self.services_layout = QtWidgets.QVBoxLayout()
        self.services_group_box = QtWidgets.QGroupBox("services")
        self.apple_tv_plus_checkbox = QtWidgets.QCheckBox("Apple TV+", self)
        self.services_layout.addWidget(self.apple_tv_plus_checkbox)
        self.disney_plus_checkbox = QtWidgets.QCheckBox("Disney+", self)
        self.services_layout.addWidget(self.disney_plus_checkbox)
        self.hbo_max_checkbox = QtWidgets.QCheckBox("HBO Max", self)
        self.services_layout.addWidget(self.hbo_max_checkbox)
        self.hulu_checkbox = QtWidgets.QCheckBox("Hulu", self)
        self.services_layout.addWidget(self.hulu_checkbox)
        self.netflix_checkbox = QtWidgets.QCheckBox("Netflix", self)
        self.services_layout.addWidget(self.netflix_checkbox)
        self.services_group_box.setLayout(self.services_layout)
        self.layout.addRow(self.services_group_box)
        buttons_layout = QtWidgets.QHBoxLayout()
        self.save_button = QtWidgets.QPushButton("save", self)
        self.save_button.clicked.connect(self.__save_settings_and_show_browse_menu)
        buttons_layout.addWidget(self.save_button)
        self.cancel_button = QtWidgets.QPushButton("cancel", self)
        self.cancel_button.clicked.connect(self.__reset_settings_and_show_browse_menu)
        buttons_layout.addWidget(self.cancel_button)
        self.layout.addRow(buttons_layout)
        self.__set_widgets()

    def __set_widgets(self) -> None:
        """Initializes widgets with the values in the user object."""
        self.name_line_edit.setText(self.user.name)
        self.email_line_edit.setText(self.user.email)
        self.region_combo_box.setCurrentText(self.user.region)
        self.apple_tv_plus_checkbox.setChecked("Apple TV+" in self.user.services)
        self.disney_plus_checkbox.setChecked("Disney+" in self.user.services)
        self.hbo_max_checkbox.setChecked("HBO Max" in self.user.services)
        self.hulu_checkbox.setChecked("Hulu" in self.user.services)
        self.netflix_checkbox.setChecked("Netflix" in self.user.services)

    def __reset_settings_and_show_browse_menu(self) -> None:
        self.__set_widgets()
        self.main_window.show_browse_menu(self.user)

    def __get_services(self) -> list[str]:
        """Determines what services are selected in the service checkboxes."""
        services = []
        if self.apple_tv_plus_checkbox.isChecked():
            services.append("Apple TV+")
        if self.disney_plus_checkbox.isChecked():
            services.append("Disney+")
        if self.hbo_max_checkbox.isChecked():
            services.append("HBO Max")
        if self.hulu_checkbox.isChecked():
            services.append("Hulu")
        if self.netflix_checkbox.isChecked():
            services.append("Netflix")
        return services

    def __save_settings_and_show_browse_menu(self) -> None:
        assert self is not None
        if not self.name_line_edit.hasAcceptableInput():
            msg = QtWidgets.QMessageBox()
            msg.setText("Please enter a name up to 100 characters long.")
            msg.exec()
            return
        if not self.email_line_edit.hasAcceptableInput():
            msg = QtWidgets.QMessageBox()
            msg.setText("Invalid email address format.")
            msg.exec()
            return
        if (
            self.password_line_edit.text()
            and not self.password_line_edit.hasAcceptableInput()
        ):
            msg = QtWidgets.QMessageBox()
            msg.setText("Invalid password. The password must have 9 to 50 characters.")
            msg.exec()
            return
        if self.password_line_edit.text() != self.confirm_password_line_edit.text():
            self.confirm_password_line_edit.clear()
            msg = QtWidgets.QMessageBox()
            msg.setText("The passwords do not match.")
            msg.exec()
            return
        if not valid_services(self.services_group_box):
            return
        name = self.name_line_edit.text()
        email = self.email_line_edit.text()
        password = self.password_line_edit.text()
        self.password_line_edit.clear()
        self.confirm_password_line_edit.clear()
        region = self.region_combo_box.currentText()
        services = self.__get_services()
        self.user = User(name, email, region, services)
        self.main_window.save_user_data(self.user, password)
        self.main_window.show_browse_menu(self.user)
