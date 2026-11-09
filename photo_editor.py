"""
Простой фоторедактор.
Заполните пропуски согласно вашему варианту.
Вариант 4: Загрузка изображения, размытие через QSlider, сохранение.
"""

import sys
import cv2
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, 
    QVBoxLayout, QWidget, QLabel, QComboBox, QFileDialog, QSlider, QHBoxLayout
)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
from filters import apply_blur


class PhotoEditor(QMainWindow):
    """Фоторедактор."""
    
    def __init__(self):
        super().__init__()
        # ВАШ КОД: установите заголовок и размеры окна
        self.setWindowTitle("Фоторедактор (Вариант 4 - Размытие со слайдером)")
        self.resize(800, 650)
        
        self.current_image = None  # Хранилище текущего изображения
        self.processed_image = None # Обработанное изображение
        
        self.init_ui()
    
    def init_ui(self):
        """Инициализация интерфейса."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # ВАШ КОД: создайте QLabel для отображения изображения
        self.image_label = QLabel("Загрузите изображение")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background-color: #1e1e1e; color: white; border-radius: 4px;")
        self.image_label.setMinimumSize(600, 400)
        
        # ВАШ КОД: создайте кнопку "Загрузить"
        self.load_button = QPushButton("Загрузить изображение")
        
        # Элементы для Варианта 4 (Слайдер размытия)
        slider_layout = QHBoxLayout()
        self.slider_label = QLabel("Радиус размытия: 0")
        self.blur_slider = QSlider(Qt.Orientation.Horizontal)
        self.blur_slider.setMinimum(0)
        self.blur_slider.setMaximum(25)
        self.blur_slider.setValue(0)
        self.blur_slider.setEnabled(False)
        slider_layout.addWidget(self.slider_label)
        slider_layout.addWidget(self.blur_slider)
        
        # ВАШ КОД: создайте кнопку "Сохранить"
        self.save_button = QPushButton("Сохранить результат")
        self.save_button.setEnabled(False)
        
        # ВАШ КОД: подключите сигналы к слотам
        self.load_button.clicked.connect(self.load_image)
        self.blur_slider.valueChanged.connect(self.update_blur)
        self.save_button.clicked.connect(self.save_image)
        
        # ВАШ КОД: добавьте виджеты в layout
        layout.addWidget(self.image_label)
        layout.addWidget(self.load_button)
        layout.addLayout(slider_layout)
        layout.addWidget(self.save_button)
    
    def load_image(self):
        """Загрузка изображения."""
        # ВАШ КОД: используйте QFileDialog для выбора файла
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите изображение", "",
            "Изображения (*.jpg *.jpeg *.png *.bmp)"
        )
        
        if file_path:
            # ВАШ КОД: загрузите изображение с помощью cv2.imread()
            self.current_image = cv2.imread(file_path)
            if self.current_image is not None:
                self.processed_image = self.current_image.copy()
                self.blur_slider.setValue(0)
                self.slider_label.setText("Радиус размытия: 0")
                self.blur_slider.setEnabled(True)
                self.save_button.setEnabled(True)
                # ВАШ КОД: отобразите изображение
                self.display_image(self.processed_image)
    
    def display_image(self, image):
        """Отображение изображения."""
        # ВАШ КОД: преобразуйте BGR в RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        h, w, channels = rgb_image.shape
        bytes_per_line = channels * w
        
        # ВАШ КОД: создайте QImage из NumPy array
        qimage = QImage(
            rgb_image.data, w, h, bytes_per_line,
            QImage.Format.Format_RGB888
        )
        
        # ВАШ КОД: создайте QPixmap и установите на label
        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap.scaled(
            self.image_label.width(), 
            self.image_label.height(), 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
        ))
    
    def update_blur(self, value):
        """Применение фильтра размытия через слайдер (вариант 4)."""
        if self.current_image is None:
            return
        
        self.slider_label.setText(f"Радиус размытия: {value}")
        # Вызываем функцию размытия из модуля filters.py
        self.processed_image = apply_blur(self.current_image, radius=value)
        # ВАШ КОД: отобразите результат
        self.display_image(self.processed_image)
    
    def save_image(self):
        """Сохранение изображения."""
        if self.processed_image is None:
            return
            
        # ВАШ КОД: используйте QFileDialog для выбора пути
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить изображение", "",
            "Изображения (*.jpg *.jpeg *.png)"
        )
        
        if file_path:
            # ВАШ КОД: сохраните изображение с помощью cv2.imwrite()
            cv2.imwrite(file_path, self.processed_image)


def main():
    app = QApplication(sys.argv)
    window = PhotoEditor()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()