from PySide6.QtWidgets import (
    QLabel, QVBoxLayout, QWidget, QGraphicsOpacityEffect, QGraphicsDropShadowEffect
)
from PySide6.QtCore import (
    QPropertyAnimation, QTimer, Qt, QPoint,
    QEasingCurve, QParallelAnimationGroup
)
from PySide6.QtGui import QColor


class Toast(QWidget):
    def __init__(self, message, parent=None, manager=None):
        super().__init__(parent)
        self.manager = manager

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        # 半透明渐变背景 + 圆角
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(50, 50, 50, 230),
                    stop:1 rgba(30, 30, 30, 230)
                );
                color: white;
                border-radius: 10px;
                padding: 14px 28px;
                font-family: 'Segoe UI', 'Microsoft YaHei';
                font-size: 14px;
                letter-spacing: 0.5px;
            }
        """)

        # 添加投影效果
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.setGraphicsEffect(shadow)

        self.label = QLabel(message)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.adjustSize()
        self.setup_animation()

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide_toast)

        self.setMouseTracking(True)
        self.under_mouse = False

    def enterEvent(self, event):
        self.under_mouse = True
        self.timer.stop()

    def leaveEvent(self, event):
        self.under_mouse = False
        self.timer.start(1500)

    def setup_animation(self):
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        # 显示动画
        self.show_anim_group = QParallelAnimationGroup()
        opacity_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        opacity_anim.setDuration(350)
        opacity_anim.setStartValue(0)
        opacity_anim.setEndValue(0.98)
        opacity_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.pos_anim = QPropertyAnimation(self, b"pos")
        self.pos_anim.setDuration(400)
        self.pos_anim.setEasingCurve(QEasingCurve.Type.OutBack)

        self.show_anim_group.addAnimation(opacity_anim)
        self.show_anim_group.addAnimation(self.pos_anim)

        # 隐藏动画
        self.hide_anim_group = QParallelAnimationGroup()
        fade_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        fade_out.setDuration(400)
        fade_out.setStartValue(0.98)
        fade_out.setEndValue(0)
        fade_out.setEasingCurve(QEasingCurve.Type.InCubic)

        slide_down = QPropertyAnimation(self, b"pos")
        slide_down.setDuration(400)
        slide_down.setEasingCurve(QEasingCurve.Type.InQuad)

        self.hide_anim_group.addAnimation(fade_out)
        self.hide_anim_group.addAnimation(slide_down)
        self.hide_anim_group.finished.connect(self._on_closed)

    def show_toast(self, start_pos=None, end_pos=None, duration=2000):
        """显示 Toast，可以独立调用，也可以由 ToastManager 传入位置"""
        if not self.parent():
            return

        parent_rect = self.parent().geometry()

        # 如果没传，就自己计算
        if start_pos is None or end_pos is None:
            start_pos = QPoint(
                parent_rect.center().x() - self.width() // 2,
                parent_rect.bottom() - 100
            )
            end_pos = QPoint(start_pos.x(), start_pos.y() - 25)

        self.move(start_pos)
        self.show()

        self.pos_anim.setStartValue(start_pos)
        self.pos_anim.setEndValue(end_pos)
        self.show_anim_group.start()

        self.timer.start(duration)

        slide_down = self.hide_anim_group.animationAt(1)
        if isinstance(slide_down, QPropertyAnimation):
            slide_down.setStartValue(end_pos)
            slide_down.setEndValue(QPoint(end_pos.x(), end_pos.y() + 20))

    def hide_toast(self):
        if not self.under_mouse:
            self.hide_anim_group.start()

    def _on_closed(self):
        self.close()
        if self.manager:
            self.manager.remove_toast(self)


class ToastManager:
    def __init__(self, parent):
        self.parent = parent
        self.toasts = []
        self.spacing = 12  # 每个 toast 之间的间距

    def show_toast(self, message, duration=2000):
        toast = Toast(message, parent=self.parent, manager=self)
        self.toasts.append(toast)
        self.reposition_toasts(duration)
        return toast

    def remove_toast(self, toast):
        if toast in self.toasts:
            self.toasts.remove(toast)
            self.reposition_toasts()

    def reposition_toasts(self, duration=2000):
        """重新排列所有 toast 的位置"""
        if not self.parent:
            return
        parent_rect = self.parent.geometry()

        base_y = parent_rect.bottom() - 100
        for i, toast in enumerate(reversed(self.toasts)):
            start_pos = QPoint(
                parent_rect.center().x() - toast.width() // 2,
                base_y - i * (toast.height() + self.spacing)
            )
            end_pos = QPoint(start_pos.x(), start_pos.y() - 25)
            toast.show_toast(start_pos, end_pos, duration)
